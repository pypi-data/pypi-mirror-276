####################################################
# this is just a simple file stream handling script#
####################################################


# will read a file from a path
def read_text_file(file_path, drop_new_lines=False):
    with open(file_path, 'r') as fd:
        reader = fd.readlines()
    lines = list(reader)
    if drop_new_lines:
        for i in range(0, len(lines)):
            lines[i] = lines[i].replace('\n', '')
    return lines


# will read a binary file (usually file which contains bytes)
def read_binary_file(file_path, bytes_count=None):
    in_file = open(file_path, "rb")
    if bytes_count:
        data = in_file.read(bytes_count)
    else:
        data = in_file.read()
    in_file.close()
    return data


# will write bytes to a file
def write_bytes_to_file(data, output_path):
    from os_file_handler import file_handler as fh
    if not fh.is_dir_exists(fh.get_parent_path(output_path)):
        fh.create_dir(fh.get_parent_path(output_path))
    with open(output_path, 'wb') as output:
        output.write(data)


# for text files you should look for the right initials
def compress_data_to_file(dst_file, data, write_type='wb'):
    import gzip
    from os_file_handler import file_handler
    if not file_handler.is_dir_exists(file_handler.get_parent_path(dst_file)):
        file_handler.create_dir(file_handler.get_parent_path(dst_file))
    with gzip.open(dst_file, write_type) as f:
        f.write(data)


def compress_text_file_to_file(src_file, dst_file):
    data = "".join(read_text_file(src_file)).encode("utf8")
    compress_data_to_file(dst_file, data, write_type='wb')


# will read a compressed file. rb stands for 'read binary'
# for text files you should look for the right initials
def read_compressed_file(file_path, read_type='rb'):
    import gzip

    with gzip.open(file_path, read_type) as f:
        return f.read()


# will write a content to a file (str or array of strings)
def write_file(file_path, content):
    from os_file_handler import file_handler as fh
    parent_dir = fh.get_parent_path(file_path)
    if not fh.is_dir_exists(parent_dir):
        fh.create_dir(parent_dir)
    with open(file_path, 'w') as f:
        from os_file_handler import file_handler as fh
        parent_dir = fh.get_parent_path(file_path)
        if not fh.is_dir_exists(parent_dir):
            fh.create_dir(parent_dir)

        if isinstance(content, str):
            f.write(content)
        if isinstance(content, list):
            for i in range(0, len(content)):
                if not str(content[i]).endswith('\n') and i != len(content) - 1:
                    content[i] += '\n'
                f.write(content[i])


# will replace a bunch of chars in a file
def replace_text_in_file(file_src, file_dst, old_expression, new_expression, replace_whole_line=False, cancel_if_exists=False):
    lines = read_text_file(file_src, drop_new_lines=True)

    if cancel_if_exists and is_line_exists_in_text(new_expression, lines=lines):
        return
    with open(file_dst, 'w') as f:
        from os_file_handler import file_handler as fh
        parent_dir = fh.get_parent_path(file_dst)
        if not fh.is_dir_exists(parent_dir):
            fh.create_dir(parent_dir)

        for line in lines:

            if old_expression in line:
                if replace_whole_line:
                    if new_expression == '':
                        continue
                    else:
                        line = new_expression
                else:
                    line = line.replace(old_expression, new_expression)
            f.write(f'{line}\n')


def replace_texts_in_file(file_src, file_dst, old_and_new_expressions_dict):
    """
    Will replace a bunch of expressions with other expressions in a file

    Args:
        file_src: the path to the file you want to load
        file_dst: the path to the output file
        old_and_new_expressions_dict: a dictionary, which carries: {"expression to be changed": "new expression"}
   """

    lines = read_text_file(file_src, drop_new_lines=True)

    with open(file_dst, 'w') as f:
        from os_file_handler import file_handler as fh
        parent_dir = fh.get_parent_path(file_dst)
        if not fh.is_dir_exists(parent_dir):
            fh.create_dir(parent_dir)

        for line in lines:
            for old_expression in old_and_new_expressions_dict.keys():
                if old_expression in line:
                    line = line.replace(old_expression, old_and_new_expressions_dict[old_expression])
            f.write(f'{line}\n')


