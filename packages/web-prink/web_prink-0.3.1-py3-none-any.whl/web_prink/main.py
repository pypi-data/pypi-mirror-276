# coding: utf-8

# https://proglib.io/p/rukovodstvo-po-rabote-s-gradio-sozdanie-veb-interfeysa-dlya-modeley-mashinnogo-obucheniya-2023-03-06

import json
import os
import sys

base_dir = os.path.dirname(__file__)
sys.path.insert(0, base_dir)

import time
import json
import gradio as gr

from . import __version__
from . import GL
from . import print_pdf
from . import scan_file


def print_pdf_main(input_file):
    print(f"Will be printed \"{input_file.name}\". ")
    res = print_pdf(input_file.name)
    return res


def scan_file_main(format_text: str, resolution: str):
    res_file = scan_file(int(resolution), format_text)
    return res_file


def parse_commands():
    json_path = os.path.join(GL.root_path, "execs.json")
    with open(json_path, "r", encoding="utf-8") as fd:
        s = fd.read()
    d = json.loads(s)
    GL.print_command_raw = d["print_command"]
    GL.scan_command_raw = d["scan_command"]
    if GL.print_command_raw == "" or GL.scan_command_raw == "":
        print(f"Please define files in file \"{json_path}\". ")
        exit(1)


def main():
    print("\n\n\tDont forget run it as root, if needed.\n")
    time.sleep(3.0)

    GL.root_path = os.path.dirname(__file__)

    parse_commands()

    with gr.Blocks() as demo:

        with gr.Tab("Print"):
            input1 = gr.File(label="Choose pdf")
            output1 = gr.Textbox(label="Output")
            submit1 = gr.Button("Print pdf")
            submit1.click(print_pdf_main, inputs=[input1], outputs=[output1])

        with gr.Tab("Scan"):
            input2_1 = gr.Radio(["tiff", "png", "pdf"], label="Output format")
            input2_2 = gr.Radio(["200", "100", "500", "1000"], label="Resolution")
            output2 = gr.File(label="Download scanned file. ")
            submit2 = gr.Button("Scan")
            submit2.click(scan_file_main, inputs=[input2_1, input2_2], outputs=[output2])

    demo.launch()

