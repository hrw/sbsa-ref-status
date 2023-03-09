#!/usr/bin/python3

import yaml

with open("status-bsa.yml", encoding="utf-8") as yml:
    status_bsa = yaml.safe_load(yml)

with open("status-sbsa.yml", encoding="utf-8") as yml:
    status_sbsa = yaml.safe_load(yml)

sbsa_level_checklist = {
    3: {
        "bsa": {
            1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13,
            51, 52, 53, 54, 55,
            76,
            102, 103,
            203, 204, 205, 206,
            226, 227, 228,
            301, 302, 305, 306,
            351, 352, 353, 354,
            401, 402, 403, 404, 405,
            501, 502, 503, 504, 505,
            601, 602, 603, 604, 606,
            701, 702
        },
        "sbsa": {
            1, 2, 3, 4,
            1301,
            101,
            701
        }
    },
    4: {
        "bsa": {
        },
        "sbsa": {
            5, 6, 7, 8,
            462
        }
    },
    5: {
        "bsa": {
        },
        "sbsa": {
            9, 10, 11, 12, 12, 14,
            15, 16,
            102
        }
    },
    6: {
        "bsa": {
        },
        "sbsa": {
            18, 19, 20, 21, 22,
            23, 24, 25, 26, 27,
            301
        }
    },
    7: {
        "bsa": {
        },
        "sbsa": {
            28, 29, 30, 31, 32, 33, 34, 35, 36, 37,
        }
    },
}

def check_sbsa_level(cpu, level, previous_level_result):
    failed = previous_level_result

    print(f"Checking SBSA level {level} for {cpu}")

    for bsa_test_id in sbsa_level_checklist[level]["bsa"]:
        if status_bsa[bsa_test_id]['status'][cpu] in ["FAIL"]:
            print(f"- BSA  test {bsa_test_id} for "
                  f"{status_bsa[bsa_test_id]['tags']} failed")
            failed = True

    for sbsa_test_id in sbsa_level_checklist[level]["sbsa"]:
        if status_sbsa[sbsa_test_id]['status'][cpu] in ["FAIL"]:
            print(f"- SBSA test {sbsa_test_id} for "
                  f"{status_sbsa[sbsa_test_id]['tags']} failed")
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
