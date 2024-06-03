"""
This script is used to compose Od ground truths from Parsing .pkl to serializing

----
ods in a sequential style 
character: non-root script
Author: Haokun Zhang <haokun.zhang@hirain.com>
Initial date: 04.07.2024
log: --

"""


import numpy as np
from collections import deque

from .utils import get_batch_dist_eu
from .parse import PickleParser
from ._internal._track_tools import *
from ._internal._assign import HungarianAssigner
from ._internal._functools import *
from ._internal._typing import *


class OdTrackingCompose:
    """

    """
    _INIT_COST_DUMMY = 0.
    def __init__(self, cost_thres: float = None, 
                 sync_box_coords: bool = True, id_req: int = None) -> None:
        self._gt_list: _Li = None
        self.n_timestamps: _IntLike = None
        self.sync_box_coords = sync_box_coords
        self._tracks_ = GtTrackContainer()
        self.cost_thres: float = cost_thres if cost_thres else np.inf
        self._optim = HungarianAssigner(dist_thres=cost_thres)
        self.id_req = 10 ** 3 if not id_req else id_req
        self._id_container = deque([i for i in range(self.id_req)])

    def load_gt_file(self, fp: _StrLike):
        self._gt_list = sorted(PickleParser().load_pkl(fp), key=lambda x: x['timestamp'])
        self._init_state_variables()

        return self
        
    def __repr__(self) -> _StrLike:
        return "ground truth id: {}\nnumber of labeled timestamps: {}\n"\
        "distance threshold: {:.2f}"\
            .format(self._gt_list[0]['sequence_id'], len(self._gt_list), self.cost_thres)

    def traverse_all_labels(self):
        self._check_loading_status()
        # print("\nGenerating gt tracks starting from sequence {}".format(self._init_seq))

        for _seq in range(self._init_seq, self.n_timestamps - 1):
            if 'annos' in self._gt_list[_seq] and 'annos' in self._gt_list[_seq + 1]:
                self.update_state(self._gt_list[_seq], self._gt_list[_seq + 1])

            elif 'annos' in self._gt_list[_seq] and 'annos' not in self._gt_list[_seq + 1]:
                self.push_all_to_lost()
            elif  'annos' not in self._gt_list[_seq] and 'annos' in self._gt_list[_seq + 1]:
                self.__init_container(self._gt_list[_seq + 1]['timestamp'], self._gt_list[_seq + 1]['annos'])

        return self

    @ToModify("logics might be optimized")
    def update_state(self, pre_info: _StrDict, cur_info: _StrDict) -> None:
        pre_anno, cur_anno = pre_info['annos'], cur_info['annos']
        pre_cls, pre_boxes = pre_anno['names'], pre_anno['boxes_3d']
        cur_cls, cur_boxes = cur_anno['names'], cur_anno['boxes_3d']
        
        _total_pre_matched_idx, _total_cur_matched_idx, _total_matched_costs = [], [], []
        _total_unassigned_idx, _total_newborn_idx = [], []
        total_cls = sorted(set(pre_cls).union(set(cur_cls))) # get total cls type

        for _cls in total_cls:
            indices = [[], []]
            pre_cls_boxes, cur_cls_boxes = [], []

            for index in range(len(pre_cls)):
                if pre_cls[index] == _cls:
                    indices[0].append(index)
                    pre_cls_boxes.append(pre_boxes[index][:3])
                    
            for index in range(len(cur_cls)):
                if cur_cls[index] == _cls:
                    indices[1].append(index)
                    cur_cls_boxes.append(cur_boxes[index][:3])

            if not indices[0] and indices[1]: # typical class born
                _total_newborn_idx.extend(indices[1])
            elif indices[0] and not indices[1]: # typical class disappear
                _total_unassigned_idx.extend(indices[0])
            else: # both pre and cur exist
                # match tracks 
                cost = get_batch_dist_eu(np.array(pre_cls_boxes), np.array(cur_cls_boxes))
                self._optim.match(cost, indices[0], indices[1])
                pre_match_idx, cur_match_idx = self._optim.assigned_indices_

                for _src, _op in zip(
                    [_total_pre_matched_idx, _total_cur_matched_idx, _total_matched_costs, _total_unassigned_idx, _total_newborn_idx],
                    [pre_match_idx, cur_match_idx, self._optim.assigned_costs_, self._optim.unassigned_indices_, self._optim.newborn_indices_]
                ): _src.extend(_op)

        # update tracks
        self.__remove_lost_tracks(_total_unassigned_idx)

        self.__update_matched_track_info(cur_info['timestamp'], _total_pre_matched_idx, _total_cur_matched_idx,
                                    _total_matched_costs, pre_cls, cur_boxes)
        
        self.__init_new_tracks(_total_newborn_idx, 
                            cur_info['timestamp'], cur_cls, cur_boxes)  
        
        # end check
        self._check_corres_idx_repetition()
        self._check_cur_track_amount(cur_cls)   

    def reset(self) -> None:
        self._gt_list: _Li = None
        self._optim.reset_state()
        self._tracks_.reset()

        self._init_seq = 0
        self._id_container = deque([i for i in range(self.id_req)])
    
    def __remove_lost_tracks(self, indices: _Iter) -> None:
        if len(indices) > 0:
            for lost_idx in indices:
                id_to_emplace = self._tracks_.set_lost(lost_idx)
                self._id_container.append(id_to_emplace)

    def __init_new_tracks(self, indices: _Iter, timestamp: _AnyT, cur_cls: _Iter, cur_ts_boxes: _AnyT) -> None:
        if len(indices) > 0:
            for new_idx in indices:
                self._tracks_.add(
                    BaseTrack(timestamp,  self._id_container.popleft(), cur_cls[new_idx], 
                            cur_ts_boxes[new_idx], self._INIT_COST_DUMMY, new_idx)
                )

    def __update_matched_track_info(self, ts: _AnyT, pre_match_idx: _NumLi, cur_match_idx: _NumLi, match_costs: _UnlimLi, 
                                    pre_class: _Iter, cur_ts_boxes: _AnyT) -> None:
        if pre_match_idx and cur_match_idx: # has matched object (not dropped by dist thres)
            for track in self._tracks_:
                cci = track.cur_corres_idx_ # latest corresponding index, could be previous
                if cci in pre_match_idx and track.class_type_ == pre_class[cci]:
                    _corres_idx_idx = pre_match_idx.index(cci)
                    _distance = match_costs[_corres_idx_idx]
                    track.update_infos(ts, _distance, 
                                        cur_ts_boxes[cur_match_idx[_corres_idx_idx]],
                                        cur_match_idx[_corres_idx_idx])
    
    def __init_container(self, init_ts: _AnyT, init_annos: _Dict) -> None:
        for index, cls in enumerate(init_annos['names']):
            self._tracks_.add(
                BaseTrack(init_ts, 
                          self._id_container.popleft(), 
                          cls, 
                          init_annos['boxes_3d'][index],
                          self._INIT_COST_DUMMY,
                          index)
            )

    def push_all_to_lost(self) -> None:
        self._id_container.extend(self._tracks_.set_all_tracks_lost())

    def _init_state_variables(self):
        self._check_loading_status()

        self.n_timestamps = len(self._gt_list)

        if self.sync_box_coords:
            self._align_orgs_to_body()

        for _ts_info in self._gt_list:
            if not 'annos' in _ts_info:
                self._tracks_.update_noobj_timestamp(_ts_info['timestamp'])
            self._tracks_.update_timestamp(_ts_info['timestamp'])

        for index, _ts_info in enumerate(self._gt_list):
            self._init_seq = index
            if 'annos' in _ts_info:
                self.__init_container(_ts_info['timestamp'], _ts_info['annos'])
                break

        if self._init_seq == self.n_timestamps:
            raise TypeError("No annotations found in this pkl file.")

        return self

    def _check_loading_status(self):
        _check_list = [self._gt_list]
        if not all(_check_list):
            raise ValueError("gt file does not exist, maybe it hasnot been loaded, call `load_gt_file()` first.")
        
    def _check_corres_idx_repetition(self) -> None:
        _checklist = []
        for track in self._tracks_:
            if track.cur_corres_idx_ in _checklist:
                raise RuntimeError("dupilcated corresponding index: {}".format(track.cur_corres_idx_))
            _checklist.append(track.cur_corres_idx_) 

    def _check_cur_track_amount(self, cur_cls: _AnyT) -> None:
        if len(self._tracks_) != len(list(cur_cls)):
            raise RuntimeError("Current tracked object amount must equal amount provided in gt, got {} vs.{}".format(
                len(self._tracks_), len(list(cur_cls))
            ))
        
    def _align_orgs_to_body(self):
        for _gt in self._gt_list:
            if 'annos' in _gt:
                boxes_3d = _gt['annos']['boxes_3d']
                _trans = _gt['annos']['anno2body']
                _sync_boxes = _trans[:3, :3] @ boxes_3d[:, :3].T + _trans[:3, 3:4]
                boxes_3d[:, :3] = _sync_boxes.T
                _gt['annos']['boxes_3d'] = boxes_3d

    @property
    def tracks_(self) -> GtTrackContainer:
        return self._tracks_
    
    @property
    def parsed_gt_info_(self) -> _AnyT:
        return self._gt_list
    
