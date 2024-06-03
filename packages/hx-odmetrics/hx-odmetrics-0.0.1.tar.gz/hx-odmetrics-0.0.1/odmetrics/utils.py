"""
Od metrics utils script
character: root script
Author: Haokun Zhang <haokun.zhang@hirain.com>
Initial date: 04.03.2024
log: --
"""

import numpy as np
import json
from PIL import Image, ImageDraw

from ._internal._functools import *
from ._internal._typing import *


__all__ : _Li = [
    "AffineTransformer",
    "swap_inplace",
    "get_batch_dist_eu",
    "get_3dboxes_iou",
    "Drawer",
    "_construct_rots",
    "load_json",
    "save_json",
    "box_olwhy_to_corners",
    "_render_stdout"
]


class AffineTransformer:
    def __init__(self) -> None:
        pass

    @classmethod
    def scale_intrinsic(cls, intrinsic: _MatLike, scale_rate: _AnyT, aug_method: _AnyT = None) -> _MatLike:
        """
        scale_rate: Any: when providing two values, the first and the second are 
            considered be involved with height, width respectively.
        """
        if not isinstance(scale_rate, _Iter):
            scale_rate = [scale_rate] * 2
        else:
            if not len(scale_rate) == 2:
                raise ValueError("Provided scale rate must no nore than 2 values")
            scale_rate = [scale_rate[0], scale_rate[1]]
        
        _intrinsic = intrinsic.copy()
        _intrinsic[0, [0, 2]] *= scale_rate[1]
        _intrinsic[1, [1, 2]] *= scale_rate[0]

        if aug_method:
            _intrinsic = cls.augment_intrinsic(_intrinsic, aug_method)
        return _intrinsic
    
    def augment_coordinates(self, coords: _MatLike, transpose_coords: bool = False, aug_value: _AnyT = None) -> _MatLike:
        """
        The method augments coordinates by padding unit vector at xyz axis for corrdinate transformation, it is defaulted that
        the xyz axis is the last second dimension, i.e. [N, xyz, N_corner] or [xyz, corner] -> [N, 3, 8] or [3, 8], 
        if argument `coords` is shaped like [N, 8, 3], one must transpose matrix to [N, 3, 8] before passing, 
        or set argument `transpose_coords` to `True` that operates an internal transpose.

        Args
        ---
            - coords:
            - transpose_coords:
            - aug_value:

        Returns:
        ---
            [_MatLike] augmented coordinates with a shape of [N, 4, 8]
        """

        if transpose_coords:
            coords = self.transpose(coords)
        
        _expand = False
        if len(coords.shape) == 2:
            coords = coords[None]
            _expand = True

        _cshape = list(coords.shape)
        _cshape[-2] += 1

        aug_value = 1. if not aug_value else aug_value
        _aug_coords = np.ones(_cshape) * aug_value
        _aug_coords[:, :3, :] = coords

        if _expand: 
            _aug_coords = _aug_coords.squeeze(0)
        
        return _aug_coords
    
    @staticmethod
    def inverse(_affine: _MatLike) -> _MatLike:
        return np.linalg.inv(_affine) 
    
    @classmethod
    def augment_intrinsic(cls, intrinsic: _MatLike, method: str = "normal"):
        if method not in ['normal', 'square']:
            raise AttributeError("Invalid method type, choice: 'normal', 'square'.")
        
        _aug_intrin = np.zeros([3, 4]) if method == 'normal' else np.eye(4)
        _aug_intrin[:3, :3] = intrinsic

        return _aug_intrin
    
    def deaug_intrinsic(self, aug_intrinsic: _MatLike):
        ...

    def construct_extrinsic(self, rot: _AnyT, trans: _AnyT, rot_type: _AnyT = None) -> _MatLike:
        ...

    def distruct_extrinsic(self, extrinsic: _MatLike) -> _Tup[_MatLike, _MatLike]:
        ...

    def z_axis_normalize(self, points: _MatLike, transpose_points: bool = False, return_2d: bool = True) -> _MatLike:
        if transpose_points:
            points = self.transpose(points)

        if return_2d is True:
            return points[..., :2] / points[..., 2: 3]
        else:
            return points / points[..., 2: 3]
        
    @staticmethod
    @DoubleCheck
    def transform_heading(yaw: _U[float, _MatLike], trans: _MatLike, yaw_type: str = "radius") -> _U[float, _MatLike]:
        if yaw_type == 'degree':
            yaw = yaw / 180 * np.pi
        yaw = np.asarray(yaw).reshape(-1, 1)

        if trans.size == 16:
            trans = trans[:3, :3]

        _yaw_vec = np.hstack([np.cos(yaw), np.sin(yaw), np.zeros_like(yaw)]).T # [3, n]
        _yaw_vec = trans @ _yaw_vec # [3, n] [0, -sin, cos]
        _yaw_indices = np.abs(trans @ np.asarray([i for i in range(_yaw_vec.shape[0])]).T).astype(np.uint8)
        _denom, _num = _yaw_indices[1], _yaw_indices[0]

        return np.arctan2(_yaw_vec[_denom], _yaw_vec[_num])
    
    def transform_orientation(self, points: _MatLike, src_ort: str, target_ort: str = 'flu', transpose_points: bool = False) -> _MatLike:
        if transpose_points:
            points = self.transpose(points)
        _points =  self.get_orientation_transform(src_ort, target_ort) @ points

        return _points

    @staticmethod
    def get_orientation_transform(src_ort: str, target_ort: str = 'flu') -> _MatLike:
        _src_hashmap = {}
        mutiplies, positions = [], []
        _hashmap = {'f': 'b', 'l': 'r', 'u': 'd', 'b': 'f', 'r': 'l', 'd': 'u'}

        for _dis, _ort in enumerate([src_ort, target_ort]):
            for index, letter in enumerate(_ort):
                assert letter in _hashmap
                if _dis == 0: # build hashmap based on src_ort
                    _src_hashmap[letter] = index
                else: # get position from target_ort based on _src_hashmap
                    if letter in _src_hashmap:
                        mutiplies.append(1.)
                        positions.append(_src_hashmap[letter])
                    else:
                        mutiplies.append(-1.)
                        positions.append(_src_hashmap[_hashmap[letter]])

        trans = np.zeros([3, 3])
        trans[[0, 1, 2], positions] = np.array(mutiplies)

        return trans  
        
    def z_axis_denormalize(self, coords: _MatLike, z_value: _AnyT) -> _MatLike:
        ...

    def _check_intrinsic(self, intrinsic: _MatLike, status: str = 'augment') -> _MatLike:
        ...

    def _check_extrinsic(self, extrinsic: _MatLike) -> _MatLike:
        ...

    @staticmethod
    def transpose(_mat: _MatLike) -> _MatLike:
        if len(_mat.shape) == 1:
            raise ValueError("transpose requires dimension larger than 1.")
        
        # shape_idx = [i for i in range(len(_mat.shape))]
        # shape_idx[-1], shape_idx[-2] = shape_idx[-2], shape_idx[-1]
        # return _mat.transpose(shape_idx)
        return _mat.swapaxes(-1, -2)
    

    def format_coordinates(self, points: _MatLike, format_mode="axis_last", num_axis: int = None) -> _MatLike:
        assert format_mode in ['axis_first', 'axis_last']
        _axis = -1 if format_mode == 'axis_last' else -2
        num_axis = 3 if not num_axis else num_axis

        if points.shape[_axis] != num_axis:
            points = self.transpose(points)

        return points
    
    def _check_and_format_coordinates(self, coords: _MatLike, format_mode="axis_last") -> _Tup[_MatLike, bool]:
        if 3 not in coords.shape:
            raise ValueError("Not a coodinate matrix or a combination, if the coordinate has been augmented, "
                             "please de-augment before passing.")
        _coords = self.format_coordinates(coords, format_mode)
        _is_transposed = _coords.shape != coords.shape

        return coords, _is_transposed
    
    @_overload
    def body2pixel(self, points: _MatLike, _affine: _MatLike):
        ...
    
    @_overload
    def body2pixel(self, points: _MatLike, extrin: _MatLike, intrin: _MatLike, *, inv_extrin: bool = True):
        ...
    
    def body2pixel(self, points, *args, **kwargs):
        ...



