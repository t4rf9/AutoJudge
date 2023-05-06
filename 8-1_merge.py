from argparse import ArgumentParser
from typing import Tuple, List
import random

from problem import Problem
from utils import re_int


class Merge(Problem):
    def __init__(
        self,
        assignment_path: str = "Assignment 8",
        student_path: str = None,
        excluded_students: List[str] = [],
        checkpoints_number: int = 10,
        generate_checkpoints: bool = True,
        compile: bool = True,
        run_checkpoints: bool = True,
        judge: bool = True,
        checkpoint_timeout: float = 2,
    ):
        super().__init__(
            assignment_path,
            problem_name="merge",
            student_path=student_path,
            excluded_students=excluded_students,
            checkpoints_number=checkpoints_number,
            generate_checkpoints=generate_checkpoints,
            compile=compile,
            run_checkpoints=run_checkpoints,
            judge=judge,
            checkpoint_timeout=checkpoint_timeout,
        )

    def _generate_input(self, index) -> str:
        if index == 0:
            n, m = 1, 1
        else:
            n = random.randint(1, 100)
            m = random.randint(1, 100)

        s = f"{n} {m}\n"

        a = [random.randint(-100, 100) for _ in range(n)]
        a.sort()
        b = [random.randint(-100, 100) for _ in range(m)]
        b.sort()

        s += " ".join([str(i) for i in a]) + "\n"
        s += " ".join([str(i) for i in b]) + "\n"

        return s

    def _compute(self, input_content: str) -> str:
        l, a, b = input_content.splitlines()

        n, m = [int(i) for i in l.split()]

        a = [int(i) for i in a.split()]
        b = [int(i) for i in b.split()]

        c = []

        # merge a, b to c
        i, j = 0, 0
        while i < n and j < m:
            if a[i] < b[j]:
                c.append(a[i])
                i += 1
            else:
                c.append(b[j])
                j += 1
        while i < n:
            c.append(a[i])
            i += 1
        while j < m:
            c.append(b[j])
            j += 1

        return " ".join([str(i) for i in c]) + "\n"

    def _judge_1_checkpoint(
        self, output_file_name, answer_file_name
    ) -> Tuple[int, int]:
        with open(answer_file_name, "r") as f_ans:
            answer_lines = f_ans.readlines()
        answers = [int(i) for i in answer_lines[0].split()]

        with open(output_file_name, "r") as f_out:
            output_lines = f_out.readlines()
        if len(output_lines) == 0:
            return 0, 1

        outputs = []
        for line in output_lines:
            line = line.strip()
            if line.startswith("#") or len(line) == 0:
                continue

            outputs += re_int.findall(line)

        if len(outputs) != len(answers):
            return 0, 1

        for output, answer in zip(outputs, answers):
            if int(output) != answer:
                return 0, 1

        return 1, 1


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-s", "--student_path", type=str, default=None)
    parser.add_argument("-e", "--exclude_students", type=str, default=[], nargs="*")
    parser.add_argument("-g", "--generate_checkpoints", action="store_true")
    parser.add_argument("-c", "--compile", action="store_true")
    parser.add_argument("-r", "--run_checkpoints", action="store_true")
    parser.add_argument("-j", "--judge", action="store_true")
    args = parser.parse_args()

    random.seed(203)

    Merge(
        student_path=args.student_path,
        excluded_students=args.exclude_students,
        generate_checkpoints=args.generate_checkpoints,
        compile=args.compile,
        run_checkpoints=args.run_checkpoints,
        judge=args.judge,
    )
