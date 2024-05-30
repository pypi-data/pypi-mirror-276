import os
from typing import Union, Optional
import subprocess
from simba.utils.read_write import get_fn_ext, get_video_meta_data

import threading
import functools
import glob
import multiprocessing
import os
import platform
import shutil
import subprocess
import time
from copy import deepcopy
from datetime import datetime
from tkinter import *
from typing import Any, Dict, List, Optional, Tuple, Union

import cv2
import numpy as np
from PIL import Image, ImageTk
from shapely.geometry import Polygon

try:
    from typing import Literal
except:
    from typing_extensions import Literal

from simba.mixins.config_reader import ConfigReader
from simba.mixins.image_mixin import ImageMixin
from simba.utils.checks import (check_ffmpeg_available,
                                check_file_exist_and_readable, check_float,
                                check_if_dir_exists,
                                check_if_filepath_list_is_empty,
                                check_if_string_value_is_valid_video_timestamp,
                                check_instance, check_int,
                                check_nvidea_gpu_available, check_str,
                                check_that_hhmmss_start_is_before_end,
                                check_valid_lst, check_valid_tuple)
from simba.utils.data import find_frame_numbers_from_time_stamp
from simba.utils.enums import OS, ConfigKey, Formats, Options, Paths
from simba.utils.errors import (CountError, DirectoryExistError,
                                FFMPEGCodecGPUError, FFMPEGNotFoundError,
                                FileExistError, FrameRangeError,
                                InvalidFileTypeError, InvalidInputError,
                                InvalidVideoFileError, NoDataError,
                                NoFilesFoundError, NotDirectoryError)
from simba.utils.lookups import (get_ffmpeg_crossfade_methods, get_fonts,
                                 percent_to_crf_lookup, percent_to_qv_lk)
from simba.utils.printing import SimbaTimer, stdout_success
from simba.utils.read_write import (
    check_if_hhmmss_timestamp_is_valid_part_of_video,
    concatenate_videos_in_folder, find_all_videos_in_directory, find_core_cnt,
    find_files_of_filetypes_in_directory, get_fn_ext, get_video_meta_data,
    read_config_entry, read_config_file, read_frm_of_video)
from simba.utils.warnings import (FileExistWarning, InValidUserInputWarning,
                                  SameInputAndOutputWarning, FrameRangeWarning, ResolutionWarning)
from simba.video_processors.extract_frames import video_to_frames
from simba.video_processors.roi_selector import ROISelector
from simba.video_processors.roi_selector_circle import ROISelectorCircle
from simba.video_processors.roi_selector_polygon import ROISelectorPolygon

from tkinter import *
from typing import Optional, Union

import numpy as np
from PIL import Image, ImageTk

import simba
from simba.labelling.extract_labelled_frames import AnnotationFrameExtractor
from simba.mixins.config_reader import ConfigReader
from simba.mixins.pop_up_mixin import PopUpMixin
from simba.plotting.frame_mergerer_ffmpeg import FrameMergererFFmpeg
from simba.ui.tkinter_functions import (CreateLabelFrameWithIcon,
                                        CreateToolTip, DropDownMenu, Entry_Box,
                                        FileSelect, FolderSelect)
from simba.utils.checks import (check_ffmpeg_available,
                                check_file_exist_and_readable,
                                check_if_dir_exists,
                                check_if_filepath_list_is_empty,
                                check_if_string_value_is_valid_video_timestamp,
                                check_int, check_nvidea_gpu_available,
                                check_str,
                                check_that_hhmmss_start_is_before_end)
from simba.utils.data import convert_roi_definitions
from simba.utils.enums import Dtypes, Formats, Keys, Links, Options, Paths
from simba.utils.errors import (CountError, DuplicationError, FrameRangeError,
                                InvalidInputError, MixedMosaicError,
                                NoChoosenClassifierError, NoFilesFoundError,
                                NotDirectoryError, ResolutionError)
from simba.utils.lookups import get_color_dict, get_fonts
from simba.utils.printing import SimbaTimer, stdout_success
from simba.utils.read_write import (
    check_if_hhmmss_timestamp_is_valid_part_of_video,
    concatenate_videos_in_folder, find_all_videos_in_directory,
    find_files_of_filetypes_in_directory, get_fn_ext, get_video_meta_data,
    seconds_to_timestamp, str_2_bool)
from simba.video_processors.brightness_contrast_ui import \
    brightness_contrast_ui
