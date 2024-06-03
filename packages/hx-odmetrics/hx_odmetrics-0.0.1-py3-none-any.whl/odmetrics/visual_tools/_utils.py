"""
Visual tools utils
----
character: non-root script
Author: Haokun Zhang <haokun.zhang@hirain.com>
Initial date: 05.15.2024
log: --

"""

import os
import numpy as np
from scipy.optimize import linear_sum_assignment

from .._internal._typing import *
from .._internal._functools import *


class ImageStruct(object):
    @VersionControl("onhold")
    def __init__(self, ip: _StrLike, ts: _U[_FltLike, _StrLike], image_array: _MatLike = None) -> None:
        self.__path = ip
        self.__ts = ts
        self.__img = image_array

    @property
    def path_(self):
        return self.__path
    
    @property
    def timestamp_(self):
        self.__ts

    @property
    def img_(self):
        return self.__img
    
    @property
    def size_(self):
        if self.__img:
            return {'height': self.__img.shape[0], 'width': self.__img.shape[1]}
        else:
             return None


class ImageLoader:
    """
    
    """
    @VersionControl("onhold")
    def __init__(self, imgs: _Dict[str, _Li[ImageStruct]] = None, timestamps: _UnlimLi = None) -> None:
        self._supported_format_postfix = ["png", "jpeg", "jpg", "tif"]
        self._imgs = {} if not imgs else imgs
        self._img_timestamps = [] if not timestamps else timestamps

    def from_directory(self, dp: _StrLike):
        _target_dirs = [f'camera_fov{fov}' for fov in [30, 120]]
        assert set(os.listdir(dp)).issuperset(_target_dirs)
        _cams_dir = [os.path.join(dp, _dir) for _dir in _target_dirs]
        _30_ts, _120_ts = [[int(_n.split("_")[-1].split(".")[0]) for _n in os.listdir(_dir)]
                                 for _dir in _cams_dir]
        assert set(_30_ts) == set(_120_ts)

        self._img_timestamps = sorted(_30_ts)
        self._imgs = {"camera_fov30": [], "camera_fov120": []}

        for _name, _dir in zip(_target_dirs, _cams_dir):
            for _ts in self._img_timestamps:
                _img_path = os.path.join(_dir, f"{_name}_{_ts}.png")
                assert os.path.isfile(_img_path), "File not found or Invalid directory: {}".format(_img_path)
                self._imgs[_name].append(
                    ImageStruct(_img_path, _ts)
                )

        self._img_timestamps = [self._process_img_timestamp(i) for i in self._img_timestamps]
        self._check_imginfo_amount()
        # self._sort_by_timestamp()

        return self
    
    @staticmethod
    def _process_img_timestamp(img_ts: _AnyT, int_digit: int = 10) -> _StrLike:
        img_ts = str(img_ts)
        return img_ts[:int_digit] + "." + img_ts[int_digit:]

    def filter_by_indices(self, indices: _AnyT):
        self._check_loading_status()
        for key in [f'camera_fov{fov}' for fov in [30, 120]]:
            self._imgs[key] = np.asarray(self._imgs[key])[indices].tolist()
        self._img_timestamps = np.asarray(self._img_timestamps)[indices].tolist()
        self._check_imginfo_amount()

    @Deprecated
    def _sort_by_timestamp(self) -> None:
        self._check_loading_status()
        
        self._img_timestamps, self._imgs['camera_fov30'], self._imgs['camera_fov120'] = \
        np.asarray(
            sorted(zip(self._img_timestamps, self._imgs['camera_fov30'], self._imgs['camera_fov120']), 
               key=lambda x: x[0])
        ).T.tolist()

    def _check_imginfo_amount(self):
        assert len(self._imgs) == 2, "Invalid dictionary items: {}".format(self._imgs.keys())
        _n_camera30, _n_camera120 = len(self._imgs['camera_fov30']), len(self._imgs['camera_fov120'])
        if _n_camera30 != _n_camera120:
            raise ValueError("Number of Images parsed from camera fov30 does not equal camera fov120: "
                             "{} vs. {}".format(_n_camera30, _n_camera120))
        print("Found {} images from cameras fov30 and 120".format(_n_camera30))

    @UnImplemented
    def from_record(self, path: _StrLike) -> None: ...

    def _check_loading_status(self) -> None:
        if not all([self._imgs, self._img_timestamps]):
            raise ValueError("Image and timestamp infos have not been loaded.")
    
    @property
    def img_infos_(self):
        self._check_loading_status()
        return self._imgs

    @property
    def timestamps_(self):
        self._check_loading_status()
        return self._img_timestamps
    

