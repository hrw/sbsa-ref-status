# Status of SBSA Reference Platform in QEMU

This repository contains my attempt to track status of SBSA Reference Platform
in QEMU ("-M sbsa-ref") in a bit more organized way.


# Scripts

There are some scripts to parse (S)BSA ACS logs:

- parse-bsa-log.py
- parse-sbsa-log.py

They expect verbose logs ("-v 1" argument) and core names. SBSA log parser also
wants SBSA level number.


# YAML files

There are two yaml files:

- status-bsa.yml
- status-sbsa.yml

They contain status of (S)BSA ACS runs. Format is simple:

```yaml
31:
  level: '7'
  status:
    cortex-a57: FAIL
    cortex-a72: FAIL
    max: PASS
    neoverse-n1: FAIL
  tags: S_L7PE_04
  title: Checks ASIMD Int8 matrix multiplc
```

There is test number ("31"), it's title, tags assigned in ACS (or not as two
SBSA ACS tests lack such information), SBSA level (only in "status-sbsa.yml"
file) and status.

Status information is split to core names. Cortex-A57/A72 are Arm v8.0 so they
lack many extensions, Neoverse-N1 is Arm v8.2 so have more of them and finally
"max" core has everything QEMU supports.
