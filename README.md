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

Status information is split to core names. Supported cpu cores are:
- Cortex-A57/A72 are Arm v8.0 so they lack many extensions
- Neoverse-N1 is Arm v8.2
- Neoverse-V1 is Arm v8.4
- Neoverse-N2 is Arm v9.0
- max has everything QEMU supports


# Boot sbsa-ref script

The "boot-sbsa-ref-sh" shell script has several arguments:

| Argument | Default       | Description
|      --- | ---           | ---
| --cpu=   | neoverse-v1   | allows to choose cpu core
| --virt   |               | allows to boot "virt" instead of "sbsa-ref" (requires own firmware files)
| --no-its |               | removes all PCIe nodes requiring GIC ITS (handy for simple systems or older QEMU)
| --gdb    |               | makes QEMU wait for GDB connection
| --cmd=   |               | provides EFI command to run in UEFI shell (in 100x31 text mode)
| --reset  |               | adds 'reset -c' command to be run after "--cmd" command to quit QEMU
| --gfx    |               | open window with graphics card output
| --os=    |               | allows to run OS installer (Alpine, CentOS Stream 8/9, Debian, Fedora, FreeBSD, NetBSD 9/10, OpenBSD, RHEL 9)

OS installer images need to be fetched first into "disks/" directory. For NetBSD 9 and OpenBSD disk images are used, other OSes use ISO files.

Virt machine gets SMMUv3 and newer GIC to be closer to SBSA Reference Platform. Also XHCI usb controller is added.


# Firmware files

In "firmware" directory I placed several firmware blobs (compressed with xz so
unpack them before use):

| filename                          | Platform Version | GIC ITS | USB   |
|    ---                            | :---:            |:---:    | :---: |
| 202109-tfa2.5-SBSA_FLASH0.fd.xz   | 0.0              | -       | EHCI  |
| its-ehci-SBSA_FLASH0.fd.xz        | 0.3              | ✔       | EHCI  |
| SBSA_FLASH0.fd.xz                 | 0.3              | ✔       | XHCI  | 

Notes:

- Firmware which exposes EHCI controller does not give working USB. BSD systems may refuse to boot.
- GIC ITS also exposes SMMU and allows complex PCI Express setup.