from simba.video_processors.clahe_ui import interactive_clahe_ui
from simba.video_processors.extract_seqframes import extract_seq_frames
from simba.video_processors.multi_cropper import MultiCropper
from simba.video_processors.px_to_mm import get_coordinates_nilsson
from simba.video_processors.video_processing import (
    VideoRotator, batch_convert_video_format, batch_create_frames,
    batch_video_to_greyscale, change_fps_of_multiple_videos, change_img_format,
    change_single_video_fps, clahe_enhance_video, clip_video_in_range,
    clip_videos_by_frame_ids, convert_to_avi, convert_to_bmp, convert_to_jpeg,
    convert_to_mov, convert_to_mp4, convert_to_png, convert_to_tiff,
    convert_to_webm, convert_to_webp,
    convert_video_powerpoint_compatible_format, copy_img_folder,
    crop_multiple_videos, crop_multiple_videos_circles,
    crop_multiple_videos_polygons, crop_single_video, crop_single_video_circle,
    crop_single_video_polygon, downsample_video, extract_frame_range,
    extract_frames_single_video, frames_to_movie, gif_creator,
    multi_split_video, remove_beginning_of_video, resize_videos_by_height,
    resize_videos_by_width, roi_blurbox, superimpose_elapsed_time,
    superimpose_frame_count, superimpose_freetext, superimpose_overlay_video,
    superimpose_video_names, superimpose_video_progressbar,
    video_bg_substraction_mp, video_bg_subtraction, video_concatenator,
    video_to_greyscale, watermark_video, rotate_video, flip_videos, create_average_frm)


class CreateAverageFramePopUp(PopUpMixin):
    def __init__(self):
        PopUpMixin.__init__(self, title="CREATE AVERAGE VIDEO FRAME")
        settings_frm = CreateLabelFrameWithIcon(parent=self.main_frm, header="SETTINGS", icon_name=Keys.DOCUMENTATION.value, icon_link=Links.VIDEO_TOOLS.value)
        self.save_dir = FolderSelect(settings_frm, "AVERAGE FRAME SAVE DIRECTORY:", title="Select a video directory", lblwidth=25)
        self.section_start_time_eb = Entry_Box(settings_frm, "START TIME:", "25")
        self.section_end_time_eb = Entry_Box(settings_frm, "END TIME:", "25")
        self.section_start_time_eb.entry_set('00:00:00')
        self.section_end_time_eb.entry_set('00:00:00')

        settings_frm.grid(row=0, column=0, sticky=NW, pady=10)
        self.save_dir.grid(row=0, column=0, sticky=NW)
        self.section_start_time_eb.grid(row=1, column=0, sticky=NW)
        self.section_end_time_eb.grid(row=2, column=0, sticky=NW)

        single_video_frm = CreateLabelFrameWithIcon(parent=self.main_frm, header="SINGLE VIDEO - CREATE AVERAGE FRAME", icon_name=Keys.DOCUMENTATION.value, icon_link=Links.VIDEO_TOOLS.value)
        self.selected_video = FileSelect(single_video_frm, "VIDEO PATH:", title="Select a video file", lblwidth=25, file_types=[("VIDEO FILE", Options.ALL_VIDEO_FORMAT_STR_OPTIONS.value)])
        single_video_run = Button(single_video_frm, text="RUN - SINGLE VIDEO", command=lambda: self.run(multiple=False))

        single_video_frm.grid(row=1, column=0, sticky="NW")
        self.selected_video.grid(row=0, column=0, sticky="NW")
        single_video_run.grid(row=1, column=0, sticky="NW")

        multiple_videos_frm = CreateLabelFrameWithIcon(parent=self.main_frm, header="MULTIPLE VIDEOS - CREATE AVERAGE FRAMES", icon_name=Keys.DOCUMENTATION.value, icon_link=Links.VIDEO_TOOLS.value)
        self.selected_video_dir = FolderSelect(multiple_videos_frm, "VIDEO DIRECTORY PATH:", title="Select a video directory", lblwidth=25)
        multiple_videos_run = Button(multiple_videos_frm, text="RUN - MULTIPLE VIDEOS", command=lambda: self.run(multiple=True))

        multiple_videos_frm.grid(row=2, column=0, sticky="NW")
        self.selected_video_dir.grid(row=0, column=0, sticky="NW")
        multiple_videos_run.grid(row=1, column=0, sticky="NW")
        self.main_frm.mainloop()

    def run(self, multiple: bool):
        start_time = self.section_start_time_eb.entry_get.strip()
        end_time = self.section_end_time_eb.entry_get.strip()
        save_dir = self.save_dir.folder_path
        check_if_dir_exists(in_dir=save_dir)
        if (start_time != '' and end_time == '') or (start_time == '' and end_time != ''):
            raise InvalidInputError(msg=f'Both start time and end time have to be either time-stamps or blank.', source=self.__class__.__name__)
        if start_time != '' and end_time != '':
            check_if_string_value_is_valid_video_timestamp(value=start_time, name='start_time')
            check_if_string_value_is_valid_video_timestamp(value=end_time, name='end_time')
            check_that_hhmmss_start_is_before_end(start_time=start_time, end_time=end_time, name=self.__class__.__name__)
        else:
            start_time, end_time = None, None
        if not multiple:
            data_path = self.selected_video.file_path
            check_file_exist_and_readable(file_path=data_path)
            data_path = [data_path]
        else:
            data_path = self.selected_video_dir.folder_path
            check_if_dir_exists(in_dir=data_path)
            data_path = list(find_all_videos_in_directory(directory=data_path, as_dict=True, raise_error=True).values())

        for video_cnt, video_path in enumerate(data_path):
            _, video_name, _ = get_fn_ext(filepath=video_path)
            save_path = os.path.join(save_dir, save_dir, f'{video_name}_avg_frm.png')
            _ = get_video_meta_data(video_path=video_path)
            if start_time != None and end_time != None:
                check_if_hhmmss_timestamp_is_valid_part_of_video(timestamp=start_time, video_path=video_path)
                check_if_hhmmss_timestamp_is_valid_part_of_video(timestamp=end_time, video_path=video_path)

            threading.Thread(target=create_average_frm(video_path=video_path,
                                                       start_time=start_time,
                                                       end_time=end_time,
                                                       save_path=save_path,
                                                       verbose=True)).start()

