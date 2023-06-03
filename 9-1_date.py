from argparse import ArgumentParser
from typing import Tuple, List
import random
import string
from datetime import date, timedelta

from problem import Problem
from utils import re_int


class Date(Problem):
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
        self.alphabet = string.ascii_lowercase
        super().__init__(
            assignment_path,
            problem_name="date",
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

        date_start = date.fromisocalendar(2000, 1, 1)
        total_days = (date.today() - date_start).days

        delta_days_0 = random.randint(0, total_days)
        delta_0 = timedelta(days=delta_days_0)

        if index == 1:
            delta_1 = timedelta(0)
        else:
            delta_1 = timedelta(days=random.randint(0, total_days - delta_days_0))

        date_0 = date_start + delta_0
        date_1 = date_0 + delta_1

        return f"{date_0.strftime('%Y %m %d')}\n{date_1.strftime('%Y %m %d')}\n"

    def _compute(self, input_content: str) -> str:
        year_0, month_0, day_0, year_1, month_1, day_1 = (
            int(i) for i in input_content.split()
        )
        date_0 = date(year=year_0, month=month_0, day=day_0)
        date_1 = date(year=year_1, month=month_1, day=day_1)

        return str((date_1 - date_0).days) + "\n"

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

    Date(
        student_path=args.student_path,
        excluded_students=args.exclude_students,
        generate_checkpoints=args.generate_checkpoints,
        compile=args.compile,
        run_checkpoints=args.run_checkpoints,
        judge=args.judge,
    )