def swap_inplace(arr: _Iter, idx1, idx2) -> None:
    arr[idx1], arr[idx2] = arr[idx2], arr[idx1]


@DoubleCheck
def get_batch_dist_eu(a: _MatLike, b: _MatLike, axis_weights: _AnyT = None) -> _MatLike:
    for item in [a, b]:
        if item.size > 0:
            assert len(item.shape) == 2 and item.shape[-1] == 3

    if not axis_weights:
        axis_weights = np.ones(3)
    else:
        axis_weights = np.asarray(axis_weights)
        assert axis_weights.size in [1, 3]
        if axis_weights.size == 1:
            axis_weights = np.ones(3)
        else: # normalize
            axis_weights = axis_weights / np.sum(axis_weights) * 3
    
    _diff = a.reshape(-1, 1, 3) - b.reshape(1, -1, 3)
    _diff_square  = (_diff * axis_weights) ** 2
    res = np.sqrt(np.sum(_diff_square, axis=-1))

    assert res.shape == (a.shape[0], b.shape[0])
    return res


@VersionControl('onhold')
def get_3dboxes_iou(boxes1: _MatLike, boxes2: _MatLike) -> _MatLike:
    ...


class Drawer:
    def __init__(self, line_width: int = None, circle_rad: int = None, colors: _AnyT = None) -> None:
        if not colors:
            self._colors = [tuple(value) for value in np.random.randint(50, 256, [100, 3]).tolist()]
        else:
            self._colors = colors

        self._lw = 1 if not line_width else line_width
        self._cr = 2 if not circle_rad else circle_rad
        self._drawer = None
        self._img_pil: _PILImg = None

    def __call__(self, *args):
        if not args:
            raise AttributeError("method  requires at least one arguments `path` but 0 was passed.")
        if args and len(args) >= 2:
            args = args[:2]
        else:
            args  = [args[0], None]

        return self.load_img(*args)
        # return self

    def load_img(self, item: _U[str, _PILImg], color_mode: _AnyT = None):
        if isinstance(item, str): 
            color_mode = "RGB" if not color_mode else color_mode
            self._img_pil = Image.open(item).convert(color_mode)
        elif isinstance(item, _PILImg):
            self._img_pil = item
        else:
            raise TypeError("Invalid type, item must be a path to an image or a PIL image.")

        self._drawer = ImageDraw.Draw(self._img_pil)

        return self
    
    def draw_boxes3d_with_center(self, coords: _MatLike = None, centers: _MatLike = None, colors: _AnyT = None) -> _PILImg:
        if colors is None:
            colors = self._colors
        
        if coords is not None:
            self.draw_boxes3d(coords, colors)
        if centers is not None:
            self.draw_points(centers, colors)
        np.random.shuffle(self._colors)
        return self._img_pil
    
    def draw_boxes3d(self, coords: _MatLike, colors: _AnyT = None) -> _PILImg:
        coords = self._format_points(coords, "box")

        if colors is None:
            colors = self._colors

        for _index, box in enumerate(coords):
            _color_lines = tuple(colors[_index])
            for index in range(4):
                self._drawer.line([tuple(box[index].astype(int)), tuple(box[(index + 1) % 4].astype(int))],
                        fill=_color_lines, width=self._lw)
                
            for index in range(4, 8):
                self._drawer.line([tuple(box[index].astype(int)), tuple(box[(index + 1) % 4 + 4].astype(int))],
                        fill=_color_lines, width=self._lw)
                
            for index in range(4):
                self._drawer.line([tuple(box[index].astype(int)), tuple(box[index + 4].astype(int))],
                        fill=_color_lines, width=self._lw)
        
        return self._img_pil

    def draw_points(self, points:_MatLike, colors: _AnyT = None) -> _PILImg:
        points = self._format_points(points, 'point')

        if colors is None:
            colors = self._colors

        ellipsis_pts = np.column_stack([
            points[:, 0] - self._cr, points[:, 1] - self._cr, 
            points[:, 0] + self._cr, points[:, 1] + self._cr,
        ])

        for index, point in enumerate(ellipsis_pts):
            _color_pt = tuple(colors[index])
            self._drawer.ellipse(list(point), _color_pt)
            self._colors.append(_color_pt)

        return self._img_pil
    
    @UnImplemented
    def draw_texts(self, texts: _Iter[str], positions: _MatLike, bias: _MatLike = None,
                  colors: _AnyT = None, alpha: int = None, font: _AnyT = None, align: str = "left"):
        if bias:
            positions  = np.asarray(positions) + np.asarray(bias)

        if len(texts) != len(colors):
            colors = [colors] * len(texts)
        for index in range(len(texts)):
            self.draw_text(texts[index], positions[index], None, tuple(colors[index]), alpha, font, align)

        return self._img_pil
    
    def draw_text(self, text: _AnyT, position: _MatLike, bias: _VecLike = None,
                  color: _AnyT = None, alpha: int = None, font: _AnyT = None, align: str = "left"):
        position = np.asarray(position)
        bias = np.zeros_like(position) if not bias else np.asarray(bias)
        position += bias
        # position[position < 0.] = 0.
        _alpha = 255 if not alpha else alpha
        color = (225, 225, 225) if not color else color
        _color = tuple([i for i in list(color) + [_alpha]])
        self._drawer.text(position, str(text), _color, font, align=align)

        return self._img_pil
    
    def _check_loading_status(self):
        if not self._img_pil or self._drawer:
            raise ValueError("Image has not been loaded, call or use `load_img` first.")
    
    @property
    def image_(self):
        # self._check_loading_status()
        return self._img_pil
        
    @staticmethod
    def _format_points(points: _MatLike, style: str = "box") -> _MatLike:
        assert style in ["box", "point"]

        if style == "box":
            if len(points.shape) != 3: points = np.expand_dims[None]
            if points.shape[-1] != 2: points = points.transpose(0, 2, 1) # [N, 8, 2]
            assert points.shape[-2:] == (8, 2), "Invalid point shape: {}".format(points.shape)
        elif style == "point":
            if len(points.shape) != 2:
                raise ValueError("Invalid shape {}".format(points.shape))
            if points.shape[-1] != 2: points = points.T # [N, 2]
        else:
            raise ValueError("invalid argument, choices: `box`, `point`")
        
        return points


