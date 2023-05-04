#!/usr/bin/python3

import sys
import yaml

with open("status-bsa.yml", encoding="utf-8") as yml:
    status_bsa = yaml.safe_load(yml)

if len(sys.argv) < 3:
    print("Give me: logfile corename")
    sys.exit(-1)

core_name = sys.argv[2]

start_parsing = False

with open(sys.argv[1], encoding="utf-8") as bsa_acs_log:

    test_id = 0
    test_title = ""
    while True:
        line = bsa_acs_log.readline()

        if not start_parsing and "Starting PE tests" in line:
            start_parsing = True

        if start_parsing:
            if "START" in line:
                test_id, test_title = line.removesuffix(
                    "START\n").strip().split(" : ")
                test_id = int(test_id)
                try:
                    tmp = status_bsa[test_id]
                except KeyError:
                    status_bsa[test_id] = {"tags": "", "title": "",
                                           "status": {core_name: ""}}

            if test_id and line.strip().startswith(("B_", "ITS_", "PCI_")):
                test_tags = line.strip()
                status_bsa[test_id]["tags"] = test_tags
                status_bsa[test_id]["title"] = test_title

            if 'Result:' in line:
                result = line.split(':')[-1].strip()
                status_bsa[test_id]["status"][core_name] = result

            if line.strip().startswith("Total Tests run"):
                break

with open("status-bsa.yml", "w", encoding="utf-8") as yml:
    yaml.dump(status_bsa, yml)
