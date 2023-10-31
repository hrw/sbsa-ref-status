#!/usr/bin/python3

from datetime import datetime, UTC
from jinja2 import Environment, FileSystemLoader

import bsa





def handle_checklist():

    checklist = []

    for category in xbsa_checklist:
        for group in xbsa_checklist[category]["groups"]:
            for rule in xbsa_checklist[category]["groups"][group]["rules"]:

                # not every entry from checklist has ACS tests
                try:
                    tests = tags_to_tests[rule["tag"]]
                    # this tag is present in BSA/SBSA spec, not only in ACS
                    tags_to_tests[rule["tag"]]["acs_only"] = False
                except KeyError:
                    tests = {"bsa": [], "sbsa": []}

                checklist.append({
                    'category': xbsa_checklist[category]["name"],
                    'group': xbsa_checklist[category]["groups"][group]["name"],
                    'tag': rule["tag"],
                    'bsa': rule["required"]["bsa"],
                    'sbsa': rule["required"]["sbsa"],
                    'tests': tests,
                })

    for tag in sorted(tags_to_tests.keys()):
        if tags_to_tests[tag]["acs_only"]:
            # we want to display it at the end on checklist
            entry = {
                'category': "ACS only tests",
                'group': "ACS",
                'tag': tag,
                'tests': tags_to_tests[tag],
                'bsa': [],
                'sbsa': []
            }

            if tags_to_tests[tag]["bsa"]:
                entry["bsa"] = True
            if tags_to_tests[tag]["sbsa"]:
                entry["sbsa"] = {
                    3: False,
                    4: False,
                    5: False,
                    6: False,
                    7: False
                }
                for test in tags_to_tests[tag]["sbsa"]:
                    sbsa_level = int(status_sbsa[test]["level"])

                    for level in range(sbsa_level, 8):
                        entry["sbsa"][level] = True

            checklist.append(entry)

    return checklist

def generate_html_file(checklist):

    file_loader = FileSystemLoader("templates")
    env = Environment(loader=file_loader,
                      trim_blocks=True,
                      lstrip_blocks=True)

    template = env.get_template("bsa-sbsa.html.j2")

    output = template.render(
        generate_time=datetime.strftime(datetime.now(UTC), 
                                        "%d %B %Y %H:%M"),
        checklist=checklist,
        status_bsa=status_bsa,
        status_sbsa=status_sbsa,
    )
    print(output)


if __name__ == "__main__":
    status_bsa, status_sbsa, xbsa_checklist = bsa.load_yamls()
    tags_to_tests = bsa.create_map_tags_to_tests(status_bsa, status_sbsa)
    checklist = handle_checklist()
    generate_html_file(checklist)
