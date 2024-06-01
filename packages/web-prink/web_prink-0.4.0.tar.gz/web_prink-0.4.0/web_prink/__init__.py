# coding: utf-8


class GL:
    print_command_raw = None
    scan_command_raw = None
    root_path = None
    overheat_pages_num = 25


from .__version__ import __version__
from .sup import *
from .pdf_logic import *
from .scan_logic import *
from .main import main


__all__ = [__version__, main, GL,
           print_pdf,
           scan_file,
           get_time_str, exe, generage_file_name, make_another_extenrion]
