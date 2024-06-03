"""
Parsers storage
Author: Haokun Zhang <haokun.zhang@hirain.com>
characher: non-root script
"""

import os, json, pickle
import numpy as np
from scipy.spatial.transform import Rotation
from cyber_record.record import Record

from .visual_tools._utils import ImageStruct, ImageLoader, TimestampSynchornizer
from ._internal._track_tools import GtTrackContainer
from ._internal._typing import *
from ._internal._functools import *


__all__ = [
    "PickleParser",
    "RecordParser",
    "CalibParamsParser",
    "TrackContainerParser",
    "GtDictPatcher"
]


class PickleParser:
    def __init__(self, root: _StrLike = None) -> None:
        self.root = root
        self.gt_list = os.listdir(root)

        if '.DS_Store' in self.gt_list:
            self.gt_list.remove('.DS_Store')

        if root:
            print("Found {} ground truths in this director:\n{}".format(len(self.gt_list), self.gt_list))
    
    def load_pkl(self, arg: _IntOrStr):
        """
        load a pickle file by specifing a index of files found from root or
            a filename of files which must exist in the root

        Args:
        arg[Union[int, str]]: index or a filename
        Raise: TypeError if arg is not int or str
        """
        if isinstance(arg, int):
            if self.root is None:
                raise TypeError('root is not provided for searching files.')
            gt_path = os.path.join(self.root, self.gt_list[arg])
        elif isinstance(arg, str):
            if self.root is None:
                if not os.path.isfile(arg):
                    raise FileNotFoundError("File does not exit: {}".format(arg))
                gt_path = arg
            else:
                assert arg in self.gt_list, 'argument {} does not exist, ref: {}'.format(arg, self.gt_list)
                gt_path = os.path.join(self.root, arg)
        else: 
            raise TypeError('arg must be an integer or a string, got {}'.format(type(arg)))
        
        with open(gt_path, 'rb') as f:
            frame = pickle.load(f)

        return frame

    def load_all_pkls(self):
        return [self.load_pkl(idx) for idx in range(len(self.gt_list))]
    

def _get_recorder(record_path: _StrLike) -> _Li:
    if not os.path.exists(record_path):
        print("Error in record path: ", record_path)
        raise NotADirectoryError("record path: ", record_path)
    else:
        if os.path.isdir(record_path):
            record_parsers = []
            for subrecord in os.listdir(record_path):
                if not os.path.isdir(subrecord) and 'record' in subrecord.split('.'): 
                    record_parsers.append(Record(os.path.join(record_path, subrecord)))
        else:
            record_parsers = [Record(record_path)]
    return record_parsers


