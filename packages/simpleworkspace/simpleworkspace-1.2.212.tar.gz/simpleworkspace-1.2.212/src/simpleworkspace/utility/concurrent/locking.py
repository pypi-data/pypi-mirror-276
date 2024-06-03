import os as _os
from simpleworkspace.types.os import OperatingSystemEnum as _OperatingSystemEnum
from typing import cast as _cast
import errno as _errno
from contextlib import suppress as _suppress

class FileLock:
    """Create a system-wide exclusive lock for a given global name."""

    def __init__(self, id: str) -> None:
        import simpleworkspace.io.file, tempfile

        self.id = id
        self._currentOS = _OperatingSystemEnum.GetCurrentOS()

        self.lock_file = _os.path.join(tempfile.gettempdir(), f"pyswl_{simpleworkspace.io.file.SantizeFilename(id)}.lock")
        self._context_lock_fh = None
        self._context_mode = 0o644
    
    @property
    def IsLocked(self):
        return self._context_lock_fh is not None

    def _Acquire_Unix(self):
        import fcntl

        self._raise_on_not_writable_file(self.lock_file)
        
        open_flags = _os.O_RDWR | _os.O_TRUNC
        if not _os.path.exists(self.lock_file):
            open_flags |= _os.O_CREAT
        
        fh = _os.open(self.lock_file, open_flags, self._context_mode)
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

    def _Acquire_Windows(self):
        import msvcrt

        self._raise_on_not_writable_file(self.lock_file)
        flags = (
            _os.O_RDWR  # open for read and write
            | _os.O_CREAT  # create file if not exists
            | _os.O_TRUNC  # truncate file if not empty
        )
        try:
            fh = _os.open(self.lock_file, flags, self._context_mode)
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


    def _Release_Unix(self):
        import fcntl

        # Do not remove the lockfile:
        #   https://github.com/tox-dev/py-filelock/issues/31
        #   https://stackoverflow.com/questions/17708885/flock-removing-locked-file-without-race-condition
        fd = _cast(int, self._context_lock_fh)
        self._context_lock_fh = None
        fcntl.flock(fd, fcntl.LOCK_UN)
        _os.close(fd)

    def _Release_Windows(self):
        import msvcrt

        fh = _cast(int, self._context_lock_fh)
        self._context_lock_fh = None
        msvcrt.locking(fh, msvcrt.LK_UNLCK, 1)
        _os.close(fh)

        with _suppress(OSError):  # Probably another instance of the application had acquired the file lock.
            _os.unlink(self.lock_file)
    
    def Acquire(self, blocking=False, timeoutMS=None):
        import time
        from simpleworkspace.utility.time import StopWatch

        if(self.IsLocked):
            return
    
        stopwatch = StopWatch()
        while(True):
            if(self._currentOS == _OperatingSystemEnum.Windows):
                self._Acquire_Windows()
            else:
                self._Acquire_Unix()
            
            if(self.IsLocked):
                break

            if(blocking is False):
                raise TimeoutError(f'Failed to immediately acquire lock on "{self.id}"')

            if(timeoutMS is not None) and (stopwatch.GetElapsedMilliseconds() > timeoutMS):
                raise TimeoutError(f'Timeout acquiring lock on {self.id} for {timeoutMS} MS')
            
            time.sleep(1)

    def Release(self):
        if(not self.IsLocked):
            return
        
        if(self._currentOS == _OperatingSystemEnum.Windows):
            self._Release_Windows()
        else:
            self._Release_Unix()

    def __enter__(self):
        self.Acquire()
        return self

    def __exit__(self):
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
            if self._currentOS == _OperatingSystemEnum.Windows:
                # On Windows, this is PermissionError
                raise PermissionError(_errno.EACCES, "Permission denied", filename)
            else:
                # On linux / macOS, this is IsADirectoryError
                raise IsADirectoryError(_errno.EISDIR, "Is a directory", filename)