def temporal_concatenation(video_paths: List[Union[str, os.PathLike]],
                           save_path: Optional[Union[str, os.PathLike]] = None,
                           save_format: Optional[Literal['mp4', 'mov', 'avi', 'webm']] = 'mp4',
                           quality: Optional[int] = 60) -> None:

    """
    Concatenates multiple video files temporally into a single video.

    :param List[Union[str, os.PathLike]] video_paths: List of paths to video files to be temporally joined. The videos will be joined in the order appearance in the list.
    :param Optional[Union[str, os.PathLike]] save_path: The location where to save the temporally concatenated videos. If None, then the video is saved in the same directory as the first video in ``video_paths`` with the name ``temporal_concat_video``.
    :param Optional[Literal['mp4', 'mov', 'avi', 'webm']] save_format: The video format of the concatenated video. Default: ``mp4``.
    :param Optional[int] quality: Integer representing the quality: 10, 20, 30.. 100.
    :return: None
    """

    timer = SimbaTimer(start=True)
    check_valid_lst(data=video_paths, source=temporal_concatenation.__name__, valid_dtypes=(str,), min_len=2)
    check_str(name='save_format', value=save_format.lower(), options=('mp4', 'mov', 'avi', 'webm'))
    check_int(name='quality', value=quality, max_value=100, min_value=1)
    crf_lk = percent_to_crf_lookup()
    crf = crf_lk[str(quality)]
    meta = []
    for i in video_paths:
        check_file_exist_and_readable(file_path=i); video_meta = get_video_meta_data(video_path=i)
        meta.append(video_meta)
    fps, resolutions = [v['fps'] for v in meta], [v['resolution_str'] for v in meta]
    unique_fps, unique_res = list(set(fps)), list(set(resolutions))
    if len(unique_fps) > 1: raise ResolutionError(msg=f'The selected videos contain more than one unique FPS: {unique_fps}', source=temporal_concatenation.__name__)
    if len(unique_res) > 1: raise ResolutionError(msg=f'The selected videos contain more than one unique resolutions: {unique_res}', source=temporal_concatenation.__name__)
    if save_path is None:
        save_path = os.path.join(os.path.dirname(video_paths[0]), f'temporal_concat_video.{save_format}')
    else:
        check_if_dir_exists(in_dir=os.path.dirname(save_path))
    filter_complex = ""
    for i, path in enumerate(video_paths):
        filter_complex += f"[{i}:v]"
    filter_complex += f"concat=n={len(video_paths)}:v=1[v]"
    input_options = " ".join([f"-i \"{path}\"" for path in video_paths])
    cmd = f'ffmpeg {input_options} -filter_complex "{filter_complex}" -crf {crf} -map "[v]" "{save_path}" -hide_banner -loglevel error -stats -y'
    subprocess.call(cmd, shell=True)
    timer.stop_timer()
    stdout_success(msg=f'{len(video_paths)} videos temporally concatenated and saved at {save_path}', elapsed_time=timer.elapsed_time_str)

