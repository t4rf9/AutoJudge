from argparse import ArgumentParser
from typing import Tuple, List
import random

from problem import Problem


class Radix(Problem):
    def __init__(
        self,
        assignment_path: str = "Assignment 5",
        student_path: str = None,
        excluded_students: List[str] = [],
        checkpoints_number: int = 10,
        generate_checkpoints: bool = True,
        compile: bool = True,
        run_checkpoints: bool = True,
        judge: bool = True,
        checkpoint_timeout: float = 60,
    ):
        super().__init__(
            assignment_path,
            problem_name="radix",
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
            n = 7
        elif index == 1:
            n = 15
        elif index < 9:
            n = random.randint(10**index + 1, 10 ** (index + 1))
        else:
            n = random.randint(10**9 + 1, 2**31 - 1)
        return f"{n}\n"

    def _compute(self, input_content: str) -> str:
        n = int(input_content.strip())

        return f"{n} 0{n:o}\n{n} {n:#x}\n"

    def _judge_1_checkpoint(
        self, output_file_name, answer_file_name
    ) -> Tuple[int, int]:
        correct, total = 0, 2.25

        with open(answer_file_name, "r") as f_ans:
            standard_answers = []
            lines = f_ans.readlines()
        for line in lines:
            standard_answers.extend(line.strip().split())
        n_10_0_std = int(standard_answers[0])
        n_8_std = int(standard_answers[1], base=8)
        n_10_1_std = int(standard_answers[2])
        n_16_std = int(standard_answers[3], base=16)

        with open(output_file_name, "r") as f_out:
            output_answers = []
            lines = f_out.readlines()
        for line in lines:
            line = line.strip()
            if len(line) == 0 or line[0] == "#":
                continue
            output_answers.extend(line.split())

        try:
            n_10_0_output = int(output_answers[0 if len(output_answers) == 4 else 2])
            if n_10_0_output == n_10_0_std:
                correct += 0.125
        except (ValueError, IndexError):
            pass
        try:
            n_8_output = int(
                output_answers[1 if len(output_answers) == 4 else 0], base=8
            )
            if n_8_output == n_8_std:
                correct += 1
        except (ValueError, IndexError):
            pass
        try:
            n_10_1_output = int(output_answers[2])
            if n_10_1_output == n_10_1_std:
                correct += 0.125
        except (ValueError, IndexError):
            pass
        try:
            n_16_output = int(
                output_answers[3 if len(output_answers) == 4 else 1], base=16
            )
            if n_16_output == n_16_std:
                correct += 1
        except (ValueError, IndexError):
            pass

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

    random.seed(2023)

    radix = Radix(
        student_path=args.student_path,
        excluded_students=args.exclude_students,
        generate_checkpoints=args.generate_checkpoints,
        compile=args.compile,
        run_checkpoints=args.run_checkpoints,
        judge=args.judge,
    )
