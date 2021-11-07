input_file = 'RB Steel Framing_v34.gto'
output_file = 'RB Steel Framing_test.txt'


def remove_blank_lines():
    with open(input_file, 'r') as f:
        with open(output_file, 'w') as w:
            for line in f:
                if line.startswith(' '):
                    line = line[1:]
                    if not line.startswith('\n'):
                        w.write(line)


def store_file_list():
    with open(output_file, 'r') as file:
        file_list = []
        for more_lines in file:
            file_list.append(more_lines.rstrip())
    return file_list
