"""
#!usr/bin/python3
This is a evaluating script provided by the package for quick direct evaluation.
character: entry
Author: Haokun Zhang <haokun.zhang@hirain.com>
log: --

"""

from argparse import ArgumentParser

from .utils import _render_stdout
from .metrics import *
from .track_compose import *
from .parse import *
from ._internal._functools import *


@VersionControl('onhold')
def _parse_arguments(args):
    ...


def _evaluate(gt_file: str, hyp_file: str):
    _gt_info = gt_file.split("/")[-1].split(".")[0]
    _hyp_info = [_s for _s in hyp_file.split("/") if _s.startswith("HHPLT")]
    compose = OdTrackingCompose(cost_thres=float(_args.gt_dist_thres)).load_gt_file(gt_file)
    adapter = MetricInterfaceAdapter(time_diff=_args.time_diff,
                                     cam_mea_bias=_args.cam_mea_bias,
                                     rough_sync=_args.rough_sync,
                                     sync_prcn_digit=_args.sync_precision)
    metric = MotOdMetricWrapper(auto_frame_id=_args.auto_frame_id,
                                max_switch_time=float(_args.max_switch_time),
                                dist_thres=float(_args.metric_dist_thres),)

    compose.traverse_all_labels()
    _parser = TrackContainerParser(priority="ts")(compose.tracks_)
    gt_dict = _parser.result()

    if _args.gt_to_json:
        _parser.to_json("./" + _gt_info + ".json")

    if not hyp_file.endswith(".json"):
        hyp_file = RecordParser("ts").load(hyp_file).get_result()
        
    # else: 
    #     raise TypeError("File must be a .json file or a .record file, got: {}"\
    #                     .format(hyp_file.split(".")[-1]))
    
    adapter.load_gt_hyp(gt_dict, hyp_file).adapt()

    metric.accumulate_from_adapter(adapter)
    if isinstance(_args.eval_metrics, str):
        _eval_metrics = _args.eval_metrics.split(",")
    else:
        _eval_metrics = None
    
    _out_color = "blue"
    print(
        _render_stdout("\nEvaluation info: {} {} | objGT: {} Hyps: {}".format(_gt_info, _hyp_info, adapter.n_gt_objects, adapter.n_hypothesis), _out_color)
    )
    metric.summarize(metrics=_eval_metrics , name_map=None, out_color=_out_color)

    if _args.save_event:
        hyp_id = hyp_file.split("/")[-1].split(".")[0]
        metric.events_.to_csv(hyp_id + "_event.csv")


if __name__ == "__main__":
    _parser = ArgumentParser(description="OD multi-object tracking evaluation")
    # positional required args
    _parser.add_argument("gt_path", type=str, help="path to groud truth file")
    _parser.add_argument("hyp_path", type=str, help="path to hypothesis file")

    # optional args 
    _parser.add_argument("--gt_dist_thres", type=float, default=5.,
                         help="distance threshold of matching gts")
    _parser.add_argument("--metric_dist_thres", type=float, default=float('inf'),
                         help="distance threshold for metric computing.")
    _parser.add_argument("--time_diff", type=int, default=8, 
                         help="time difference between hypothesis log and ground truth log, "
                         "for synchronizing timestamps.")
    _parser.add_argument("--cam_mea_bias", type=float, default=0.,
                         help="difference between camera and measurement timestamp: cam_ts - mea_ts")
    _parser.add_argument("--rough_sync", type=bool, default=False,
                         help="timestamp sychornizing precision defined by keeping ts floatpoint digit.")
    _parser.add_argument("--sync_precision", type=int, default=2,
                         help="timestamp sychornizing precision defined by keeping ts floatpoint digit.")
    _parser.add_argument("--eval_metrics", type=str, default=None,
                         help="metrics involved in evaluation, default: motchallenge metrics.")
    # _parser.add_argument("--eval_metrics_names", type=list, default=motmetrics.io.motchallenge_metric_names,
    #                      help="names for substituting metrics names displayed, default: motchallenge metric name abbrvs")
    
    # low-priorities
    _parser.add_argument("--auto_frame_id", type=bool, default=False, 
                         help="frame id is automatically assigned, default: False, i.e. using timestamp.")
    _parser.add_argument("--max_switch_time", type=float, default=float('inf'),
                         help="see `motmetrics.MOTAccumulator` for more info.")
    _parser.add_argument("--gt_to_json", type=bool, default=False,
                         help="whether to save parsed gt as a .json file.")
    _parser.add_argument("--save_event", type=bool, default=False,
                         help="whether to save ultimate tracking events as a .csv file., default: False")
    
    _args = _parser.parse_args()
    
    _evaluate(_args.gt_path, _args.hyp_path)
    
    

