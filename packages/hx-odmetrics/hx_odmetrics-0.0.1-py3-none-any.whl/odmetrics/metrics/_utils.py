"""
Metric utils
character: non-root script
Author: Haokun Zhang <haokun.zhang@hirain.com>
Initial date: 05.21.2024
log: --
"""

import numpy as np
import warnings, json
from scipy.optimize import linear_sum_assignment
from motmetrics.lap import linear_sum_assignment as lsa

from ..utils import get_batch_dist_eu, _render_stdout
from .._internal._functools import *
from .._internal._typing import *
from .._internal._std import *


__all__ = [
    "Reduction",
    "State",
    "match_global_ids",
    "MetricInterfaceAdapter"
]


class Reduction:
    """
    Reduction (non Enum) for defining metric reducing methodologies (Literal).
    """
    NONE = "none"
    AUTO = "auto"
    SUM = "sum"
    MEAN = "mean"
    MAX = "max"
    MIN = "min"


class State:
    """
    
    """
    def __init__(self, name: _StrLike = None, dtype: _DType = None, shape: _AnyT = None, 
                 init: _StrLike = None, reduction: _LtrlAny = Reduction.AUTO) -> None:
        super().__init__()
        self.name = name
        self.dtype = dtype
        self.shape = self.__reformat_shape(shape) if shape is not None else None
        self._init = "empty" if init is None else init
        self.reduction = reduction

        self.__values: _MatLike = None

    def __array__(self) -> _MatLike:
        return self.__values
    
    def __repr__(self) -> str:
        return "State {} shape:{}\n{} ".format(
            self.name, self.__values.shape, str(self.__values)
        )
        
    def append(self, value: _AnyT = None, shape: _AnyT = None) -> None:
        try:
            if shape is None:
                _shape = [1, -1] if self.shape is None else self.shape
            else:
                _shape = self.__reformat_shape(shape)
            value = np.asarray(value, dtype=self.dtype).reshape(_shape)
        except Exception as e:
            raise ValueError("Shape of passed value differ from pre-defined value shape, "
                             "error occured from:\n {}".format(e))
        
        if self.shape is None:
            self.shape = value.shape

        if self.__values is None:
            self.__values = self.__inital_methods(self._init)(self.shape)
        
        self.__values = np.append(self.__values, value, axis=0)
    
    def reset(self):
        self.__values = self.__inital_methods(self._init)(self.shape)

    def reduce(self, reduction: _LtrlAny = None, keepdims: bool = False) -> _AnyT:
        self.reduction = reduction if reduction else self.reduction
        res = self.__reduction_methods(keepdims)(self.__values)

        return res if res.size > 1 else res[0]
    
    def cast(self, dtype: _DType) -> None:
        self.__values.astype(dtype)

    def __reformat_shape(self, shape: _AnyT = None) -> _AnyT:
        if shape is None:
            return [1, 1]
        
        if not isinstance(shape, _Iter):
            if not isinstance(shape, int):
                raise TypeError("shape must be an integer or a tuple of integers.")
            shape = [1, shape]
        else:
            if len(shape) == 1:
                shape = [1] + list(shape)

        return shape

    def __inital_methods(self, method: _StrLike) -> _Func:
        _rand = np.random
        __initm = {
            "empty": lambda s: np.empty([0, s[-1]], dtype=self.dtype),
            "random": lambda s: _rand.random(s),
            "normal": lambda s: _rand.randn(*s),
            "uniform": lambda s: _rand.rand(*s),
            "zeros": lambda s: np.zeros(shape=s, dtype=self.dtype),
            "ones": lambda s: np.ones(shape=s, dtype=self.dtype),
        }

        return __initm[method]
    
    def __reduction_methods(self, keepdims: bool = False) -> _Func:
        __rn = {  
            Reduction.NONE: lambda x: np.asarray(x),  
            Reduction.MEAN: lambda x: np.mean(x, axis=0, keepdims=keepdims),  
            Reduction.SUM: lambda x: np.sum(x, axis=0, keepdims=keepdims),  
            Reduction.AUTO: lambda x: np.mean(x, axis=0, keepdims=keepdims)\
                if self.reduction in [Reduction.MEAN, Reduction.AUTO] else np.asarray(x),
            Reduction.MAX: lambda x: np.max(x, axis=0, keepdims=keepdims),
            Reduction.MIN: lambda x: np.min(x, axis=0, keepdims=keepdims),
        }

        return __rn[self.reduction]
    

