#!/usr/bin/python3

import sys
import yaml

with open("status-pcbsa.yml", encoding="utf-8") as yml:
    status_pcbsa = yaml.safe_load(yml)
    if status_pcbsa is None:
        status_pcbsa = {}

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
                # BSA ACS output changed:
                # 1 : Check Arch symmetry across PE         
                #     START
                test_id, test_title = prev_line.strip().split(" : ")
                test_id = int(test_id)
                try:
                    tmp = status_pcbsa[test_id]
                except KeyError:
                    status_pcbsa[test_id] = {"tags": "", "title": "",
                                           "status": {core_name: ""}}

            if test_id and line.strip().startswith(("P_", "B_", "ITS_", "PCI_")):
                test_tags = line.strip()
                status_pcbsa[test_id]["tags"] = test_tags
                status_pcbsa[test_id]["title"] = test_title

            if 'Result:' in line:
                result = line.split(':')[-1].strip()
                status_pcbsa[test_id]["status"][core_name] = result

            if line.strip().startswith("Total Tests run"):
                break

        # we need previous line to extract test id/title
        prev_line = line

with open("status-pcbsa.yml", "w", encoding="utf-8") as yml:
    yaml.dump(status_pcbsa, yml)
