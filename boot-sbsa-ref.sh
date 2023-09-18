#!/bin/bash

CPU="neoverse-v1"

for i in "$@"; do
	case $i in
		--cmd=*)
			CMD="${i#*=}"
			shift
			;;
		--cpu=*)
			CPU="${i#*=}"
			shift
			;;
		--no-its)
			NOITS=1
			shift
			;;
		--reset)
			RESET=1
			shift
			;;
		--gfx)
			GFX=1
			shift
			;;
		--gdb)
			GDB=1
			shift
			;;
		-*|--*)
			echo "Unknown option $i"
			exit 1
			;;
		*)
			;;
	esac
done

rm -f disks/virtual/startup.nsh

if [ ! -z "$CMD" ]; then
        echo "mode 100 31"  > disks/virtual/startup.nsh
        echo "pci"         >> disks/virtual/startup.nsh
        echo "$CMD"        >> disks/virtual/startup.nsh
    if [ ! -z "$RESET" ]; then
        echo "reset -c"    >> disks/virtual/startup.nsh
    fi
fi

common_qemu_args=(

-machine sbsa-ref
-m 4096
-smp 2
-cpu $CPU

# firmware
-drive if=pflash,file=SBSA_FLASH0.fd,format=raw
-drive if=pflash,file=SBSA_FLASH1.fd,format=raw

# basic disk with EFI apps and generic Debian d-i
-drive file=fat:rw:$PWD/disks/virtual/,format=raw

# full Debian installation
-drive format=raw,file=$PWD/disks/full-debian.hddimg

# Debian install ISO
#-drive if=ide,file=$PWD/../disks/debian-bookworm.iso,format=raw,media=cdrom

# Fedora install ISO
#-drive if=ide,file=$PWD/../disks/Fedora-Server-netinst-aarch64-Rawhide-20230704.n.0.iso,format=raw,media=cdrom

# ServerReady ACS
#  -drive file=../disks/sr_acs_live_image-v23.01_2.0.0_BETA-0.img,format=raw,if=ide

# userspace networking
#-net nic
#-net user

# usb for graphical console
#-usb
-device usb-kbd
-device usb-tablet

-watchdog-action none

# exit instead of rebooting
-no-reboot

# have a way to check internals
-monitor telnet::45454,server,nowait

# output on console
-serial stdio

# Intel network card to have interrupt debugging information
-device igb

# --------------------------------------------------------------------------------------
# some random disks/isos
# --------------------------------------------------------------------------------------

# direct use of USB pendrive
# -drive if=ide,format=raw,file=/dev/sdc

# -drive if=ide,format=raw,media=cdrom,file=disks/debian-bookworm-DI-alpha2-arm64-netinst.iso
# -drive file=disks/alpine-standard-3.17.2-aarch64.iso,format=raw,media=cdrom

# -drive if=ide,format=raw,file=disks/luv-live-image-gpt.img

)

its_pci_setup=(

# --------------------------------------------------------------------------------------
# now some PCIe stuff for system with ITS
# --------------------------------------------------------------------------------------

# 104c:8232 x3130-upstream  
# 1274:5000 es1370          
# 1af4:1044 virtio-rng-pci  
# 1b36:000c pcie-root-port  
# 1b36:000e pcie-pci-bridge 
# 1b36:0010 qemu nvme       
# 8086:10c9 intel igb       
# 8086:2922 ahci            

# PCIe switch with ac97 behind it
-device pcie-root-port,id=root_port_for_switch1,chassis=0,slot=0
  -device x3130-upstream,id=upstream_port1,bus=root_port_for_switch1
    -device xio3130-downstream,id=downstream_port1,bus=upstream_port1,chassis=1,slot=0
      -device ac97,bus=downstream_port1

# NVME card
-device pcie-root-port,id=root_port_for_nvme1,chassis=2,slot=0
 -device nvme,serial=deadbeef,bus=root_port_for_nvme1

# Intel network card
-device pcie-root-port,id=root_port_for_igb,chassis=3,slot=0
  -device igb,bus=root_port_for_igb

# XHCI USB card
-device pcie-root-port,id=root_port_for_xhci,chassis=4,slot=0
  -device qemu-xhci,bus=root_port_for_xhci

# virtio rng
-device pcie-root-port,id=root_port_for_rng,chassis=5,slot=0
  -device virtio-rng-pci,bus=root_port_for_rng

# PCIe-PCI bridge with es1370 behind
-device pcie-root-port,id=root_port_for_pci,chassis=6,slot=0
  -device pcie-pci-bridge,id=pci,bus=root_port_for_pci
    -device es1370,bus=pci,addr=9
    -device e1000,bus=pci,addr=10

# another PCIe bus
 -device pxb-pcie,id=pxb1,bus_nr=1
   -device pcie-root-port,id=root_port_for_ahci,bus=pxb1,chassis=10,slot=0
     -device ahci,bus=root_port_for_ahci
)


if [ -z $NOITS ]; then
	qemu_args="${common_qemu_args[@]} ${its_pci_setup[@]}"
else
	qemu_args="${common_qemu_args[@]}"
fi

if [ ! -z $GDB ]; then
	qemu_args="${qemu_args} -s -S"
fi

if [ -z $GFX ]; then
        qemu_args="${qemu_args} -nographic"
fi


echo "QEMU command line arguments:"
echo "${qemu_args}" | sed -e "s/ -/\n-/g"
echo ""

./code/qemu/build/aarch64-softmmu/qemu-system-aarch64 $qemu_args

if [ ! -z "$CMD" ]; then
        rm disks/virtual/startup.nsh
fi
