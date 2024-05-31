from . import registries


def print_error(error, registry):
    print(error + "\n")
    print(registries.infos[registry])


def parse(raw_data, registry):
    if registry not in registries.raw_parser:
        registry = registries.CUSTOM

    results = registries.raw_parser[registry](raw_data)
    parsed_results = []

    for result in results:
        # Generate empty result template based on registry
        template = registries.factories[registry]()
        # Get template parameters
        fields = dir(template)

        # Iterate over result lines
        for line in result.split("\n"):
            # Obtain tuple for format key:value
            key_value = line.split(":")
            # Replace dash to underscore to match python class syntax
            key = key_value[0].strip().replace("-", "_")
            # Check the tuple has actually a key:value shape and
            # that the key belongs to the model if the registry is not CUSTOM
            if len(key_value) > 1 and (key in fields or registry is registries.CUSTOM):
                # Get the value
                value = key_value[1].strip()
                # Get already assigned value if present
                attr_value = getattr(template, key) if hasattr(template, key) else None
                if attr_value is not None:
                    # Check if the key can be appendable or a new instance must be added
                    if key in registries.appendable[registry]:
                        value = attr_value + '\n' + value
                    else:
                        # Continue increasing keys to determine how many key duplicates are present
                        while hasattr(template, key):
                            previous_index = int(key[-1]) if key[-2] == "_" and key[-1].isnumeric() else None
                            if previous_index is None:
                                # Create first duplicate
                                key = str(key) + "_2"
                            else:
                                # Create nth duplicate
                                key = key[:-1] + str(previous_index + 1)
                setattr(template, key, value)
            else:
                for error in registries.errors[registry]:
                    if error in line:
                        print_error(line, registry)

        parsed_results.append(template)

    return parsed_results