def _extract_counts_from_events(event: _DFrame):
    """
    Extract gt ids, hypthesis occurance times and true positives from MOTAaccumulator events.\n
    Adapted from `motmetrics.metrics.extract_counts_from_df_map(...)`.

    Args:
    ---
        - events: events DataFrame accumulated by `MOTAaccumulator`.

    Returns:
    ---
        Tuple (ocs, hcs, tps).
        - ocs: Dict from object id to count.
        - hcs: Dict from hypothesis id to count.
        - tps: Dict from (object id, hypothesis id) to true-positive count.
            The ids are arbitrary, they might NOT be consecutive integers from 0.
    """
    oids = event["OId"].dropna().unique()
    hids = event["HId"].dropna().unique()
    
    flat = event[event.Type == "RAW"].reset_index()
    flat = flat[flat["OId"].isin(oids) | flat["HId"].isin(hids)]
    o_occur = flat.set_index("OId")["FrameId"].groupby("OId").nunique().to_dict()
    h_occur = flat.set_index("HId")["FrameId"].groupby("HId").nunique().to_dict()
    dists = flat[["OId", "HId", "D"]].set_index(["OId", "HId"]).dropna()
    tps = dists.groupby(["OId", "HId"])["D"].count().to_dict()

    return o_occur, h_occur, tps


@ToModify("Do not use external LSA")
def match_global_ids(event: _DFrame):
    """
    ID measures: Global min-cost assignment for ID measures.
    Copied from `motmetrics.metrics.id_global_assignment`.

    Args:
    ---
        - events: events DataFrame accumulated by `MOTAaccumulator`.

    Returns:
    ---
        - A dictionary contains assigned ids and cost matrices.
    
    """
    ocs, hcs, tps = _extract_counts_from_events(event)

    no, nh = len(ocs), len(hcs)
    oids, hids = [sorted(list(map(int, _ids))) for _ids in [ocs.keys(), hcs.keys()]]
    oids_idx, hids_idx = [
        dict((_id, _idx) for _idx, _id in enumerate(_ids)) 
        for _ids in [oids, hids]
        ]
    
    fpmatrix = np.zeros((no + nh, no + nh), np.float_)
    fnmatrix = np.zeros((no + nh, no + nh), np.float_)
    fpmatrix[no:, :nh] = np.nan
    fnmatrix[:no, nh:] = np.nan

    for oid, oc in ocs.items():
        r = oids_idx[oid]
        fnmatrix[r, :nh] = oc
        fnmatrix[r, nh + r] = oc

    for hid, hc in hcs.items():
        c = hids_idx[hid]
        fpmatrix[:no, c] = hc
        fpmatrix[c + no, c] = hc

    for (oid, hid), ex in tps.items():
        r = oids_idx[oid]
        c = hids_idx[hid]
        fpmatrix[r, c] -= ex
        fnmatrix[r, c] -= ex

    costs = fpmatrix + fnmatrix
    rids, cids = lsa(costs)

    return {
        "n_objects": sum(ocs.values()),
        "fpmatrix": fpmatrix,
        "fnmatrix": fnmatrix,
        "rids": rids,
        "cids": cids,
        "costs": costs,
        "min_cost": costs[rids, cids].sum(),
    }


