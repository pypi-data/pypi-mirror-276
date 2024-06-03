"""
#!usr/bin/python3
This is a evaluating script provided for evaluating multiple cases.
character: entry
Author: Haokun Zhang <haokun.zhang@hirain.com>
log: --

"""

from argparse import ArgumentParser
from tqdm import tqdm
import pandas as pd
import warnings

from .utils import _render_stdout
from .metrics import *
from .track_compose import *
from .parse import *
from ._internal._functools import *


@VersionControl('onhold')
def _parse_arguments(args):
    ...


def _evaluate_many(gt_txt: str, hyp_txt: str):
    filenames, total_res_with_dist, _metric_names = [], [], []
    events = []
    _out_color = "blue"
    # _dists = [i for i in range(0, 140, 20)]
    # _dists = [[0, float("inf")]] + [[a, b] for a, b, in zip(_dists[:-1], _dists[1:])]
    _dists = [[0, float("inf")]] + [[0, 10], [10, 50], [50, 100], [100, 200]]

    for path in [gt_txt, hyp_txt]:
        with open(path, "r") as f:
            filenames.append([line.strip() for line in f.readlines()])

    assert len(filenames[0]) == len(filenames[1])
    print(_render_stdout(
        "Found {} cases to be evaluated.".format(len(filenames[0])),
        "blue"
    ))
    
    adapter = MetricInterfaceAdapter(time_diff=_args.time_diff,
                                     cam_mea_bias=_args.cam_mea_bias,
                                     rough_sync=_args.rough_sync,
                                     sync_prcn_digit=_args.sync_precision)
    metric = MotOdMetricWrapper(auto_frame_id=_args.auto_frame_id,
                                max_switch_time=float(_args.max_switch_time),
                                dist_thres=float(_args.metric_dist_thres),)
    compose = OdTrackingCompose(cost_thres=float(_args.gt_dist_thres))
    _parser = TrackContainerParser('ts')
    _hypparser = RecordParser("ts")

    pbar = tqdm(_dists, ncols=90, colour='red')
    for index, _dist in enumerate(pbar):
        pbar.set_description("distance: {}".format(_dist))
        total_res, _metric_names = [], []
        evaled_cases = []
        num_obj_gt, num_hyps = 0, 0
        for _gt, _hyp in zip(*filenames):
            _gt_info = _gt.split("/")[-1].split(".")[0]
            _hyp_info = [_s for _s in _hyp.split("/") if _s.startswith("HHPLT")]

            compose.load_gt_file(_gt)
            gt_dict = _parser(compose.traverse_all_labels().tracks_).result()

            if _args.gt_to_json:
                _parser.to_json("./" + _gt_info + ".json")

            if not _hyp.endswith(".json"):
                _hyp = _hypparser.load(_hyp).get_result()
            
            adapter.load_gt_hyp(gt_dict, _hyp, foward_range=_dist).adapt()
            metric.accumulate_from_adapter(adapter)

            _res = metric.summarize(display=False)
            _metric_names = _res.columns
            total_res.append(_res.to_numpy())

            num_obj_gt += adapter.n_gt_objects
            num_hyps += adapter.n_hypothesis
            evaled_cases.extend(_hyp_info)

            if index == 0:
                events.append(metric.mot_events_)

            compose.reset()
            adapter.reset()
            _parser.reset()
            metric.reset()
            _hypparser.reset()

        # metric scores settlement
        total_res = np.vstack(total_res)
        total_res = np.hstack([
            total_res[:, :5].mean(0, keepdims=True),
            total_res[:, 5: 13].sum(0, keepdims=True),
            total_res[:, 13: 15].mean(0, keepdims=True),
            total_res[:, 15:].sum(0, keepdims=True),
        ])

        # statistics insertion
        res = metric.format_result(metric_names=_metric_names, scores=total_res)
        res.insert(9, column="objGT", value=num_obj_gt)
        res.insert(10, column="Hyps", value=num_hyps)
        res.insert(0, column="Range(m:m)", value=":".join(list(map(str, _dist))))
        total_res_with_dist.append(res)
        res = metric.render_result(res, round_decimal=3)

        if index == 0:
            events = pd.concat(events, ignore_index=False)
            if _args.save_event:
                events.to_csv("all_events.csv")

        if index == len(_dists) - 1:
            pbar.set_description("Finished.")

    # events MOTP quantiles settlement
    _base_cols = ['Nmatch', 'mean', 'median', 'max', 'min']
    _quan_cols = [.1, .35, .75, .9, .95]

    _matched_dist = events["D"].dropna()
    values = np.asarray([
        len(_matched_dist), _matched_dist.mean(), _matched_dist.median(), _matched_dist.max(), _matched_dist.min()
    ]).round(3)
    values = np.append(values, _matched_dist.quantile(_quan_cols).values.round(3)).reshape(1, -1)

    # render summaries
    _render_stdout("\nEvaluation info: {} @[max distance threshold={}]\n"\
                    .format(" | ".join(evaled_cases), _args.metric_dist_thres), _out_color, True)
    
    
    _render_stdout("Overall evaluation:", _out_color, True)
    print(metric.render_result(total_res_with_dist[0].iloc[:, 2:-3], round_decimal=3), "\n")

    _render_stdout("Multi-range evaluation:", _out_color, True)
    all_res = pd.concat(total_res_with_dist[1:], ignore_index=True)
    print(metric.render_result(all_res.iloc[:, : -3], round_decimal=3), "\n")

    _render_stdout("Distances info of matched pairs:", _out_color, True)
    print(metric.render_result(_base_cols + [f"q{int(i * 100)}%" for i in _quan_cols], values))
    

