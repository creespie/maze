import typing
import io

def file_parser(filename: str) -> tuple[dict, bool]:
    configuration = {}
    keys_set = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT", "SEED"}
    try:
        with open(filename) as file:
            one_line = file.read()
            one_line = one_line.rstrip("\n")
            actual_text = one_line.split("\n")
            
            for line in actual_text:
                if line == "" or line[0] == "#":
                    continue
                else:
                    parsed_line = line.split("=", 1)
                    if len(parsed_line) != 2 or parsed_line[0] not in keys_set:
                        raise ValueError("Wrong key input format")
                    else:
                        if parsed_line[0] == "WIDTH":
                            try:
                                parsed_line[1] = int(parsed_line[1])
                                if parsed_line[1] < 1: 
                                    raise TypeError("WIDTH value can't be lower than 1")
                                elif "WIDTH" in configuration.keys():
                                    raise TypeError("WIDTH was submitted more than once")
                                else:
                                    configuration[parsed_line[0]] = parsed_line[1]
                            except ValueError:
                                raise ValueError("WIDTH must be submitted in the format 'WIDTH=number'")
                        elif parsed_line[0] == "HEIGHT":
                            try:
                                parsed_line[1] = int(parsed_line[1])
                                if parsed_line[1] < 1: 
                                    raise TypeError("HEIGHT value can't be lower than 1")
                                elif "HEIGHT" in configuration.keys():
                                    raise TypeError("HEIGHT was submitted more than once")
                                else:
                                    configuration[parsed_line[0]] = parsed_line[1]
                            except ValueError:
                                raise ValueError("HEIGHT must be submitted in the format 'HEIGHT=number'")
                        elif parsed_line[0] == "ENTRY":
                            try:
                                parsed_line[1] = [int(n.strip()) for n in parsed_line[1].split(",")]
                                if len(parsed_line[1]) != 2:
                                    raise TypeError("ENTRY value must be formatted as number,number")
                                elif parsed_line[1][0] < 0 or parsed_line[1][1] < 0:
                                    raise TypeError("ENTRY values can't be negatives")
                                elif "ENTRY" in configuration.keys():
                                    raise TypeError("ENTRY was submitted more than once")
                                else:
                                    configuration[parsed_line[0]] = (parsed_line[1][0], parsed_line[1][1])
                            except ValueError:
                                raise ValueError("ENTRY must be submitted in the format 'ENTRY=number,number'")
                        elif parsed_line[0] == "EXIT":
                            try:
                                parsed_line[1] = [int(n.strip()) for n in parsed_line[1].split(",")]
                                if len(parsed_line[1]) != 2 or parsed_line[1][0] < 0 or parsed_line[1][1] < 0:
                                    raise TypeError("Wrong EXIT input for  return _parse_int(raw, kmat")
                                elif "EXIT" in configuration.keys():
                                    raise TypeError("EXIT was submitted more than once")
                                else:
                                    configuration[parsed_line[0]] = (parsed_line[1][0], parsed_line[1][1])
                            except ValueError:
                                raise ValueError("EXIT must be submitted in the format 'EXIT=number,number'")
                        elif parsed_line[0] == "OUTPUT_FILE":
                            if "OUTPUT_FILE" in configuration.keys():
                                    raise TypeError("OUTPUT_FILE was submitted more than once")
                            try:
                                parsed_line[1] = parsed_line[1].strip()
                                output_file = open(parsed_line[1], "w")
                                output_file.close()
                                configuration[parsed_line[0]] = parsed_line[1]
                            except ValueError:
                                raise ValueError("OUTPUT_FILE must be submitted in the format 'OUTPUT_FILE=file' with appropiate permissions")
                        elif parsed_line[0] == "PERFECT":
                            try:
                                if "PERFECT" in configuration.keys():
                                    raise TypeError("PERFECT was submitted more than once")
                                parsed_line[1] = parsed_line[1].strip().capitalize()
                                if parsed_line[1] == "True":
                                    configuration[parsed_line[0]] = True
                                elif parsed_line[1] == "False":
                                    configuration[parsed_line[0]] = False
                                else:
                                    raise TypeError("PERFECT value can only be true or false")
                            except ValueError:
                                raise ValueError("PERFECT must be submitted in the format 'PERFECT=bool'")
                        elif parsed_line[0] == "SEED":
                            try:
                                parsed_line[1] = int(parsed_line[1])
                                if "SEED" in configuration.keys():
                                    raise TypeError("SEED was submitted more than once")
                                else:
                                    configuration[parsed_line[0]] = parsed_line[1]
                            except ValueError:
                                raise ValueError("SEED must be formatted in the format 'SEED=number'")
        if keys_set == set(configuration.keys()):
            return (configuration, True)
        else:
            raise ValueError(f"Missing informations about {keys_set.difference(configuration)}")
    except Exception as e:
        print(e)
        return (configuration, False)