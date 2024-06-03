"""
Metric Wrapper & Compose, used for overall evaluation of E2E Tracking system.
character: non-root script
Author: Haokun Zhang <haokun.zhang@hirain.com>
Initial date: 05.21.2024
log: --
"""

import numpy as np
import motmetrics as mm
from motmetrics import MOTAccumulator
import pandas as pd

from .base_metric import Metric, MetricWrapper
from ._utils import MetricInterfaceAdapter
from ..parse import RecordParser, TrackContainerParser
from ..utils import _render_stdout
from ..track_compose import OdTrackingCompose
from .._internal._functools import *
from .._internal._typing import *
from .._internal._std import *


class CustomMotMetricWrapper(MetricWrapper):
    """
    
    """
    def __init__(self,
                 gt_match_thres: _FltLike = 5.,
                 dist_thres: _FltLike = 2.,
                 model: _StrLike = "pilot",
                 time_diff: _AnyT = 8,
                 cam_mea_bias: _AnyT = 0.,
                 rough_sync: bool = True,
                 sync_prcn_digit: _IntLike = 2,
                 name: _StrLike = None,) -> None:
        super().__init__(name)
        self._acc = MOTAccumulator(False)
        self._idgen = OdTrackingCompose(cost_thres=gt_match_thres, sync_box_coords=True)
        self._adapter = MetricInterfaceAdapter(time_diff=time_diff, cam_mea_bias=cam_mea_bias, 
                                               rough_sync=rough_sync, sync_prcn_digit=sync_prcn_digit)
        self._hparser = RecordParser(priority="ts", model=model)
        self._cparser = TrackContainerParser("ts")
        self._event: _DFrame = None
        self._fr: _ScalarLike = None

        self._dist_thres: _FltLike = dist_thres
        self._records: _Li = []

    def set_forward_range(self, upperbound: _ScalarLike, lowerbound: _ScalarLike) -> None:
        self._fr = [lowerbound, upperbound]

    def accumulate_step(self, gt_ids: _Iter, hyp_ids: _Iter, cost: _U[_Li, _MatLike], frame_id: _AnyT = None) -> None:
        cost = np.where(cost >= self._dist_thres, np.nan, cost)
        self._acc.update(gt_ids, hyp_ids, cost, frame_id)

    @_overload
    def accumulate(self, ground_truth:  _StrLike, hypothesis: _U[_Dict, _StrLike]) -> None:...
    @_overload
    def accumulate(self, _info: _U[MetricInterfaceAdapter, _DFrame, MOTAccumulator]) -> None:...

    def accumulate(self, *args) -> None:
        assert len(args) in [1, 2]
        if len(args) == 1:
            self._accumulate(args[0])
        else:
            self._accumulate(
                self._preprocess_infos(*args)
            )
        
    def summarize(self, 
                  display: bool = True, 
                  color: _AnyT = None,
                  nmap: _AnyT = None, 
                  round_decimal: _IntLike = None, 
                  col_space: _IntLike = None) -> _DFrame:

        return self._summarize([self.result()], display, color, nmap, round_decimal, col_space)
    
    @VersionControl("onhold")
    def summarize_record(self, 
                         display: bool = True,
                         reset_record: bool = True,
                         color: _AnyT = None,
                         nmap: _AnyT = None, 
                         round_decimal: _IntLike = None, 
                         col_space: _IntLike = None) -> _DFrame:
        
        res = self._summarize(self._records, display, color, nmap, round_decimal, col_space)
        if reset_record:
            self._records.clear()

        return res
        
    def _summarize(self,
                   result: _Li[_DFrame],
                   display: bool = True,
                   color: _AnyT = None,
                   nmap: _AnyT = None, 
                   round_decimal: _IntLike = None, 
                   col_space: _IntLike = None) -> _DFrame:
        
        color = "blue" if color is None else color
        round_decimal = 4 if not round_decimal else round_decimal
        col_space = 7 if not col_space else col_space

        rendered_res = pd.DataFrame(result).round(round_decimal)
        if nmap is not None:
            rendered_res = rendered_res.rename(columns=nmap)

        _title_summary = "\nMetric Scores@[forward range = {} | distance upperbound = {}]:".format(
                self._adapter.x_range_, self._dist_thres
            )
        
        _render_stdout(_title_summary, color, display)
        _render_stdout(rendered_res.to_string(col_space=col_space, index=False), color, display)

        return rendered_res
    
    def reset(self):
        super().reset()
        self._fr = None
        self._records.clear()
        # for _host in [self._acc, self._idgen, self._adapter, self._hparser, self._cparser]:
        #     _host.reset()

    @VersionControl("onhold")
    def record_result(self, reset: bool = False) -> None:
        """
        Record current accumulated result to a container.
        Custom usage: 
        ```python
            wrapper = SomeWrapper(...)
            
            for args in some_iterable:
                wrapper.accumulate(*args)
                wrapper.record_result(reset=True)

            wrapper.summarize_record(...)
            wraper.reset()
        ```

        Args:
        ---
            - reset: whether reset internal states before next accumulation round, default `False`
        """
        self._records.append(self.result())

        if reset:
            self.reset()


    def _preprocess_infos(self, ground_truth: _StrLike, hypothesis: _U[_Dict, _StrLike]) -> MetricInterfaceAdapter:
        # ground truth
        self._idgen.load_gt_file(ground_truth).traverse_all_labels()
        _parsed_gt = self._cparser(self._idgen.tracks_).result()

        # hypothesis
        if not hypothesis.endswith(".json"):
            hypothesis = self._hparser.load(hypothesis).get_result()

        return self._adapter.load_gt_hyp(_parsed_gt, hypothesis, self._fr).adapt()
    
    def _accumulate(self, _info: _U[MetricInterfaceAdapter, _DFrame, MOTAccumulator]) -> None:
        if isinstance(_info, MetricInterfaceAdapter):
            if _info.adapting_status is False:
                raise RuntimeError('the adapter has not adapt or fit any data yet,'\
                                'chould call `MetricInterfaceAdapter.adapt()` first.')
            _all_ts, _gt_ids, _hyp_ids, _costs = _info.get_results()
            _all_ts = [float(value) for value in _all_ts]

            for _ts, _gt_id, _hyp_id, _cost in zip(_all_ts, _gt_ids, _hyp_ids, _costs):
                self.accumulate_step(_gt_id, _hyp_id, _cost, _ts)

            self._event = self._acc.events.reset_index()
        else:
            self._event = _info if isinstance(_info, _DFrame) else _info.events.reset_index()
        
        for _met in self.metrics:
            _met.accumulate_step(self._event)

        for _host in [self._acc, self._idgen, self._adapter, self._hparser, self._cparser]:
            _host.reset()

    def _reset_accumulator_indices(self, events: _DFrame) -> _DFrame:
        return events.reset_index()


