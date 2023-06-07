from argparse import ArgumentParser
from typing import Tuple, List
import random
import string

from problem import Problem
from utils import re_int


class String(Problem):
    def __init__(
        self,
        assignment_path: str = "Assignment 9",
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
            problem_name="string",
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
            return "2021 10 31\n2021 11 1\n"
        else:
            length_0 = index * 5
            letters_0 = random.randint(0, length_0)
            digits_0 = random.randint(0, length_0 - letters_0)
            space_0 = length_0 - letters_0 - digits_0

            length_1 = length_0 + (
                random.randint(-length_0 + 1, length_0 - 1) if index % 2 == 0 else 0
            )
            letters_1 = letters_0 + (
                random.randint(-letters_0, length_1 - letters_0) if index % 4 < 2 else 0
            )
            digits_1 = digits_0 + (
                random.randint(-digits_0, length_1 - letters_1 - digits_0)
                if index % 8 < 4
                else 0
            )
            space_1 = length_1 - letters_1 - digits_1

            letters_0 = random.choices(string.ascii_letters, k=letters_0)
            letters_1 = random.choices(string.ascii_letters, k=letters_1)
            digits_0 = random.choices(string.digits, k=digits_0)
            digits_1 = random.choices(string.digits, k=digits_1)
            space_0 = [" "] * space_0
            space_1 = [" "] * space_1

            str_0 = letters_0 + digits_0 + space_0
            str_1 = letters_1 + digits_1 + space_1

            random.shuffle(str_0)
            random.shuffle(str_1)

            str_0 = "".join(str_0)
            str_1 = "".join(str_1)

            return str_0 + "\n" + str_1 + "\n"

    def _compute(self, input_content: str) -> str:
        line_0, line_1 = input_content.splitlines()

        length_0, length_1 = len(line_0), len(line_1)
        space_0 = line_0.count(" ")
        space_1 = line_1.count(" ")

        letters_0, letters_1 = 0, 0
        digits_0, digits_1 = 0, 0

        for c in line_0:
            if c.isalpha():
                letters_0 += 1
            elif c.isdigit():
                digits_0 += 1
        for c in line_1:
            if c.isalpha():
                letters_1 += 1
            elif c.isdigit():
                digits_1 += 1

        length = 1 if length_0 == length_1 else 0
        space = 1 if space_0 == space_1 else 0
        letters = 1 if letters_0 == letters_1 else 0
        digits = 1 if digits_0 == digits_1 else 0

        return f"{length} {space} {letters} {digits}\n"

    def _judge_1_checkpoint(
        self, output_file_name, answer_file_name
    ) -> Tuple[int, int]:
        with open(answer_file_name, "r") as f_ans:
            answer_lines = f_ans.readlines()
        answer_words = answer_lines[0].split()

        with open(output_file_name, "r") as f_out:
            output_lines = f_out.readlines()
        if len(output_lines) == 0:
            return 0, 1

        output_words = []
        for line in output_lines:
            line = line.strip()
            if line.startswith("#") or len(line) == 0:
                continue

            output_words.extend(line.split())

        if len(output_words) != len(answer_words):
            return 0, 1

        for output, answer in zip(output_words, answer_words):
            if output != answer:
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

    String(
        student_path=args.student_path,
        excluded_students=args.exclude_students,
        generate_checkpoints=args.generate_checkpoints,
        compile=args.compile,
        run_checkpoints=args.run_checkpoints,
        judge=args.judge,
    )
