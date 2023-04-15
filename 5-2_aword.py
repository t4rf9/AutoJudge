from argparse import ArgumentParser
from typing import Tuple, List
import random
import string

from problem import Problem


class Aword(Problem):
    def __init__(
        self,
        assignment_path: str = "Assignment 5",
        student_path: str = None,
        excluded_students: List[str] = [],
        checkpoints_number: int = 20,
        generate_checkpoints: bool = True,
        compile: bool = True,
        run_checkpoints: bool = True,
        judge: bool = True,
        checkpoint_timeout: float = 5,
    ):
        self.alphabet = string.ascii_letters + string.digits
        self.alphabet_counts = [1 for _ in range(len(self.alphabet))]
        self.alphabet_counts[0] = 20
        self.alphabet_counts[26] = 20
        super().__init__(
            assignment_path,
            problem_name="aword",
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
        if index == 1:
            return "a\n"
        tokens = [
            "".join(
                random.sample(
                    self.alphabet, random.randint(1, 5), counts=self.alphabet_counts
                )
            )
            for _ in range(index)
        ]

        res = " ".join(tokens) + "\n"
        if index < 15:
            return res.lower()
        else:
            return res

    def _compute(self, input_content: str) -> str:
        tokens = input_content.split()

        res, length = [], 0

        for token in tokens:
            if not "a" in token.lower():
                continue
            token_length = len(token)
            if token_length > length:
                res = [token]
                length = token_length
            elif token_length == length:
                res.append(token)

        if len(res) == 0:
            return "Error\n"
        else:
            return "\n".join(res) + "\n"

    def _judge_1_checkpoint(
        self, output_file_name, answer_file_name
    ) -> Tuple[int, int]:
        with open(answer_file_name, "rb") as f_ans:
            answer_lines = f_ans.readlines()
        answers = []
        for line in answer_lines:
            line = line.strip()
            if len(line) > 0:
                answers.append(line)

        with open(output_file_name, "rb") as f_out:
            output_lines = f_out.readlines()
        outputs = []
        for line in output_lines:
            line = line.strip()
            if len(line) > 0 and not line.startswith(b"#"):
                outputs.extend(line.split())

        if len(outputs) != len(answers):
            return 0, 1

        for output, answer in zip(outputs, answers):
            if output.strip() != answer.strip():
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

    aword = Aword(
        student_path=args.student_path,
        excluded_students=args.exclude_students,
        generate_checkpoints=args.generate_checkpoints,
        compile=args.compile,
        run_checkpoints=args.run_checkpoints,
        judge=args.judge,
    )
