"""
Od ground truth MOT Hypothesis / object targeting and managing tools script
character: root script
Author: Haokun Zhang <haokun.zhang@hirain.com>
log: --
"""

import json

from ._functools import *
from ._typing import *


class BaseTrack(object):
    """
    Args:

    ts:
    obj_id:
    """
    def __init__(self, 
                 init_ts: float, 
                 obj_id: int, 
                 label: _AnyT, 
                 box: _AnyT,
                 cost: _AnyT, 
                 init_corres_idx: int,
                 **kwargs) -> None:
        self._obj_id = obj_id
        self._label = label

        self.timestamps = [init_ts]
        self.boxes = [box]
        self.match_cost = [cost]
        self.corres_indices = [init_corres_idx]

    def update_infos(self, ts: float, cost: _AnyT, box: _AnyT, corres_idx: int, *args) -> None:
        self.update_timestamp(ts)
        self.update_cost(cost)
        self.update_box(box)
        self.update_corres_idx(corres_idx)

    def update_timestamp(self, ts: float) -> None:
        self.timestamps.append(ts)

    def update_cost(self, cost: _AnyT) -> None:
        self.match_cost.append(cost)

    def update_box(self, box: _AnyT) -> None:
        self.boxes.append(box)

    def update_corres_idx(self, corres_idx: int) -> None:
        self.corres_indices.append(corres_idx)

    def __repr__(self) -> str:
        return "obj: {} id: {} current corresponding index: {}\ntime stamp when tracked: {}\n"\
            "current time stamp: {}\nsuccessful track times: {}\n".format(
            self._label, self._obj_id, self.cur_corres_idx_, self.timestamps[0], self.timestamps[-1], len(self.timestamps)
        )
    
    @property
    def start_time_stamp_(self) -> _AnyT:
        return self.timestamps[0]

    @property
    def cur_time_stamp_(self) -> _AnyT:
        return self.timestamps[-1]
    
    @property
    def cur_corres_idx_(self) -> int:
        return self.corres_indices[-1]
    
    @property
    def id_(self) -> int:
        return self._obj_id
    
    @property
    def tracked_times_(self) -> int:
        return len(self.timestamps)
    
    @property
    def class_type_(self) -> _AnyT:
        return self._label


class GtTrackContainer(object):
    """
    
    """
    def __init__(self, container: _Iter[BaseTrack] = None) -> None:
        self._container: _Li[BaseTrack] = []
        if container and len(container) > 0:
            for item in container:
                self._container.append(
                    self._check_instance(item)
                )
        self._lost_container: _Li[BaseTrack] = []
        self._timestamps: _Iter = []
        self._noobj_ts: _Iter = []
            
        self.__iter_idx: int = 0

    def __iter__(self):
        self.__iter_idx = 0
        return self
    
    def __next__(self):
        if self.__iter_idx < len(self._container):
            res = self._container[self.__iter_idx]
            self.__iter_idx += 1
            return res
        else:
            self.__iter_idx = 0
            raise StopIteration
        
    def __getitem__(self, idx):
        return self._container[idx]
    
    def __len__(self):
        return len(self._container)
    
    def __repr__(self) -> str:
        return "TrackContainer Current State:\n"\
        "Number of tracked objects (current): {}\n"\
        "Number of lost objects (current): {}\n".format(len(self._container), len(self._lost_container))
    
    def set_lost(self, corres_idx: int) -> int:
        id_to_emplace: int = -1
        for track in self._container:
            if track.cur_corres_idx_ == corres_idx:
                id_to_emplace = track.id_
                self._lost_container.append(track)
                self._container.remove(track)
                return id_to_emplace
        else:
            raise ValueError('No BaseTrack which corresponding index is {}'.format(corres_idx))
        
    def set_all_tracks_lost(self) -> _Li[int]:
        ids = []
        if self._container:
            for track in self._container:
                ids.append(track.id_)
                self._lost_container.append(track)
            self._container.clear()
        return ids

    def add(self, obj: BaseTrack) -> None:
        self._container.append(
            self._check_instance(obj)
        )

    def remove(self, obj_id: int):
        self._container.pop(obj_id)

    def popleft(self):
        self._container.pop(0)

    def _check_instance(self, x):
        if not isinstance(x, BaseTrack):
            raise TypeError('Type of value must be BaseTrack.')
        return x
        
    def reset(self):
        for it in [self._container, self._lost_container, self._timestamps]:
            it.clear()

    def update_timestamp(self, ts: _AnyT):
        self._timestamps.append(ts)

    def update_noobj_timestamp(self, ts: _AnyT):
        self._noobj_ts.append(ts)

    @property
    def n_cur_tracked_objs_(self) -> int:
        return len(self._container)
    
    @property
    def n_cur_lost_objs_(self) -> int:
        return len(self._lost_container)
    
    @property
    def all_tracks_(self) -> _Li[BaseTrack]:
        return self._container + self._lost_container
    
    @property
    def lost_tracks_(self) -> _Li[BaseTrack]:
        return self._lost_container
    
    @property
    def n_all_tracks_(self) -> int:
        return len(self.all_tracks_)
    
    @property
    def timestamps_(self) -> _Li[_AnyT]:
        return self._timestamps
    
    @property
    def n_noobj_ts_(self) -> int:
        return len(self._noobj_ts)

