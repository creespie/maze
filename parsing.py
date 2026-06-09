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
                                if parsed_line[1] < 1 or "WIDTH" in configuration.keys():
                                    raise ValueError("Wrong WIDTH input format")
                                else:
                                    configuration[parsed_line[0]] = parsed_line[1]
                            except Exception:
                                raise ValueError("Wrong WIDTH input format")
                        elif parsed_line[0] == "HEIGHT":
                            try:
                                parsed_line[1] = int(parsed_line[1])
                                if parsed_line[1] < 1 or "HEIGHT" in configuration.keys():
                                    raise ValueError("Wrong HEIGHT input format")
                                else:
                                    configuration[parsed_line[0]] = parsed_line[1]
                            except Exception:
                                raise ValueError("Wrong HEIGHT input format")
                        elif parsed_line[0] == "ENTRY":
                            try:
                                parsed_line[1] = [int(n.strip()) for n in parsed_line[1].split(",")]
                                if len(parsed_line[1]) != 2 or parsed_line[1][0] < 0 or parsed_line[1][1] < 0 or "ENTRY" in configuration.keys():
                                    raise ValueError("Wrong ENTRY input format")
                                else:
                                    configuration[parsed_line[0]] = (parsed_line[1][0], parsed_line[1][1])
                            except Exception:
                                raise ValueError("Wrong ENTRY input format")
                        elif parsed_line[0] == "EXIT":
                            try:
                                parsed_line[1] = [int(n.strip()) for n in parsed_line[1].split(",")]
                                if len(parsed_line[1]) != 2 or parsed_line[1][0] < 0 or parsed_line[1][1] < 0 or "EXIT" in configuration.keys():
                                    raise ValueError("Wrong EXIT input format")
                                else:
                                    configuration[parsed_line[0]] = (parsed_line[1][0], parsed_line[1][1])
                            except Exception:
                                raise ValueError("Wrong EXIT input format")
                        elif parsed_line[0] == "OUTPUT_FILE":
                            try:
                                if "OUTPUT_FILE" in configuration.keys():
                                    raise ValueError("Wrong OUTPUT FILE input format")
                                parsed_line[1] = parsed_line[1].strip()
                                output_file = open(parsed_line[1], "w")
                                output_file.close()
                                configuration[parsed_line[0]] = parsed_line[1]
                            except Exception:
                                raise ValueError("Wrong OUTPUT FILE input format")
                        elif parsed_line[0] == "PERFECT":
                            if "PERFECT" in configuration.keys():
                                raise ValueError("Wront PERFECT input format")
                            parsed_line[1] = parsed_line[1].strip().capitalize()
                            if parsed_line[1] == "True":
                                configuration[parsed_line[0]] = True
                            elif parsed_line[1] == "False":
                                configuration[parsed_line[0]] = False
                            else:
                                raise ValueError("Wront PERFECT input format")
                        elif parsed_line[0] == "SEED":
                            try:
                                parsed_line[1] = int(parsed_line[1])
                                if "SEED" in configuration.keys():
                                    raise ValueError("Wrong SEED input format")
                                else:
                                    configuration[parsed_line[0]] = parsed_line[1]
                            except Exception:
                                raise ValueError("Wrong SEED input format")
        if keys_set == set(configuration.keys()):
            return (configuration, True)
        else:
            raise ValueError("Missing informations")
    except Exception as e:
        print(e)
        return (configuration, False)