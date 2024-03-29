from typing import Dict, Tuple, List
import os
import shutil
import subprocess
import math
import toml
from functools import partial
from abc import abstractmethod, ABC

from utils import for_each_student, switch_encoding


class Problem(ABC):
    def __init__(
        self,
        assignment_path: str,
        problem_name: str,
        student_path: str = None,
        excluded_students: List[str] = [],
        checkpoints_number: int = 20,
        generate_checkpoints: bool = True,
        compile: bool = True,
        run_checkpoints: bool = True,
        judge: bool = True,
        checkpoint_timeout: float = 1,
    ) -> None:
        """
        File System Structure
        - Assignment Path
            - Student 1
            - Student 2
            ...
            - Student N
                - Problem 1.cpp
                - Problem 2.c
                ...
                - Problem k.c

        Args:
            assignment_path (str): Root path to the assignment.
            problem_name (str): Name of the problem, used as source file name without suffices
            student_path (str): Path to a student's submissions
            checkpoints_number (int, optional): Number of checkpoints. Defaults to 20.
        """
        self.assignment_path = assignment_path

        self.problem_name = problem_name
        self.problem_path = os.path.join(self.assignment_path, problem_name)

        self.student_path = student_path
        self.excluded_students = excluded_students

        self.checkpoints_path = os.path.join(self.problem_path, "checkpoints")

        self.checkpoints_number = checkpoints_number

        if generate_checkpoints:
            if os.path.exists(self.checkpoints_path):
                shutil.rmtree(self.checkpoints_path)
            os.makedirs(self.checkpoints_path)
            self.generate_checkpoints()
        if compile:
            self.compile()
        if run_checkpoints:
            self.checkpoint_timeout = checkpoint_timeout
            self.run_checkpoints()
        if judge:
            self.judge()

    @abstractmethod
    def _generate_input(self, index) -> str:
        pass

    @abstractmethod
    def _compute(self, input_content: str) -> str:
        pass

    def generate_checkpoints(self):
        for i in range(self.checkpoints_number):
            input_content = self._generate_input(i)
            answer_content = self._compute(input_content)
            with open(os.path.join(self.checkpoints_path, f"{i}.in"), "w") as f_in:
                f_in.write(input_content)
            with open(os.path.join(self.checkpoints_path, f"{i}.ans"), "w") as f_ans:
                f_ans.write(answer_content)

    def _compile_for_1_student(self, student_path: str):
        student = student_path.split("/")[-1]
        if student in self.excluded_students:
            return

        file_names = os.listdir(student_path)
        if f"{self.problem_name}.c" in file_names:
            compiler = "gcc"
            std = "gnu17"
            file_name = f"{self.problem_name}.c"
        elif f"{self.problem_name}.cpp" in file_names:
            compiler = "g++"
            std = "gnu++14"
            file_name = f"{self.problem_name}.cpp"
        else:
            print(f"{student_path}:\t{self.problem_name}.cpp not found")
            return

        file_name = os.path.join(student_path, file_name)
        executable_file_name = os.path.join(student_path, self.problem_name)

        switch_encoding(file_name)

        # compile
        compile_args = [
            f"{compiler}",
            "-O2",
            "-Wmain-return-type",
            f"--std={std}",
            "-o",
            executable_file_name,
            file_name,
        ]
        compile_process = subprocess.run(compile_args)
        if compile_process.returncode != 0:
            compile_command = " ".join(compile_process.args)
            raise RuntimeError(
                f"Compile failure: {compile_command}, return code: {compile_process.returncode}"
            )

    def compile(self):
        if self.student_path is None:
            for_each_student(
                self.assignment_path,
                partial(self._compile_for_1_student),
            )
        else:
            self._compile_for_1_student(self.student_path)

    def _run_checkpoints_for_1_student(self, student_path: str):
        student = student_path.split("/")[-1]
        executable_file_name = os.path.join(student_path, self.problem_name)
        if student in self.excluded_students or not os.path.exists(
            executable_file_name
        ):
            return

        output_path = os.path.join(self.problem_path, os.path.join("outputs", student))
        os.makedirs(output_path, exist_ok=True)

        for i in range(self.checkpoints_number):
            input_file_name = os.path.join(self.checkpoints_path, f"{i}.in")
            output_file_name = os.path.join(output_path, f"{i}.out")

            input_file = open(input_file_name)
            output_file = open(output_file_name, "w")
            try:
                execution_process = subprocess.run(
                    executable_file_name,
                    stdin=input_file,
                    stdout=output_file,
                    timeout=self.checkpoint_timeout,
                )
            except subprocess.TimeoutExpired:
                print(
                    f'Timeout:    "{executable_file_name}" with input "{input_file_name}"'
                )
            else:
                if execution_process.returncode != 0:
                    print(
                        f'Execution of "{execution_process.args}" with input "{input_file_name}" returns {execution_process.returncode}'
                    )

            input_file.close()
            output_file.close()

    def run_checkpoints(self):
        if self.student_path is None:
            for_each_student(self.assignment_path, self._run_checkpoints_for_1_student)
        else:
            self._run_checkpoints_for_1_student(self.student_path)

    @abstractmethod
    def _judge_1_checkpoint(
        output_file_name: str, answer_file_name: str
    ) -> Tuple[int, int]:
        return False

    def _judge_1_student(self, student_path: str) -> Tuple[int, int]:
        student = student_path.split("/")[-1]
        output_path = os.path.join(self.problem_path, os.path.join("outputs", student))

        if student in self.excluded_students or not os.path.exists(output_path):
            return "N/A"

        correct, total = 0, 0
        wrong = []
        for i in range(self.checkpoints_number):
            output_file_name = os.path.join(output_path, f"{i}.out")
            answer_file_name = os.path.join(self.checkpoints_path, f"{i}.ans")

            correct_ckpt, total_ckpt = self._judge_1_checkpoint(
                output_file_name, answer_file_name
            )
            correct += correct_ckpt
            total += total_ckpt
            if correct_ckpt != total_ckpt:
                wrong.append(i)

        return f"{correct} / {total} = {math.ceil(correct/total * 100)}, wrong: {wrong}"

    def judge(self):
        results_file = os.path.join(self.problem_path, f"results.toml")
        if self.student_path is None:
            results = for_each_student(self.assignment_path, self._judge_1_student)
        else:
            result_1_student = self._judge_1_student(self.student_path)
            with open(results_file, "r") as f:
                results = toml.load(f)
            results[self.student_path.split("/")[-1]] = result_1_student

        results_ordered = dict(sorted(results.items()))

        with open(results_file, "w") as f:
            toml.dump(results_ordered, f)
