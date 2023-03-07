import random
import math
from argparse import ArgumentParser

from problem import Problem
from utils import re_float_fixed


class TriangularPrism(Problem):
    def __init__(
        self,
        assignment_path: str = "Assignment 1",
        checkpoints_number: int = 20,
        generate_checkpoints: bool = True,
        compile: bool = True,
        run_checkpoints: bool = True,
        judge: bool = True,
    ):
        super().__init__(
            assignment_path,
            problem_name="2",  # name of source file: 2.cpp
            checkpoints_number=checkpoints_number,
            generate_checkpoints=generate_checkpoints,
            compile=compile,
            run_checkpoints=run_checkpoints,
            judge=judge,
        )

    def _generate_input(self) -> str:
        a = random.randint(0, 100000) / 1000
        h = random.randint(0, 100000) / 1000

        input_content = f"{a} {h}\n"

        return input_content

    def _compute(self, input_content: str) -> str:
        input_tokens = input_content.split()
        a, h = [float(token) for token in input_tokens]

        surface_area = a * h + math.sqrt(3) * a**2 / 2
        volume = math.sqrt(3) * h * a**2 / 4

        res = f"{surface_area:.3f} {volume:.3f}\n"

        return res

    def _judge_1_checkpoint(self, output_file_name, answer_file_name) -> bool:
        with open(answer_file_name, "r") as f_ans:
            standard_answers = []
            for line in f_ans.readline():
                standard_answers.extend(re_float_fixed.findall(line))

        with open(output_file_name, "r") as f_out:
            answers = []
            for line in f_out.readline():
                answers.extend(re_float_fixed.findall(line))
        for standard_answer, answer in zip(standard_answers, answers):
            if standard_answer != answer:
                return False
        return True


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-g", "--generate_checkpoints", action="store_true")
    parser.add_argument("-c", "--compile", action="store_true")
    parser.add_argument("-r", "--run_checkpoints", action="store_true")
    parser.add_argument("-j", "--judge", action="store_true")
    args = parser.parse_args()

    triangular_prism = TriangularPrism(
        generate_checkpoints=args.generate_checkpoints,
        compile=args.compile,
        run_checkpoints=args.run_checkpoints,
        judge=args.judge,
    )
