class Error(Exception):
    exit_code = 100
    def __init__(self):
        super(Error, self).__init__()
        # Exception.__init__(self)

class NoSuchPath(Error):
    exit_code = 101
class InvalidOperation(Error):
    exit_code = 102
class NotEmptyDirectory(Error):
    exit_code = 103
class ItIsDirectory(Error):
    exit_code = 104
class PermissionDenied(Error):
    exit_code = 105
class BasketDoesNotExists(Error):
    exit_code = 106
class FileExists(Error):
    exit_code = 107
class DirectoryExists(Error):
    exit_code = 108
class NoSuchFileInBasket(Error):
    exit_code = 109
    