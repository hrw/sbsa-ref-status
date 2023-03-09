# Status of SBSA Reference Platform in QEMU

This repository contains my attempt to track status of SBSA Reference Platform
in QEMU ("-M sbsa-ref") in a bit more organized way.


# Scripts

There are some scripts provided:

| Name                   | Function
|                      - | - 
| boot-sbsa-ref.sh       | Boot QEMU with several options enabled.
| check-sbsa.py          | Check "sbsa-ref" against SBSA checklists.
| parse-bsa-log.py       | Parse BSA ACS logs. Needs verbose logs and core name.
| parse-sbsa-log.py      | Parse SBSA ACS logs. Needs verbose logs, core name and SBSA level.
| run-gathering-logs.sh  | Gather (S)BSA ACS logs.
| run-parsing-logs.sh    | Parse all (S)BSA ACS logs.


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


# External patches

This work was done using some external patches.


## QEMU

- target/arm: Add Neoverse-N1 registers from Chen Baozi
- target/arm: Add ITS support from Shashi Mallela


## EDK2

Both patches I got from Shashi Mallela:

- add ITS support
- add SMMU support


## TF-A

Here are my patches:

- [feat(qemu): allow to use hardware assisted coherency](https://review.trustedfirmware.org/c/TF-A/trusted-firmware-a/+/17772)
- [fix(qemu-sbsa): enable FGT](https://review.trustedfirmware.org/c/TF-A/trusted-firmware-a/+/19459)
- not shared yet patch to add Neoverse-N1 into qemu_sbsa platform
