"""
Image Visualizers
----
character: non-root script
Author: Haokun Zhang <haokun.zhang@hirain.com>
Initial date: 05.15.2024
log: --

"""

import numpy as np
import os, shutil
from tqdm import tqdm
from matplotlib import pyplot as plt
from matplotlib.transforms import Affine2D
from PIL import Image

from ..utils import box_olwhy_to_corners
from .base_visual import CustomVisual
from .._internal._typing import *
from .._internal._functools import *


class CamImageVisual(CustomVisual):
    def __init__(self, line_width: int = 1, center_rad: int = 2, draw_center: bool = False, filter_boxes: bool = True, 
                 draw_info: bool = True, colors: _AnyT = None, info_colors: _AnyT = "unique") -> None:
        super().__init__(line_width, center_rad, draw_center, filter_boxes, draw_info, colors, info_colors)
        self._pil_images: _Dict[str, _Li[_PILImg]] = None
        self._drawed_img_size: _UnlimTup = None
        
    def draw_all(self, save_dir: str, cache_imgs: bool = False, stack_img_if_plural: str = "vertical"):
        """
        
        """
        self._check_loading_status()
        if os.path.exists(save_dir):
            shutil.rmtree(save_dir)
        os.mkdir(save_dir)
        
        self._pil_images = {"camera_fov30": [], "camera_fov120": []}
        print("\nDrawing camera images...")
        _pbar = tqdm(self._timestamps, ncols=90, colour='red')
        for index, _ts in enumerate(_pbar):
            imgs = self.process_step(index)
            if cache_imgs:
                self._pil_images["camera_fov30"].append(imgs[0])
                self._pil_images["camera_fov120"].append(imgs[1])

            _img_name = str(_ts).replace(".", "") + ".png"
            _pbar.set_description(f"drawing {_img_name}")
            if stack_img_if_plural:
                _stacked = self._stack_imgs(*imgs, stack_method=stack_img_if_plural)
                _stacked.save(os.path.join(save_dir, _img_name))
                self._drawed_img_size = (_stacked.height, _stacked.width)
            else:
                for _img_idx, (key, _) in enumerate(self._pil_images.items()):
                    _dir = os.path.join(save_dir, key)
                    if not os.path.exists(dir): os.mkdir(_dir)
                    imgs[_img_idx].save(
                        os.path.join(_dir, key + _img_name)
                    )
                self._drawed_img_size = (imgs[0].height, imgs[0].width)

            if index == len(self._timestamps) - 1:
                _pbar.set_description("Draw finished.")

        return self
    
    def process_step(self, _step: int) -> _Li[_PILImg]: 
        _infos = self._refined_annos[self._timestamps[_step]]
        _img_paths = _infos['img_path']
        _anno2body = _infos['anno2body']
        _orientation = _infos['orientation']
        _boxes = np.asarray([item['boxes'][:7] for item in _infos['infos']])
        _ort2flu = self._af.get_orientation_transform(_orientation, 'flu')

        _types, _ids = [[item[key] for item in _infos['infos']] for key in ['type', 'id']]
        _colors = self._generate_colors_by_types(_types, self._colors)

        pil_images = []
        for _path, _params, _fov in zip(_img_paths, [self._cam30_params, self._cam120_params], [30, 90]):
            self._drawer.load_img(_path)

            if _boxes.size > 0:
                _centers = _anno2body[:3, :3] @ _boxes[:, :3].T + _anno2body[:3, -1:] # anno -> body

                _kept = self._filter_boxes_outof_vision(_centers.T, _fov, fov_bias=0., return_mask=True)
                _boxesf, _typesf, _idsf, _colorsf = self._boolean_mask(_boxes, _types, _ids, _colors, mask=_kept)

                if len(_boxesf) > 0:
                    corners, centers = self._compute_box_center2d(_boxesf, _ort2flu, _params[1], _params[0], _anno2body)
                    centers = None if not self._draw_center else centers
                    
                    self._drawer.draw_boxes3d_with_center(corners, centers, _colorsf)

                    if self._draw_text:
                        for _type, _id, _loc, _c in zip(_typesf, _idsf, corners[:, 2], _colorsf):
                            self._drawer.draw_text(
                                f"{_type}|id {_id}", _loc, [0., -12], _c if self._info_colors == 'follow' else None
                            )
                        
            pil_images.append(self._drawer.image_)

        return pil_images
    
    def _compute_box_center2d(self, boxes: _MatLike, ort_trans: _MatLike, extrin: _MatLike, intrin: _MatLike,
                     anno2body: _MatLike = None):
        _boxes = np.asarray(boxes).copy()
        _centers_anno = _boxes[:, :3]
        # _boxes[:, 3:6] = (ort_trans @ _boxes[:, 3:6].T).T # lwh
        _boxes[:, -1] = self._af.transform_heading(_boxes[:, -1], ort_trans) # yaw
        _trans = self._af.augment_intrinsic(intrin) @ self._af.inverse(extrin)

        _corners_anno = []
        for box in _boxes:
            _corners_anno.append(box_olwhy_to_corners(box, ort_trans, True, 'radius', 'x'))
        _corners_anno = np.asarray(_corners_anno)

        if anno2body is not None:
            _trans = _trans @ anno2body

        _corners_pixel, _centers_pixel = [self._anno2pixel(points, _trans, True) 
                                          for points in [_corners_anno, _centers_anno]]
        
        return _corners_pixel, _centers_pixel

    def _anno2pixel(self, points: _MatLike, trans: _MatLike, aug_points: bool = True):
        points = self._af.format_coordinates(points, "axis_first")
        if aug_points:
            points = self._af.augment_coordinates(points)
        
        _points = trans @ points # [3, 4] @ [n, 4, 8]
        _points = self._af.z_axis_normalize(_points, transpose_points=True) # [n, 8, 2]

        return _points
    
    def _check_loading_status(self) -> None:
        _check_list = [self._refined_gt, self._cam30_params, self._cam120_params, 
                self._timestamps, self._refined_annos]
        if not all(_check_list):
            raise RuntimeError("Refined gt file has not been loaded yet, load the file first "\
                               "by calling the instantiated class.")
        
    @staticmethod
    def _stack_imgs(img1: _PILImg, img2: _PILImg, stack_method: str) -> _PILImg:
        if stack_method == "horizontal":
            assert img1.height == img2.height, "Can not stack imgs horizontally due to diferent heights: "\
                                                "{} vs. {}".format(img1.height, img2.height)
            size = (img1.width + img2.width, img1.height)
            paste_box = (img1.width, 0)
        else:
            assert img1.width == img2.width, "Can not stack imgs vertically due to diferent widths: "\
                                                "{} vs. {}".format(img1.width, img2.width)
            size = (img1.width, img1.height + img2.height)
            paste_box = (0, img1.height)

        
        result = Image.new('RGB', size)  
        result.paste(img1, (0, 0))  
        result.paste(img2, paste_box)

        return result


