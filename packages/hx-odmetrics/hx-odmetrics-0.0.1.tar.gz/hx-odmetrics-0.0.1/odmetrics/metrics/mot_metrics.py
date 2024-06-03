"""
Pre-defined custom MOT metrics
character: non-root script
Author: Haokun Zhang <haokun.zhang@hirain.com>
Initial date: 05.24.2024
log: --
"""

from motmetrics import MOTAccumulator
import pandas as pd
import numpy as np

from .base_metric import Metric, MetricWrapper
from ._utils import Reduction, MetricInterfaceAdapter, _render_stdout
from .base_motmetric import *
from .._internal._functools import *
from .._internal._typing import *
from .._internal._std import *


class IdTruePositives(_MotIdStatSubclass):
    def _compute(self) -> _IntLike:
        return self._n_objs - self._fnmat[self._rids, self._cids].sum()


class IdFalsePositives(_MotIdStatSubclass):
    def _compute(self) -> _IntLike:
        return self._fpmat[self._rids, self._cids].sum()


class IdFalseNegatives(_MotIdStatSubclass):
    def _compute(self) -> _IntLike:
        return self._fnmat[self._rids, self._cids].sum()


class IdPrecision(_MotIdCombSubclass):
    def __init__(self, name: _StrLike = None, reduction=Reduction.AUTO) -> None:
        super().__init__(2, name, reduction)

    @_overload
    def accumulate_step(self, idtp: _IntLike, idfp: _IntLike) -> None:...
    @_overload
    def accumulate_step(self, event: _DFrame) -> None:...
    def accumulate_step(self, *args) -> None:
        return super().accumulate_step(*args)

    def _compute(self) -> _AnyT:
        return self._n_objs - self._fnmat[self._rids, self._cids].sum(),\
            self._fpmat[self._rids, self._cids].sum()
    
    def result(self):
        idtp, idfp = super().result()
        return idtp / (idtp + idfp + 1e-8)
        

class IdRecall(_MotIdCombSubclass):
    def __init__(self, name: _StrLike = None, reduction=Reduction.AUTO) -> None:
        super().__init__(2, name, reduction)

    @_overload
    def accumulate_step(self, idtp: _IntLike, idfn: _IntLike) -> None:...
    @_overload
    def accumulate_step(self, event: _DFrame) -> None:...
    def accumulate_step(self, *args) -> None:
        return super().accumulate_step(*args)

    def _compute(self) -> _AnyT:
        idfn = self._fnmat[self._rids, self._cids].sum()
        return self._n_objs - idfn, idfn
    
    def result(self) -> _ScalarLike:
        idtp, idfn = super().result()
        return idtp / (idtp + idfn + 1e-8)


class IdF1Score(_MotIdCombSubclass):
    def __init__(self, name: _StrLike = None, reduction=Reduction.AUTO) -> None:
        super().__init__(3, name, reduction)

    @_overload
    def accumulate_step(self, idtp: _IntLike, idfp: _IntLike, idfn: _IntLike) -> None:...
    @_overload
    def accumulate_step(self, event: _DFrame) -> None:...
    def accumulate_step(self, *args) -> None:
        return super().accumulate_step(*args)

    def _compute(self) -> _AnyT:
        return self._compute_stats()
    
    def result(self):
        idtp, idfp, idfn = super().result()
        return  2 * idtp / (2 * idtp + idfp + idfn + 1e-8)


class UniqueObjectAmount(_MotCustomStatSubclass):
    def _compute(self) -> _IntLike:
        return len(self._obj_freq)

class MostlyTrackedAmount(_MotCustomStatSubclass):
    def __init__(self, threshold: _FltLike = 0.8, name: _StrLike = None) -> None:
        super().__init__(name)
        self.threshold: _FltLike = threshold

    def _compute(self) -> _IntLike:
        return self._tracked_ratio[self._tracked_ratio >= self.threshold].count()
    
class PartiallyTrackedAmount(_MotCustomStatSubclass):
    def __init__(self, upper: _FltLike = 0.8, lower: _FltLike = 0.2, name: _StrLike = None) -> None:
        super().__init__(name)
        self.upper: _FltLike = upper
        self.lower: _FltLike = lower

    def _compute(self) -> _IntLike:
        return self._tracked_ratio[
            (self._tracked_ratio >= self.lower) & (self._tracked_ratio < self.upper)
        ].count()

