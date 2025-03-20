"""The official simpy interpreter"""


def simpy(file_path: str) -> None:
    """
    This is where all the code of a (.sp) file gets parsed and ran.

    This function checks if the given file path ends in (.sp) and loops through every line of that 
    file, and then runs the logic on it.

    Parameters:
        (str) file_path: The file path to loop through.

    Returns:
        str: The outcome of the code.
    """
    variables = {}
    if file_path.endswith(".sp") is False:
        raise FileNotFoundError(f"{file_path} does not end with .sp")
    with open(file_path, "r", encoding="utf-8") as f:
        iterable_reading = f.read().split("\n")
        for line_num, line in enumerate(iterable_reading):
            if line.startswith("out "):
                print(line[len("out "):])
                continue
            elif line.startswith("in "):
                easier_line = line[len("in "):]
                in_var = []
                for len_x_, x in enumerate(easier_line):
                    if x != " ":
                        in_var.append(x)
                        continue
                    len_x = len_x_
                    break
                in_var = "".join(in_var)
                out_for_in = line[len_x+1+len("in "):]
                in_var_value = input(out_for_in)
                variables[in_var] = in_var_value
                continue
            raise NotImplementedError(
                f"Line {line_num+1}: {line}\nNot implemented yet.")
