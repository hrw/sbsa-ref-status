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

    for bsa_test_id in sbsa_level_checklist[level]["bsa"]:
        if status_bsa[bsa_test_id]['status'][cpu] in ["FAIL"]:
            print(f"- BSA  test {bsa_test_id} for "
                  f"{status_bsa[bsa_test_id]['tags']} "
                  f"({status_bsa[bsa_test_id]['title']}) failed")
            failed = True

    for sbsa_test_id in sbsa_level_checklist[level]["sbsa"]:
        if status_sbsa[sbsa_test_id]['status'][cpu] in ["FAIL"]:
            print(f"- SBSA test {sbsa_test_id} for "
                  f"{status_sbsa[sbsa_test_id]['tags']} "
                  f"({status_sbsa[sbsa_test_id]['title']}) failed")
            failed = True

    if not failed:
        print(f"SBSA level {level} for {cpu}: PASS")

    return failed


for cpu in ["cortex-a57", "cortex-a72", "neoverse-n1", "max"]:

    level_result = False
    for level in range(3, 8):
        level_result = check_sbsa_level(cpu, level, level_result)
        print("")

    print("----------------------------------------")
