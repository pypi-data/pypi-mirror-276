"""
Video Generators
----
character: non-root script
Author: Haokun Zhang <haokun.zhang@hirain.com>
Initial date: 05.15.2024
log: --

"""

import numpy as np
import os, shutil
from PIL import Image
from tqdm import tqdm

from .base_visual import CustomVisual
from .image_visual import CamImageVisual, BEVImageVisual
from .._internal._typing import *
from .._internal._functools import *


class VideoGenerator:
    def __init__(self, backend_solver: _AnyT = None) -> None:
        self._bs = "ffmpeg" if backend_solver is None else backend_solver
        assert self._bs in ['cv', 'ffmpeg']

    def generate_video(self, img_dir: _StrLike, save_path: _StrLike, fps: _AnyT, size: _UnlimIter = None, 
                       encode: _AnyT = None, pixel_fmt: _AnyT = "yuv420p"):
        _img_format = self._check_img_format(img_dir)

        if self._bs == "cv":
            _img_list = []
            size = self._drawed_img_size[::-1] if size is None else size
            for _ts in self._timestamps:
                _ts_ = str(_ts).replace(".", "") + f".{_img_format}"
                _img_list.append(os.path.join(img_dir, _ts_))
            self.__solve_by_cv2(_img_list, save_path, fps, size)
        else:
            encode = "libx264" if encode is None else encode
            self.__solve_by_ffmpeg(img_dir, save_path, fps, _img_format, encode, pixel_fmt)

        print("Video saved to {}".format(save_path))
    
    @VersionControl('onhold')
    def __solve_by_cv2(self, img_list: _StrLi, vid_dir: _StrLike, fps: _AnyT, size: _UnlimIter) -> None:
        import cv2
        _vid_formats = {"mp4": "mp4v", "avi": "xvid", "flash": "flv1"}
        _fourcc =cv2.VideoWriter_fourcc(*_vid_formats[vid_dir.split(".")[-1]])
        _writer = cv2.VideoWriter(vid_dir, _fourcc, fps, size)

        for _img in tqdm(img_list, ncols=90):
            _frame = cv2.imread(_img)
            _writer.write(_frame)
        _writer.release()

    def __solve_by_ffmpeg(self, img_dir: _StrLike, vid_dir: _StrLike, fps: int, img_fmt: _StrLike = None, 
                          encode: _AnyT = None, pixel_fmt: _AnyT = "yuv420p"):
        ffmpeg_cmd = f"ffmpeg -framerate {fps} -pattern_type glob -i '{img_dir}/*.{img_fmt}' "\
            f"-c:v {encode} -r {fps} -pix_fmt {pixel_fmt} {vid_dir}"
        
        os.system(ffmpeg_cmd)

    def _check_img_format(self, img_dir: _StrLike):
        _imgs_format = [_name.split(".")[-1] for _name in os.listdir(img_dir)]
        _format = set(_imgs_format)
        if ".DS_Store" in _format:
            _format.remove(".DS_Store")

        if not len(_format) == 1:
            raise TypeError("Found multiple formats from image list: {}".format(_format))
        return _format.pop()


class CameraVisualizer(CamImageVisual, VideoGenerator):
    def __init__(self, save_path: _StrLike, line_width: int = 1, center_rad: int = 2, draw_center: bool = False, 
                 filter_boxes: bool = True, draw_info: bool = True, colors: _AnyT = None, info_colors: _AnyT = "unique") -> None:
        CamImageVisual.__init__(self, line_width, center_rad, draw_center, filter_boxes, draw_info, colors, info_colors)
        VideoGenerator.__init__(self, backend_solver="ffmpeg")
        self.save_path = save_path

    def generate_video(self, img_dir: _StrLike, fps: _AnyT, size: _UnlimIter = None, encode: _AnyT = None, pixel_fmt: _AnyT = "yuv420p"):
        return super().generate_video(img_dir, self.save_path, fps, size, encode, pixel_fmt)


class BEVVisualizer(BEVImageVisual, VideoGenerator):
    def __init__(self, save_path: _StrLike, canvas_size: _Tup, bev_range: _Tup, self_size: _Tup = None, linewidth: _AnyT = None, cmap: _AnyT = None) -> None:
        if bev_range is None:
            bev_range = ((-5, 105), (-36, 36))

        BEVImageVisual.__init__(self, canvas_size, bev_range, self_size, linewidth, cmap)
        VideoGenerator.__init__(self, backend_solver="ffmpeg")

        self.save_path = save_path

    def generate_video(self, img_dir: _StrLike, fps: _AnyT, size: _UnlimIter = None, encode: _AnyT = None, pixel_fmt: _AnyT = "yuv420p"):
        return super().generate_video(img_dir, self.save_path, fps, size, encode, pixel_fmt)
    

