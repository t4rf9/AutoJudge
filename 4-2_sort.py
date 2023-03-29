from argparse import ArgumentParser
from typing import Tuple, List
import random

from problem import Problem

CHARS_NORMAL = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
CHARS_OBSTRUCTION = '<>?:"!@#$%^&*() '
SPACE = " "


class Sort(Problem):
    def __init__(
        self,
        assignment_path: str = "Assignment 4",
        student_path: str = None,
        excluded_students: List[str] = [],
        checkpoints_number: int = 20,
        generate_checkpoints: bool = True,
        compile: bool = True,
        run_checkpoints: bool = True,
        judge: bool = True,
        checkpoint_timeout: float = 60,
    ):
        super().__init__(
            assignment_path,
            problem_name="sort",
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
        length = index * 3 + 1
        res = []
        for i in range(length):
            char_type = random.random()
            if index < 6:
                char_set = CHARS_NORMAL
            elif index < 12:
                if char_type < 0.8:
                    char_set = CHARS_NORMAL
                else:
                    char_set = SPACE
            else:
                if char_type < 0.6:
                    char_set = CHARS_NORMAL
                elif char_type < 0.9:
                    char_set = CHARS_OBSTRUCTION
                else:
                    char_set = SPACE
            res.append(random.choice(char_set))
        return "".join(res) + "\n"

    def _compute(self, input_content: str) -> str:
        s = input_content.strip().upper()

        chars = set()
        for c in s:
            if not c in CHARS_OBSTRUCTION:
                chars.add(c)

        return "\n".join(sorted(chars))

    def _judge_1_checkpoint(
        self, output_file_name, answer_file_name
    ) -> Tuple[int, int]:
        with open(answer_file_name, "r") as f_ans:
            standard_answer_lines = f_ans.readlines()
        standard_answers = [line.strip() for line in standard_answer_lines]

        with open(output_file_name, "r") as f_out:
            try:
                output_lines = f_out.readlines()
            except Exception as err:
                print(output_file_name)
                print(err)
                print()
                return 0, 1
        answers = []
        for line in output_lines:
            line = line.strip()
            if len(line) > 0 and line[0] != "#":
                answers.extend(line.split())

        if len(answers) != len(standard_answers):
            return 0, 1

        for char_std, char_ans in zip(standard_answers, answers):
            if char_std != char_ans:
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

    random.seed(2023)

    sort = Sort(
        student_path=args.student_path,
        excluded_students=args.exclude_students,
        generate_checkpoints=args.generate_checkpoints,
        compile=args.compile,
        run_checkpoints=args.run_checkpoints,
        judge=args.judge,
    )
