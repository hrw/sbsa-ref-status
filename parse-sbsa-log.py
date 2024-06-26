#!/usr/bin/python3

import sys
import yaml

with open("status-sbsa.yml", encoding="utf-8") as yml:
    status_sbsa = yaml.safe_load(yml)

if len(sys.argv) < 4:
    print("Give me: logfile corename sbsalevel")
    sys.exit(-1)

core_name = sys.argv[2]
sbsa_level = sys.argv[3]

start_parsing = False

with open(sys.argv[1], encoding="utf-8") as sbsa_acs_log:

    test_id = 0
    test_title = ""
    prev_line = False
    while True:
        line = sbsa_acs_log.readline()

        if not start_parsing and "Starting PE tests" in line:
            start_parsing = True

        if start_parsing:
            if "START" in line:
                test_id, test_title = prev_line.removesuffix(
                    "START\n").strip().split(" : ")
                test_id = int(test_id)
                try:
                    tmp = status_sbsa[test_id]
                except KeyError:
                    status_sbsa[test_id] = {"tags": "", "title": "",
                                            "level": 0,
                                            "status": {core_name: ""}}

            if test_id and line.strip().startswith(("B_", "ETE_", "GPU_",
                                                    "IE_", "ITS_",
                                                    "PCI_", "PMU_", "RE_",
                                                    "S_")):
                test_tags = line.strip()
                status_sbsa[test_id]["tags"] = test_tags
                status_sbsa[test_id]["title"] = test_title

            if 'Result:' in line:
                result = line.split(':')[-1].strip()
                if sbsa_level <= status_sbsa[test_id]["level"]:
                    status_sbsa[test_id]["status"][core_name] = result

            if test_id and status_sbsa[test_id]["level"] == 0:
                status_sbsa[test_id]["level"] = sbsa_level

            if line.strip().startswith("Total Tests run"):
                break

        prev_line = line

with open("status-sbsa.yml", "w", encoding="utf-8") as yml:
    yaml.dump(status_sbsa, yml)
