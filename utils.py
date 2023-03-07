import os
from concurrent.futures import ProcessPoolExecutor
import re
from typing import Dict, Tuple
from functools import partial


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
