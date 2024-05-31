try:
    import esmpy
except ImportError as exc:
    # Prior to v8.4.0, `esmpy`` could be imported as `ESMF`.
    try:
        import ESMF as esmpy  # noqa: N811
    except ImportError:
        raise exc

# constants needs to be above schemes, as it is used within
from .constants import Constants, check_method, check_norm
from .schemes import *


__version__ = "0.10.0"
