#version info
_VERSION_UNRELEASED = "unreleased"
_VERSION_RELEASED = "0.0.1"
_VERSION_MAJOR_MAX = None
_VERSION_MINOR_MAX = 15
_VERSION_PATCH_MAX = None
_VERSION_PATCH_MIN = 10
_VERSION_ONHOLD = f"{_VERSION_MAJOR_MAX}.{_VERSION_MINOR_MAX}.{_VERSION_PATCH_MIN}"
_VERSION_STAYBACK = "0.0.1"

#status info
_STATUS_TEST: bool = False
_STATUS_ANNOUNCED: bool = not _STATUS_TEST

# controls info
_WARNING_RENDER_COLOR = "gray"

__name__: str = "hx-odmetrics"
__version__: str = _VERSION_RELEASED
__status__: bool = _STATUS_ANNOUNCED

# decorator controls
# _CAST = not _STATUS_TEST
# _UNCAST = _STATUS_TEST
_FORCE_CAST = True
_UNFORCE_CAST = False

__all__ = ["_FORCE_CAST", "_UNFORCE_CAST", "_WARNING_RENDER_COLOR", "_STATUS_TEST", "_STATUS_ANNOUNCED",
           "__name__", "__version__", "__status__"]

assert _FORCE_CAST is True and _UNFORCE_CAST is False
assert _STATUS_TEST is False
