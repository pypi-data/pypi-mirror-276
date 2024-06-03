"""
Package typing for formulated variable type definition
Author: Haokun Zhang <haokun.zhang@hirain.com>
character: strict root script
"""

import typing as _t
import types as _types
import pandas as pd
from numpy import (ndarray as _arr, matrix as _mat)
from PIL.Image import Image as _Image
from matplotlib.figure import Figure

__all__: _t.List = []

# type like
_DType = type
__all__.extend(["_DType"])

# scalar like
_ScalarLike = _t.TypeVar("_ScalarLike", int, float)
_IntLike = int
_FltLike = float
_StrLike = str
__all__.extend(["_ScalarLike", "_IntLike", "_FltLike", "_StrLike"])

# any / combinations
_AnyT = _t.Any
_Auto = _t.Any
__all__.extend(["_AnyT", "_Auto"])


# combined literals
_Ltrl = _t.Literal
_LtrlAny = _t.TypeVar("_LtrlAny", int, float, bool, str)
_NumOrStr = _t.Union[int, float, str]
_IntOrStr = _t.Union[int, str]
_FltOrStr = _t.Union[float, str]
__all__.extend(["_Ltrl", "_LtrlAny", "_NumOrStr", "_IntOrStr", "_FltOrStr"])


# matrices and vectors
_MatLike = _t.TypeVar("_MatLike", bound=_mat)
_ArrLike = _t.TypeVar("_ArrLike", bound=_arr)
_VecLike = _arr
__all__.extend(["_MatLike", "_ArrLike", "_VecLike"])


# Pillow images
_PILImg = _Image
__all__.extend(["_PILImg"])


# data structure
__iterable = _t.Iterable
_Iter = __iterable
_UnlimIter = __iterable[_AnyT]
_ArrIter = _Iter[_MatLike]
__all__.extend(["_Iter", "_UnlimIter", "_ArrIter"])

_Tup = _t.Tuple
_UnlimTup = _t.Tuple[_AnyT]
_NumTup = _t.Tuple[_ScalarLike]
_StrTup = _t.Tuple[_StrLike]
_MatTup = _t.Tuple[_MatLike]
_ArrTup = _t.Tuple[_ArrLike]
__all__.extend(["_Tup", "_UnlimTup", "_NumTup", "_StrTup", "_MatTup", "_ArrTup"])

_Li = _t.List
_UnlimLi = _t.List[_AnyT]
_NumLi = _t.List[_ScalarLike]
_StrLi = _t.List[_StrLike]
_MatLi = _t.List[_MatLike]
_ArrLi = _t.List[_ArrLike]
__all__.extend(["_Li", "_UnlimLi", "_NumLi", "_StrLi", "_MatLi", "_ArrLi"])

_Dict = _t.Dict
_UnlimDict = _t.Dict[_AnyT, _AnyT]
_StrDict = _t.Dict[_StrLike, _AnyT]
__all__.extend(["_Dict", "_UnlimDict", "_StrDict"])


_DFrame = pd.DataFrame
_Series = pd.Series
__all__.extend(["_DFrame", "_Series"])

_MplFig = Figure
__all__.extend(["_MplFig"])

# others
_U = _t.Union
_overload = _t.overload
_Cal = _t.Callable
_Func = _types.FunctionType
_Hash = _t.Hashable
__all__.extend(["_U", "_overload", "_Cal", "_Func", "_Hash"])
