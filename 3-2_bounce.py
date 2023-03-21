import random
from argparse import ArgumentParser
from typing import Tuple, List

from problem import Problem
from utils import re_float_fixed


class Bounce(Problem):
    def __init__(
        self,
        assignment_path: str = "Assignment 3",
        student_path: str = None,
        excluded_students: List[str] = [],
        checkpoints_number: int = 14,
        generate_checkpoints: bool = True,
        compile: bool = True,
        run_checkpoints: bool = True,
        judge: bool = True,
    ):
        super().__init__(
            assignment_path,
            problem_name="bounce",
            student_path=student_path,
            excluded_students=excluded_students,
            checkpoints_number=checkpoints_number,
            generate_checkpoints=generate_checkpoints,
            compile=compile,
            run_checkpoints=run_checkpoints,
            judge=judge,
        )

    def _generate_input(self, index) -> str:
        if index < 12:
            return f"{index + 1}"
        elif index == 12:
            return "1000000"
        return f"{random.randint(1000001, 2147483647)}\n"

    def _compute(self, input_content: str) -> str:
        input_tokens = input_content.strip()
        n = int(input_tokens)

        res = 100 * (2 / 3) ** n
        if res < 1:
            return "No Bounce"

        return f"{res:.3f}"

    def _judge_1_checkpoint(
        self, output_file_name, answer_file_name
    ) -> Tuple[int, int]:
        correct, total = 0, 1

        with open(answer_file_name, "r") as f_ans:
            standard_answer = f_ans.readline().strip().replace(" ", "").lower()
        with open(output_file_name, "r") as f_out:
            answer_lines = []
            for line in f_out.readlines():
                line = line.strip()
                if len(line) == 0 or line[0] == "#":
                    continue
                answer_lines.append(line.replace(" ", "").lower())
        try:
            standard_answer = float(standard_answer)
            for line in answer_lines:
                match = re_float_fixed.search(line)
                if (
                    match is not None
                    and abs((float(match[0]) - standard_answer) / standard_answer)
                    < 1e-4
                ):
                    correct += 1
                    break
        except ValueError:
            for line in answer_lines:
                if line.find(standard_answer) != -1:
                    correct += 1
                    break
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

    bounce = Bounce(
        student_path=args.student_path,
        excluded_students=args.exclude_students,
        generate_checkpoints=args.generate_checkpoints,
        compile=args.compile,
        run_checkpoints=args.run_checkpoints,
        judge=args.judge,
    )
