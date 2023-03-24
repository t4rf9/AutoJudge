from argparse import ArgumentParser
from typing import Tuple, List

from problem import Problem
from utils import re_int


def f(n, m, grid=None, next_number=1):
    if grid is None:
        grid = [[0 for j in range(m)] for i in range(n)]
    res = 0
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 0:
                if (i == 0 or grid[i - 1][j] > 0) and (j == 0 or grid[i][j - 1] > 0):
                    grid[i][j] = next_number
                    if next_number < n * m:
                        res += f(n, m, grid, next_number + 1)
                    else:
                        res += 1
                    grid[i][j] = 0
    return res


class Count(Problem):
    def __init__(
        self,
        assignment_path: str = "Assignment 4",
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
            problem_name="count",
            student_path=student_path,
            excluded_students=excluded_students,
            checkpoints_number=checkpoints_number,
            generate_checkpoints=generate_checkpoints,
            compile=compile,
            run_checkpoints=run_checkpoints,
            judge=judge,
        )

    def _generate_input(self, index) -> str:
        n, m = index // 4 + 1, index % 4 + 1
        return f"{n} {m}"

    def _compute(self, input_content: str) -> str:
        n, m = input_content.split()
        n, m = int(n.strip()), int(m.strip())

        res = f(n, m)

        return f"{res}"

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
        standard_answer = int(standard_answer)
        for line in answer_lines:
            match = re_int.search(line)
            if match is not None and int(match[0]) == standard_answer:
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

    count = Count(
        student_path=args.student_path,
        excluded_students=args.exclude_students,
        generate_checkpoints=args.generate_checkpoints,
        compile=args.compile,
        run_checkpoints=args.run_checkpoints,
        judge=args.judge,
    )
