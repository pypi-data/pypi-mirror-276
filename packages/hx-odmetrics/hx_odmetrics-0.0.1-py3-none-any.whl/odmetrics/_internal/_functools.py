"""
function and class decorators for version control and test verification
character: root script
Author: Haokun Zhang <haokun.zhang@hirain.com>
log: --
"""

import warnings
from time import time

from ._configs import *
from ._typing import *


def _cast_warning(msg: str, category: _AnyT = None, force_cast: bool = _UNFORCE_CAST) -> None:
    category = UserWarning if not category else category
    if force_cast or (not force_cast and __status__ is _STATUS_TEST):
        warnings.warn(
            _render_color_stdout(msg, _WARNING_RENDER_COLOR), category
        )


def _cast_error(msg: str, error: Exception, force_cast: bool = _UNFORCE_CAST) -> None:
    if force_cast or (not force_cast and __status__ is _STATUS_TEST):
        raise error(msg)


class VersionControl:
    """
    """
    def __init__(self, required_version: str = None):
        """
        """  
        self._required_version = required_version

    def __call__(self, func):  
        def _wrapper(*args, **kwargs):
            if __status__ is _STATUS_ANNOUNCED:
                if self._required_version == 'onhold':
                    _cast_error(f'Function {func.__name__} onhold by version', PermissionError, _FORCE_CAST) 

                current_version = self._get_current_version()  
                if not self._version_larger_equal(current_version, self._required_version): 
                    msg = f'Function {func.__name__} requires version {self._required_version} or above, '\
                                    f'but current version is {current_version}'
                    _cast_error(msg, PermissionError, _FORCE_CAST)
            
            return func(*args, **kwargs)
        return _wrapper
    
    @staticmethod
    def _decode_version(version: str) -> _Dict:
        if version is None or version == "unreleased":
            version = '0.0.0'
        major, minor, patch = [int(syn) for syn in version.split(".")]
        return {'major': major, 'minor': minor, 'patch': patch}
    
    def _version_larger_equal(self, ver1: str, ver2: str) -> bool:
        ver1, ver2 = [self._decode_version(version) for version in [ver1, ver2]]
        _vers_encoded = []
        for ver in [ver1, ver2]:
            _up = max(max(ver.values()) + 1, 10)
            _encode = ver['major'] * _up ** 2 + ver['minor'] * _up ** 1 + _up
            _vers_encoded.append(_encode)
            
        if _vers_encoded[0] >= _vers_encoded[1]:
            return True
        return False
    
    def _get_current_version(self) -> str:
        try:
            return __version__
        except Exception:
            _cast_error("package version not found", ModuleNotFoundError, _FORCE_CAST)
        

class Unreleased:...


class ToModify:
    def __init__(self, mark: str = None) -> None:
        self._mark = " " if not mark else mark

    def __call__(self, func) -> _AnyT:
        def _wrapper(*args, **kwargs):
            msg = "function needs to be modified, specific mark: `{}`."\
                " ToModify called at {}".format(self._mark, func.__name__)
            _cast_warning(msg, FutureWarning)
            return func(*args, **kwargs)
        
        return _wrapper
    

def Duplicated(func):
    def _wrapper(*args, **kwargs):
        msg = "method duplicates other methods. Duplicated called at {}".format(func.__name__)
        _cast_warning(msg, RuntimeWarning)
        return func(*args, **kwargs)
    
    return _wrapper


def Deprecated(func):
    def _wrapper(*args, **kwargs):
        msg = "method will be deprecated. Deprecated called at {}".format(func.__name__)
        _cast_warning(msg, DeprecationWarning)
        return func(*args, **kwargs)
    
    return _wrapper


def UnImplemented(func):  
    def _wrapper(*args, **kwargs):
        msg = "method not implemented. UnImplemented called at {}".format(func.__name__)
        _cast_error(msg, ModuleNotFoundError)
    
    return _wrapper


def Temporary(func):
    def _wrapper(*args, **kwargs):
        msg = "A temporary class or function should be replaced or removed to a certain script after accomplished."\
        "Temporary called at: {}".format(func.__name__)
        _cast_warning(msg, RuntimeWarning)
        return func(*args, **kwargs)
    
    return _wrapper


def DoubleCheck(func):
    def _wrapper(*args, **kwargs):
        msg = "DoubleCheck called at: {}".format(func.__name__)
        _cast_warning(msg, RuntimeWarning)
        return func(*args, **kwargs)
    
    return _wrapper


def Timer(func):
    def _wrapper(*args, **kwargs):
        start = time()
        res = func(*args, **kwargs)
        end = time()
        print(
            _render_color_stdout(f"\nfunction {func.__name__} elapsed: {round(end - start, 3)}s", "gray")
        )
        return res
    
    return _wrapper


def _render_color_stdout(out: str, color: _AnyT = None):
        _endc = "\033[0m"
        if isinstance(color, str):
            _colormap = {
                'gray': "\033[90m",
                'black': "\033[0m", 'red': "\033[91m", 'blue': "\033[94m",
                'green': "\033[92m", 'yellow': "\033[93m", 'purple': "\033[95m",
            }
            assert color in _colormap, "Invalid key, available color for ref: {}".format(
                [i for i in _colormap.keys()]
            )
            _color = _colormap[color]
        elif isinstance(color, int):
            _color = "\033[{}m".format(color)
        else: 
            raise TypeError("Type of arg `color` must be int or str.")

        return _color + out + _endc
