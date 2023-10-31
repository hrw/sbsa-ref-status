#!/usr/bin/python3

from datetime import datetime, UTC
from jinja2 import Environment, FileSystemLoader

import yaml

with open("xbsa-checklist.yml", encoding="utf-8") as yml:
    xbsa_checklist = yaml.safe_load(yml)

with open("status-bsa.yml", encoding="utf-8") as yml:
    status_bsa = yaml.safe_load(yml)

with open("status-sbsa.yml", encoding="utf-8") as yml:
    status_sbsa = yaml.safe_load(yml)


def handle_checklist():

    checklist = []

    tag_to_test = {}

    for test in status_bsa:
        for tag in status_bsa[test]["tags"].split(','):
            tag = tag.strip()
            try:
                tag_to_test[tag]["bsa"].append(test)
            except KeyError:
                tag_to_test[tag] = {"bsa": [], "sbsa": [], "acs_only": True}
                tag_to_test[tag]["bsa"].append(test)

    for test in status_sbsa:
        for tag in status_sbsa[test]["tags"].split(','):
            tag = tag.strip()
            try:
                tag_to_test[tag]["sbsa"].append(test)
            except KeyError:
                tag_to_test[tag] = {"bsa": [], "sbsa": [], "acs_only": True}
                tag_to_test[tag]["sbsa"].append(test)

    for category in xbsa_checklist:
        for group in xbsa_checklist[category]["groups"]:
            for rule in xbsa_checklist[category]["groups"][group]["rules"]:

                # not every entry from checklist has ACS tests
                try:
                    tests = tag_to_test[rule["tag"]]
                    # this tag is present in BSA/SBSA spec, not only in ACS
                    tag_to_test[rule["tag"]]["acs_only"] = False
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

    for tag in sorted(tag_to_test.keys()):
        if tag_to_test[tag]["acs_only"]:
            # we want to display it at the end on checklist
            entry = {
                'category': "ACS only tests",
                'group': "ACS",
                'tag': tag,
                'tests': tag_to_test[tag],
                'bsa': [],
                'sbsa': []
            }

            if tag_to_test[tag]["bsa"]:
                entry["bsa"] = True
            if tag_to_test[tag]["sbsa"]:
                entry["sbsa"] = {
                    3: False,
                    4: False,
                    5: False,
                    6: False,
                    7: False
                }
                for test in tag_to_test[tag]["sbsa"]:
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
    checklist = handle_checklist()
    generate_html_file(checklist)
