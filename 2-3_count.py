import random
from argparse import ArgumentParser
from typing import Tuple

from problem import Problem
from utils import re_int


class Count(Problem):
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
            problem_name="count",
            student_path=student_path,
            checkpoints_number=checkpoints_number,
            generate_checkpoints=generate_checkpoints,
            compile=compile,
            run_checkpoints=run_checkpoints,
            judge=judge,
        )

    def _generate_input(self, index) -> str:
        input_content = ""
        line_number = random.randint(1, 20)
        for line in range(line_number):
            input_content += f"{random.randint(-2147483648, 2147483647)}\n"
        return input_content

    def _compute(self, input_content: str) -> str:
        input_tokens = input_content.split()

        count = 0
        for token in input_tokens:
            count += token.count("1")

        return str(count)

    def _judge_1_checkpoint(
        self, output_file_name, answer_file_name
    ) -> Tuple[int, int]:
        with open(answer_file_name, "r") as f_ans:
            standard_answers = []
            for line in f_ans.readlines():
                standard_answers.extend(re_int.findall(line))

        with open(output_file_name, "r") as f_out:
            answers = []
            for line in f_out.readlines():
                answers.extend(re_int.findall(line))

        correct, total = 0, len(standard_answers)
        for standard_answer, answer in zip(standard_answers, answers):
            standard_answer = int(standard_answer)
            answer = int(answer)
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

    count = Count(
        student_path=args.student_path,
        generate_checkpoints=args.generate_checkpoints,
        compile=args.compile,
        run_checkpoints=args.run_checkpoints,
        judge=args.judge,
    )