class RecordParser:
    def __init__(self, priority: _StrLike = 'ts', type_map: _Dict = None):
        assert priority in ['ts', 'id']
        # assert model in ['pilot', 'noa']
        self.priority = priority
        # self._ch = "vision" if model == 'pilot' else 'tracked'
        self._ch = "tracked"
        self._record_parsers: _Li = [] # List[Record(str)]
        self._raw_od_dict: _Dict = {}

        self._type_map = {
            0: "UNKNOWN", 1: "UNKNOWN_MOVABLE", 2: "UNKNOWN_UNMOVABLE", 3: "Car", 4: "Van", 5: "Truck",
            6: "Bus", 7: "Cyclist", 8: "Motorcyclist", 9: "Tricyclist", 10: "Pedestrian", 11: "Cone",
            12: "Bicycle", 13: "Split_vehicle", 14: "Barrier", 15: "Warning_triangle", 16: "Animal"
        } if not type_map else type_map

    def load(self, record_path: _StrLike):
        self._record_parsers = _get_recorder(record_path)
        self._parse(self.priority)

        return self

    def _parse(self, prior):
        for record_parser in self._record_parsers:
            if record_parser:
                for channel_name, msg, msg_ts in record_parser.read_messages():
                    if channel_name == f'/rina/perception/{self._ch}_obstacles':
                        measure_ts = msg.header.measurement_time
                        # measure_ts = msg_ts / 10e8
                        if prior == 'id':
                            self._parse_od_id_prior(str(measure_ts), msg)
                        else:
                            self._parse_od_ts_prior(str(measure_ts), msg)
    
    def get_result(self) -> _StrDict:
        """
        structure prioritized by id:
        ```python
        self._raw_od_dict
        {
            obs_id[int] : {
                measure_ts[int]: {
                    body_info[str] : List[float],
                    center[str] : List[float],
                    body_velo[str] : List[float],
                    velo[str] : List[float]
                }
            }
        }
        ```

        structure prioritized by ts:
        ```python
        self._raw_od_dict
        {
            measure_ts[int] : {
                {
                    type[str] : str,
                    id[str] : int,
                    boxes[str] : List[float],
                }
            }
        }
        ```
        """
        return self._raw_od_dict
    
    def reset(self) -> None:
        self._raw_od_dict.clear()
        self._record_parsers.clear()

    def _parse_od_id_prior(self, measure_ts, msg):
        for obs in msg.perception_obstacles:
            obs_id = obs.id
            obs_body_info = [obs.position.x, obs.position.y, obs.position.z, obs.length, obs.width, obs.height, obs.theta, obs.id]
            obs_body_velo = [obs.velocity.x, obs.velocity.y]
            obs_center = [obs.position.x, obs.position.y]
            obs_velo = [obs.velocity.x, obs.velocity.y]
            obs_info = {'body_info': obs_body_info, 'center': obs_center, 'body_velo': obs_body_velo, 'velo': obs_velo}
            if obs_id not in self._raw_od_dict.keys():
                self._raw_od_dict[obs_id] = {}
            else:
                self._raw_od_dict[obs_id].update({measure_ts: obs_info})

    def _parse_od_ts_prior(self, measure_ts, msg):
        self._raw_od_dict[measure_ts] = []
        for obs in msg.perception_obstacles:
            obs_body_info = [obs.position.x, obs.position.y, obs.position.z, obs.length, obs.width, obs.height, obs.theta, obs.id]
            obs_info = {'type': obs.type, 'id': obs.id, 'boxes': obs_body_info}
            self._raw_od_dict[measure_ts].append(obs_info)


class CalibParamsParser:
    def __init__(self, path: str = None, aug_intrins: bool = False) -> None:
        if path is None:
            path = './data/configs/calibration.json'

        with open(path, 'r') as f:
            self._params = json.load(f)

        self._aug_intrins = aug_intrins

    def get_camera_params(self, camera_name: str = "ADAS_Front30"):
        if not camera_name:
            return self._params['cameras']
        
        _cam_params = dict()
        for item in self._params['cameras']:
            if item['name'] == camera_name:
                _extrin = item['extrinsic_param']
                _ext_rots, _ext_trans = [np.asarray(item) for item in 
                                         [_extrin['rotation'], _extrin['translation']]]
                _intrin = np.asarray(item['intrinsic_param']['camera_intrinsics'])
                _cam_params['extrinsic'] = self._aug_calib_extrin(_ext_rots, _ext_trans)
                _cam_params['intrinsic'] = self._aug_calib_intrin(_intrin)
                _cam_params['distortion'] = np.array(item['intrinsic_param']['distortion_coeffcients'])
                _cam_params['height'] = item['intrinsic_param']['height']
                _cam_params['width']  = item['intrinsic_param']['width']

                return _cam_params
        else:
            raise KeyError('no key named {}'.format(camera_name))
        
    def get_lidar_params(self, lidar_name: str = "INNO300"):
        for item in self._params['lidars']:
            if item['name'] == lidar_name:
                _extrin = item['extrinsic_param']
                _ext_rots, _ext_trans = [np.asarray(item) for item in 
                                         [_extrin['rotation'], _extrin['translation']]]
                return self._aug_calib_extrin(_ext_rots, _ext_trans)
        else:
            raise KeyError('no key named {}'.format(lidar_name))

    def _aug_calib_extrin(self, rot_vec: _MatLike, trans_vec: _MatLike):
        rot = Rotation.from_rotvec(rot_vec).as_matrix()
        _aug = np.eye(4)
        _aug[:3, :3], _aug[:3, -1] = rot, trans_vec.T
        return _aug

    def _aug_calib_intrin(self, intrin: _MatLike):
        _aug = np.eye(3)
        for index, (row, col) in enumerate([[0, 0], [1, 1], [0, 2], [1, 2]]):
            _aug[row, col] = intrin[index]
        
        if self._aug_intrins is True:
            return np.hstack([_aug, np.zeros([3, 1])])
        else:
            return _aug



