import random
from argparse import ArgumentParser
from typing import Tuple

from problem import Problem
from utils import re_float_fixed


class Maximum(Problem):
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
            problem_name="maximum",
            student_path=student_path,
            checkpoints_number=checkpoints_number,
            generate_checkpoints=generate_checkpoints,
            compile=compile,
            run_checkpoints=run_checkpoints,
            judge=judge,
        )

    def _generate_input(self, index) -> str:
        if index == 0:
            return "0 0 0 0\n"

        a = random.randint(-1000000, 1000000) / 1000
        b = random.randint(-1000000, 1000000) / 1000
        c = random.randint(-1000000, 1000000) / 1000
        d = random.randint(-1000000, 1000000) / 1000
        if index == 1:
            return f"{a:.3f} {a:.3f} {c:.3f} {d:.3f}\n"
        if index == 2:
            return f"{a:.3f} {b:.3f} {a:.3f} {d:.3f}\n"
        if index == 3:
            return f"{a:.3f} {b:.3f} {c:.3f} {a:.3f}\n"
        if index == 4:
            return f"{a:.3f} {b:.3f} {b:.3f} {d:.3f}\n"
        if index == 5:
            return f"{a:.3f} {b:.3f} {c:.3f} {b:.3f}\n"
        if index == 6:
            return f"{a:.3f} {b:.3f} {c:.3f} {c:.3f}\n"
        if index == 7:
            return f"-1000.1 {a:.3f} {b:.3f} {c:.3f}\n"
        if index == 8:
            return f"{a:.3f} -1000.1 {b:.3f} {c:.3f}\n"
        if index == 9:
            return f"{a:.3f} {b:.3f} -1000.1 {c:.3f}\n"
        if index == 10:
            return f"{a:.3f} {b:.3f} {c:.3f} -1000.1\n"
        if index == 11:
            return f"1000.1 {a:.3f} {b:.3f} {c:.3f}\n"
        if index == 12:
            return f"{a:.3f} 1000.1 {b:.3f} {c:.3f}\n"
        if index == 13:
            return f"{a:.3f} {b:.3f} 1000.1 {c:.3f}\n"
        if index == 14:
            return f"{a:.3f} {b:.3f} {c:.3f} 1000.1\n"
        if index == 15:
            return f"{a:.3f} 1000.1 {c:.3f} 1000.1\n"
        return f"{a:.3f} {b:.3f} {c:.3f} {d:.3f}\n"

    def _compute(self, input_content: str) -> str:
        input_tokens = input_content.split()
        a, b, c, d = [float(token) for token in input_tokens]

        if a == b == c == d == 0:
            return "Exit"
        if a == b or a == c or a == d or b == c or b == d or c == d:
            return "Error:Equal"

        res = max(a, b, c, d)
        if res > 1000 or min(a, b, c, d) < -1000:
            return "Error:Out of Range"

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
                    < 1e-6
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
    parser.add_argument("-g", "--generate_checkpoints", action="store_true")
    parser.add_argument("-c", "--compile", action="store_true")
    parser.add_argument("-r", "--run_checkpoints", action="store_true")
    parser.add_argument("-j", "--judge", action="store_true")
    args = parser.parse_args()

    maximum = Maximum(
        student_path=args.student_path,
        generate_checkpoints=args.generate_checkpoints,
        compile=args.compile,
        run_checkpoints=args.run_checkpoints,
        judge=args.judge,
    )
