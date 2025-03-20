"""The official simpy interpreter"""


def simpy(file_path: str) -> str:
    """
    This is where all the code of a (.sp) file gets parsed and ran.

    This function checks if the given file path ends in (.sp) and loops through every line of that 
    file, and then runs the logic on it.

    Parameters:
        (str) file_path: The file path to loop through.

    Returns:
        str: The outcome of the code.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        out = []
        iterable_reading = f.read().split("\n")
        for line in iterable_reading:
            if line.startswith("out "):
                out.append(line[len("out "):])
                continue
            # Continue rest of logic later
            raise NotImplementedError(line + ": Has not been implemented.")
        return out