class MotOdMetricWrapper(object):
    """
    
    """
    def __init__(self, auto_frame_id: bool = False, max_switch_time: float = None, 
                 dist_thres: _AnyT = None, matured: int = None) -> None:
        """
        
        """
        self._max_switch_time = float('inf') if not max_switch_time else max_switch_time
        # self.matured = 1 if not matured else matured
        self._dist_thres = np.inf if not dist_thres else dist_thres
        self._auto_frame_id = auto_frame_id
        self._accum = mm.MOTAccumulator(auto_frame_id, self._max_switch_time)
        self._computer = mm.metrics.create()

        if matured is not None:
            raise NotImplementedError("Matured object count is not supported provisionally.")

    def accumulate_step(self, gt_ids: _Iter, hyp_ids: _Iter, 
                        cost: _U[_Li, _MatLike], frame_id: _AnyT = None) -> None:
        """
        
        """
        self._check_gt_hyp_cost_uniformity(gt_ids, hyp_ids, cost)
        self._accum.update(gt_ids, hyp_ids, cost, frame_id)

    def accumulate_from_adapter(self, adapter: MetricInterfaceAdapter) -> None:
        """
        
        """
        if not isinstance(adapter, MetricInterfaceAdapter):
            raise TypeError('argument must be an MetricInterfaceAdapter, but got {}'.format(type(adapter)))
        if adapter.adapting_status is False:
            raise RuntimeError('the adapter has not adapt or fit any data yet,'\
                               'chould call `MetricInterfaceAdapter.adapt()` first.')
        
        _all_ts, _gt_ids, _hyp_ids, _costs = adapter.get_results()
        _all_ts = [float(value) for value in _all_ts]

        for _ts, _gt_id, _hyp_id, _cost in zip(_all_ts, _gt_ids, _hyp_ids, _costs):
            frame_id = None if self._auto_frame_id is True else _ts
            _cost = np.where(_cost >= self._dist_thres, np.nan, _cost)
            self.accumulate_step(_gt_id, _hyp_id, _cost, frame_id)

    @UnImplemented
    def accumulate_all(*args, **kwargs):
        ...

    @UnImplemented
    def add_metric(metric: Metric, loc: int = None):...

    def _check_gt_hyp_cost_uniformity(self, *args, **kwargs) -> None:
        if args:
            gt_ids, hyp_ids, cost = args
        elif kwargs:
            gt_ids, hyp_ids, cost = kwargs['gt_ids'], kwargs['hyp_ids'], kwargs['cost']

        for item in [gt_ids, hyp_ids]:
            if not isinstance(item, _Iter):
                    raise ValueError('argument must be an iterable.')
        if len(gt_ids) != cost.shape[0] or len(hyp_ids) != cost.shape[1]:
            raise ValueError('id amout does not match cost dimension: gt: {}, hypothesis: {}, cost dimension: {}'.format(
                len(gt_ids), len(hyp_ids), cost.shape
            ))

    def summarize(self, 
                metrics: _U[str, _StrLi] = None,
                formatters: _AnyT = None,
                name_map: _AnyT = None,
                display: bool = True,
                out_color: _AnyT = None
                ) -> _DFrame:
        """
        
        """
        if out_color is None:
            out_color = ['black'] * 2
        if not isinstance(out_color, str) and isinstance(out_color, _Iter):
            if len(out_color) >= 2:
                out_color = out_color[:2]
            else:
                out_color = [out_color[0]] * 2
        else:
            out_color = [out_color] * 2

        if metrics is None:
            metrics = mm.metrics.motchallenge_metrics
        
        if not name_map:
            name_map = mm.io.motchallenge_metric_names

        _results = self._calculate(metrics, True).round(3)
        _rendered_results = self._render_summary(_results, formatters, name_map)

        if display:
            _title_summary = "\nMetric Scores@[max switch time = {} | cost threshold = {}]:".format(
                self._max_switch_time, self._dist_thres
            )
            print(_render_stdout(_title_summary, out_color[0]))
            print(_render_stdout(_rendered_results, out_color[1]))
            print("\n")

        return _results
    
    def format_result(self, metric_names: _StrLi, scores: _VecLike, round_scores: int = None) -> _DFrame:
        if not isinstance(scores, str) and round_scores:
            scores = np.array(scores)
            scores = np.round(scores, round_scores)
        return pd.DataFrame(scores, columns=metric_names)
    
    @_overload
    def render_result(self, metric_names: _StrLi, scores: _VecLike, *, round_decimal: int = None, nmap: _StrDict = None, out_color: _AnyT = None) -> _StrLike:...
    @_overload
    def render_result(self, dataframe: _DFrame, *, round_decimal: int = None, nmap: _StrDict = None, out_color: _AnyT = None) -> _StrLike:...
    
    def render_result(self, *args, round_decimal: int = None, nmap: _StrDict = None, out_color: _AnyT = None) -> _StrLike:
        if not nmap:
            nmap = mm.io.motchallenge_metric_names

        out_color = "blue" if out_color is None else out_color

        if len(args) == 1:
            _dataframe = args[0].round(round_decimal)
        elif len(args) == 2:
            _dataframe = self.format_result(args[0], args[1], round_decimal)
        else:
            raise InvalidArgumentError(
                "Function requires no more than 2 positional arguments, but got {}".format(len(args))
            )
        
        _rendered_res = self._render_summary(_dataframe, namemap=nmap)
        return _render_stdout(_rendered_res, out_color)
    
    def _calculate(self, metrics: _U[str, _StrLi] = None, return_dataframe: bool = True) -> _U[_DFrame, _Dict]:
        return self._computer.compute(self._accum, metrics=metrics, return_dataframe=return_dataframe)
    
    @staticmethod
    def _render_summary(summary: _DFrame, formatters=None, namemap=None, buf=None, col_space=None):
        r"""Render metrics summary to console friendly tabular output. 
            Adapted from `motmetrics.io.render_summary(...)`

        Params
        ------
        summary : pd.DataFrame
            Dataframe containing summaries in rows.

        Kwargs
        ------
        buf : StringIO-like, optional
            Buffer to write to
        formatters : dict, optional
            Dicionary defining custom formatters for individual metrics.
            I.e `{'mota': '{:.2%}'.format}`. You can get preset formatters
            from MetricsHost.formatters
        namemap : dict, optional
            Dictionary defining new metric names for display. I.e
            `{'num_false_positives': 'FP'}`.

        Returns
        -------
        string
            Formatted string
        """

        if namemap is not None:
            summary = summary.rename(columns=namemap)
            if formatters is not None:
                formatters = {namemap.get(c, c): f for c, f in formatters.items()}

        if col_space is None:
            col_space = 8

        output = summary.to_string(
            buf=buf,
            formatters=formatters,
            index=False,
            col_space=col_space
        )

        return output
    
    @VersionControl('onhold')
    def calculate_parts(self) -> _AnyT:
        ...

    def reset(self) -> None:
        self._accum.reset()

    @property
    def mot_events_(self):
        return self._accum.mot_events
    
    @property
    def events_(self):
        return self._accum.events
    