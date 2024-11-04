#!/usr/bin/python3

import argparse
import os
import random
import string
import sys
import yaml

from pprint import pprint

# for plugging pcie devices
chassis = 0

qemu_args = [
    "bin/qemu-system-aarch64",
    "-monitor", "telnet::45454,server,nowait",
    "-serial", "stdio"
]


def parse_args():

    parser = argparse.ArgumentParser(description="Run virtual machine.")

    parser.add_argument("--cmd", help="command to run in EFI shell")
    parser.add_argument("--cpu", default="neoverse-n2",
                        help="cpu core to use")
    parser.add_argument("--gdb", action="store_true",
                        help="wait for GDB connection")
    parser.add_argument("--gfx", action="store_true",
                        help="open window with graphics output")
    parser.add_argument("--no-reset", action="store_true",
                        help="do not shutdown after running EFI command")
    parser.add_argument("--numa", action="store_true",
                        help="use NUMA configation")
    parser.add_argument("--os",
                        help="select OS to attach")
    parser.add_argument("--pcie", help="add some PCIe cards",
                        action="store_true")
    parser.add_argument("--secure", action="store_true",
                        help="")
    parser.add_argument("--smp", help="amount of cpu cores", default=4)
    parser.add_argument("--virt", action="store_true",
                        help='use "virt" instead of "sbsa-ref"')

    return parser.parse_args()


def handle_uefi_command(command, no_reset):
    script = f"""
              mode 100 31
              pci
              {command}
              """

    # we shutdown by default
    if not no_reset:
        script += ("reset -c\n")

    with open("disks/virtual/startup.nsh", "w") as startup:
        startup.write(script)

    print("EFI startup script:")
    print(script, flush=True)

def add_drive(drive_file, drive_type="", media="", drive_format="raw",
              drive_id=""):
    drive_extra = ""
    if drive_type:
        drive_extra = f",if={drive_type}"

    if media:
        drive_extra += ",media=cdrom"
    else:
        drive_extra += ",snapshot=on"

    if drive_id:
        drive_extra += f",id={drive_id}"

    qemu_args.extend(["-drive",
                     f"file={drive_file},format={drive_format}{drive_extra}"])


def add_firmware(is_it_virt):
    if is_it_virt:
        add_drive("firmware/VIRT_FLASH0.fd", "pflash")
        add_drive("firmware/VIRT_FLASH1.fd", "pflash")
    else:
        add_drive("firmware/SBSA_FLASH0.fd", "pflash")
        add_drive("firmware/SBSA_FLASH1.fd", "pflash")


def add_machine(is_it_virt):
    if is_it_virt:
        qemu_args.extend(["-machine", "virt,iommu=smmuv3,gic-version=max"])
        # virt does not have USB host controller
        add_device("qemu-xhci,id=usb")
        add_device("ahci")
    else:
        qemu_args.extend(["-machine", "sbsa-ref"])


def add_cpu(cpu_type, is_it_numa, smp):
    global chassis

    qemu_args.extend(["-cpu", cpu_type])

    if not is_it_numa:
        qemu_args.extend(["-smp", f"{str(smp)}", "-m", "8G"])
    else:
        qemu_args.extend([
                        "-smp", f"{smp},sockets={smp},maxcpus={smp}",
                        "-m", "4G,slots=2,maxmem=5G",
                        "-object", "memory-backend-ram,size=1G,id=m0",
                        "-object", "memory-backend-ram,size=3G,id=m1",
                        "-numa", "node,nodeid=0,cpus=0-1,memdev=m0",
                        "-numa", "node,nodeid=1,cpus=2,memdev=m1",
                        "-numa", "node,nodeid=2,cpus=3"])

        qemu_args.extend([
            "-device", "pxb-pcie,id=npxb1,bus_nr=64,numa_node=1",
                "-device", f"pcie-root-port,id=nroot_port3,bus=npxb1,chassis={chassis},slot=0",
                "-device", "sdhci-pci,bus=nroot_port3,id=nsdhci",
                "-device", f"pcie-root-port,id=nroot_port4,bus=npxb1,chassis={chassis + 1},slot=0",
                "-device", "igb,bus=nroot_port4,id=nigb",
            "-device", "pxb-pcie,id=npxb2,bus_nr=128,numa_node=2,bus=pcie.0",
                "-device", "pcie-pci-bridge,id=npci,bus=npxb2",
                "-device", "es1370,bus=npci,addr=9,id=nes1370",
                "-device", "e1000,bus=npci,addr=10,id=ne1000",
                "-device", f"pcie-root-port,id=nroot_port_for_ahci,bus=npxb2,chassis={chassis + 2},slot=0",
                "-device", "ahci,bus=nroot_port_for_ahci,id=nahci"
                ])

        chassis += 3

