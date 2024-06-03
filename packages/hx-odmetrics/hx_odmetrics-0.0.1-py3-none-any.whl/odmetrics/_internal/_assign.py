"""
Hungarian Assigner Wrapper 
algorithm API: scipy.optimize.linear_sum_assignment(cost: NDArray, maximize: bool)
characher: root script
Author: Haokun Zhang <haokun.zhang@hirain.com>
Initial date: 04.07.2024
log: --

"""

from scipy.optimize import linear_sum_assignment
import numpy as np

from ._functools import *
from ._typing import *


class HungarianAssigner:
    """
    
    """
    MATCHED_, HAS_LOST_, HAS_NEWBORN_, HAS_LOST_AND_BORN_ = 0, 1, 2, 3
    NON_INIT_ = -1
    def __init__(self, maximize: bool = False, dist_thres: float = None) -> None:
        self.maximize = maximize
        self.dist_thres = np.inf if not dist_thres else dist_thres
        self._assign = linear_sum_assignment

        self._unassigned_indices, self._newborn_indices = [], []
        self._matched_agents, self._matched_tasks = None, None
        self._matched_costs = None
        self._status = self.NON_INIT_

    def match(self, cost: _MatLike, agent_indices: _Iter = None, task_indices: _Iter = None) -> None:
        self.reset_state()
        _n_agent, _n_task = self._check_cost_matrix(cost)
        
        self._matched_agents, self._matched_tasks = self._assign(cost, self.maximize)
        self._matched_costs = [cost[row, col] for row, col in zip(self._matched_agents, self._matched_tasks)]

        if agent_indices:
            if len(agent_indices) != _n_agent:
                raise ValueError('number of cost agents must equal number of elements in agent_indices')
            self._matched_agents = np.asarray(agent_indices, np.uint8)[self._matched_agents]
        else:
            agent_indices = np.asarray([i for i in range(_n_agent)])
        
        if task_indices:
            if len(task_indices) != _n_task:
                raise ValueError('number of cost tasks must equal number of elements in task_indices')
            self._matched_tasks = np.asarray(task_indices, np.uint8)[self._matched_tasks]
        else:
            task_indices = np.asarray([i for i in range(_n_task)])

        if _n_agent > _n_task: # lost objects
            _idx = set(agent_indices).difference(self._matched_agents)
            self._unassigned_indices.extend(_idx)
            self._status = self.HAS_LOST_
        elif _n_agent < _n_task: # new objects
            _idx = set(task_indices).difference(self._matched_tasks)
            self._newborn_indices.extend(_idx)
            self._status = self.HAS_NEWBORN_
        else:
            self._status = self.MATCHED_

        self._reassign_by_dist_thres()

    def _reassign_by_dist_thres(self) -> None:
        if self.dist_thres == np.inf:
            return
        
        self._check_matched_agents_tasks_status()

        border_idx = 0 # slow fast ptrs trick
        for ptr, value in enumerate(self._matched_costs):
            if value <= self.dist_thres:
                for it in [self._matched_costs, self._matched_agents, self._matched_tasks]:
                    self._swap_inplace(it, border_idx, ptr)
                border_idx += 1

        if border_idx < len(self._matched_costs):
            self._status = self.HAS_LOST_AND_BORN_
            self._unassigned_indices.extend(self._matched_agents[border_idx:])
            self._newborn_indices.extend(self._matched_tasks[border_idx:])

            self._matched_agents = self._matched_agents[: border_idx]
            self._matched_tasks = self._matched_tasks[: border_idx]
            self._matched_costs = self._matched_costs[: border_idx]

    def reset_state(self) -> None:
        self._status = self.NON_INIT_
        self._matched_agents, self._matched_tasks, self._matched_costs = [None] * 3
        
        for it in [self._unassigned_indices, self._newborn_indices]:
            it.clear()

    @DoubleCheck
    def _check_matched_agents_tasks_status(self) -> None:
        if not all([self._matched_agents.tolist(), self._matched_tasks.tolist(), self._matched_costs]):
            raise RuntimeError("the algorithm has not optimized any cost, call `match` method first.")
    
    def _check_amount_equal(self) -> _Tup[_Li]:
        lengths = [len(list(item)) for item in 
                   [self._matched_agents.tolist(), 
                    self._matched_tasks.tolist(), 
                    self._matched_costs]
                   if item]

        if lengths and len(set(lengths)) > 1:
            raise ValueError('number of matched agents, tasks and corresponding costs must be equal.')
        elif len(lengths) < 3:
            return [], [], []
        else: 
            return  tuple(list(item) for item in 
                        [self._matched_agents.tolist(), 
                        self._matched_tasks.tolist(), 
                        self._matched_costs])     

    def _check_cost_matrix(self, cost: _MatLike) -> _Tup[int]:
        if cost.size == 0:
            raise ValueError(
                'cost has no value, perhaps no object of typical class in the previous or current'\
                'frame, please check.'
            )
        if len(cost.shape) != 2:
            raise ValueError('cost matrix must be 2-dimensional')
        
        return cost.shape[0], cost.shape[1]
        
    @staticmethod
    def _swap_inplace(arr: _Iter, idx1, idx2) -> None:
        arr[idx1], arr[idx2] = arr[idx2], arr[idx1]
            
    @property
    def assigned_indices_(self) -> _Tup[_Li[int]]:
        return self._check_amount_equal()[:2]
    
    @property
    def assigned_costs_(self) -> _UnlimLi:
        return self._check_amount_equal()[-1]
    
    @property
    def unassigned_indices_(self) -> _Li[int]:
        return self._unassigned_indices
    
    @property
    def newborn_indices_(self) -> _Li[int]:
        return self._newborn_indices
    
    @property
    def matching_status_(self) -> _Ltrl:
        self._status

        