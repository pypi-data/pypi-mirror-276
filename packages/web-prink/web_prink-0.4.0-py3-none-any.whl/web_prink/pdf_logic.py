# coding: utf-8

import os
from pypdf import PdfReader
from pypdf.errors import PdfReadError

from . import GL, exe, get_time_str


def is_pdf(pdf_path: str) -> bool:
    try:
        PdfReader(pdf_path)
    except PdfReadError:
        return False
    else:
        return True


def calc_pdf_pages(pdf_path: str) -> int:
    reader = PdfReader(pdf_path)
    return len(reader.pages)


def print_pdf(pdf_path: str) -> str:
    if not is_pdf(pdf_path):
        return f"\"{os.path.basename(pdf_path)}\" is not pdf file. "
    pdf_pages_num = calc_pdf_pages(pdf_path)
    if GL.overheat_pages_num is not None and pdf_pages_num > GL.overheat_pages_num:
        return (f"Please make less pages, then {GL.overheat_pages_num} (current={pdf_pages_num}). "
                f"Otherwise the printer will overheat. "
                f"Before printing again, wait 5 minutes to allow the oven to cool down.")
    res_of_exe = exe(GL.print_command_raw.replace("{print_file}", f"\"{pdf_path}\""))
    print(res_of_exe)
    if res_of_exe[2] != 0:
        return f"Error: {res_of_exe}"
    else:
        return "Wait until printing will be finished."