# temporal_concatenation(video_paths=['/Users/simon/Desktop/envs/simba/troubleshooting/RAT_NOR/project_folder/videos/2022-06-26_NOB_IOT_1.mp4',
#                                     '/Users/simon/Desktop/envs/simba/troubleshooting/RAT_NOR/project_folder/videos/2022-06-20_NOB_IOT_1.mp4'])
#

class ManualTemporalJoinPopUp(PopUpMixin):
    def __init__(self):
        PopUpMixin.__init__(self, title="MANUAL TEMPORAL JOIN")
        video_cnt_frm = CreateLabelFrameWithIcon(parent=self.main_frm, header="NUMBER OF VIDEOS TO JOIN", icon_name=Keys.DOCUMENTATION.value, icon_link=Links.VIDEO_TOOLS.value)
        self.video_cnt_dropdown = DropDownMenu(video_cnt_frm, "NUMBER OF VIDEOS:", list(range(2, 101, 1)), labelwidth=25)
        self.select_video_cnt_btn = Button(video_cnt_frm, text="SELECT", command=lambda: self.select())
        self.quality_dropdown = DropDownMenu(video_cnt_frm, "OUTPUT VIDEO QUALITY:", list(range(10, 110, 10)), labelwidth=25)
        self.quality_dropdown.setChoices(60)
        self.out_format_dropdown = DropDownMenu(video_cnt_frm, "OUTPUT VIDEO FORMAT:", Options.ALL_VIDEO_FORMAT_OPTIONS.value, labelwidth=25)
        self.out_format_dropdown.setChoices('.mp4')
        self.video_cnt_dropdown.setChoices(2)
        video_cnt_frm.grid(row=0, column=0, sticky=NW)
        self.video_cnt_dropdown.grid(row=0, column=0, sticky=NW)
        self.select_video_cnt_btn.grid(row=0, column=1, sticky=NW)
        self.quality_dropdown.grid(row=1, column=0, sticky=NW)
        self.out_format_dropdown.grid(row=2, column=0, sticky=NW)
        self.main_frm.mainloop()

    def select(self):
        video_cnt = int(self.video_cnt_dropdown.getChoices())
        if hasattr(self, 'video_paths_frm'):
            self.video_paths_frm.destroy()
            self.run_frm.destroy()
        self.video_paths_frm = CreateLabelFrameWithIcon(parent=self.main_frm, header="VIDEO PATHS", icon_name=Keys.DOCUMENTATION.value, icon_link=Links.VIDEO_TOOLS.value)
        self.video_paths_frm.grid(row=1, column=0, sticky=NW)
        self.video_paths = {}
        for video_cnt in range(video_cnt):
            self.video_paths[video_cnt] = FileSelect(self.video_paths_frm, f"VIDEO PATH {video_cnt+1}:", title="Select a video file", lblwidth=25, file_types=[("VIDEO FILE", Options.ALL_VIDEO_FORMAT_STR_OPTIONS.value)])
            self.video_paths[video_cnt].grid(row=video_cnt, column=0, sticky=NW)
        self.create_run_frm(run_function=self.run)

    def run(self):
        video_file_paths, meta = [], []
        for cnt, video_file_select in self.video_paths.items():
            video_path = video_file_select.file_path
            check_file_exist_and_readable(file_path=video_path)
            video_meta = get_video_meta_data(video_path=video_path)
            video_file_paths.append(video_path)
            meta.append(video_meta)
        fps, resolutions = [v['fps'] for v in meta], [v['resolution_str'] for v in meta]
        unique_fps, unique_res = list(set(fps)), list(set(resolutions))
        format = self.out_format_dropdown.getChoices()
        quality = self.quality_dropdown.getChoices()
        if len(unique_fps) > 1: raise ResolutionError(msg=f'The selected videos contain more than one unique FPS: {unique_fps}', source=self.__class__.__name__)
        if len(unique_res) > 1: raise ResolutionError(msg=f'The selected videos contain more than one unique resolutions: {unique_res}', source=self.__class__.__name__)
        threading.Thread(temporal_concatenation(video_paths=video_file_paths, save_format=format[1:], quality=quality)).start()

# ManualTemporalJoinPopUp()
        #self.save_dir = FolderSelect(settings_frm, "AVERAGE FRAME SAVE DIRECTORY:", title="Select a video directory", lblwidth=25)
        #self.section_start_time_eb = Entry_Box(settings_frm, "START TIME:", "25")





#CreateAverageFramePopUp()

