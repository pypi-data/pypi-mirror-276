"""
Base Visual classes
----
character: non-root script
Author: Haokun Zhang <haokun.zhang@hirain.com>
Initial date: 05.15.2024
log: --

"""

import numpy as np

from .._internal._typing import *
from .._internal._functools import *
from .._internal._std import *
from ..utils import *


class Colors(object):
    NuScenes_ = [(240, 200, 0), (220, 0, 120), (255, 192, 203), 
                (0, 220, 240), (200, 0, 240), (72, 0, 255), (0, 140, 150)]
    CityScapes_ = ...
    VOC12_ = ...
    COCOdet_ = ...
    Kitti_ = ...


class Visual:
    """
    A Visual interface API for encapsulating using steps and logic for a custom visualizer subclass. Users who need 
    to develop futher visualizing functions are requested to use this interface.

    Args:
    ----
        - name [Optional]: name of this visualizer

    Standalone usage:

        ```python
            vis = SomeVisual(...)
            vis.load_info(...)
            fig = vis[index]
        ```

        for those backend solver is Pillow, a `__getitem__` builtin method should be overwritten and return 
        a `PIL.Image.Image` then use:
        
            ```python
                fig.show()
            ```

        or a visualizer which is solved by `matplotlib` solver should return a `matplotlib.figure.Figure` 
        type from `__getitem__`, in this case, use 
        
            ```python
                plt.show()
                plt.close(fig)
            ```

    Methods to be implemented by subclasses:
        - `__init__()`: A constructor to create all the state variables.
        - `__len__()`: To return a length that represents number of timestamps.
        - `load_gt(...)`: To define how the gt file is loaded and format of which is checked.
        - `process_step(...)`: To define how a step of drawing boxes and others on an image is performed.
        - `draw_all()`: To define how the whole drawing process is performed. This might be refined a bas framework 
            and will be prohibited implemnting in the future version.

    Methods can be overwritten by subclasses:
        - `__getitem__(index: _IntLike)`: This method automatically call `process_step(...)` method, and it
            is strictly limited to one argument `index` for indexing and slicing. Therefore it might have to be
            overwritten as  `process_step(...)` requires more arguments.
        - `_check_loading_status(...)`: To define whether the required information is loaded or variables exist.
        - `__repr__`: To display current information of a particular subclass.

    Methods prohibited to be overwritten:
        - `__call__(*args: _AnyT, **kwargs: _AnyT)`: arguments are automatically passed to `load_gt(...)`.
    
    """
    def __init__(self, name: _StrLike = None) -> None:
        """
        ### This method needs to be implemented.
        A constructor to create all the state variables.
        
        Args:
        ---
            - name [Optional]: name of the visualizer class or subclass.
        """
        self.name = self.__reformat_class_name(name)

    def __call__(self, *args: _AnyT, **kwargs: _AnyT):
        """
        ### This method is prohibited to be overwritten.
        A loading wrapper, arguments are automatically passed to `load_gt(...)`.
        It is provisionally not allowed to pass redundant arguments otherwise raises an error

        Args:
        ---
          *args: Positional arguments to be passed to `self.load_gt(...)`.
          **kwargs: Keyword arguments to be passed to `self.load_gt(...)`.
        
        Raises:
        ---
        TypeError: if no argument is passed.
        InvalidArgumentError: if passed argument(s) that do not exist.
        """
        if not args or not kwargs:
            raise TypeError("__call__() requires a positional argument but none has passed.")
        if args:
            assert len(args) == 1
            __p = args[0]
        elif kwargs:
            assert len(kwargs) == 1
            __p = kwargs
        else:
            raise InvalidArgumentError("Invalid arguments exsit.")

        self.load_info(__p)
        return self

    def __getitem__(self, index: _IntLike) -> _AnyT:
        """
        ### This method can be overwritten.
        This method automatically call `process_step(...)` method

        Args:
        ---
         - index: A number specifies the position of the sequence.
        """
        return self.process_step(index)
    
    def __len__(self) -> _IntLike:
        """
        ### This method needs to be implemented.
        To return a length that represents amount of timestamps.
        """
        raise NotImplementedError("This method needs to be implemented by subclasses")

    def __repr__(self) -> _StrLike:
        """
        ### This method can be overwritten.
        """
        return self.name

    def load_info(self, info: _AnyT):
        """
        ### This method needs to be implemented.
        Load a ground truth information

        Args:
        ---
            - info: required information, usually a dictionary.
        """
        raise NotImplementedError("This method needs to be implemented by subclasses")

    def process_step(self, _step: _IntLike, **kwargs: _AnyT) -> _AnyT:
        """
        ### This method needs to be implemented.
        Parse infos and draw them onto an loaded image.

        Args:
        ---
            - _step: an index to define which step of the sequence should be processed/drawn.

        Returns:
        ---
            A drawn image which type depends on backend solver.
        """

        # if kwargs and _step not in kwargs.keys():
        #     raise InvalidArgumentError("method `process_step()` requires a positional argument `_step`.")

        raise NotImplementedError("This method needs to be implemented by subclasses")
    
    def draw_all(self):
        """
        ### This method needs to be implemented.
        Draw the whole images sequentially.
        """
        raise NotImplementedError("This method needs to be implemented by subclasses")
    
    def _check_loading_status(self, _check_list: _Li) -> None:
        """
        ### This method can be overwritten.
        To check whether the required information is loaded or variables exist.

        Args:
        ---
            _check_list: state variables to be checked.

        Raises:
        ---
            RuntimeError: if file is not loaded.
        """
        if not all(_check_list):
            raise RuntimeError("Information has not been loaded yet, load the info file first "\
                               "by `load_info()` or calling the instantiated class.")

    def __reformat_class_name(self, name: _StrLike = None):
        _raw_name = []
        name = type(self).__name__ if name is None else name
        for index, _char in enumerate(type(self).__name__):
            if index != 0 and _char.isupper():
                _char = "_" + _char
            _raw_name.append(_char)

        return "".join(_raw_name).lower()


