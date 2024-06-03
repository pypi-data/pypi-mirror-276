"""
Base mot-metirc interface for metric extention
character: non-root script
Author: Haokun Zhang <haokun.zhang@hirain.com>
Initial date: 05.29.2024
log: --
"""

from .base_metric import Metric, StatMetric, CombMetric
from ._utils import match_global_ids, Reduction
from .._internal._functools import *
from .._internal._typing import *
from .._internal._std import *


__all__ = [
    "MotMetric",
    "MotIdMetric",
    "MotCustomMetric",
    "_MotIdCombSubclass",
    "_MotIdStatSubclass",
    "_MotCustomCombSubclass",
    "_MotCustomStatSubclass"
]


class MotMetric(Metric):
    def __init__(self, name: _StrLike = "mot_metric") -> None:
        super().__init__(name=name)

    def _check_event_attributes(self, event: _DFrame) -> _DFrame:
        _requried_attributes = ["FrameId", "Type", "OId", "HId", "D"]
        _requried_type_cates = ['FP', 'MATCH', 'MISS', 'RAW', 'SWITCH']

        for _attr in _requried_attributes:
            if not hasattr(event, _attr):
                raise AttributeError("Event does not have attribute {}".format(_attr))
            
        if not set(event.Type).issuperset(_requried_type_cates):
            diff = set(_requried_type_cates).difference(event.Type)
            raise KeyError("events Type series does not have key(s): `{}`".format(" ".join(diff)))
        
        return event
    
    def _check_accumulator_status(self) -> bool:
        if self.event_.to_numpy().size == 0:
            return False
        return True
    
    def _check_status(self, _check_list: _Iter = None) -> None:
        if _check_list is None:
            _check_list = [self._check_accumulator_status()]

        for _item in _check_list:
            if _item is None:
                raise RuntimeError("Metric has not loaded anything yet, `call` the metric first.")


class MotIdMetric(MotMetric):
    """
    
    """
    def __init__(self, name: _StrLike = "mot_id_metric") -> None:
        super().__init__(name=name)
        self._idtp, self._idfp, self._idfn = [None] * 3

        self._n_objs: _IntLike = None
        self._fpmat: _MatLike =  None
        self._fnmat: _MatLike = None
        self._rids: _VecLike = None
        self._cids: _VecLike = None
        self._costs: _MatLike = None
        self._min_cost: _FltLike = None

    def accumulate_step(self, event: _DFrame) -> None:
        _assigns = match_global_ids(self._check_event_attributes(event))
        self._n_objs = _assigns['n_objects']
        self._fpmat, self._fnmat = _assigns['fpmatrix'], _assigns['fnmatrix']
        self._rids, self._cids = _assigns['rids'], _assigns['cids']
        self._costs, self._min_cost = _assigns['costs'], _assigns['min_cost']

    def reset(self):
        self._idtp, self._idfp, self._idfn = [None] * 3

        self._n_objs = None
        self._fpmat, self._fnmat = None, None
        self._rids, self._cids = None, None
        self._costs = None
        self._min_cost = None

    def _compute_stats(self) -> None:
        self._check_status([
            self._fpmat, self._fnmat, self._rids, self._cids, 
            self._costs, self._min_cost
        ])
        idfp = self._fpmat[self._rids, self._cids].sum()
        idfn = self._fnmat[self._rids, self._cids].sum()
        idtp = self._n_objs - idfn

        return idtp, idfp, idfn
    
    @property
    def idtp_(self):
        self._check_status([self._idtp])
        return self._idtp
    
    @property
    def idfp_(self):
        self._check_status([self._idfp])
        return self._idfp
    
    @property
    def idfn_(self):
        self._check_status([self._idfn])
        return self._idfn
    