# will delete a line contains an expression from a text
def delete_line_in_file(file_src, file_dst, expression):
    replace_text_in_file(file_src, file_src, expression, '', True)


# will add text below some other text in a file
def append_text_below_line_in_file(file_src, file_dst, below_line, new_expression, cancel_if_exists=False):
    lines = read_text_file(file_src, drop_new_lines=True)

    if cancel_if_exists and is_line_exists_in_text(new_expression, lines=lines):
        return
    with open(file_dst, 'w') as f:
        from os_file_handler import file_handler as fh
        parent_dir = fh.get_parent_path(file_dst)
        if not fh.is_dir_exists(parent_dir):
            fh.create_dir(parent_dir)

        for i in range(0, len(lines)):
            f.write(f'{lines[i]}\n')
            if below_line in lines[i]:
                f.write(f'{new_expression}\n')


# will add text above some other text in a file
def append_text_above_line_in_file(file_src, file_dst, above_line, new_expression, cancel_if_exists=False):
    lines = read_text_file(file_src, drop_new_lines=True)
    if cancel_if_exists and is_line_exists_in_text(new_expression, lines=lines):
        return

    with open(file_dst, 'w') as f:
        from os_file_handler import file_handler as fh
        parent_dir = fh.get_parent_path(file_dst)
        if not fh.is_dir_exists(parent_dir):
            fh.create_dir(parent_dir)

        for i in range(0, len(lines)):
            if above_line in lines[i]:
                f.write(f'{new_expression}\n')
            f.write(f'{lines[i]}\n')


# will check if line exists in a file
def is_line_exists_in_text(line_to_find, file_src=None, lines=None):
    if file_src:
        lines = read_text_file(file_src)
    for line in lines:
        if line_to_find in line:
            return True
    return False


# will delete a text in a range
def delete_text_range_in_file(file_src, file_dst, from_text, to_text, include_bundaries=False):
    lines = read_text_file(file_src, drop_new_lines=True)

    with open(file_dst, 'w') as f:
        from os_file_handler import file_handler as fh
        parent_dir = fh.get_parent_path(file_dst)
        if not fh.is_dir_exists(parent_dir):
            fh.create_dir(parent_dir)

        from_text_found = False
        done = False
        for i in range(0, len(lines)):
            if done:
                f.write(f'{lines[i]}\n')
                continue
            if from_text in lines[i]:
                from_text_found = True
                if include_bundaries:
                    f.write(f'{lines[i]}\n')
            if from_text_found and to_text in lines[i]:
                done = True
                if include_bundaries:
                    f.write(f'{lines[i]}\n')
            if not from_text_found:
                f.write(f'{lines[i]}\n')


# will return a text in a range with/without the boundaries
def get_text_in_range(file_src, from_text, to_text, lines=None, include_boundaries=False):
    if file_src is not None:
        lines = read_text_file(file_src, drop_new_lines=True)
    text_to_return = []
    from_text_found = False

    for i in range(0, len(lines)):

        if from_text in lines[i]:
            from_text_found = True
            if include_boundaries:
                text_to_return.append(lines[i])
            continue

        if from_text_found:
            if to_text in lines[i]:
                if include_boundaries:
                    text_to_return.append(lines[i])
                return text_to_return
            else:
                text_to_return.append(lines[i])
    return None


# will uncomment a line. For example:
# uncommentLineInFile("#", "pod 'google-cast-sdk-no-bluetooth'", os.path.join(finals.PROJECT_PATH, 'Podfile'))
def uncomment_line_in_file(comment_sign, line_to_uncomment, file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        line_changed = False
        new_lines = []
        for line in lines:
            stripped_line = line.lstrip()
            if stripped_line.startswith(comment_sign + line_to_uncomment):
                new_lines.append(line.replace(comment_sign, '', 1))
                line_changed = True
            else:
                new_lines.append(line)

        if line_changed:
            with open(file_path, 'w') as file:
                file.writelines(new_lines)

        return line_changed

    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def clear_text_from_last(lines, text):
    for i in reversed(range(0, len(lines))):
        found = False
        if text in lines[i]:
            found = True
        lines.pop(-1)
        if found:
            return lines