def _construct_rots(yaw: float, rot_axis: str = "z"):
    assert rot_axis in ['x', 'y', 'z']
    _rots = np.asarray([np.cos(yaw), -np.sin(yaw), np.sin(yaw), np.cos(yaw)])
    _frame = np.eye(3)

    if rot_axis == 'y':
        for index, (row, col) in enumerate([(0, 0), (0, 2), (2, 0), (2, 2)]):
            _frame[row, col] = _rots[index]
    else:
        if rot_axis == "z":
            _frame[:2, :2] = _rots.reshape(2, 2)
        else:
            _frame[1:3, 1:3] = _rots.reshape(2, 2)

    return _frame


def load_json(fp: str, mode: str = "r") -> _Dict:
    with open(fp, mode) as f:
        _file = json.load(f)

    return _file


def save_json(file: _AnyT, fp: str, mode='w') -> None:
    with open(fp, mode) as f:
        json.dump(file, f, indent=4)


@ToModify("To vectorize")
def box_olwhy_to_corners(boxes: _MatLike, ort_trans: _MatLike = None, with_yaw: bool = True, yaw_type: str = 'radius', rot_axis: str = "z"):
    assert boxes.size == 7
    assert yaw_type in ['radius', 'degree']
    x, y, z, l, w, h, yaw = boxes

    if yaw_type == 'degree':
        yaw = yaw / 180 * np.pi

    _x_cor = np.array([l / 2.] * 8) * np.array([1, 1, -1, -1, 1, 1, -1, -1])
    _y_cor = np.array([w / 2.] * 8) * np.array([-1, 1, 1, -1, -1, 1, 1, -1])
    _z_cor = np.array([h / 2.] * 8) * np.array([1] * 4 + [-1] * 4)

    _coords = np.vstack([_x_cor, _y_cor, _z_cor]) # [3, 8]
    if ort_trans is not None:
        _coords = ort_trans @ _coords
    if with_yaw:
        _coords = _construct_rots(yaw, rot_axis) @ _coords # [3, 3] @ [3, 8]
    _coords += np.asarray([x, y, z]).reshape(-1, 1) # [3, 8] + [3, 1]
    return _coords


def _render_stdout(out_str: str, color: _AnyT = None, display: bool = False):
        _endc = "\033[0m"
        if isinstance(color, str):
            _colormap = {
                'gray': "\033[90m",
                'black': "\033[0m", 'red': "\033[91m", 'blue': "\033[94m",
                'green': "\033[92m", 'yellow': "\033[93m", 'purple': "\033[95m",
            }
            assert color in _colormap, "Invalid key, available color for ref: {}".format(
                [i for i in _colormap.keys()]
            )
            _color = _colormap[color]
        elif isinstance(color, int):
            _color = "\033[{}m".format(color)
        else: 
            raise TypeError("Type of arg `color` must be int or str.")
        
        _rout = _color + out_str + _endc
        
        if display:
            print(_rout)

        return _rout