if __name__ == "__main__":
    _parser = ArgumentParser(description="OD multi-object tracking evaluation")
    # positional required args
    # _parser.add_argument("root", type=str, help="root/path to two .txt files below")
    _parser.add_argument("gt_txt", type=str, help="a .txt file that describes gt file names")
    _parser.add_argument("hyp_txt", type=str, help="a .txt file that describes hypothesis file names")

    # optional args 
    _parser.add_argument("--gt_dist_thres", type=float, default=5.,
                         help="distance threshold of matching gts")
    _parser.add_argument("--metric_dist_thres", type=float, default=float('inf'),
                         help="distance threshold for metric computing.")
    # _parser.add_argument("--model", type=str, default="pilot",
    #                      help="model type, choices: `pilot`, `noa`.")
    _parser.add_argument("--time_diff", type=int, default=8, 
                         help="time difference between hypothesis log and ground truth log, "
                         "for synchronizing timestamps.")
    _parser.add_argument("--cam_mea_bias", type=float, default=0.,
                         help="difference between camera and measurement timestamp: cam_ts - mea_ts")
    _parser.add_argument("--sync_precision", type=int, default=2,
                         help="timestamp sychornizing precision defined by keeping ts floatpoint digit.")
    _parser.add_argument("--max_switch_time", type=float, default=float('inf'),
                         help="see `motmetrics.MOTAccumulator` for more info.")
    
    # booleans
    _parser.add_argument("--rough_sync", action="store_true",
                         help="timestamp sychornizing precision defined by rough synchronization.")
    _parser.add_argument("--ignore_warns", action="store_true",
                         help="whther to ignore all RuntimeWarning during the runing process, default True.")
    _parser.add_argument("--auto_frame_id", action="store_false", 
                         help="frame id is automatically assigned, default: False, i.e. using timestamp.")
    _parser.add_argument("--gt_to_json", action="store_false", 
                         help="whether to save parsed gt as a .json file.")
    _parser.add_argument("--save_event", action="store_false", 
                         help="whether to save ultimate tracking events as a .csv file., default: False")
    
    _args = _parser.parse_args()

    if _args.ignore_warns:
        warnings.filterwarnings("ignore", category=RuntimeWarning)
    
    _evaluate_many(_args.gt_txt, _args.hyp_txt)
    
    

