def file_parser(filename: str) -> tuple[dict, bool]:
    configuration = {}

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

                    parsed_line[0] = parsed_line[0].strip()
                    parsed_line[1] = parsed_line[1].strip()

                    if parsed_line[0] not in accepted_keys_set:
                        raise ValueError("Wrong key input format")

                    if parsed_line[0] in configuration.keys():
                        raise TypeError(
                            f"{parsed_line[0]} was submitted more than once"
                        )

                    if parsed_line[0] == "WIDTH":
                        try:
                            parsed_line[1] = int(parsed_line[1])
                            if parsed_line[1] < 1:
                                raise TypeError("WIDTH value can't be "
                                                "lower than 1")
                            else:
                                configuration[parsed_line[0]] = parsed_line[1]
                        except ValueError:
                            raise ValueError(
                                "WIDTH must be submitted in the format "
                                "'WIDTH=number'"
                            )

                    elif parsed_line[0] == "HEIGHT":
                        try:
                            parsed_line[1] = int(parsed_line[1])
                            if parsed_line[1] < 1:
                                raise TypeError("HEIGHT value can't be "
                                                "lower than 1")
                            else:
                                configuration[parsed_line[0]] = parsed_line[1]
                        except ValueError:
                            raise ValueError(
                                "HEIGHT must be submitted in "
                                "the format 'HEIGHT=number'"
                            )

                    elif parsed_line[0] == "ENTRY":
                        try:
                            parsed_line[1] = [
                                int(n.strip()) for n in parsed_line[
                                    1].split(",")
                            ]

                            if len(parsed_line[1]) != 2:
                                raise TypeError(
                                    "ENTRY value must be formatted "
                                    "as number,number"
                                )
                            elif parsed_line[
                                    1][0] < 0 or parsed_line[1][1] < 0:
                                raise TypeError("ENTRY values can't "
                                                "be negatives")
                            else:
                                configuration[parsed_line[0]] = (
                                    parsed_line[1][0],
                                    parsed_line[1][1],
                                )
                        except ValueError:
                            raise ValueError(
                                "ENTRY must be submitted in the format "
                                "'ENTRY=number,number'"
                            )

                    elif parsed_line[0] == "EXIT":
                        try:
                            parsed_line[1] = [
                                int(n.strip()) for n in parsed_line[
                                    1].split(",")
                            ]

                            if len(parsed_line[1]) != 2:
                                raise TypeError(
                                    "EXIT value must be formatted "
                                    "as number,number"
                                )
                            elif parsed_line[
                                            1][
                                            0] < 0 or parsed_line[1][1] < 0:
                                raise TypeError("EXIT values "
                                                "can't be negatives")
                            else:
                                configuration[parsed_line[0]] = (
                                    parsed_line[1][0],
                                    parsed_line[1][1],
                                )
                        except ValueError:
                            raise ValueError(
                                "EXIT must be submitted in the format "
                                "'EXIT=number,number'"
                            )

                    elif parsed_line[0] == "OUTPUT_FILE":
                        parsed_line[1] = parsed_line[1].strip()

                        if parsed_line[1] == "":
                            raise TypeError("OUTPUT_FILE can't be empty")

                        configuration[parsed_line[0]] = parsed_line[1]

                    elif parsed_line[0] == "PERFECT":
                        parsed_line[1] = parsed_line[1].strip().capitalize()

                        if parsed_line[1] == "True":
                            configuration[parsed_line[0]] = True
                        elif parsed_line[1] == "False":
                            configuration[parsed_line[0]] = False
                        else:
                            raise TypeError("PERFECT value can only be true "
                                            "or false")

                    elif parsed_line[0] == "SEED":
                        try:
                            parsed_line[1] = int(parsed_line[1])
                            configuration[parsed_line[0]] = parsed_line[1]
                        except ValueError:
                            raise ValueError(
                                "SEED must be formatted in the format "
                                "'SEED=number'"
                            )

        if keys_set.issubset(set(configuration.keys())):
            if "SEED" not in configuration.keys():
                configuration["SEED"] = 0

            width = configuration["WIDTH"]
            height = configuration["HEIGHT"]
            entry = configuration["ENTRY"]
            exit = configuration["EXIT"]

            if entry == exit:
                raise ValueError("ENTRY and EXIT must be different")

            if entry[0] >= width or entry[1] >= height:
                raise ValueError("ENTRY is out of maze bounds")

            if exit[0] >= width or exit[1] >= height:
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