class MetricInterfaceAdapter:
    """
    MetricInterfaceAdapter: an adapter for MOT od tracking evaluating metrics.\n
    The class takes as input `gt` and `hypothesis` dictionaries, synchronizes timestamps 
    and shift to outputs that adapt `py-motmetrics` interface. 
    See <https://github.com/cheind/py-motmetrics> for more information.

    The loaded json file or dictionary file should be strictly 
    structured priorly by timestamp, i.e.:
    ```python
    {<timestamp>[str]: 
        [
            {'type'[str]: ..., 
            'id'[int]: ..., 
            'boxes'[list]: ...
            } 
            ...
        ]
        ...
    }
    ```
    """
    _HAS_ADAPTED = False
    def __init__(self, time_diff: int = 0, cam_mea_bias: float = 0.,
                 rough_sync: bool = False, sync_prcn_digit: int = 2) -> None:
        """
        Args:
        ----
            - time_diff Optional[int]: gt time differ from hypothesis timestamps, unit: per hour, default 0.
            - cam_mea_bias Optional[float]: time bias beteen camera sensor and msg measurement timestamp: cam_ts - mea_ts
            - rough_sync Optional[bool]: synchronize by nearest timestamp matching, default: False
            - sync_prcn_digit Optional[int]: number of kept float-point digits used for synchronizing timestamps, default: 2,
                if `rough_sync` is True, the arg will not be considered.

        """
        self._sync_prcn_digit = sync_prcn_digit
        self._cam_mea_bias = cam_mea_bias
        self._rough_sync = rough_sync
        self._unix_time_diff = time_diff * 60 ** 2
        self._gt, self._hyp = None, None
        self._all_timestamps, self._gt_ids, self._hyp_ids, self._costs = [None] * 4
        self._x_range: _Iter = None
    
    def load_gt_hyp(self, gt: _U[_Dict, _StrLike], hyp: _U[_Dict, _StrLike], foward_range: _Li = None):
        """
        Load groud truth and hypothesis information.

        Args:
        ----
            - gt Union[dict, str]: a gt dictionary data structure or a path to gt .json file.
            - hyp Union[dict, str]: a hypothesis dictionary data structure or a path to hypothesis .json file.

        Returns:
        ---
            Self@MetricInterfaceAdapter
        """
        _args = [gt, hyp]
        for _idx, _arg in enumerate(_args):
            if not isinstance(_arg, (_Dict, str)):
                raise TypeError("Type of arguments must be a string or a dictionary, got {} at argument {}".format(type(_arg), _idx))
        __f = lambda x: self._load_json(x) if isinstance(x, str) else x

        self._gt, self._hyp = [__f(_arg) for _arg in _args]
        for index, _item in enumerate([self._gt, self._hyp]):
            if not _item:
                raise ValueError("Arg {} does not have any content.".format(index))
        self._x_range = self._filter_result_centers(self._gt, self._hyp, x_range=foward_range)

        del _args
        return self
    
    def adapt(self):
        """
        This method modifies the format of inputs to that fitted by py-motmetrics. Note that if there is no object
        appeared at a particular timestamp, the cost matrix will be made a placeholder NDArray with a empty size.
        This method takes no argument and return the class itself.\n
        """
        self._synchronize_by_timestamp()

        _iter_list = [self._gt] * 2 if self._rough_sync is False else [self._gt, self._hyp]
        _all_timestamps = [[_ts for _ts in item.keys()] for item in _iter_list]

        _gt_ids, _hyp_ids, _costs = [], [], []
        for _gts, _hts in zip(*_all_timestamps):
            _gt_ts, _hyp_ts = self._gt[_gts], self._hyp[_hts]
            _gt_ids.append([item['id'] for item in _gt_ts])
            _hyp_ids.append([item['id'] for item in _hyp_ts])

            _gt_boxes = [item['boxes'][:3] for item in _gt_ts]
            _hyp_boxes = [item['boxes'][:3] for item in _hyp_ts]

            if _gt_ts and _hyp_ts:
                _costs.append(
                    get_batch_dist_eu(np.asarray(_gt_boxes), np.asarray(_hyp_boxes))
                )
            else: # other 3 cases
                _costs.append(np.empty([len(_gt_ts), len(_hyp_ts)]))

        self._all_timestamps, self._gt_ids, self._hyp_ids, self._costs =\
            _all_timestamps[0], _gt_ids, _hyp_ids, _costs
        self._HAS_ADAPTED = True
        
        del _iter_list
        return self
    
    def get_results(self) -> _Tup[_StrLi, _Li[_Li[int]], _Li[_Li[int]], _ArrLi]:
        """
        
        """
        if self._HAS_ADAPTED is False:
            raise ValueError('No result is provided as the adapter has not adapt data yet.')
        return self._all_timestamps, self._gt_ids, self._hyp_ids, self._costs
    
    def reset(self) -> None:
        self._all_timestamps, self._gt_ids, self._hyp_ids, self._costs = [None] * 4
        self._HAS_ADAPTED = False
    
    @staticmethod
    def _correct_timestamps(timestamps: _U[_Iter, str], diff: float) -> _StrLi:
        if diff != 0:
            timestamps = [
                str(float(item) - diff) for item in timestamps
            ]
        return timestamps

    def _synchronize_by_timestamp(self) -> None:
        _ts_intersect = self._check_gt_hyp_uniformity()
        
        if self._rough_sync is False:
            _ts_intersect = sorted(_ts_intersect)

            self._gt = {_ts: self._gt[_ts] for _ts in _ts_intersect}
            self._hyp = {_ts: self._hyp[_ts] for _ts in _ts_intersect}
        else:
            _gt_ts, _hyp_ts = _ts_intersect
            self._gt = {_ts: self._gt[_ts] for _ts in _gt_ts}
            self._hyp = {_ts: self._hyp[_ts] for _ts in _hyp_ts}

        for _dic in [self._gt, self._hyp]:
            self._check_seq_mono_increase(_dic.keys())
        assert len(self._gt) == len(self._hyp), 'final gt and hypothesis must have equal amount,'\
            ' got {} vs. {}, {}'.format(len(self._gt), len(self._hyp), _ts_intersect)
        
    @Deprecated
    def _sort_dict_by_ts(self, dictionary: _Dict):
        res_list = sorted(dictionary.items(), key=lambda x: x[0])
        sorted_dict = {x[0]: x[1] for x in res_list}
        self._check_seq_mono_increase(sorted_dict.keys())
        return sorted_dict
    
    @staticmethod
    def _substitude_dict_key(_dic: _Dict, _new_keys: _Iter) -> _Dict:
        assert len(_dic) == len(_new_keys), 'amount of new keys must equal dict length,'\
            'got {} vs. {}'.format(len(_new_keys), len(_dic))
        
        _key_map = {_old: _new for _old, _new in zip(list(_dic.keys()), _new_keys)}

        return {_key_map[old_key]: value for old_key, value in _dic.items()}

    def _check_loading_status(self):
        if not all([self._gt, self._hyp]):
            raise ValueError("gt and hypothesis do not exist, please load files first.")
        
    def _check_seq_mono_increase(self, arr: _Iter) -> None:
        arr = np.asarray([i for i in arr], dtype=np.float32)
        _cum_subtract = arr[1:] - arr[:-1]
        if any(_cum_subtract < 0.):
            raise ValueError("timestamp in dict is not ordered sequentially.")
    
    def _round_timestamps(self, arr: _Iter) -> _StrLi:
        _border_idx = 10 + 1 + self._sync_prcn_digit # 10 int digit 1 point + n_keep digitals
        return [str(value)[:_border_idx] for value in arr]
    
    def _check_gt_hyp_uniformity(self):
        self._check_loading_status()
        _gt_timestamps = self._correct_timestamps([_ts for _ts in self._gt.keys()], 
                                                  self._unix_time_diff)
        self._gt = self._substitude_dict_key(self._gt, _gt_timestamps)
        _hyp_timestamps = self._correct_timestamps([_ts for _ts in self._hyp.keys()], -self._cam_mea_bias)
        self._hyp = self._substitude_dict_key(self._hyp, _hyp_timestamps)

        if self._rough_sync is False:
            _gt_timestamps, _hyp_timestamps = [
                self._round_timestamps(_list) for _list in [_gt_timestamps, _hyp_timestamps]
            ]

            self._gt, self._hyp = [self._substitude_dict_key(_dict, _keys) for _dict, _keys in zip(
                [self._gt, self._hyp], [_gt_timestamps, _hyp_timestamps]
                                )]
            _intersect = set(_gt_timestamps).intersection(_hyp_timestamps)

            if not _intersect:
                raise TypeError("gt and hypothesis timestamps do not match.")
            elif len(_intersect) != len(_gt_timestamps):
                msg = "gt timestamps do not completely contained in hypothesis timestamps, "\
                            "contained timestamp amount: {}/{}".format(len(_intersect), len(_gt_timestamps))
                warnings.warn(
                    _render_stdout(msg, 'red'), RuntimeWarning
                )
                
            return _intersect
        else:
            _gt_timestamps, _hyp_timestamps = [np.asarray([float(i) for i in item])  # convert to float
                                               for item in [_gt_timestamps, _hyp_timestamps]]
            
            _gt_timestamps, _hyp_timestamps = self._filter_by_range_intesection(_gt_timestamps, _hyp_timestamps) # get range
            
            _gt_ts_idx, _hyp_ts_idx = self._match_timestamps(_gt_timestamps, _hyp_timestamps) # match

            # applying match indices
            _gt_timestamps, _hyp_timestamps = _gt_timestamps[_gt_ts_idx], _hyp_timestamps[_hyp_ts_idx]
            _gt_timestamps, _hyp_timestamps = [[str(i) for i in item] for item in # convert back to str
                                               [_gt_timestamps.tolist(), _hyp_timestamps.tolist()]]
            
            return _gt_timestamps, _hyp_timestamps
    
    @staticmethod
    def _filter_by_range_intesection(_gt_ts, _hyp_ts) -> _NumTup:
        _gt_min, _gt_max = np.min(_gt_ts), np.max(_gt_ts)
        _hyp_min, _hyp_max = np.min(_hyp_ts), np.max(_hyp_ts)
        _range_intersect = (np.maximum(_gt_min, _hyp_min), np.minimum(_gt_max, _hyp_max))

        if _range_intersect[0] >= _range_intersect[1]:
            raise TypeError("No intersection between gt and hypothesis, perhaps they do not match: "\
                            "gt range: ({:.2f}, {:.2f}) vs. hypothesis range: ({:.2f}, {:.2f})"\
                                .format(_gt_min, _gt_max, _hyp_min, _hyp_max)
                                )
        _masked_gt_ts, _masked_hyp_ts = [
            item[np.logical_and(item >= _range_intersect[0], item <= _range_intersect[1])]
                     for item in [_gt_ts, _hyp_ts]]
        
        if len(_masked_gt_ts) != len(_gt_ts):
            msg = "gt timestamps do not completely contained in hypothesis timestamps, "\
                            "contained timestamp amount: {}/{}".format(len(_masked_gt_ts), len(_gt_ts))
            warnings.warn(
                _render_stdout(msg, 'red'), RuntimeWarning
            )
        
        return _masked_gt_ts, _masked_hyp_ts
    
    @staticmethod
    def _filter_result_centers(*results: _Iter[_StrDict], 
                               max_fov: _ScalarLike = 120, x_range: _Li = None) -> _Li:
        """
        Filter boxes that are out of perceptive area. Default: filter boxes outside ADAS front camera with fov of 120
        at coordinate of 'ego' which is self body coordinate. Self orientation coordinates is defaulted to: 'xyz'->'flu'.

        Args:
        ----
            - results Iterable[dict[str, list]: dictionaries which boxes need to be filtered.\n
            - max_fov Any: camera forward vision angle limit, default: 120.\n
            - x_range Any: threshold of distances of boxes at 'forward' direction. boxes which x are less than this range
                is considered too close (far) to keep.

        This method operates in-plcace and does not return anything.
        """
        if x_range is None:
            x_range = [0., float("inf")]
        else:
            if len(x_range) != 2 or x_range[0] >= x_range[1]:
                raise ValueError("Invalid distance range")
            x_range = list(x_range)
        x_range[0] = max(x_range[0], 1.5)

        _tolerant_edge_radius = (max_fov / 2) / 180 * np.pi
        for _result in results:
            for _ts, _item_list in _result.items():
                _filtered_list = []
                for _item in _item_list:
                    _x, _y = _item["boxes"][:2]
                    if np.logical_and(x_range[0] < _x <= x_range[1], 
                                      np.abs(_y / (_x - x_range[0])) <= np.tan(_tolerant_edge_radius)):
                        _filtered_list.append(_item)
                _result.update({_ts: _filtered_list})

        return x_range
    
    @staticmethod
    def _match_timestamps(arr1: _VecLike, arr2: _VecLike):
        arr1, arr2 = [np.asarray(item).reshape(-1, 1) for item in [arr1, arr2]]
        agent, task = arr1.reshape(-1, 1), arr2.reshape(1, -1)

        cost = np.abs(agent - task)
        return linear_sum_assignment(cost)

    @staticmethod
    def _load_json(path: str) -> _Dict:
        with open(path, "r") as f:
            _res = json.load(f)
        return _res
    
    def _check_adapting_status(self) -> None:
        if not self._HAS_ADAPTED:
            raise RuntimeError(
                "Unadapted adapter might cause inaccurate statistics/properties, please use method `adapt` first."
            )
    
    @property
    def adapting_status(self) -> bool:
        return self._HAS_ADAPTED
    
    @property
    def n_hypothesis(self) -> _IntLike:
        self._check_loading_status()
        self._check_adapting_status()
        _res = [len(_val) for _, _val in self._hyp.items()]

        return sum(_res)
    
    @property
    def n_gt_objects(self) -> _IntLike:
        self._check_loading_status()
        self._check_adapting_status()
        _res = [len(_val) for _, _val in self._gt.items()]

        return sum(_res)
    
    @property
    def x_range_(self):
        return self._x_range