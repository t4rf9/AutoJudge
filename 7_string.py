from argparse import ArgumentParser
from typing import Tuple, List
import random

from problem import Problem


class String(Problem):
    def __init__(
        self,
        assignment_path: str = "Assignment 7",
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
        s = "123456789"
        m = index + 1

        return f"{s}\n{m}\n"

    def _compute(self, input_content: str) -> str:
        s, m = input_content.splitlines()
        m = int(m)

        if m > len(s):
            return "Error:Out of length\n"
        else:
            return s[:m] + s[m + 5 : m - 1 if m > 0 else None : -1] + s[m + 6 :] + "\n"

    def _judge_1_checkpoint(
        self, output_file_name, answer_file_name
    ) -> Tuple[int, int]:
        with open(answer_file_name, "rb") as f_ans:
            answer_lines = f_ans.readlines()

        answer = answer_lines[0].strip()

        with open(output_file_name, "rb") as f_out:
            output_lines = f_out.readlines()
        if len(output_lines) == 0:
            return 0, 1

        output = None
        for line in output_lines:
            line = line.strip()
            if line.startswith(b"#") or len(line) == 0:
                continue
            if output is not None:
                return 0, 1
            output = line
        if output is None:
            return 0, 1

        if answer == b"Error:Out of length":
            answer = answer.replace(b" ", b"").lower()
            output = output.replace(b" ", b"").lower()
            if answer == output:
                return 1, 1
            else:
                return 0, 1
        else:
            if answer == output:
                return 1, 1
            else:
                return 0, 1


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
