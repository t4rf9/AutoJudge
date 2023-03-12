import random
from argparse import ArgumentParser
from typing import Tuple

from problem import Problem
from utils import re_float_fixed


class Money(Problem):
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
            problem_name="money",
            student_path=student_path,
            checkpoints_number=checkpoints_number,
            generate_checkpoints=generate_checkpoints,
            compile=compile,
            run_checkpoints=run_checkpoints,
            judge=judge,
        )

    def _generate_input(self, index) -> str:
        if index == 0:
            n = random.randint(1, 5)
        elif index == 1:
            n = random.randint(6, 20)
        elif index == 2:
            n = random.randint(21, 50)
        elif index == 3:
            n = random.randint(51, 300)
        elif index == 4:
            n = random.randint(301, 400)
        else:
            n = random.randint(1, 400)

        return f"{n}\n"

    def _compute(self, input_content: str) -> str:
        input_content = input_content.strip()
        n = int(input_content)

        if 1 <= n <= 5:
            x = n - 1
        elif 6 <= n <= 20:
            x = 4 + 0.4 * (n - 5)
        elif 21 <= n <= 50:
            x = 10 + 0.15 * (n - 20)
        elif 51 <= n <= 300:
            x = 14.5 + 0.03 * (n - 50)
        elif n > 300:
            x = 22
        else:
            return "Error\n"

        return f"{n * (1-x)}\n"

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
            if abs(answer - standard_answer) < 1e-3 * abs(standard_answer):
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

    money = Money(
        student_path=args.student_path,
        generate_checkpoints=args.generate_checkpoints,
        compile=args.compile,
        run_checkpoints=args.run_checkpoints,
        judge=args.judge,
    )