class BEVImageVisual(CustomVisual):
    _BACKEND_SOLVER = _Ltrl['matplotlib']
    def __init__(self, canvas_size: _Tup, bev_range: _Tup[_UnlimTup], ego_size: _Tup = None, linewidth: _AnyT = None, cmap: _AnyT = None) -> None:
        super().__init__(colors=cmap)
        self._canvas: _MatLike = None
        self._ch, self._cw = canvas_size
        self._c_center = (self._ch // 2, self._cw // 2)
        self._lw = 1.5 if linewidth is None else linewidth
        self._sl, self._sw = ego_size if ego_size is not None else (5.101, 1.987)

        self._ort = np.asarray([[0, -1], [-1, 0]])
        self._bev2pix: _Tup = self.get_bev2pix(bev_range)
        self._bev_range = bev_range
        self._pil_images: _Li = None

    def __getitem__(self, index: int) -> _MplFig:
        return self.process_step(index, None)
    
    def draw_all(self, save_dir: str, cache_imgs: bool = False, dpi: _AnyT = 100):
        """
        
        """
        self._check_loading_status()
        if os.path.exists(save_dir):
                shutil.rmtree(save_dir)
        os.mkdir(save_dir)
            
        self._pil_images = []
        print("\nDrawing BEV images...")
        _pbar = tqdm(self._timestamps, ncols=90, colour='red')
        for index, _ts in enumerate(_pbar):
            _img_name = str(_ts).replace(".", "") + ".png"
            _pbar.set_description(f"drawing {_img_name}")
            fig = self.process_step(index, save_path=os.path.join(save_dir, _img_name), dpi=dpi)

            if cache_imgs:
                self._pil_images.append(fig)

            if index == len(self._timestamps) - 1:
                _pbar.set_description("Draw finished.")

        return self

    def process_step(self, _step: int, save_path: _AnyT = None, dpi: _AnyT = 100) -> _MplFig:
        _infos = self._refined_annos[self._timestamps[_step]]
        _anno2body = _infos['anno2body']
        _boxes = np.asarray([item['boxes'][:7] for item in _infos['infos']])
        _ort2flu = self._af.get_orientation_transform(_infos['orientation'], 'flu')

        _types, _ids = [[item[key] for item in _infos['infos']] for key in ['type', 'id']]
        _colors = self._generate_colors_by_types(_types, self._colors, True)

        fig = plt.figure(figsize=(self._cw / dpi, self._ch / dpi))
        if _boxes.size > 0:
            _yaws = self._af.transform_heading(_boxes[:, -1], _ort2flu)
            _boxes_anno = []
            for _box in _boxes:
                _boxes_anno.append(box_olwhy_to_corners(_box, _ort2flu, False))
            _boxes_anno = np.asarray(_boxes_anno) # [N, 3, 8]
            _boxes_body = _anno2body @ self._af.augment_coordinates(_boxes_anno) # [N, 4, 8]

            _boxes_bev = self.boxes_3d_to_bev(_boxes_body, transpose=True, yaws=_yaws)
            self.draw_bev_boxes(_boxes_bev, fig, cmap=_colors, save_path=save_path, dpi=dpi)
        else:
            if save_path is not None:
                fig.savefig(save_path, bbox_inches='tight', pad_inches=0, dpi=dpi)  

        plt.close(fig)  
        return fig
        
    def boxes_3d_to_bev(self, boxes: _MatLike, transpose: bool = False, yaws: _VecLike = None, box_fmt: _StrLike = "tlbr") -> _MatLike:
        """
        Calculate 2D boxes in BEV which is fomatted as [N, 4] or [N, 5] given boxes with shape of [n_boxes, n_corners, coords].
        It is defaulted that the coordinate axis is at the last dimension i.e. [N, 8, xyz1] or [N, 8, xyz]

        Args:
        ---
            - boxes:
            - transpose:
            - yaws:

        Returns:
        ---
        """
        assert box_fmt in ["tlbr", "xywh"]
        if transpose:
            boxes = self._af.transpose(boxes)

        __minmax = lambda x: (np.min(x, axis=-1), np.max(x, axis=-1))
        (xmin, xmax), (ymin, ymax) = [__minmax(boxes[..., i]) for i in [0, 1]] # [N,]

        if box_fmt == "xywh":
            cx, cy = (xmin + xmax) / 2, (ymin + ymax) / 2
            h, w = ymax - ymin, xmax - xmin
            _stacks = [cx, cy, w, h]
        else:
            _stacks = [xmin, ymin, xmax, ymax]
        if yaws is not None: _stacks.append(yaws)

        return np.column_stack(_stacks) # [N, 5] or [N, 4]
    
    def draw_bev_boxes(self, boxes: _MatLike, fig: _MplFig = None, transpose_box: bool = False, box_fmt: str = 'tlbr', yaw_type: str = 'radius', 
                       cmap: _AnyT = None, display: bool = False, save_path: _AnyT = None, dpi: int = 100) -> _MplFig:
        _colors = cmap if cmap is not None else np.asarray([240, 200, 0])[None].repeat(boxes.shape[0], 0) / 255
        # self._check_loading_status()
        assert len(boxes.shape) <= 2
        assert yaw_type in ['radius', 'degree']
        assert box_fmt in ['tlbr', 'xywh']
         
        if len(boxes.shape) == 1:
            boxes = boxes.reshape(1, -1)
        if transpose_box:
            boxes = boxes.T
        assert boxes.shape[-1] == 5 # [x, y, x, y, yaw]

        self_box = np.asarray([[-self._sl / 2, -self._sw / 2., self._sl / 2, self._sw / 2.]])

        _boxes = boxes[:, :-1]
        if box_fmt == "xywh": # uniform to tlbr
            _boxes[:, 2:4] = boxes[:, :2] + boxes[:, 2:4]
        _boxes = np.concatenate([_boxes, self_box], axis=0)

        _boxes = self._trans_bev_to_pixel(_boxes)
        _centers = _boxes[:, :2] + (_boxes[:, 2:4] - _boxes[:, :2]) / 2
        _boxes, self_box = _boxes[:-1], _boxes[-1]
        _centers, self_center = _centers[:-1], _centers[-1]
        
        _yaws = boxes[:, -1]
        if yaw_type == "degree":
            _yaws = _yaws / 180. * np.pi
        _yaws = self._trans_yaw2d(_yaws)

        if fig is None:
            fig = plt.figure(figsize=(self._cw / dpi, self._ch / dpi))
        fig, ax = self._decorate_canvas(fig, yticks=[-15, 0, 15], xticks=[0, 50, 100])

        for index, (_cls, _c) in enumerate(self._cmap.items()):
            ax.text(1, 25 * (index) + 35, _cls, color=_c, fontsize=10,
                    fontfamily='serif', fontweight='bold',
                    )

        for _box, _center, _yaw, _color in zip(_boxes, _centers, _yaws, _colors):
            xmin, ymin, xmax, ymax = _box
            # draw & rotate bounding box
            _rect = plt.Rectangle(
                (xmin, ymin), xmax - xmin, ymax - ymin,
                linewidth=self._lw, edgecolor=_color, facecolor='none'
            )
            _trans = Affine2D().rotate_around(_center[0], _center[1], -_yaw)

            # draw heading lines
            heads = [_center[0], ymin]
            heads = _trans.transform(heads)
            _rect.set_transform(_trans + ax.transData)
            ax.plot([_center[0], heads[0]], [_center[1], heads[1]], color=_color, linewidth=1.)

            ax.add_patch(_rect)

        self_color = [.3] * 3
        ax.text(1, 15, "Self", color=self_color, fontsize=10,
                    fontfamily='serif', fontweight='bold',
                    )
        _rect = plt.Rectangle(
                (self_box[0], self_box[1]), self_box[2] - self_box[0], self_box[3] - self_box[1],
                linewidth=self._lw, edgecolor=self_color, facecolor='none'
            )
        ax.plot([self_center[0], self_center[0]], [self_center[1], self_box[3]], color=self_color, linewidth=1.)
        ax.add_patch(_rect)

        ax.set_xlim(0, self._cw)
        ax.set_ylim(self._ch, 0)
        ax.axis("off")

        if save_path:
            fig.savefig(save_path, bbox_inches='tight', pad_inches=0, dpi=dpi) # scaling bias of inch/dpi is 0.77

        if display:
            plt.show()
            plt.close(fig)

        return fig
    
    def get_bev2pix(self, bev_range: _Tup[_UnlimTup]) -> _ArrTup:
        (xmin, xmax), (ymin, ymax) = bev_range
        _rx, _ry = xmax - xmin, ymax - ymin
        if _rx <= 0 or _ry <= 0:
            raise ValueError("Invalid BEV map range.")
        
        dy, dx = self._cw / _ry, self._ch / _rx
        if dx < dy:
            raise ValueError("BEV to pixel canvas requires euqal-ratio scaling, "\
                             "whereas BEV size is not similar to size of defined canvas.")
        dy = dx  # similarity assurance

        _scale = self._ort * np.asarray([dx, dy])
        _trans = np.array([self._cw / 2. + (ymin + ymax) / 2 * dy, self._ch + xmin * dx]).reshape(-1, 1)

        return _scale, _trans
    
    @UnImplemented
    def draw_text(self, text: str) -> _MatLike: ...

    def _trans_bev_to_pixel(self, points: _MatLike) -> _MatLike:
        """
        points must be `tlbr` format
        """
        assert len(points.shape) == 2 and points.shape[-1] == 4 # [n, 2]

        _points = points.reshape(-1, 2)
        
        _scale, _trans = self._bev2pix
        _points = (_scale @ _points.T + _trans).T # [2, n]

        return _points.reshape(-1, 4)

    def _trans_yaw2d(self, yaws: np.ndarray):
        _yaws_vec = np.row_stack([np.cos(yaws), np.sin(yaws)]) # [2, n]
        _trans_yaw_vec = self._ort @ _yaws_vec

        return np.arctan2(_trans_yaw_vec[0], _trans_yaw_vec[1])
    
    def _decorate_canvas(self, fig: _MplFig = None, dpi: _AnyT = 100, xticks: _Iter = None, yticks: _Iter = None):
        (xmin, xmax), (ymin, ymax) = self._bev_range
        xticks = [50, 100] if xticks is None else xticks
        yticks = [-10, 10] if yticks is None else yticks

        line_hor = np.asarray([[(i, ymin), (i, ymax)] for i in xticks])
        line_ver = np.asarray([[(xmin, i), (xmax, i)] for i in yticks])

        # print("test line shape", lines.shape)
        _scale, _trans = self._bev2pix
        line_hor, line_ver = [_scale @ self._af.transpose(_line) + _trans for _line in [line_hor, line_ver]]

        if fig is None:
            fig = plt.figure(figsize=(self._cw / dpi, self._ch / dpi))
        ax = fig.subplots(1, 1)
        ax.imshow(np.ones([self._ch, self._cw, 3]))

        for lines, ticks in zip([line_hor, line_ver], [xticks, yticks]):
            for index, line in enumerate(lines):
                ax.plot(line[0], line[1], linestyle="--", color="gray", alpha=.5)
                ax.text(line[0, 0], line[1, 0], f"{ticks[index]}m", verticalalignment='top', color=[.5] * 3, fontsize=10, fontweight='bold')

        return fig, ax
    
    def _check_loading_status(self):
        _check_list = [self._refined_gt, self._timestamps, self._refined_annos]
        if not all(_check_list):
            raise RuntimeError("Refined gt file has not been loaded yet, load the file first "\
                               "by calling the instantiated class.")