class CustomVisual(Visual):
    @VersionControl("onhold")
    def __init__(self, line_width: int = 1, center_rad: int = 2, draw_center: bool = False, filter_boxes: bool = True,
                 draw_info: bool = True, colors: _AnyT = None, info_colors: _AnyT = "unique") -> None:
        super().__init__(name="custom_visual")

        assert info_colors in ['unique', 'follow']
        self._colors = Colors.NuScenes_ if colors is None else colors
        self._info_colors = info_colors
        self._drawer = Drawer(line_width, center_rad, None)
        self._draw_center = draw_center
        self._draw_text = draw_info
        self._filter_boxes = filter_boxes
        self._af = AffineTransformer()

        self._refined_gt: _Dict = None
        self._cam30_params: _Tup[_MatLike] = None
        self._cam120_params: _Tup[_MatLike] = None
        self._timestamps: _UnlimLi = None
        self._refined_annos: _Dict = None
        self._cmap: _Dict = {}

    def load_info(self, refined_gt: _Dict):
        r"""
        Refined gt dictionary must be structured as follow:
        ```python
        {
            'cameras': {
                'camera_fov30': {'camera2body': [_MatLike], 'intrinsic': [_MatLike]}
                'camera_fov120': {'camera2body': [_MatLike], 'intrinsic': [_MatLike]}
                }
            'annos':{
                `timestamps`[str]: {
                    'img_path':[str],
                    'infos': {'type': [str], 'id': [int], 'boxes': [_U[_UnlimLi, _MatLike]]}
                    'anno2body': [_MatLike],
                    'orientation': [str]
                }
                ...
            }
        }
        ```
        """ 
        self._refined_gt = self._check_refined_gt_structure(refined_gt)
        _cam_30_params = self._refined_gt['cameras']['camera_fov30']
        _cam_120_params = self._refined_gt['cameras']['camera_fov120']

        _intrin30, _intrin120 = _cam_30_params['camera_intrinsic'], _cam_120_params['camera_intrinsic']
        _intrin30, _intrin120 = [self._af.scale_intrinsic(_intrin, 2 / 3) 
                                 for _intrin in [_intrin30, _intrin120]]

        self._cam30_params = (_intrin30, _cam_30_params['camera2body'])
        self._cam120_params = (_intrin120, _cam_120_params['camera2body'])
        self._refined_annos = self._refined_gt['annos']
        self._timestamps = [_key for _key in self._refined_annos.keys()]

        return self

    def __len__(self):
        assert self._timestamps is not None
        return len(self._timestamps)
    
    def __getitem__(self, index: int) -> _Li[_PILImg]: 
        return self.process_step(index)
    
    def set_colormap(self, cmap: _StrDict, normalize: bool = False) -> None:
        if normalize:
            for key, val in cmap.items():
                cmap[key] = tuple(np.asarray(val) / 255.)

        self._cmap = cmap
    
    def _check_refined_gt_structure(self, _gt: _Dict) -> _UnlimDict:
        # maybe solved by dfs
        self._check_keys(_gt, *['cameras', 'annos'])
        for key in [f'camera_fov{fov}' for fov in [30, 120]]:
            self._check_keys(_gt['cameras'][key], *['camera2body', 'camera_intrinsic'])

        _ts_keys = [key for key in _gt['annos'].keys()]
        for key in _ts_keys:
            self._check_keys(_gt['annos'][key], *['img_path', 'infos', 'anno2body', 'orientation'])

        return _gt
    
    @staticmethod
    def _filter_boxes_outof_vision(boxes: _MatLike, fov: _AnyT, fov_bias: _AnyT = 0., thres_x: _AnyT = 1.5, return_mask=False):
        _frustum_edge_angle = ((fov + fov_bias) / 2) / 180 * np.pi
        x, y = boxes[..., 0], boxes[..., 1]
        kept = np.logical_and(x >= thres_x, np.abs(y / (x - thres_x)) <= np.tan(_frustum_edge_angle))
        return boxes[kept] if not return_mask else kept
    
    def _boolean_mask(self, *_iter: _AnyT, mask: _MatLike):
        _filtered_iters = (np.asarray(_item_to_be_filtered)[mask].tolist() for _item_to_be_filtered in _iter)
        return _filtered_iters if len(_iter) > 1 else _filtered_iters[0]
    
    @staticmethod
    def _check_keys(__dic: _Dict, *__keys: _AnyT) -> bool:
        for key in __keys:
            if not key in __dic:
                raise KeyError("dict does not have key: `{}`".format(key))
        return True
    
    def _generate_colors_by_types(self, types: _AnyT, colors: _Li[_Tup[int]], normalize: bool = False):
        if not types: # no object appears in a particular frame
            return []
        
        for _t in set(types):
            if _t not in self._cmap:
                _color = colors.pop(0)
                if normalize:
                    _color = np.asarray(_color) / 255.
                self._cmap[_t] = tuple(_color)
                colors.append(_color)

        return [self._cmap[_t] for _t in types]
    
    @property
    def colormap_(self) -> _StrDict:
        return self._cmap
         