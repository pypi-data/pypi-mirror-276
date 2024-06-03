"""
Base metric Interface and Custom metric wrapper
character: non-root script
Author: Haokun Zhang <haokun.zhang@hirain.com>
Initial date: 05.21.2024
log: --
"""

import inspect

from ._utils import *
from .._internal._functools import *
from .._internal._typing import *
from .._internal._std import *


class Metric:
    """
    Metric inferface for encapsulating using steps and logic.

    Args:
    ---
        - name: name of metric
        - dtype: value type to be accumulated
        - shape: shape of passed value. Default to `None` as it is maybe passed a data structure.
        - reduction: reduce method when summarizing, available methods: `none`,
            `auto`, `sum`, `mean`, `max`, `min`.

    Standalone usage:

        ```python

            m = SomeMetric(...)

            for c1, c2, ... in _required_value_yielder:
                m.accumulate_step(c1, c2, ...)
            
            result = m.result() # get result variable
            m.summarize() # display results
            m.reset() # reset accumulations
        ```

    An example for calculating squared error using inside value container:

        ```python
            class SquaredError(Metric):
                def __init__(self, reduction="mean") -> None:
                    super().__init__(name="squared_error", reduction=reduction)
                    self._mse = self.add_value(float, initial="empty")

                def accumulate_step(self, dist1: float, dist2: float) -> None:
                    self._mse.append((dist1 - dist2) ** 2)

                def result(self):
                    return self._mse.reduce()
                
                def reset(self):
                    self._mse.reset()
        ```

    Or initialize an iterable as a state container in `__init__()` method:

        ```python
            class SquaredError(Metric):
                def __init__(self, reduction="mean") -> None:
                    super().__init__(name="squared_error", reduction=reduction)
                    self._mse = []

                def accumulate_step(self, dist1: float, dist2: float) -> None:
                    self._mse.append((dist1 - dist2) ** 2)

                def result(self):
                    return np.mean(self._mse)
                
                def reset(self):
                    self._mse.clear()
        ```

    Methods to be implemented by subclasses:
        - `__init__()`: A constructor to create all the state variables.
        - `accumulate_step(...)`: To define the pre-process and storage of value scores 
            or how a single-step metric is calculated.
        - `result()`: To define how the metric is calculated and return reduced values.
        - `reset()`: To define how the container is cleared and others are distructed.

    Methods can be overwritten by subclasses:
        - `summarize(...)`: This method is usually defined to display final metric scores. It
            commonly does not return.

    Other methods is strictly prohibited to be overwritten.
    """
    def __init__(self, name: _StrLike = None, dtype: _DType = None, shape: _AnyT = None, reduction: _LtrlAny = Reduction.AUTO) -> None:
        self.name: _StrLike = self.__reformat_class_name(name)
        self.dtype: _DType = dtype
        self.shape: _AnyT = shape
        self.reduction: _LtrlAny = reduction

    def __call__(self, *args: _AnyT, **kwargs: _AnyT):
        """
        
        """
        if kwargs:
            self._validate_kwargs(
                self.__get_func_arguments(self.accumulate_step),
                [_ for _ in kwargs.keys()]
            )
        self.accumulate_step(*args, **kwargs)

        return self
    
    def add_value(self, dtype: _DType = None, shape: _AnyT = None, init: _StrLike = None) -> State:
        return State(self.name, dtype, shape, init, self.reduction)
    
    def accumulate_step(self, *args: _AnyT, **kwargs: _AnyT) -> None:
        """
        
        """
        raise NotImplementedError("Method must be implemented by subclasses")

    def summarize(self, display: bool = ...) -> None:
        """
        
        """
        ...

    def result(self, reduction: _LtrlAny = None):
        """
        
        """
        raise NotImplementedError("Method must be implemented by subclasses")
    
    def reset(self):
        """
        
        """
        raise NotImplementedError("Method must be implemented by subclasses")
    
    @staticmethod
    def _validate_kwargs(kwargs: _Hash, kvals: _Hash):
        if not set(kwargs).issuperset(kvals):
            diff = set(kvals).difference(kwargs)
            raise InvalidArgumentError("Invalid argument(s): `{}`, valid arguments are: {}".format(" ".join(diff), kwargs))

    def __reformat_class_name(self, name: _StrLike = None):
        if name is None:
            _raw_name = []
            for index, _char in enumerate(type(self).__name__):
                if index != 0 and _char.isupper():
                    _char = "_" + _char
                _raw_name.append(_char)
            name = "".join(_raw_name).lower()
        return name
    
    @staticmethod
    def __get_func_arguments(func: _Func) -> _Iter:
        __param_wrap = inspect.signature(func)
        return [__a for __a in __param_wrap.parameters.keys()]
    

class StatMetric(Metric):
    def __init__(self, name: _StrLike = None, dtype: _DType = None, shape: _AnyT = None) -> None:
        super().__init__(name, dtype, shape=None, reduction=Reduction.SUM)
        self._values = self.add_value(dtype, shape, "empty")
        self.shape = self._values.shape

    def accumulate_step(self, value: _AnyT) -> None:
        self._values.append(value)

    def result(self):
        return self._values.reduce()
    
    def reset(self):
        self._values.reset()

    @property
    def state(self):
        return self._values
    

class CombMetric(Metric):
    def __init__(self, n_stats: _IntLike = 1, name: _StrLike = None, dtype: _DType = None, reduction: _LtrlAny = Reduction.AUTO) -> None:
        super().__init__(name, dtype, reduction=reduction)
        self.n_stats = n_stats
        self._value_list = [self.add_value(dtype, init="empty") for _ in range(n_stats)]

    def accumulate_step(self, *values: _AnyT) -> None:
        for val, _accum in zip(values, self._value_list):
            _accum.append(val)

    def result(self):
        return [_r.reduce() for _r in self._value_list]
    
    def reset(self):
        for _accum in self._value_list:
            _accum.reset()

    @property
    def states(self):
        return self._value_list


class MetricWrapper(Metric):
    def __init__(self, name: _StrLike = None) -> None:
        super().__init__(name=name)
        self.metrics: _Li[Metric] = []

    @_overload
    def register_metrics(self, metrics: _Li[Metric]) -> None:...
    @_overload
    def register_metrics(self, *metrics: Metric) -> None:...

    def register_metrics(self, *args: Metric) -> None:
        if len(args) == 1 and isinstance(args[0], _Iter):
            metrics = args[0]
        else:
            assert isinstance(args, tuple)
            metrics = args
        
        for _index, _m in enumerate(metrics):
            if not isinstance(_m, Metric):
                raise TypeError("Argument {} type must be a `Metric`, got {}".format(_index, type(_m)))
            self.metrics.append(_m)
            
    def reset_metrics(self):
        self.metrics.clear()

    def accumulate_step(self, *args: _AnyT) -> None:
        assert len(args) == len(self.metrics)
        for _arg, _met in zip(args, self.metrics):
            _met.accumulate_step(_arg)

    def result(self):
        return {k: v for k, v in 
                zip(self.registered_metrics_, 
                    [_r.result() for _r in self.metrics]
                    )
                }
    
    def reset(self):
        for _m in self.metrics:
            _m.reset()

    @property
    def registered_metrics_(self):
        return [m.name for m in self.metrics]
    
    @property
    def num_registered_metrics_(self):
        return len(self.metrics)
