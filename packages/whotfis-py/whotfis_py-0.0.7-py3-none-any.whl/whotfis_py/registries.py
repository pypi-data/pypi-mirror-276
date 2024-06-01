from . import result

ARIN = "-a"
APNIC = "-A"
ABUSE = "-b"
AFRINIC = "-f"
USMILITARY = "-g"
INTERNIC = "-i"
IANA = "-I"
KRNIC = "-k"
LACNIC = "-l"
RIPE = "-r"
RADB = "-m"
CUSTOM = "-h"


def create_radb_result():
    return result.radb_result()


def create_ripe_result():
    return result.ripe_result()


def create_lacnic_result():
    return result.lacninc_result()


def create_custom_result():
    return result.custom_result()


factories = {
    RADB: create_radb_result,
    RIPE: create_ripe_result,
    LACNIC: create_lacnic_result,
    CUSTOM: create_custom_result
}

raw_parser = {
    RADB: lambda raw_data: raw_data.split("\n\n")[:-1],
    RIPE: lambda raw_data: [raw_data.split("\n\n")[0]],
    LACNIC: lambda raw_data: [raw_data],
    CUSTOM: lambda raw_data: [raw_data]
}

errors = {
    LACNIC: [
        "Unallocated and unassigned in LACNIC block:",
        "No match for"
    ],
    RADB: [],
    RIPE: [],
    ARIN: [],
    APNIC: [],
    ABUSE: [],
    AFRINIC: [],
    USMILITARY: [],
    INTERNIC: [],
    IANA: [],
    KRNIC: [],
    CUSTOM: []
}

infos = {
    LACNIC: "whois.lacnic.net accepts only direct match queries.\n"
            "Types of queries are: POCs, ownerid, CIDR blocks, IP\n"
            "and AS numbers.",
    RADB: "",
    RIPE: "",
    ARIN: "",
    APNIC: "",
    ABUSE: "",
    AFRINIC: "",
    USMILITARY: "",
    INTERNIC: "",
    IANA: "",
    KRNIC: "",
    CUSTOM: ""
}

appendable = {
    LACNIC: ["Comment"],
    RADB: ["remarks"],
    RIPE: ["remarks"],
    ARIN: [],
    APNIC: [],
    ABUSE: [],
    AFRINIC: [],
    USMILITARY: [],
    INTERNIC: [],
    IANA: [],
    KRNIC: [],
    CUSTOM: []
}