class MostlyLostAmount(_MotCustomStatSubclass):
    def __init__(self, threshold: _FltLike = 0.2, name: _StrLike = None) -> None:
        super().__init__(name)
        self.threshold: _FltLike = threshold

    def _compute(self) -> _IntLike:
        return self._tracked_ratio[self._tracked_ratio < self.threshold].count()
    

class SwitchedAmount(_MotCustomStatSubclass):
    def _compute(self) -> _IntLike:
        return self._eventn.Type.isin(["SWITCH"]).sum()
    
class TransferredAmount(_MotCustomStatSubclass):
    def _compute(self) -> _IntLike:
        return self._mot_event.Type.isin(["TRANSFER"]).sum()
    

class AscendedAmount(_MotCustomStatSubclass):
    def _compute(self) -> _IntLike:
        return self._mot_event.Type.isin(["ASCEND"]).sum()
    

class MigratedAmount(_MotCustomStatSubclass):
    def _compute(self) -> _IntLike:
        return self._mot_event.Type.isin(["MIGRATE"]).sum()
    

class FragmentationAmount(_MotCustomStatSubclass):
    def _compute(self) -> _IntLike:
        fra = 0
        for _o in self._obj_freq.index:
            _dfo = self._eventn[self._eventn.OId == _o]
            _not_miss = _dfo[_dfo.Type != "MISS"]
            if len(_not_miss) == 0: 
                continue

            _first_notmiss = _not_miss.index[0]
            _last_notmiss = _not_miss.index[-1]
            diffs = _dfo.loc[_first_notmiss: _last_notmiss].Type.apply(
                lambda x: 1 if x == "MISS" else 0
            ).diff()
            fra += diffs[diffs == 1].count()

        return fra

class ObjectAmount(_MotCustomStatSubclass):
    def _compute(self) -> _IntLike:
        return self._eventn[self._eventn.Type.isin(["MATCH", "MISS", "SWITCH"])].OId.count()


class HypothesisAmount(_MotCustomStatSubclass):
    def _compute(self) -> _IntLike:
        return self._eventn[self._eventn.Type.isin(["MATCH", "FP", "SWITCH"])].HId.count()
    
class TruePositives(_MotCustomStatSubclass):
    def _compute(self) -> _IntLike:
        return self._eventn.Type.isin(["MATCH", "SWITCH"]).sum()
    

class FalsePositives(_MotCustomStatSubclass):
    def _compute(self) -> _IntLike:
        return self._eventn.Type.isin(["FP"]).sum()
    

class FalseNegatives(_MotCustomStatSubclass):
    def _compute(self) -> _IntLike:
        return self._eventn.Type.isin(["MISS"]).sum()


class MotAccuracy(_MotCustomCombSubclass):
    def __init__(self, name: _StrLike = None, reduction=Reduction.AUTO) -> None:
        super().__init__(4, name, reduction)

    @_overload
    def accumulate_step(self, n_obj: _IntLike, fp: _IntLike, fn: _IntLike, switched: _IntLike) -> None:...
    @_overload
    def accumulate_step(self, event: _DFrame) -> None:...
    def accumulate_step(self, *args) -> None:
        return super().accumulate_step(*args)
    
    def _compute(self) -> _FltLike:
        return self._eventn[self._eventn.Type.isin(["MATCH", "MISS", "SWITCH"])].OId.count(),\
        self._eventn.Type.isin(["FP"]).sum(), self._eventn.Type.isin(["MISS"]).sum(),\
        self._eventn.Type.isin(["SWITCH"]).sum()
    
    def result(self):
        n_obj, fp, fn, sw = super().result()
        return 1. - (fp + fn + sw) / (n_obj + 1e-8)
        
        
class MotPrecision(_MotCustomCombSubclass):
    def __init__(self, name: _StrLike = None, reduction=Reduction.AUTO) -> None:
        super().__init__(2, name, reduction)

    @_overload
    def accumulate_step(self, dist_sum: _FltLike, n_match: _IntLike) -> None:...
    @_overload
    def accumulate_step(self, event: _DFrame) -> None:...
    def accumulate_step(self, *args) -> None:
        return super().accumulate_step(*args)
    
    def _compute(self) -> _AnyT:
        _matched = self._mot_event[self._mot_event.Type == "MATCH"]
        return _matched.D.sum(), _matched.OId.count()
    
    def result(self):
        ds, n_match = super().result()
        return ds / (n_match + 1e-8)
    