class TrackContainerParser:
    """
    
    """
    def __init__(self, priority: str = 'ts') -> None:
        self._priority = priority
        self._parsed_gt_tracks = dict()
        self._container = None
        self._all_ts = None

        assert priority in ['timestamp', 'ts', 'id']

    def __call__(self, *args, **kwargs):
        self.load_container(*args, **kwargs)
        
        return self
    
    def load_container(self, container: GtTrackContainer):
        if not isinstance(container, GtTrackContainer):
            raise TypeError('container must be a GtTrackContainer, but got {}'.format(type(container)))
        self._container = container.all_tracks_
        self._all_ts = container.timestamps_
        self._parse(self._priority)

        return self

    def result(self) -> _StrDict:
        if not self._parsed_gt_tracks:
            raise ValueError("Tracks file have not been loaded yet, call the class first.")
        return self._parsed_gt_tracks

    def reset(self):
        self._parsed_gt_tracks.clear()

    def _parse(self, priority: str) -> None:
        if priority in ['ts', 'timestamp']:
            self._process_by_ts_prior()
        elif priority == 'id':
            self._process_by_id_prior()

    def _process_by_ts_prior(self) -> None:
        """
        The parsed result format is:
        ```python
        {
            'ts'[float]: [
            {'type'[str]: ..., 
            'id'[int]: ..., 
            'boxes'[list]: ...} 
            ...
            ],
            ...
        }
        ```
        """
        for ts in self._all_ts:
            self._parsed_gt_tracks[str(ts)] = []
            for track in self._container:
                if ts in track.timestamps:
                    self._parsed_gt_tracks[str(ts)].append({
                        'type': track.class_type_,
                        'id': track.id_,
                        'boxes': track.boxes[track.timestamps.index(ts)].tolist()
                    })

    @VersionControl('onhold')
    def _process_by_id_prior(self) -> None:
        """
        The parsed result format is:
        ```python
        {
            'id'[int]: [
            {'type'[str]: ..., 
            'ts'[float]: ..., 
            'boxes'[Any]: ...} 
            ...
            ],
            ...
        }
        ```
        """
        self._container = sorted(self._container, key=lambda x: x.id_)
        for track in self._container:
            self._parsed_gt_tracks[str(track.id_)] = []
            for index, ts in enumerate(track.timestamps):
                self._parsed_gt_tracks[str(track.id_)].append({
                    'ts': ts,
                    'type': track.class_type_,
                    'boxes': track.boxes[index].tolist()
                })

    @property
    def num_obj_gt_(self):
        if not self._parsed_gt_tracks:
            raise ValueError("Tracks file have not been loaded yet, call the class first.")
        
        res = 0
        for _, val in self._parsed_gt_tracks.items():
            res += len(val)

        return res

    @UnImplemented
    def add_camera_params(self, gt_dict: _UnlimDict):
        """
        The parsed result format is:
        ```python
            {
                'ts'[float]:
                {
                'anno2body':...,
                'orientation':...,
                'annos':
                    [
                        {
                            'type'[str]: ..., 
                            'id'[int]: ..., 
                            'boxes'[list]: ...
                        } 
                        ...
                    ],
                }
                ...
            }
        ```
        """
        assert self._priority == 'ts'
        if not self._parsed_gt_tracks:
            raise ValueError("gt tracks has not been parsed")

    def _sort_result_by_timestamp(self):
        self._parsed_gt_tracks = sorted(self._parsed_gt_tracks)

    def to_json(self, path: _StrLike) -> None:
        with open(path, 'w') as f:
            json.dump(self._parsed_gt_tracks, f, indent=4)
        print('file saved to {}'.format(path))
        

