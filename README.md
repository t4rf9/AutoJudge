# AutoJudge

This is a utility for judging homework assignments of the Tsinghua course Programming Fundamentals.

`extract.sh` helps decompress received zip files.

`utils.py` works like a toolbox.

For a new assignment, one needs to inherit `class Problem` and implement all 3 abstract methods: `_generate_input`, `_compute` and `_judge_1_checkpoint`, as is done in `complex.py` and `traiangular_prism.py`.
