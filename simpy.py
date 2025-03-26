"""The official simpy interpreter"""
import math
import re
import exceptions


def variables_to_data(line: str, variables: dict = None, end: str = " "):
    variables_in_string = line.count("$")
    dollar_positions = [[] * variables_in_string]
    vars_found = 0
    for char_index, char in enumerate(line):
        if char != "$":
            continue
        dollar_positions[vars_found].append(char_index)
        vars_found = + 1
    vars_found = 0
    var_names = [[] * variables_in_string]
    starting_point = line[dollar_positions[0][0]:]
    for char_index, char in enumerate(starting_point):
        if char != end:
            continue
        continue  # Continue logic later


def simpy(file_path: str) -> None:
    """
    This is where all the code of a (.sp) file gets parsed and ran.

    This function checks if the given file path ends in (.sp) and loops
    through every line of that file, and then runs the logic on it.

    Parameters:
        (str) file_path: The file path to loop through.

    Returns:
        None: Nothing, But it shows the outcome of the code through print
        statements.
    """
    variables = {}
    condition_true = False
    if file_path.endswith(".sp") is False:
        raise exceptions.NotASimpyFile(f"{file_path} does not end with .sp")
    with open(file_path, "r", encoding="utf-8") as f:
        iterable_reading = f.read().split("\n")
        for line_num, line_ in enumerate(iterable_reading):
            line = line_
            if condition_true and line.startswith("\t"):
                line = line.strip("\t")
            elif not condition_true and line.startswith("\t"):
                continue
            elif condition_true and line.startswith("\t") is False:
                condition_true = False
            elif not line.lstrip(" ") == line:
                continue

            if line.startswith("out "):
                print_msg = line[len("out "):]
                print_parts = print_msg.split(" + ")
                final_output = []
                for part in print_parts:
                    if not part.startswith("$"):
                        final_output.append(part)
                        continue

                    if part[1:] not in variables:
                        raise NameError(
                            f"In line {line_num+1}: {line}\n"
                            f"No such variable: {part[1:]}")
                    final_output.append(variables[part[1:]])
                print("".join(final_output))
                continue

            elif line.startswith("in "):
                no_prefix = line[len("in "):]
                var_name = []
                for len_char_, char in enumerate(no_prefix):
                    if char != " ":
                        var_name.append(char)
                        continue
                    len_x = len_char_
                    break
                var_name = "".join(var_name)
                input_string = line[len_x+1+len("in "):]
                in_var_value = input(input_string)
                variables[var_name] = in_var_value
                continue

            elif line.startswith("$"):
                no_prefix = line[1:]
                var_name = []
                dollar_string = False
                for len_char_, char in enumerate(no_prefix):
                    if char != " ":
                        var_name.append(char)
                        continue
                    len_char = len_char_
                    break
                var_name = "".join(var_name)
                var_value = line[len_char+len("$ "):]
                if var_value.startswith("$$"):
                    dollar_string = True
                    var_value = var_value[1:]

                elif var_value.startswith("$") and not dollar_string:
                    if not var_value[1:] in variables:
                        raise NameError(
                            f"In line {line_num}: {line}\n"
                            f"No such variable: {var_value}")
                    var_value = variables[var_value[1:]]

                variables[var_name] = var_value
                continue

            elif line.startswith("eval("):
                statement_ = line[len("eval("):]
                statement = []
                allowed_locals = {
                    '__builtins__': None,
                    'abs': abs,
                    'max': max,
                    'min': min,
                    'sum': sum,
                    'pow': pow,
                    'math': math
                }
                for char_len_, char in enumerate(statement_):
                    if char != ")":
                        statement.append(char)
                        continue
                    char_len = char_len_
                    break
                statement = "".join(statement)
                result = eval(statement, allowed_locals)
                var_name = line[char_len+8:]
                result = str(result)
                variables[var_name] = result
                continue

            elif line.startswith("if "):
                operators = ["=", "<", ">", "<=", ">="]
                for operator_index_, operator in enumerate(operators):
                    if operator not in line:
                        continue
                    operator_index = operator_index_

                operator = re.search(operators[operator_index], line)
                start = operator.start()
                end = operator.end()
                operator = line[start:end]
                if operator == "=":
                    variables_for_condition_ = list(re.finditer(r'\$', line))
                    variables_for_condition = [
                        (match.start(), match.end()) for match in variables_for_condition_]
                    variables_to_compare = [line[variables_for_condition[0][0]+1:start-1],
                                            line[variables_for_condition[1][0]+1:-1]]
                    if '' in variables_to_compare:
                        raise SyntaxError(f"In line {line_num+1}: {line}\n"
                                          f"Syntax error.")
                    for variable in variables_for_condition:
                        if line[variable[0]+1:variable[1]+1] not in variables:
                            raise NameError(f"In line {line_num+1}: {line}\n"
                                            f"No such variable: {variable}")
                    if variables[variables_to_compare[0]] == variables[variables_to_compare[1]]:
                        condition_true = True
                elif operator == "<":
                    variables_for_condition_ = list(re.finditer(r'\$', line))
                    variables_for_condition = [
                        (match.start(), match.end()) for match in variables_for_condition_]
                    variables_to_compare = [line[variables_for_condition[0][0]+1:start-1],
                                            line[variables_for_condition[1][0]+1:-1]]
                    if '' in variables_to_compare:
                        raise SyntaxError(f"In line {line_num+1}: {line}\n"
                                          f"Syntax error.")
                    for variable in variables_for_condition:
                        if line[variable[0]+1:variable[1]+1] not in variables:
                            raise NameError(f"In line {line_num+1}: {line}\n"
                                            f"No such variable: {variable}")
                    if variables[variables_to_compare[0]] < variables[variables_to_compare[1]]:
                        condition_true = True

                elif operator == ">":
                    variables_for_condition_ = list(re.finditer(r'\$', line))
                    variables_for_condition = [
                        (match.start(), match.end()) for match in variables_for_condition_]
                    variables_to_compare = [line[variables_for_condition[0][0] + 1:start - 1],
                                            line[variables_for_condition[1][0] + 1:-1]]
                    if '' in variables_to_compare:
                        raise SyntaxError(f"In line {line_num + 1}: {line}\n"
                                          f"Syntax error.")
                    for variable in variables_for_condition:
                        if line[variable[0] + 1:variable[1] + 1] not in variables:
                            raise NameError(f"In line {line_num + 1}: {line}\n"
                                            f"No such variable: {variable}")
                    if variables[variables_to_compare[0]] > variables[variables_to_compare[1]]:
                        condition_true = True

                elif operator == "<=":
                    variables_for_condition_ = list(re.finditer(r'\$', line))
                    variables_for_condition = [
                        (match.start(), match.end()) for match in variables_for_condition_]
                    variables_to_compare = [line[variables_for_condition[0][0] + 1:start - 1],
                                            line[variables_for_condition[1][0] + 1:-1]]
                    if '' in variables_to_compare:
                        raise SyntaxError(f"In line {line_num + 1}: {line}\n"
                                          f"Syntax error.")
                    for variable in variables_for_condition:
                        if line[variable[0] + 1:variable[1] + 1] not in variables:
                            raise NameError(f"In line {line_num + 1}: {line}\n"
                                            f"No such variable: {variable}")
                    if variables[variables_to_compare[0]] <= variables[variables_to_compare[1]]:
                        condition_true = True

                elif operator == ">=":
                    variables_for_condition_ = list(re.finditer(r'\$', line))
                    variables_for_condition = [
                        (match.start(), match.end()) for match in variables_for_condition_]
                    variables_to_compare = [line[variables_for_condition[0][0] + 1:start - 1],
                                            line[variables_for_condition[1][0] + 1:-1]]
                    if '' in variables_to_compare:
                        raise SyntaxError(f"In line {line_num + 1}: {line}\n"
                                          f"Syntax error.")
                    for variable in variables_for_condition:
                        if line[variable[0] + 1:variable[1] + 1] not in variables:
                            raise NameError(f"In line {line_num + 1}: {line}\n"
                                            f"No such variable: {variable}")
                    if variables[variables_to_compare[0]] >= variables[variables_to_compare[1]]:
                        condition_true = True

                continue

            raise NotImplementedError(
                f"In line {line_num+1}: {line}\n"
                f"Not implemented yet.")
