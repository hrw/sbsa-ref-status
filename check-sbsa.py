#!/usr/bin/python3

import yaml

from sbsa_checklist import sbsa_level_checklist

with open("status-bsa.yml", encoding="utf-8") as yml:
    status_bsa = yaml.safe_load(yml)

with open("status-sbsa.yml", encoding="utf-8") as yml:
    status_sbsa = yaml.safe_load(yml)


def check_sbsa_level(cpu, level, previous_level_result):
    failed = previous_level_result

    print(f"Checking SBSA level {level} for {cpu}")

    # some tests lists several tests and we do want to show it once
    checked_tests = []

    # SBSA Level 4 does not lists BSA tags
    if sbsa_level_checklist[level]["bsa"] is not None:
        for bsa_tag in sbsa_level_checklist[level]["bsa"]:
            try:
                for bsa_test_id in tags_to_tests[bsa_tag]["bsa"]:
                    if bsa_test_id not in checked_tests:
                        checked_tests.append(bsa_test_id)

                        if status_bsa[bsa_test_id]['status'][cpu] in ["FAIL"]:
                            print(f"- BSA  test {bsa_test_id} for "
                                  f"{status_bsa[bsa_test_id]['tags']} "
                                  f"({status_bsa[bsa_test_id]['title']}) "
                                  f"failed")
                            failed = True
            except KeyError:
                pass

    # some tests lists several tests and we do want to show it once
    checked_tests = []

    for sbsa_tag in sbsa_level_checklist[level]["sbsa"]:
        try:
            for sbsa_test_id in tags_to_tests[sbsa_tag]["sbsa"]:
                if sbsa_test_id not in checked_tests:
                    checked_tests.append(sbsa_test_id)

                    if status_sbsa[sbsa_test_id]['status'][cpu] in ["FAIL"]:
                        print(f"- SBSA test {sbsa_test_id} for "
                              f"{status_sbsa[sbsa_test_id]['tags']} "
                              f"({status_sbsa[sbsa_test_id]['title']}) failed")
                        failed = True
        except KeyError:
            pass

    if not failed:
        print(f"SBSA level {level} for {cpu}: PASS")

    return failed


# create a map of (S)BSA tag to tests
tags_to_tests = {}

for test in status_bsa:
    for tag in status_bsa[test]["tags"].split(","):
        tag = tag.strip()
        if tag not in tags_to_tests:
            tags_to_tests[tag] = {"bsa": [], "sbsa": []}

        tags_to_tests[tag]["bsa"].append(test)

for test in status_sbsa:
    for tag in status_sbsa[test]["tags"].split(','):
        tag = tag.strip()
        if tag not in tags_to_tests:
            tags_to_tests[tag] = {"bsa": [], "sbsa": []}

        tags_to_tests[tag]["sbsa"].append(test)

for cpu in ["cortex-a57", "cortex-a72", "neoverse-n1", "max"]:

    level_result = False
    for level in range(3, 8):
        level_result = check_sbsa_level(cpu, level, level_result)
        print("")

    print("----------------------------------------")
