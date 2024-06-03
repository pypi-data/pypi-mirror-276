import os as _os, sys as _sys
from typing import cast as _cast
import errno as _errno
from contextlib import suppress as _suppress
from simpleworkspace.types.time import TimeSpan as _TimeSpan

__ISWIN__ = _sys.platform.startswith("win")


class FileLock():
    """Create a system-wide exclusive lock for a given global name."""

    def __init__(self, id: str) -> None:
        import simpleworkspace.io.file, tempfile

        self.id = id
        self._context_lock_filepath = _os.path.join(tempfile.gettempdir(), f"pyswl_{simpleworkspace.io.file.SantizeFilename(id)}.lock")
        self._context_lock_fh = None
        self._context_mode = 0o644

    @property
    def IsLocked(self):
        return self._context_lock_fh is not None

    def _windows_acquire(self):
        """If the file lock could be acquired, self._context_lock_fh holds the file handle of the lock file."""

        import msvcrt

        self._raise_on_not_writable_file(self._context_lock_filepath)
        flags = (
            _os.O_RDWR  # open for read and write
            | _os.O_CREAT  # create file if not exists
            | _os.O_TRUNC  # truncate file if not empty
        )
        try:
            fh = _os.open(self._context_lock_filepath, flags, self._context_mode)
        except OSError as exception:
            if exception.errno != _errno.EACCES:  # has no access to this lock
                raise
        else:
            try:
                msvcrt.locking(fh, msvcrt.LK_NBLCK, 1)
            except OSError as exception:
                _os.close(fh)  # close file first
                if exception.errno != _errno.EACCES:  # file is already locked
                    raise
            else:
                self._context_lock_fh = fh

    def _windows_release(self):
        """Releases the lock and sets self._context_lock_fh to None."""
        import msvcrt

        fh = _cast(int, self._context_lock_fh)
        self._context_lock_fh = None
        msvcrt.locking(fh, msvcrt.LK_UNLCK, 1)
        _os.close(fh)

        with _suppress(OSError):  # Probably another instance of the application had acquired the file lock.
            _os.unlink(self._context_lock_filepath)

    def _unix_acquire(self):
        """If the file lock could be acquired, self._context_lock_fh holds the file handle of the lock file."""

        import fcntl

        self._raise_on_not_writable_file(self._context_lock_filepath)

        open_flags = _os.O_RDWR | _os.O_TRUNC
        if not _os.path.exists(self._context_lock_filepath):
            open_flags |= _os.O_CREAT

        fh = _os.open(self._context_lock_filepath, open_flags, self._context_mode)
        with _suppress(PermissionError):  # This locked is not owned by this UID
            _os.fchmod(fh, self._context_mode)
        try:
            fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exception:
            _os.close(fh)
            if exception.errno == _errno.ENOSYS:  # NotImplemented error
                msg = "FileSystem does not appear to support flock"
                raise NotImplementedError(msg) from exception
        else:
            self._context_lock_fh = fh

    def _unix_release(self):
        """Releases the lock and sets self._context_lock_fh to None."""
        import fcntl

        # Do not remove the lockfile:
        #   https://github.com/tox-dev/py-filelock/issues/31
        #   https://stackoverflow.com/questions/17708885/flock-removing-locked-file-without-race-condition
        fd = _cast(int, self._context_lock_fh)
        self._context_lock_fh = None
        fcntl.flock(fd, fcntl.LOCK_UN)
        _os.close(fd)

    def Acquire(self, blocking=False, timeout: _TimeSpan = None, poll_interval=_TimeSpan(milliSeconds=100)):
        """Tries to aquire a system wide file lock. 
        The lock lives until either release is called or no references left to instance

        :param blocking: when blocking is enabled, waits until a lock is available. \
            When blocking is not used, an exception is thrown if a lock can't be acquired immediately
        :param timeout: duration to wait before timing out when blocking is enabled
        :param poll_interval: How often to recheck acquire status
        :returns: self instance, to enable support for context manager

        :raises TimeoutError: When blocking is not used and lock is busy, or when blocking is enabled and timeout reached

        :Examples:
        
        Scope:
        >>> lock = FileLock("lockID")
        >>> lock.Acquire() #raises timeout when not acquirable
        >>> lock.Release()

        ContextManager:
        >>> with FileLock("lockID").Acquire():
        >>>     ...
        """

        import time
        from simpleworkspace.utility.time import StopWatch

        if self.IsLocked:
            return self

        stopwatch = StopWatch()
        stopwatch.Start()
        while True:
            if(__ISWIN__):
                self._windows_acquire()
            else:
                self._unix_acquire()

            if self.IsLocked:
                break

            if blocking is False:
                raise TimeoutError(f'Failed to immediately acquire lock on "{self.id}"')

            if (timeout is not None) and (stopwatch.GetElapsedSeconds() > timeout.TotalSeconds):
                raise TimeoutError(f'Timeout acquiring lock on "{self.id}" for {timeout.TotalSeconds} seconds')

            time.sleep(poll_interval.TotalSeconds)
        return self

    def Release(self):
        if not self.IsLocked:
            return
        if(__ISWIN__):
            self._windows_release()
        else:
            self._unix_release()

    def __enter__(self):
        if(not self.IsLocked):
            raise SyntaxError("A lock must be Acquired first")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.Release()

    def __del__(self):
        """Called when the lock object is deleted"""
        self.Release()

    def _raise_on_not_writable_file(self, filename: str) -> None:
        """
        Raise an exception if attempting to open the file for writing would fail.

        This is done so files that will never be writable can be separated from files that are writable but currently
        locked.

        :param filename: file to check
        :raises OSError: as if the file was opened for writing.

        """
        import stat

        try:  # use stat to do exists + can write to check without race condition
            file_stat = _os.stat(filename)  # noqa: PTH116
        except OSError:
            return  # File does not exist or other errors, nothing to do

        if file_stat.st_mtime == 0:
            return  # if _os.stat returns but modification is zero that's an invalid _os.stat - ignore it

        if not (file_stat.st_mode & stat.S_IWUSR):
            raise PermissionError(_errno.EACCES, "Permission denied", filename)

        if stat.S_ISDIR(file_stat.st_mode):
            if __ISWIN__:
                # On Windows, this is PermissionError
                raise PermissionError(_errno.EACCES, "Permission denied", filename)
            else:
                # On linux / macOS, this is IsADirectoryError
                raise IsADirectoryError(_errno.EISDIR, "Is a directory", filename)