class Precision(_MotCustomCombSubclass):
    def __init__(self, name: _StrLike = None, reduction=Reduction.AUTO) -> None:
        super().__init__(2, name, reduction)

    @_overload
    def accumulate_step(self, tp: _FltLike, fp: _IntLike) -> None:...
    @_overload
    def accumulate_step(self, event: _DFrame) -> None:...
    def accumulate_step(self, *args) -> None:
        return super().accumulate_step(*args)
    
    def _compute(self) -> _AnyT:
        return [self._eventn.Type.isin(_rep).sum() for _rep in [["MATCH", "SWITCH"], ["FP"]]]
    
    def result(self):
        tp, fp = super().result()
        return tp / (tp + fp + 1e-7)
    

class Recall(_MotCustomCombSubclass):
    def __init__(self, name: _StrLike = None, reduction=Reduction.AUTO) -> None:
        super().__init__(2, name, reduction)

    @_overload
    def accumulate_step(self, tp: _FltLike, fn: _IntLike) -> None:...
    @_overload
    def accumulate_step(self, event: _DFrame) -> None:...
    def accumulate_step(self, *args) -> None:
        return super().accumulate_step(*args)
    
    def _compute(self) -> _AnyT:
        return [self._eventn.Type.isin(_rep).sum() for _rep in [["MATCH", "SWITCH"], ["MISS"]]]
    
    def result(self):
        tp, fn = super().result()
        return tp / (tp + fn + 1e-7)


class MetricNameMap:
    def __init__(self, metrics: _Li[Metric], nmap: _Li) -> None:
        assert len(metrics) == len(nmap)
        self.metrics: _Li = metrics
        self.nmap: _Dict = {k.name: v for k, v in zip(metrics, nmap)}
    
    @property
    def metric_names_(self):
        return [_m.name for _m in self.metrics]

    
class MetricEnum:
    mot_metrics = MetricNameMap(
        [
        IdF1Score(),
        IdPrecision(),
        IdRecall(),
        Recall(),
        Precision(),
        UniqueObjectAmount(),
        MostlyTrackedAmount(threshold=.8),
        PartiallyTrackedAmount(upper=.8, lower=.2),
        MostlyLostAmount(threshold=.2),
        ObjectAmount(),
        HypothesisAmount(),
        FalsePositives(),
        FalseNegatives(),
        SwitchedAmount(),
        FragmentationAmount(),
        MotAccuracy(),
        MotPrecision()
    ],
    [
        "IDF1", "IDP", "IDR", "Rcll", "Prcn", "GT", "MT", "PT",
        "ML", "objGT", "Hyps", "FP", "FN", "IDs", "FM", "MOTA", "MOTP"
        ]
    )

    common_metrics = MetricNameMap(
        [
        IdPrecision(),
        IdRecall(),
        Recall(),
        Precision(),
        UniqueObjectAmount(),
        MostlyTrackedAmount(threshold=.8),
        MostlyLostAmount(),
        ObjectAmount(),
        HypothesisAmount(),
        FalsePositives(),
        FalseNegatives(),
        SwitchedAmount(),
        MotAccuracy(),
        MotPrecision()
    ],
    [
        "IDP", "IDR", "Rcll", "Prcn", "GT", "MT", 
        "ML", "objGT", "Hyps", "FP", "FN", "IDs", "MOTA", "MOTP"
        ]
    )
    
    stat_metrics = MetricNameMap(
        [
        UniqueObjectAmount(),
        MostlyTrackedAmount(threshold=.8),
        PartiallyTrackedAmount(upper=.8, lower=.2),
        MostlyLostAmount(threshold=.2),
        ObjectAmount(),
        HypothesisAmount(),
        FalsePositives(),
        FalseNegatives(),
        SwitchedAmount(),
        FragmentationAmount(),
    ],
    [
        "GT", "MT", "PT", "ML", "objGT", "Hyps", "FP", "FN", "IDs", "FM"
        ]
    )
    
    comb_metrics = MetricNameMap(
        [
        IdF1Score(),
        IdPrecision(),
        IdRecall(),
        Recall(),
        Precision(),
        MotAccuracy(),
        MotPrecision()
    ],
    [
        "IDF1", "IDP", "IDR", "Rcll", "Prcn", "MOTA", "MOTP"
        ]
    )
    
