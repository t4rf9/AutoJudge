#! /bin/zsh
# Usage: ./extract.sh <zip file> <output path>

file="$1"
# check if the file name ends with .zip
if [[ "$(echo "$file" | cut -f 2 -d '.')" != zip ]]; then
    exit
fi

assignment_path="${2:-Extract}" # default path is "Extract"

unzip -O GB18030 "$file" -d "$assignment_path"

# .zip
for z in $(ls "$assignment_path" | grep ".zip"); do
    output_path="$(echo "$z" | cut -f 1,2 -d '_')"
    unzip -j -B -a -O GB18030 "$assignment_path/$z" -d "$assignment_path/$output_path"
    rm "$assignment_path/$z"
done

# .rar
for z in $(ls "$assignment_path" | grep ".rar"); do
    output_path="$(echo "$z" | cut -f 1,2 -d '_')"
    unrar e "$assignment_path/$z" "-op$assignment_path/$output_path" -or
    rm "$assignment_path/$z"
done

# .7z
for z in $(ls "$assignment_path" | grep .7z); do
    output_path="$(echo "$z" | cut -f 1,2 -d '_')"
    7zz e "$assignment_path/$z" "-o$assignment_path/$output_path" -aou
    rm "$assignment_path/$z"
done

# remove non-cpp files
ls -a "$assignment_path"/*/* | grep -v -e "\.cpp$" -e "\.c$" | sed "s/^/\"/;s/$/\"/" | xargs -n1 rm

# remove hidden files which start with .
ls -a "$assignment_path"/*/.* | grep -v -e "\.$" | sed "s/^/\"/;s/$/\"/" | xargs -n1 rm