class FileLockPool():
    """Manages multiple file locks to be able to acquire one of many instead of waiting on a single lock"""

    def __init__(self, *id: str) -> None:
        self._locks = [FileLock(x) for x in id]
        self.acquiredLock:FileLock = None

    @property
    def IsLocked(self):
        return (self.acquiredLock is not None) and (self.acquiredLock.IsLocked)

    def Acquire(self, blocking=False, timeout: _TimeSpan = None, poll_interval=_TimeSpan(milliSeconds=100)):
        import time
        from simpleworkspace.utility.time import StopWatch

        if self.IsLocked:
            return self

        stopwatch = StopWatch()
        stopwatch.Start()
        while True:
            for lock in self._locks:
                try:
                    lock.Acquire(blocking=False)
                    self.acquiredLock = lock
                    return self
                except TimeoutError as ex:
                    pass
            
            if blocking is False:
                raise TimeoutError(f'Failed to immediately acquire a lock from the pool')

            if (timeout is not None) and (stopwatch.GetElapsedSeconds() > timeout.TotalSeconds):
                raise TimeoutError(f"Timeout acquiring lock on pool for {timeout.TotalSeconds} seconds")

            time.sleep(poll_interval.TotalSeconds)


    def Release(self):
        if(not self.IsLocked):
            return
        self.acquiredLock.Release()
        self.acquiredLock = None


    def __enter__(self):
        if(not self.IsLocked):
            raise SyntaxError("A lock must be Acquired first")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.Release()

    def __del__(self):
        """Called when the lock pool object is deleted"""
        self.Release()