class BEVCamVisualizer(CustomVisual, VideoGenerator):
    def __init__(self, video_fp: _StrLike, img_fp: _StrLike = None, canvas_size: _Tup = None, bev_range: _Tup[_UnlimTup] = None, 
                 cam_lw: int = 1, cam_cs: int = 2, draw_center: bool = False, ego_size: _Tup = None, bev_lw: _AnyT = None, cmap: _AnyT = None) -> None:
        CustomVisual.__init__(self)
        VideoGenerator.__init__(self, backend_solver="ffmpeg")

        self._vfp = video_fp
        self._ifp = "./temp_res/" if img_fp is None else img_fp
        self._cam_fp, self._bev_fp = [os.path.join(self._ifp, _p) for _p in ["camera_imgs", "bev_imgs"]]
        self._concat_fp = os.path.join(self._ifp, "concat_imgs")

        if not os.path.exists(self._ifp):
            os.mkdir(self._ifp)

        for _dir in [self._cam_fp, self._bev_fp, self._concat_fp]:
            if os.path.exists(_dir):
                shutil.rmtree(_dir)
            os.mkdir(_dir)
        
        canvas_size = (1000, 600) if canvas_size is None else canvas_size
        bev_range = ((-5, 105), (-36, 36)) if bev_range is None else bev_range
        self.__camvis: CamImageVisual = CamImageVisual(cam_lw, cam_cs, draw_center, colors=cmap)
        self.__bevvis: BEVImageVisual = BEVImageVisual(canvas_size, bev_range, ego_size, bev_lw, cmap)

    def load_info(self, refined_gt: _Dict):
        super().load_info(refined_gt)
        self.__camvis.load_info(refined_gt)
        self.__bevvis.load_info(refined_gt)
        return self

    def draw_all(self, subsample: bool = True):
        self.__camvis.draw_all(self._cam_fp, False, "vertical")
        self.__bevvis.set_colormap(self.__camvis.colormap_, True)
        self.__bevvis.draw_all(self._bev_fp, False, 100)

        _cam_names, _bev_names = self._sort_by_ts(*[os.listdir(_dir) for _dir in [self._cam_fp, self._bev_fp]], 
                                                  key=lambda x: x.split(".")[0])
        assert len(_cam_names) == len(_bev_names)

        pbar = tqdm(range(len(_cam_names)), ncols=90, colour='red')
        for index in pbar:
            _cam, _bev = _cam_names[index], _bev_names[index]
            pbar.set_description(f"Stacking {_cam}")

            _stack = self.stack_imgs_horizontal(
                os.path.join(self._cam_fp, _cam),
                os.path.join(self._bev_fp, _bev),
                subsample=subsample
            )
            _stack.save(os.path.join(self._concat_fp, _cam))

            if index == len(_cam_names) - 1:
                pbar.set_description(f"Finished.")

        return self

    def generate_video(self, fps: _AnyT, size: _UnlimIter = None, encode: _AnyT = None, pixel_fmt: _AnyT = "yuv420p"):
        return super().generate_video(self._concat_fp, self._vfp, fps, size, encode, pixel_fmt)
    
    def stack_imgs_horizontal(self, *imgs: _StrLi, subsample: bool = False):
        pil_imgs = [Image.open(path) for path in imgs]

        __u = lambda x: min(*x) if subsample else max(*x)
        target_height = __u([img.height for img in pil_imgs])
        __c = lambda x: np.greater(x, target_height) if subsample else np.less(x, target_height)
        widths = []

        for index, _img in enumerate(pil_imgs):
            _inter_width = _img.width
            if __c(_img.height):
                _inter_width = int(target_height / _img.height * _img.width)
                pil_imgs[index] = _img.resize((_inter_width, target_height), 
                            Image.Resampling.BILINEAR)
            
            widths.append(_inter_width)

        _stacked = Image.new("RGB", tuple([self._make_even(_n) for _n in [sum(widths), target_height]]))
        widths = [0] + widths[:-1]
        for _w, _img in zip(widths, pil_imgs):
            _stacked.paste(_img, (_w, 0))

        return _stacked
    
    @staticmethod
    def _sort_by_ts(*__iter: _Iter, key = None):
        _res = [sorted(_i, key=key) for _i in __iter]

        return _res[0] if len(__iter) == 1 else _res
    
    @staticmethod
    def _make_even(_num: _IntLike) -> _IntLike:
        return _num if _num % 2 == 0 else _num + 1
