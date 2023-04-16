from argparse import ArgumentParser
from typing import Tuple, List
import random

from problem import Problem
from utils import re_int

F = [1, 2]
G = [0, 1]

P = 10000019


def f(n):
    l = len(F)
    if n < l:
        return F[n]
    for i in range(l, n + 1):
        F.append((2 * F[i - 1] + F[i - 2]) % P)
    return F[n]


def g(n):
    l = len(G)
    if n < l:
        return G[n]
    for i in range(l, n + 1):
        G.append((G[i - 1] + 2 * G[i - 2]) % P)
    return G[n]


class Array(Problem):
    def __init__(
        self,
        assignment_path: str = "Assignment 6",
        student_path: str = None,
        excluded_students: List[str] = [],
        checkpoints_number: int = 8,
        generate_checkpoints: bool = True,
        compile: bool = True,
        run_checkpoints: bool = True,
        judge: bool = True,
        checkpoint_timeout: float = 2,
    ):
        super().__init__(
            assignment_path,
            problem_name="array",
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
            res = 0
        elif index == 1:
            res = 1
        elif index == 2:
            res = 2
        else:
            res = random.randint(2 ** (index - 1), 2**index)
        return f"{res}\n"

    def _compute(self, input_content: str) -> str:
        n = int(input_content.strip())
        return f"{f(n)} {g(n)}\n"

    def _judge_1_checkpoint(
        self, output_file_name, answer_file_name
    ) -> Tuple[int, int]:
        with open(answer_file_name, "r") as f_ans:
            answer_lines = f_ans.readlines()
        answers = []
        for line in answer_lines:
            line = line.strip()
            if len(line) > 0:
                answers.extend(re_int.findall(line))

        with open(output_file_name, "r") as f_out:
            output_lines = f_out.readlines()
        outputs = []
        for line in output_lines:
            line = line.strip()
            if len(line) > 0 and not line.startswith("#"):
                outputs.extend(re_int.findall(line))

        correct, total = 0, 2

        if len(outputs) != len(answers):
            return 0, 2

        for output, answer in zip(outputs, answers):
            if int(output) == int(answer):
                correct += 1

        return correct, total


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

    array = Array(
        student_path=args.student_path,
        excluded_students=args.exclude_students,
        generate_checkpoints=args.generate_checkpoints,
        compile=args.compile,
        run_checkpoints=args.run_checkpoints,
        judge=args.judge,
    )
