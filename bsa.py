import yaml

def create_map_tags_to_tests(status_bsa, status_sbsa):
    # create a map of (S)BSA tag to tests
    tags_to_tests = {}

    for test in status_bsa:
        for tag in status_bsa[test]["tags"].split(","):
            tag = tag.strip()
            if tag not in tags_to_tests:
                tags_to_tests[tag] = {"bsa": [], "sbsa": [], "acs_only": True}

            tags_to_tests[tag]["bsa"].append(test)

    for test in status_sbsa:
        for tag in status_sbsa[test]["tags"].split(','):
            tag = tag.strip()
            if tag not in tags_to_tests:
                tags_to_tests[tag] = {"bsa": [], "sbsa": [], "acs_only": True}

            tags_to_tests[tag]["sbsa"].append(test)

    return tags_to_tests


def load_yamls():
    with open("xbsa-checklist.yml", encoding="utf-8") as yml:
        xbsa_checklist = yaml.safe_load(yml)

    with open("status-bsa.yml", encoding="utf-8") as yml:
        status_bsa = yaml.safe_load(yml)

    with open("status-sbsa.yml", encoding="utf-8") as yml:
        status_sbsa = yaml.safe_load(yml)

    return status_bsa, status_sbsa, xbsa_checklist