def add_some_pcie():
    global chassis

    add_pcie("igb")

    qemu_args.extend([
     "-device", f"pcie-root-port,id=root_port_for_switch1,chassis={chassis},slot=12",
       "-device", "x3130-upstream,id=upstream_port1,bus=root_port_for_switch1",
       "-device", f"xio3130-downstream,id=downstream_port1,bus=upstream_port1,chassis={chassis + 1},slot=20",
         "-device", "pcie-pci-bridge,id=pci,bus=downstream_port1",
            "-device", "es1370,bus=pci,addr=9,id=es1370",
            "-device", "e1000,bus=pci,addr=10,id=e1000",
            "-device", f"pci-bridge,bus=pci,addr=13,id=pci-pci,chassis_nr={chassis + 2}",
              "-device", "ac97,bus=pci-pci,addr=12",
       "-device", f"xio3130-downstream,id=downstream_port2,bus=upstream_port1,chassis={chassis + 3},slot=21",
         "-device", "igb,bus=downstream_port2,id=igb2",
     ])

    chassis += 4


def add_nvme(disk_image):
    drive_id = "".join(random.choices(string.ascii_letters, k=5))

    add_pcie(f"nvme,drive={drive_id},serial={drive_id}")

    add_drive(disk_image, drive_type="none", drive_id=drive_id)


def add_device(device_name):
    qemu_args.extend(["-device", device_name])


def add_usb_devices():
    add_device("usb-kbd")
    add_device("usb-tablet")
    # FreeBSD prefers mouse over tablet
    add_device("usb-mouse")


def add_os_drive(os_name):
    if os_name is None:
        return

    with open("os.yml") as yml:
        os_data = yaml.safe_load(yml)

    if os_name not in os_data:
        print(f"Selected OS: {os_name} is not defined!")
        sys.exit(-1)

    if os_data[os_name]["file"].endswith(".iso"):
        add_drive(os_data[os_name]["file"], "", "cdrom")
    elif os_data[os_name]["file"].endswith(".qcow2"):
        add_drive(os_data[os_name]["file"], drive_format="qcow2")
    else:
        add_drive(os_data[os_name]["file"])

    if "reset" in os_data[os_name] and os_data[os_name]["reset"]:
        qemu_args.append("--no-reboot")


def enable_graphics_window(is_gfx):
    if is_gfx:
        qemu_args.extend(["-display", "gtk,show-tabs=on"])
    else:
        qemu_args.append("-nographic")


def enable_gdb(is_gdb):
    if is_gdb:
        qemu_args.extend(["-s", "-S"])


def show_args():
    prev_arg = qemu_args[0]

    print("QEMU command arguments:\n")
    for arg in qemu_args:
        try:
            if arg.startswith("-") and prev_arg.startswith("-"):
                print(prev_arg)
            elif arg.startswith("-"):
                pass
            elif prev_arg.startswith("-"):
                print(f"{prev_arg} {arg}")
            else:
                print(arg)
            prev_arg = arg
        except AttributeError:
            print(f"ERROR: prev_arg:{prev_arg} arg:{arg}")

    print("", flush=True)


def add_pcie(card_name, add_root_port=True):
    global chassis

    bus = ""
    if add_root_port:
        rpid = "".join(random.choices(string.ascii_letters, k=5))
        qemu_args.extend(["-device",
                         f"pcie-root-port,id={rpid},slot=0,chassis={chassis}"])
        chassis += 1
        bus = f",bus={rpid}"

    qemu_args.extend(["-device", f"{card_name}{bus}"])


def boot_sbsa_ref():
    args = parse_args()

    # drop EFI shell autostart script
    if os.path.exists("disks/virtual/startup.nsh"):
        os.remove("disks/virtual/startup.nsh")

    add_firmware(args.virt)
    add_machine(args.virt)

    if args.pcie:
        add_some_pcie()

    nvme_drive = "disks/nvme.img"

    if os.path.exists(nvme_drive):
        add_nvme(nvme_drive)

    add_cpu(args.cpu, args.numa, args.smp)
    add_usb_devices()
    enable_graphics_window(args.gfx)
    enable_gdb(args.gdb)
    add_os_drive(args.os)

    add_drive("fat:ro:disks/virtual")

    show_args()

    if args.cmd:
        handle_uefi_command(args.cmd, args.no_reset)

    if not args.no_reset:
        qemu_args.extend(["--no-reboot"])

    os.execv(qemu_args[0], qemu_args)

    try:
        os.remove("disks/virtual/startup.nsh")
    except FileNotFoundError:
        pass


if __name__ == '__main__':
    boot_sbsa_ref()