class GtDictPatcher:
    """
    
    """
    @VersionControl("onhold")
    def __init__(self, gt_dict: _Dict = None, gt_pkl: _Li = None, img_dir: str = None, time_diff: _AnyT = 8) -> None:
        self._parsed_gt = gt_dict
        self.gt_pkl = sorted(gt_pkl, key=lambda x: x['timestamp'])
        self._img_dir = img_dir
        self._td = time_diff

        self._refined_gt = None
        self._parsed_gt_ts = None
        self._gt_pkl_ts = None

        self._loader: ImageLoader = None
        self._syncer: TimestampSynchornizer = None

        if gt_dict and gt_pkl:
            self.__init_global_params(gt_dict, gt_pkl, img_dir, time_diff)

        assert self._parsed_gt_ts == self._gt_pkl_ts

    def load_files(self, gt_dict: _Dict, gt_pkl: _Li, img_dir: str = None):
        self.__init_global_params(gt_dict, gt_pkl, img_dir, self._td)

        return self
    
    def __init_global_params(self, gt_dict: _Dict, gt_pkl: _Li, img_dir: str = None, time_diff: _AnyT = 8):
        self._refined_gt = None
        self._parsed_gt = gt_dict
        self._parsed_gt_ts = [ts for ts in gt_dict.keys()]

        self.gt_pkl = sorted(gt_pkl, key=lambda x: x['timestamp'])
        self._gt_pkl_ts = [str(x['timestamp']) for x in self.gt_pkl]

        if img_dir is not None:
            self._loader = ImageLoader().from_directory(img_dir)
            self._syncer = TimestampSynchornizer(self._parsed_gt_ts, self._loader.timestamps_, time_diff)
        self._img_dir = img_dir

    def process(self):
        if self._img_dir is not None:
            _gt_kept, _sensor_kept = self._syncer.rough_synchornize()
            _filtered_gt_pkl_ts = self._filter_by_indices(self._gt_pkl_ts, _gt_kept)
            self._loader.filter_by_indices(_sensor_kept)
            _img_infos = self._loader.img_infos_
        else:
            _gt_kept = self._parsed_gt_ts
            _filtered_gt_pkl_ts = self._gt_pkl_ts
            _img_infos = None
        
        self._parsed_gt = self._add_params_to_parsed_gt(self._parsed_gt, self.gt_pkl, 
                                                           _filtered_gt_pkl_ts)
        self._refined_gt = self._add_paths_to_parsed_gt(self._parsed_gt, _img_infos)

        return self
    
    def result(self):
        assert self._refined_gt is not None
        return self._refined_gt

    def _add_params_to_parsed_gt(self, parsed_gt: _Dict, gt_pkl: _Li, filtered_ts: _Iter) -> _Dict:
        _new_gt = {}
        item = gt_pkl[0]
        camera_30, camera_120 = item['cameras']['CAMERA_FRONT_FAR'], item['cameras']['CAMERA_FRONT_WIDE']
        for item in gt_pkl:
            _ts = str(item['timestamp'])
            if _ts in filtered_ts and 'annos' in item:
                anno2body = item['annos']['anno2body']
                ort = item['annos']['orientation']
                _new_gt[_ts] = {'infos': parsed_gt[_ts], 
                                        'anno2body': anno2body, 'orientation': ort}
                
        _new_gt = {'cameras': {'camera_fov30': camera_30, 'camera_fov120': camera_120},
                              'annos': _new_gt}
        
        return _new_gt
    
    def _add_paths_to_parsed_gt(self, parsed_gt: _Dict, img_infos: _Dict[str, _Li[ImageStruct]] = None) -> _Dict:
        _new_dict = {}
        _annos = parsed_gt['annos']
        for index, (_ts, _val) in enumerate(_annos.items()):
            if img_infos is not None:
                _info30, _info120 = img_infos['camera_fov30'][index], img_infos['camera_fov120'][index]
                assert _info30.timestamp_ == _info120.timestamp_
                paths = (_info30.path_, _info120.path_)
            else:
                paths = (None, None)

            _val['img_path'] = paths
            _new_dict[_ts] = _val

        return {'cameras': parsed_gt['cameras'], 'annos': _new_dict}
    
    def _filter_by_indices(self, iterable: _Iter, indices: _Iter):
        return np.array(iterable)[indices].tolist()

