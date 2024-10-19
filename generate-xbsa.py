#!/usr/bin/python3

from datetime import datetime, UTC
from jinja2 import Environment, FileSystemLoader

import bsa


def check_tag(tag):
    cpu = "neoverse-n2"
    passed = "?"

    try:
        for bsa_test_id in tags_to_tests[tag]["bsa"]:
            if status_bsa[bsa_test_id]['status'][cpu] not in ["FAIL"]:
                passed = "✔"

        for sbsa_test_id in tags_to_tests[tag]["sbsa"]:
            try:
                if status_sbsa[sbsa_test_id]['skip_for_qemu']:
                    passed = "-"
            except KeyError:
                pass
            match status_sbsa[sbsa_test_id]['status'][cpu]:
                case "FAIL":
                    passed = "-"
                case "SKIPPED":
                    passed = "?"
                case "PASS":
                    passed = "✔"
                case _:
                    pass
    except KeyError:
        pass

    return passed


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
                    'sbsaref': check_tag(rule["tag"]),
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
                'sbsa': [],
                'sbsaref': check_tag(tag),
            }

            if tags_to_tests[tag]["bsa"]:
                entry["bsa"] = True
            if tags_to_tests[tag]["sbsa"]:
                entry["sbsa"] = {
                    3: False,
                    4: False,
                    5: False,
                    6: False,
                    7: False,
                    8: False
                }
                for test in tags_to_tests[tag]["sbsa"]:
                    try:
                        sbsa_level = int(status_sbsa[test]["level"])
                    except ValueError:
                        if "future" == status_sbsa[test]["level"]:
                            sbsa_level = 8

                    for level in range(sbsa_level, 9):
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
        generate_time=datetime.strftime(datetime.now(timezone.utc),
                                        "%d %B %Y %H:%M"),
        checklist=checklist,
        status_bsa=status_bsa,
        status_sbsa=status_sbsa,
        git_repo="sbsa-ref-status",
    )
    print(output)


if __name__ == "__main__":
    status_bsa, status_sbsa, xbsa_checklist = bsa.load_yamls()
    tags_to_tests = bsa.create_map_tags_to_tests(status_bsa, status_sbsa)
    checklist = handle_checklist()
    generate_html_file(checklist)
