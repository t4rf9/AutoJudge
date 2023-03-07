#! /bin/bash
file="$1"
if [[ "$(echo "$file" | cut -f 2 -d '.')" != zip ]]; then
    exit
fi
assignment_path="${2:-'.'}"
unzip -O GB18030 "$file" -d "$assignment_path"
for z in $(ls "$assignment_path" | grep ".zip"); do
    output_path="$(echo "$z" | cut -f 1,2 -d '_')";
    unzip -j -B -a -O GB18030 "$assignment_path/$z" -d "$assignment_path/$output_path";
    rm "$assignment_path/$z";
done
for z in $(ls "$assignment_path" | grep ".rar"); do
    output_path="$(echo "$z" | cut -f 1,2 -d '_')";
    unrar e "$assignment_path/$z" "-op$assignment_path/$output_path" -or;
    rm "$assignment_path/$z";
done
for z in $(ls "$assignment_path" | grep .7z); do
    output_path="$(echo "$z" | cut -f 1,2 -d '_')";
    7zz e "$assignment_path/$z" "-o$assignment_path/$output_path" -aou;
    rm "$assignment_path/$z";
done
rm $(ls -a "$assignment_path"/*/* | grep -v -e ".cpp$" -e ".c$")
rm "$assignment_path"/*/.*
python switch_encoding.py "$assignment_path"