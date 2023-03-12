import random
from argparse import ArgumentParser
from typing import Tuple

from problem import Problem
from utils import re_float_fixed


class Maximum(Problem):
    def __init__(
        self,
        assignment_path: str = "Assignment 2",
        student_path: str = None,
        checkpoints_number: int = 20,
        generate_checkpoints: bool = True,
        compile: bool = True,
        run_checkpoints: bool = True,
        judge: bool = True,
    ):
        super().__init__(
            assignment_path,
            problem_name="maximum",
            student_path=student_path,
            checkpoints_number=checkpoints_number,
            generate_checkpoints=generate_checkpoints,
            compile=compile,
            run_checkpoints=run_checkpoints,
            judge=judge,
        )

    def _generate_input(self, index) -> str:
        if index == 0:
            return "0 0 0 0\n"

        a = random.randint(-1000000, 1000000) / 1000
        b = random.randint(-1000000, 1000000) / 1000
        c = random.randint(-1000000, 1000000) / 1000
        d = random.randint(-1000000, 1000000) / 1000
        if index == 1:
            return f"{a} {b} {c} {a}\n"
        if index == 2:
            return f"{a} {b} {c} -1000.1\n"
        return f"{a} {b} {c} {d}\n"

    def _compute(self, input_content: str) -> str:
        input_tokens = input_content.split()
        a, b, c, d = [float(token) for token in input_tokens]

        if a == b == c == d == 0:
            return "Exit"
        if a == b or a == c or a == d or b == c or b == d or c == d:
            return "Error:Equal"

        res = max(a, b, c, d)
        if res > 1000 or min(a, b, c, d) < -1000:
            return "Error:Out of Range"

        return str(res)

    def _judge_1_checkpoint(
        self, output_file_name, answer_file_name
    ) -> Tuple[int, int]:
        with open(answer_file_name, "r") as f_ans:
            standard_answers = []
            for line in f_ans.readlines():
                line = line.strip()
                if len(line) > 0:
                    standard_answers.append(line)

        with open(output_file_name, "r") as f_out:
            answers = []
            for line in f_out.readlines():
                line = line.strip()
                if len(line) == 0 or line[0] == "#":
                    continue
                answers.append(line)

        correct, total = 0, len(standard_answers)
        for standard_answer, answer in zip(standard_answers, answers):
            try:
                standard_answer = float(standard_answer)
                try:
                    answer = float(answer)
                except ValueError:
                    continue
                if abs(answer - standard_answer) < 1e-6 * abs(standard_answer):
                    correct += 1
            except ValueError:
                if standard_answer == answer:
                    correct += 1

        return correct, total


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-s", "--student_path", type=str, default=None)
    parser.add_argument("-g", "--generate_checkpoints", action="store_true")
    parser.add_argument("-c", "--compile", action="store_true")
    parser.add_argument("-r", "--run_checkpoints", action="store_true")
    parser.add_argument("-j", "--judge", action="store_true")
    args = parser.parse_args()

    maximum = Maximum(
        student_path=args.student_path,
        generate_checkpoints=args.generate_checkpoints,
        compile=args.compile,
        run_checkpoints=args.run_checkpoints,
        judge=args.judge,
    )
