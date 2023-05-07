from argparse import ArgumentParser
from typing import Tuple, List
import random
import string

from problem import Problem
from utils import re_int


class Negative(Problem):
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
        self.alphabet = string.ascii_lowercase
        super().__init__(
            assignment_path,
            problem_name="negative",
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
            return "we will do it\n"
        else:
            total_length = (index - 1) * 9 + 1

            words = []
            prev_space = -1
            while prev_space < total_length:
                distance = min(
                    random.randint(2, 10)
                    if total_length >= 2
                    else total_length,
                    total_length - prev_space,
                )
                prev_space += distance
                if prev_space == total_length - 1:
                    distance += 1
                    prev_space += 1
                words.append("".join(random.choices(self.alphabet, k=distance)))

            return " ".join(words) + "\n"

    def _compute(self, input_content: str) -> str:
        words = input_content.split()

        words = [word[0].upper() + word[1:] for word in words[::-1]]

        return " ".join(words) + "\n"

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

    Negative(
        student_path=args.student_path,
        excluded_students=args.exclude_students,
        generate_checkpoints=args.generate_checkpoints,
        compile=args.compile,
        run_checkpoints=args.run_checkpoints,
        judge=args.judge,
    )
