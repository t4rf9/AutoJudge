from typing import Dict, Tuple
import os
import json
from functools import partial
from abc import abstractmethod, ABC

from utils import for_each_student, switch_encoding


class Problem(ABC):
    def __init__(
        self,
        assignment_path: str,
        problem_name: str,
        student_path: str = None,
        checkpoints_number: int = 20,
        generate_checkpoints: bool = True,
        compile: bool = True,
        run_checkpoints: bool = True,
        judge: bool = True,
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

        self.checkpoints_path = os.path.join(self.problem_path, "checkpoints")
        os.makedirs(self.checkpoints_path, exist_ok=True)

        self.checkpoints_number = checkpoints_number

        if generate_checkpoints:
            self.generate_checkpoints()
        if compile:
            self.compile()
        if run_checkpoints:
            self.run_checkpoints()
        if judge:
            self.judge()

    @abstractmethod
    def _generate_input(self) -> str:
        pass

    @abstractmethod
    def _compute(self, input_content: str) -> str:
        pass

    def generate_checkpoints(self):
        for i in range(self.checkpoints_number):
            input_content = self._generate_input()
            answer_content = self._compute(input_content)
            with open(os.path.join(self.checkpoints_path, f"{i}.in"), "w") as f_in:
                f_in.write(input_content)
            with open(os.path.join(self.checkpoints_path, f"{i}.ans"), "w") as f_ans:
                f_ans.write(answer_content)

    def _compile_for_1_student(self, student_path: str):
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
        compile_command = f'{compiler} -O2 -Wmain-return-type --std={std} -o "{executable_file_name}" "{file_name}"'
        res = os.system(compile_command)
        if res != 0:
            raise RuntimeError(
                f"Compile failure: {compile_command}, return value: {res}"
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
        executable_file_name = os.path.join(student_path, self.problem_name)
        student = student_path.split("/")[-1]
        output_path = os.path.join(self.problem_path, os.path.join("outputs", student))
        os.makedirs(output_path, exist_ok=True)

        for i in range(self.checkpoints_number):
            input_file_name = os.path.join(self.checkpoints_path, f"{i}.in")
            output_file_name = os.path.join(output_path, f"{i}.out")
            command = (
                f'"{executable_file_name}" < "{input_file_name}" > "{output_file_name}"'
            )
            res = os.system(command)
            if res != 0:
                print(f"Execution of {command} returns {res}")
                # raise RuntimeError(f"Execution failure: {command}, return value: {res}")

    def run_checkpoints(self):
        if self.student_path is None:
            for_each_student(self.assignment_path, self._run_checkpoints_for_1_student)
        else:
            self._run_checkpoints_for_1_student(self.student_path)

    @abstractmethod
    def _judge_1_checkpoint(output_file_name: str, answer_file_name: str) -> bool:
        return False

    def _judge_1_student(self, student_path: str) -> Tuple[int, int]:
        student = student_path.split("/")[-1]
        output_path = os.path.join(self.problem_path, os.path.join("outputs", student))
        os.makedirs(output_path, exist_ok=True)

        correct = 0
        for i in range(self.checkpoints_number):
            output_file_name = os.path.join(output_path, f"{i}.out")
            answer_file_name = os.path.join(self.checkpoints_path, f"{i}.ans")

            if self._judge_1_checkpoint(output_file_name, answer_file_name):
                correct += 1

        return correct, self.checkpoints_number

    def judge(self):
        if self.student_path is None:
            results = for_each_student(self.assignment_path, self._judge_1_student)
            results_json = os.path.join(self.problem_path, f"results.json")
        else:
            results = self._judge_1_student(self.student_path)
            results_json = os.path.join(
                self.student_path, f"results_{self.problem_name}.json"
            )
        with open(results_json, "w") as f:
            json.dump(results, f)
