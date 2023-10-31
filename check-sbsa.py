#!/usr/bin/python3

import bsa

def check_tag(tag, failed):
    try:
        for bsa_test_id in tags_to_tests[tag]["bsa"]:
            if bsa_test_id not in checked_tests["bsa"]:
                checked_tests["bsa"].append(bsa_test_id)

                if status_bsa[bsa_test_id]['status'][cpu] in ["FAIL"]:
                    print(f"- BSA  test {bsa_test_id} for "
                            f"{status_bsa[bsa_test_id]['tags']} "
                            f"({status_bsa[bsa_test_id]['title']}) "
                            f"failed")
                    failed = True

        for sbsa_test_id in tags_to_tests[tag]["sbsa"]:
            if sbsa_test_id not in checked_tests["sbsa"]:
                checked_tests["sbsa"].append(sbsa_test_id)

                if status_sbsa[sbsa_test_id]['status'][cpu] in ["FAIL"]:
                    print(f"- SBSA test {sbsa_test_id} for "
                        f"{status_sbsa[sbsa_test_id]['tags']} "
                        f"({status_sbsa[sbsa_test_id]['title']}) failed")
                    failed = True
    except KeyError:
        pass

    return failed


def check_sbsa_level(cpu, level, previous_level_result):
    failed = previous_level_result

    print(f"Checking SBSA level {level} for {cpu}")

    for category in xbsa_checklist:
        for group in xbsa_checklist[category]["groups"]:
            for rule in xbsa_checklist[category]["groups"][group]["rules"]:
                if rule["required"]["sbsa"][level]:
                    failed = check_tag(rule["tag"], failed)

    if not failed:
        print(f"SBSA level {level} for {cpu}: no failures found")

    return failed


# some tests lists several tags and we do want to show it once
checked_tests = {"bsa": [], "sbsa": []}

status_bsa, status_sbsa, xbsa_checklist = bsa.load_yamls()
tags_to_tests = bsa.create_map_tags_to_tests(status_bsa, status_sbsa)

# SBSA Level 3 requires Arm v8.0
# SBSA Level 4 requires Arm v8.3
# SBSA Level 5 requires Arm v8.4
# SBSA Level 6 requires Arm v8.5/9.0
# SBSA Level 7 requires Arm v8.6/9.1

cpus = {
#   "core name":   sbsa level
    "cortex-a57":  3,
    "cortex-a72":  3,
    "neoverse-n1": 3,
    "neoverse-v1": 5,
    "neoverse-n2": 6,
    "max":         99 }

for cpu in cpus:

    level_result = False
    info_given = False
    checked_tests["bsa"].clear()
    checked_tests["sbsa"].clear()

    for level in range(3, 8):

        if (cpus[cpu] < level):
            if not info_given:
                print(f"{cpu} is too old for SBSA level {level} and above")
                info_given = True
            continue

        level_result = check_sbsa_level(cpu, level, level_result)
        print("")

    print("----------------------------------------")