class MotCustomMetric(MotMetric):
    def __init__(self, name: _StrLike = "mot_custom_metric") -> None:
        super().__init__(name)
        self._event: _DFrame = None
        self._mot_event: _DFrame = None
        self._eventn: _DFrame = None
        self._tracked_ratio = None

        self._obj_freq = None
        self._pred_freq = None

    def accumulate_step(self, event: _DFrame) -> None:
        self._event = self._check_event_attributes(event)
        self._mot_event = self._event[self._event.Type != "RAW"]
        self._eventn = self._event[self._event.Type.isin(["MATCH", "MISS", "SWITCH", "FP"])]
        self._obj_freq = self._eventn.OId.value_counts()
        self._pred_freq = self._eventn.HId.value_counts()
        _tracked = self._eventn[self._eventn.Type != 'MISS'].OId.value_counts()
        self._tracked_ratio = _tracked.div(self._obj_freq).fillna(0.)

    def reset(self):
        self._event: _DFrame = None
        self._mot_event: _DFrame = None
        self._eventn: _DFrame = None
        self._tracked_ratio = None

        self._obj_freq = None
        self._pred_freq = None
    

class _MotIdStatSubclass(MotIdMetric, StatMetric):
    def __init__(self, name: _StrLike = None) -> None:
        MotIdMetric.__init__(self, name=name)
        StatMetric.__init__(self, name, dtype=_IntLike)

    @_overload
    def accumulate_step(self, value: _U[_IntLike, _MatLike]) -> None:...
    @_overload
    def accumulate_step(self, event: _DFrame) -> None:...

    def accumulate_step(self, *args) -> None:
        assert len(args) == 1
        if isinstance(args[0], _DFrame):
            super().accumulate_step(args[0])
            self._values.append(self._compute())
        else:
            self._values.append(args[0])

    def _compute(self) -> _AnyT:...

    def result(self):
        return StatMetric.result(self)

    def reset(self):
        for _class in [MotIdMetric, StatMetric]:
            _class.reset(self)


class _MotIdCombSubclass(MotIdMetric, CombMetric):
    def __init__(self, n_stats: _IntLike = 1, name: _StrLike = None, reduction=Reduction.AUTO) -> None:
        MotIdMetric.__init__(self, name=name)
        CombMetric.__init__(self, n_stats, name, dtype=_FltLike, reduction=reduction)

    def accumulate_step(self, *args) -> None:
        if isinstance(args[0], _DFrame):
            MotIdMetric.accumulate_step(self, args[0])
            CombMetric.accumulate_step(self, *self._compute())
        else:
            assert len(args) == self.n_stats
            CombMetric.accumulate_step(self, *args)

    def _compute(self) -> _AnyT:...
        
    def result(self):
        return CombMetric.result(self)
    
    def reset(self):
        for _class in [MotIdMetric, CombMetric]:
            _class.reset(self)


class _MotCustomStatSubclass(MotCustomMetric, StatMetric):
    def __init__(self, name: _StrLike = None) -> None:
        MotCustomMetric.__init__(self, name)
        StatMetric.__init__(self, name=name, dtype=_IntLike)

    @_overload
    def accumulate_step(self, value: _U[_IntLike, _MatLike]) -> None:...
    @_overload
    def accumulate_step(self, event: _DFrame) -> None:...

    def accumulate_step(self, *args) -> None:
        assert len(args) == 1
        if isinstance(args[0], _DFrame):
            MotCustomMetric.accumulate_step(self, args[0])
            self._values.append(self._compute())
        else:
            self._values.append(args[0])

    def _compute(self) -> _IntLike:...

    def result(self):
        return StatMetric.result(self)

    def reset(self):
        for _class in [MotCustomMetric, StatMetric]:
            _class.reset(self)


class _MotCustomCombSubclass(MotCustomMetric, CombMetric):
    def __init__(self, n_stats: _IntLike = 1, name: _StrLike = None, reduction=Reduction.AUTO) -> None:
        MotCustomMetric.__init__(self, name=name)
        CombMetric.__init__(self, n_stats, name, dtype=_FltLike, reduction=reduction)

    def accumulate_step(self, *args) -> None:
        if isinstance(args[0], _DFrame):
            MotCustomMetric.accumulate_step(self, args[0])
            CombMetric.accumulate_step(self, *self._compute())
        else:
            assert len(args) == self.n_stats
            CombMetric.accumulate_step(self, *args)

    def _compute(self) -> _AnyT:...
        
    def result(self):
        return CombMetric.result(self)
    
    def reset(self):
        for _class in [MotCustomMetric, CombMetric]:
            _class.reset(self)
