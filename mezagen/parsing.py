from typing import TypeAlias


ConfigValue: TypeAlias = int | bool | str | tuple[int, int]
Config: TypeAlias = dict[str, ConfigValue]


def file_parser(filename: str) -> tuple[Config, bool]:
    configuration: Config = {}

    keys_set = {"WIDTH", "HEIGHT", "ENTRY",
                "EXIT", "OUTPUT_FILE", "PERFECT"}
    optional_keys_set = {"SEED"}
    accepted_keys_set = keys_set.union(optional_keys_set)

    try:
        with open(filename) as file:
            one_line = file.read()
            one_line = one_line.rstrip("\n")
            actual_text = one_line.split("\n")

            for line in actual_text:
                line = line.strip()

                if line == "" or line[0] == "#":
                    continue
                else:
                    parsed_line = line.split("=", 1)

                    if len(parsed_line) != 2:
                        raise ValueError("Wrong input format")

                    key = parsed_line[0].strip()
                    value = parsed_line[1].strip()

                    if key not in accepted_keys_set:
                        raise ValueError("Wrong key input format")

                    if key in configuration.keys():
                        raise TypeError(
                            f"{key} was submitted more than once"
                        )

                    if key == "WIDTH":
                        try:
                            width = int(value)
                            if width < 1:
                                raise TypeError("WIDTH value can't be "
                                                "lower than 1")
                            else:
                                configuration[key] = width
                        except ValueError:
                            raise ValueError(
                                "WIDTH must be submitted in the format "
                                "'WIDTH=number'"
                            )

                    elif key == "HEIGHT":
                        try:
                            height = int(value)
                            if height < 1:
                                raise TypeError("HEIGHT value can't be "
                                                "lower than 1")
                            else:
                                configuration[key] = height
                        except ValueError:
                            raise ValueError(
                                "HEIGHT must be submitted in "
                                "the format 'HEIGHT=number'"
                            )

                    elif key == "ENTRY":
                        try:
                            entry = [
                                int(n.strip()) for n in value.split(",")
                            ]

                            if len(entry) != 2:
                                raise TypeError(
                                    "ENTRY value must be formatted "
                                    "as number,number"
                                )
                            elif entry[0] < 0 or entry[1] < 0:
                                raise TypeError("ENTRY values can't "
                                                "be negatives")
                            else:
                                configuration[key] = (
                                    entry[0],
                                    entry[1],
                                )
                        except ValueError:
                            raise ValueError(
                                "ENTRY must be submitted in the format "
                                "'ENTRY=number,number'"
                            )

                    elif key == "EXIT":
                        try:
                            exit_coord = [
                                int(n.strip()) for n in value.split(",")
                            ]

                            if len(exit_coord) != 2:
                                raise TypeError(
                                    "EXIT value must be formatted "
                                    "as number,number"
                                )
                            elif exit_coord[0] < 0 or exit_coord[1] < 0:
                                raise TypeError("EXIT values "
                                                "can't be negatives")
                            else:
                                configuration[key] = (
                                    exit_coord[0],
                                    exit_coord[1],
                                )
                        except ValueError:
                            raise ValueError(
                                "EXIT must be submitted in the format "
                                "'EXIT=number,number'"
                            )

                    elif key == "OUTPUT_FILE":
                        if value == "":
                            raise TypeError("OUTPUT_FILE can't be empty")

                        configuration[key] = value

                    elif key == "PERFECT":
                        perfect = value.capitalize()

                        if perfect == "True":
                            configuration[key] = True
                        elif perfect == "False":
                            configuration[key] = False
                        else:
                            raise TypeError("PERFECT value can only be true "
                                            "or false")

                    elif key == "SEED":
                        try:
                            seed = int(value)
                            configuration[key] = seed
                        except ValueError:
                            raise ValueError(
                                "SEED must be formatted in the format "
                                "'SEED=number'"
                            )

        if keys_set.issubset(set(configuration.keys())):
            if "SEED" not in configuration.keys():
                configuration["SEED"] = 0

            width_value = configuration["WIDTH"]
            height_value = configuration["HEIGHT"]
            entry_value = configuration["ENTRY"]
            exit_value = configuration["EXIT"]

            if not isinstance(width_value, int):
                raise TypeError("WIDTH must be an integer")
            if not isinstance(height_value, int):
                raise TypeError("HEIGHT must be an integer")
            if not isinstance(entry_value, tuple):
                raise TypeError("ENTRY must be a coordinate")
            if not isinstance(exit_value, tuple):
                raise TypeError("EXIT must be a coordinate")

            if entry_value == exit_value:
                raise ValueError("ENTRY and EXIT must be different")

            if entry_value[0] >= width_value or entry_value[1] >= height_value:
                raise ValueError("ENTRY is out of maze bounds")

            if exit_value[0] >= width_value or exit_value[1] >= height_value:
                raise ValueError("EXIT is out of maze bounds")

            return (configuration, True)

        else:
            raise ValueError(
                f"Missing informations about "
                f"{keys_set.difference(configuration)}"
            )

    except Exception as e:
        print(e)
        return (configuration, False)
