# coding: utf-8


import os
import sys
import subprocess
import datetime
import random
import string


def generate_rnd_str(length=20) -> str:
    characters = string.ascii_letters + string.digits
    random_string = "".join(random.choice(characters) for _ in range(length))
    return random_string


def get_time_str() -> str:
    time_str = datetime.datetime.now().strftime("%y_%m_%d_%H_%M_%S_%f")
    return time_str


def generage_file_name(extension: str = "") -> str:
    res = os.path.join("/", "tmp")
    if extension == "":
        res_name = f"{get_time_str}_{generate_rnd_str}"
    else:
        res_name = f"{get_time_str()}_{generate_rnd_str()}.{extension}"
    res = os.path.join(res, res_name)
    return res


def make_another_extenrion(path: str, new_extension: str) -> str:
    base = os.path.splitext(path)[0]
    return f"{base}.{new_extension}"


def exe(command: str, debug: bool = True, std_out_fd=subprocess.PIPE, std_err_fd=subprocess.PIPE,
        stdin_msg: str = None) -> tuple:
    '''
    Аргумент command - команда для выполнения в терминале. Например: "ls -lai ."
    if(std_out_fd or std_err_fd) == subprocess.DEVNULL   |=>    No output enywhere
    if(std_out_fd or std_err_fd) == subprocess.PIPE      |=>    All output to return
    if(std_out_fd or std_err_fd) == open(path, "w")      |=>    All output to file path
    Возвращает кортеж, где элементы:
        0 - строка stdout
        1 - строка stderr
        2 - returncode
    '''
    _ENCODING = "utf-8"

    if debug:
        # pout(f"> " + " ".join(command))
        if (stdin_msg != None):
            print(f"> {command}, with stdin=\"{stdin_msg}\"")
        else:
            print(f"> {command}")

    # proc = subprocess.run(command, shell=True, capture_output=True, input=stdin_msg.encode("utf-8"))
    if stdin_msg is None:
        proc = subprocess.run(command, shell=True, stdout=std_out_fd, stderr=std_err_fd)
    else:
        proc = subprocess.run(command, shell=True, stdout=std_out_fd, stderr=std_err_fd,
                              input=stdin_msg.encode("utf-8"))

    # return (proc.stdout.decode("utf-8"), proc.stderr.decode("utf-8"))

    res_stdout = proc.stdout.decode("utf-8") if proc.stdout != None else None
    res_errout = proc.stderr.decode("utf-8") if proc.stderr != None else None

    return (res_stdout, res_errout, proc.returncode)
