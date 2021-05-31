from .production import *
try:
    from .local_setings import *
except ImportError:
    pass
