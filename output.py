import re

def read_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return lines

def write_txt_file(file_path, lines):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

def is_chinese_start(line):
    return re.match(r'^[\u4e00-\u9fff]', line)

def get_group_length(line):
    match = re.search(r'valid fase res (\d)', line)
    if match:
        return int(match.group(1)) + 4
    return 4

def process_lines(lines):
    processed_lines = []
    group = []
    last_group = None

    i = 0
    while i < len(lines):
        if lines[i].startswith('valid fase time'):
            group = [lines[i]]
            group_length = get_group_length(lines[i+3])
            group.extend(lines[i+1:i+group_length])
            i += group_length
            if group != last_group:
                processed_lines.extend(group)
                last_group = group
        elif is_chinese_start(lines[i]):
            processed_lines.append(lines[i])
            i += 1
        else:
            i += 1
            print('error',i)

    return processed_lines

if __name__ == "__main__":
    input_file_path = 'output1.txt'  # 输入文件路径
    output_file_path = 'output rate2.txt'  # 输出文件路径

    lines = read_txt_file(input_file_path)
    processed_lines = process_lines(lines)
    write_txt_file(output_file_path, processed_lines)

    print("Processing complete. Check the output file.")