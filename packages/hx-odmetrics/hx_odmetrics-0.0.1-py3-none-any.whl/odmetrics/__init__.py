"""
# ODMetrics
Multi-object Tracking (MOT) for perceptionn OD(Obstacle Detection), used for overall evaluation of
E2E Tracking system.

The MOT metrics are supported by third-party library `py-motmetrics`. In particular py-motmetrics supports
CLEAR-MOT metrics and ID metrics. Both metrics attempt to find a minimum cost assignment between 
ground truth objects and predictions. For more information about the API See 
<https://github.com/cheind/py-motmetrics>. 
Standard metrics provided please refer to: <https://motchallenge.net/>
-----
## Notice
This package is used for ground truths which ids of objects have not been assigned, for those assigned, it
has not been developed provisionally and will be released at future version.
The package asserts that ground truths are encoded and stored as .pkl file, does not supoort for those
with other encoding styles. And will be developed and released in future version for specific needs.

The .pkl must contain keys as follows:
    ```python
        {
            "frame_id": UUID[str],
            "timestamp": float,
            "cameras": {
                "CAMERA_FRONT_FAR": {"camera2body": NDArray[Any], "camera_intrinsic": NDArray[Any]},
                "CAMERA_FRONT_WIDE": {"camera2body": NDArray[Any], "camera_intrinsic": NDArray[Any]},
            }
            "annos": {
                "names": NDArray[<U18], 
                "boxes_3d": NDArray[Any], 
                "anno2body": NDArray[Any], 
                "orientation": str
            }
        }
    ```
it does not provide sufficient information otherwise.

## How to use odmetrics in python script
-----
It is recommend that the package can be imported as `od`::

    >>> import odmetrics as odm

Instantiate a OdTrackingCompose for generating and assigning ids for object gts::

    >>> file_name = "./path/to/file.pkl"  # declare a path to gt
    >>> compose = odm.OdTrackingCompose(cost_thres=5).load_gt_file(file_name) # inst a Compose pipeline
    >>> compose.traverse_all_labels() # generate ids

Then use TrackContainerParser for parsing generated ids and output a dictionary::

    >>> parser = odm.TrackContainerParser()
    >>> gt_dict = parser(compose.tracks_).result()

where `compose.tracks_` is a container that stores all tracks in all timestamps.
Or it can be chosen to save parsed data structure to a json file::

    >>> parsed_file = "./path/to/saving_file.json"
    >>> parser.to_json(parsed_file)

Before computing metric scores, instantiate a MetricInterfaceAdapter for adapting 
metric interface, where a hypothesis output file path should be provided::

    >>> hyp_file = "./path/to/hyp_output.json"
    >>> adapter = odm.MetricInterfaceAdapter(rought_sync=True).load_gt_hyp(gt_dict, hyp_file)
    >>> adapter.adapt() # reformatting gt and hypothesis for adapting interface

Note that the hypthesis file / dictionary should be structured as:

    ```python
        {
            "1707118247.255981":[
                {"id":..., "boxes":...}
                ...
                ]
                ...
        }
    ``` 
or at least contains keys as above ("1707118247.255981" is a specific timestamp with Unix style).

Alternatively, a hypothesis with `.record` file or a directory contains  `.record` files is also 
supported, however, it should be parsed individually before the adapting::

    >>> hyp_path = "./path/to/hyp_output.record" # path to .record file
    >>> hyp_path = "./path/to/hyp_output_dir/" # path to dir that contains .record files
    >>> hyp_file = utils.RecordParser(hyp_path, "ts").get_result()

Finally, use MotOdMetricWrapper for computing metric scores::

    >>> metric = odm.MotOdMetricWrapper()
    >>> metric.accumulate_from_adapter(adapter)

The results can be visualized by calling `.summarize()` method::

    >>> metric.summarize()

The results will look like this if they are not rendered or modified:

```
IDF1    IDP    IDR   Rcll   Prcn   GT   MT   PT   ML   FP    FN   IDs  FM  MOTA    MOTP
0.785  0.821  0.752  0.831  0.907  697  436  102  159  684  1365  272  56  0.713  43.093
```

For more information of usage of these methods please refer to subscripts of them,
or simply call builtin `help()` for explanations.

------
Author: Haokun Zhang <haokun.zhang@hirain.com>
Version: Un-released
Copyright: Haokun Zhang (c)
MotMeticsCopyright: 2017-2022 Christoph Heindl (c), 2018 Toka (c), 2019-2022 Jack Valmadre (c)
"""

from . import track_compose, utils, evaluate, parse, visual_tools

from .track_compose import OdTrackingCompose
from .metrics import MotOdMetricWrapper, MetricInterfaceAdapter


from ._internal import _configs, _std
__version__ = _configs.__version__
__name__ = _configs.__name__
__status__ = _configs.__status__

if __version__ == _configs._VERSION_UNRELEASED and __status__ == _configs._STATUS_ANNOUNCED:
    msg = "package is still not be permitted for using as `announced` status as it is not released."
    raise PermissionError(msg)
else:
    import warnings
    if __version__ == _configs._VERSION_RELEASED and __status__ == _configs._STATUS_TEST:
        warnings.warn(
            "package is in test status and might raise internal error in the future running,"\
                      "please compile it to status of `run` to avoid it if necessary.", FutureWarning
        )
        

    def _decode_version_decimal(_version):
        _major, _minor, _patch = [int(_dig) for _dig in _version.split(".")]
        _rnd_up = max(_configs._VERSION_PATCH_MIN, max(_major, _minor, _patch) + 1)

        assert isinstance(_version, str), "package version unclear."
        return _major * _rnd_up ** 2 + _minor * _rnd_up + _patch
    

    def _try_dependency_and_lowest_versions():
        import numpy, typing, scipy, motmetrics, tqdm, pickle, cyber_record, PIL, pandas

        return [(numpy, "1.22.0"), 
                (typing, None), 
                (scipy, "1.10.3"), 
                (motmetrics, "1.3.0"), 
                (tqdm, "4.62.0"),
                (pickle, None),
                (cyber_record, None),
                (PIL, "9.0.0"),
                (pandas, "1.4.0")]
    
    
    for _pkg, _version in _try_dependency_and_lowest_versions():
        if _version is not None:
            if not hasattr(_pkg, "__version__"):
                warnings.warn(
                    f"Could not check version info of package {_pkg}.", _std.DependencyWarning
                )
            else:
                if not _decode_version_decimal(_pkg.__version__) >= _decode_version_decimal(_version):
                    warnings.warn(
                        f"package {_pkg.__name__} does not meet the requirement of lowest version,"\
                                "which might cause internall error raise running in the future: "\
                                    f"current version {_pkg.__version__} vs. required {_version}",
                                    _std.DependencyIncompatibleWarning
                    )

        del _pkg

    del _try_dependency_and_lowest_versions
    del _decode_version_decimal

    del warnings
    del _configs
    del _std
