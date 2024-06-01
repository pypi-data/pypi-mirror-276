# coding: utf-8

import os

from . import exe, GL, make_another_extenrion, generage_file_name


def scan_file(resolution: int, format_: str, crop: str) -> str or None:
    out_path = generage_file_name(format_)
    tiff_file = make_another_extenrion(out_path, "tiff")
    command = (GL.scan_command_raw.replace("{resolution}", f"{resolution}").replace("{format}", f"tiff")
               .replace("{output_file}", f"\"{tiff_file}\""))
    if crop == "A4":
        command = f"{command} -x 210 -y 297"

    res_of_exe = exe(command)
    print(res_of_exe)

    if format_ == "tiff":
        return tiff_file
    elif format_ == "png" or format_ == "pdf":
        res_of_exe = exe(f"convert \"{tiff_file}\" \"{out_path}\"")
        print(res_of_exe)
        return out_path
    else:
        print("Failed successfully (scan_file). ")
        return None
