from argparse import ArgumentParser
from utils import for_each_source_file


def switch_encoding(file_path):
    with open(file_path, "rb") as f:
        lines_bytes = f.readlines()

    lines_bytes = [
        line_bytes.expandtabs(4).replace(b"\r\n", b"\n").replace(b"scanf_s", b"scanf")
        for line_bytes in lines_bytes
    ]

    try:
        lines = [line_bytes.decode("utf-8") for line_bytes in lines_bytes]
        print(f"{file_path}: utf-8")
    except UnicodeDecodeError as err:
        lines = [line_bytes.decode("gb18030") for line_bytes in lines_bytes]
        print(f"{file_path}: gb18030")

    with open(file_path, "w") as f:
        f.writelines(lines)


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("assignment_path", type=str)

    args = parser.parse_args()

    for_each_source_file(args.assignment_path, switch_encoding)
