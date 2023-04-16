from argparse import ArgumentParser
from typing import Tuple, List
import random
import string

from problem import Problem
from utils import re_int


class String(Problem):
    def __init__(
        self,
        assignment_path: str = "Assignment 6",
        student_path: str = None,
        excluded_students: List[str] = [],
        checkpoints_number: int = 10,
        generate_checkpoints: bool = True,
        compile: bool = True,
        run_checkpoints: bool = True,
        judge: bool = True,
        checkpoint_timeout: float = 2,
    ):
        self.alphabet = string.ascii_letters + string.digits
        self.alphabet_counts = [45 for _ in range(len(self.alphabet))]
        for i in range(4):
            self.alphabet_counts[i] = 17
        for i in range(11, 52):
            self.alphabet_counts[i] = 17
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
            return "EE22\n"
        else:
            d = 10
            start = d * (index - 1)
            end = start + d
            res = "".join(
                random.sample(
                    self.alphabet,
                    random.randint(start, end),
                    counts=self.alphabet_counts,
                )
            )
            return res + "\n"

    def _compute(self, input_content: str) -> str:
        s = input_content.strip().encode()

        digits, letters = 0, 0

        for c in s:
            if b"e"[0] <= c <= b"k"[0]:
                letters += 1
            elif b"0"[0] <= c <= b"9"[0]:
                digits += 1
        return f"{digits} {letters}\n"

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

    String(
        student_path=args.student_path,
        excluded_students=args.exclude_students,
        generate_checkpoints=args.generate_checkpoints,
        compile=args.compile,
        run_checkpoints=args.run_checkpoints,
        judge=args.judge,
    )