class TimestampSynchornizer:
    #typedef
    _CUSTOM_STRING = str
    _CUSTOM_FLOAT = float
    @VersionControl("onhold")
    def __init__(self, gt_ts: _Iter, sensor_ts: _Iter, time_diff: int = 8,
                 cam_mea_time_bias: float = 0.) -> None:
        """
        cam_mea_time_bias: time bias between camera sensor and msg measurement timestamp: cam - mea
        """
        self._gt_timestamps = sorted(self._correct_timestamps(gt_ts, time_diff * 60 ** 2))
        self._sensor_timestamps = sensor_ts
        self._cam_mea_time_bias = cam_mea_time_bias
        self._time_diff = time_diff

    def load_timestamps(self, gt_times: _Iter, sensor_times: _Iter) -> None:
        self._sensor_timestamps = sensor_times
        self._gt_timestamps = sorted(self._correct_timestamps(gt_times, self._time_diff * 60 ** 2))

    def rough_synchornize(self, return_indices: bool = True):
        self._check_gt_video_ts_satus()
        _range = self._check_gt_video_intersect(self._gt_timestamps, self._sensor_timestamps)
        _masked_items, _masked_indices = self._filter_with_range(
            _range, self._gt_timestamps, self._sensor_timestamps
        )
        self._gt_timestamps, self._sensor_timestamps = _masked_items
        _gt_idx, _sensor_idx = _masked_indices
        _gt_match_idx, _sensor_match_idx = self._match_timestamps(self._gt_timestamps, 
                                                                  self._sensor_timestamps, return_indices)
        
        return np.array(_gt_idx)[_gt_match_idx], np.array(_sensor_idx)[_sensor_match_idx]

    def _check_gt_video_ts_satus(self):
        if not self._gt_timestamps or not self._sensor_timestamps:
            raise ValueError("gt and video timestamps have not been loaded.")
    
    @staticmethod
    @Duplicated
    def _correct_timestamps(timestamps: _U[_Iter, str], diff: _ScalarLike) -> _StrLi:
        if diff != 0:
            timestamps = [
                str(float(item) - diff) for item in timestamps
            ]
        return timestamps

    @Duplicated
    def _check_gt_video_intersect(self, _gt_ts, _vid_ts):
        _gt_ts, _vid_ts = self._ele_any2float(_gt_ts, _vid_ts)
        _gt_min, _gt_max = np.min(_gt_ts), np.max(_gt_ts)
        _hyp_min, _hyp_max = np.min(_vid_ts), np.max(_vid_ts)
        _range_intersect = (np.maximum(_gt_min, _hyp_min), np.minimum(_gt_max, _hyp_max))

        if _range_intersect[0] >= _range_intersect[1]:
            raise TypeError("No intersection between gt and hypothesis, perhaps they do not match.")
        return _range_intersect
    
    def _filter_with_range(self, _range: _Iter, *args):
        if not len(_range) == 2:
            raise ValueError("range must have 2 elements.")
        
        _masked_items, _masked_indices = [], []
        for item in args:
            _indices = np.asarray([i for i in range(len(item))])
            item = np.asarray(self._ele_any2float(item))
            _mask = np.logical_and(item >= _range[0], item <= _range[1])
            _masked_items.append(item[_mask].tolist())
            _masked_indices.append(_indices[_mask].tolist())

        if len(args) == 1:
            return _masked_items[0], _masked_indices[0] 
        else:
            return _masked_items, _masked_indices
    
    @staticmethod
    @ToModify("hungarian to nearest matching")
    def _match_timestamps(arr1: _Iter, arr2: _Iter, return_indices: bool = True) -> _AnyT:
        arr1, arr2 = [np.asarray(item).reshape(-1, 1) for item in [arr1, arr2]]
        agent, task = arr1.reshape(-1, 1), arr2.reshape(1, -1)

        cost = np.sqrt((agent - task) ** 2)
        agent_indices, task_indices = linear_sum_assignment(cost)
        if return_indices:
            return agent_indices, task_indices
        else:
            arr1, arr2 = arr1[agent_indices], arr2[task_indices]
            return (arr.tolist() for arr in [arr1, arr2])

    def _ele_any2str(self, *args) -> _AnyT:
        return self.__ele_any2specific(self._CUSTOM_STRING, *args)
    
    def _ele_any2float(self, *args) -> _AnyT:
        return self.__ele_any2specific(self._CUSTOM_FLOAT, *args)
    
    @staticmethod
    def __ele_any2specific(dtype: _DType, *args) -> _AnyT:
        _converted = [[dtype(value) for value in _iterable] for _iterable in args]

        return _converted[0] if len(args) == 1 else _converted
    

