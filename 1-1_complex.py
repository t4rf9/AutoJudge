import random
from argparse import ArgumentParser
from typing import Tuple, List

from problem import Problem
from utils import re_float_fixed


class Complex(Problem):
    def __init__(
        self,
        assignment_path: str = "Assignment 1",
        student_path: str = None,
        excluded_students: List[str] = [],
        checkpoints_number: int = 20,
        generate_checkpoints: bool = True,
        compile: bool = True,
        run_checkpoints: bool = True,
        judge: bool = True,
    ):
        super().__init__(
            assignment_path,
            problem_name="1",
            student_path=student_path,
            excluded_students=excluded_students,
            checkpoints_number=checkpoints_number,
            generate_checkpoints=generate_checkpoints,
            compile=compile,
            run_checkpoints=run_checkpoints,
            judge=judge,
        )

    def _generate_input(self, index) -> str:
        r1 = random.randint(-100000, 100000) / 1000
        i1 = random.randint(-100000, 100000) / 1000
        r2 = random.randint(-100000, 100000) / 1000
        i2 = random.randint(-100000, 100000) / 1000

        input_content = f"{r1} {i1}\n"
        input_content += f"{r2} {i2}\n"

        return input_content

    def _compute(self, input_content: str) -> str:
        input_tokens = input_content.split()
        r1, i1, r2, i2 = [float(token) for token in input_tokens]

        res = f"{r1 + r2:.3f} {i1 + i2:.3f}\n"
        res += f"{r1 - r2:.3f} {i1 - i2:.3f}\n"
        res += f"{r1 * r2 - i1 * i2:.3f} {r1 * i2 + r2 * i1:.3f}\n"
        res += f"{(r1 * r2 + i1 * i2) / (r2**2  + i2**2):.3f} {(i1 * r2 - i2 * r1) / (r2**2  + i2**2):.3f}\n"

        return res

    def _judge_1_checkpoint(
        self, output_file_name, answer_file_name
    ) -> Tuple[int, int]:
        with open(answer_file_name, "r") as f_ans:
            standard_answers = []
            for line in f_ans.readlines():
                standard_answers.extend(re_float_fixed.findall(line))

        with open(output_file_name, "r") as f_out:
            answers = []
            for line in f_out.readlines():
                answers.extend(re_float_fixed.findall(line))

        correct, total = 0, len(standard_answers)
        for standard_answer, answer in zip(standard_answers, answers):
            standard_answer = float(standard_answer)
            answer = float(answer)
            if abs(answer - standard_answer) < 1e-6 * abs(standard_answer):
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

    complex = Complex(
        student_path=args.student_path,
        excluded_students=args.exclude_students,
        generate_checkpoints=args.generate_checkpoints,
        compile=args.compile,
        run_checkpoints=args.run_checkpoints,
        judge=args.judge,
    )
