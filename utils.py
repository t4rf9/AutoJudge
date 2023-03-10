import os
from concurrent.futures import ProcessPoolExecutor
import re
from typing import Dict, Tuple
from functools import partial


def switch_encoding(file_path):
    with open(file_path, "rb") as f:
        lines_bytes = f.readlines()

    lines_bytes = [
        line_bytes.expandtabs(4).replace(b"\r\n", b"\n").replace(b"scanf_s", b"scanf")
        for line_bytes in lines_bytes
    ]

    try:
        lines = [line_bytes.decode("utf-8") for line_bytes in lines_bytes]
        # print(f"{file_path}: utf-8")
    except UnicodeDecodeError as err:
        lines = [line_bytes.decode("gb18030") for line_bytes in lines_bytes]
        # print(f"{file_path}: gb18030")

    with open(file_path, "w") as f:
        f.writelines(lines)


def for_each_student(assignment_path: str, f) -> Dict[str, Tuple[int, int]]:
    students = os.listdir(assignment_path)
    res = {}
    executor = ProcessPoolExecutor()
    for student in students:
        if student[:2] != "20":
            continue
        student_path = os.path.join(assignment_path, student)

        future = executor.submit(f, student_path)

        res[student] = future.result()

    return res


def _visit_student(f, student_path: str):
    res = []
    source_files = os.listdir(student_path)
    for source_file_name in source_files:
        if source_file_name == ".DS_Store":
            continue
        file_path = os.path.join(student_path, source_file_name)

        res.append(f(file_path))
    return res


def for_each_source_file(assignment_path: str, f) -> Dict[str, Tuple[int, int]]:
    return for_each_student(assignment_path, partial(_visit_student, f))


re_int = re.compile(r"[\+-]?\d+")
re_float_fixed = re.compile(r"[\+-]?\d+\.\d*")
