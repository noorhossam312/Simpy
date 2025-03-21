"""The official simpy interpreter"""


def simpy(file_path: str) -> None:
    """
    This is where all the code of a (.sp) file gets parsed and ran.

    This function checks if the given file path ends in (.sp) and loops through every line of that file, and then runs the logic on it.

    Parameters:
        (str) file_path: The file path to loop through.

    Returns:
        None: Nothing, But it shows the outcome of the code through print statements.
    """
    variables = {}
    if file_path.endswith(".sp") is False:
        raise FileNotFoundError(f"{file_path} does not end with .sp")
    with open(file_path, "r", encoding="utf-8") as f:
        iterable_reading = f.read().split("\n")
        for line_num, line in enumerate(iterable_reading):
            if not line:
                continue
            
            elif line.startswith("out "):
                print_msg = line[len("out "):]
                print_parts = print_msg.split(" + ")
                final_output = []
                for part in print_parts:
                    if not part.startswith("$"):
                        final_output.append(part)
                        continue
                    
                    if part[1:] not in variables:
                        raise NameError(f"In line {line_num+1}: {line}\nNo such variable: {part[1:]}")
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
                        raise NameError(f"In line {line_num}: {line}\nNo such variable: {var_value}")
                    var_value = variables[var_value[1:]]
                variables[var_name] = var_value
                print(f"{var_name} + {in_var_value}")
                continue
                
            raise NotImplementedError(
                f"In line {line_num+1}: {line}\nNot implemented yet.")