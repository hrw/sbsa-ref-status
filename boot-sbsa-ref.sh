#!/bin/bash

CPU="neoverse-v1"
MACHINE="sbsa-ref"

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
		--virt)
			MACHINE="virt"
			shift
			;;
		--os=*)
			OS="${i#*=}"
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

if [ $MACHINE == "sbsa-ref" ]; then
	firmware_args=(

# firmware
-drive if=pflash,file=firmware/SBSA_FLASH0.fd,format=raw
-drive if=pflash,file=firmware/SBSA_FLASH1.fd,format=raw

		)
elif [ $MACHINE == "virt" ]; then
	firmware_args=(

# firmware
-drive if=pflash,file=firmware/VIRT_FLASH0.fd,format=raw
-drive if=pflash,file=firmware/VIRT_FLASH1.fd,format=raw

		)
MACHINE_OPTIONS=",iommu=smmuv3,gic-version=max"

fi


common_qemu_args=(

-machine ${MACHINE}${MACHINE_OPTIONS}
-m 4096
-smp 2
-cpu $CPU

# basic disk with EFI apps and generic Debian d-i
-drive file=fat:rw:$PWD/disks/virtual/,format=raw

# full Debian installation
-drive format=raw,file=$PWD/disks/full-debian.hddimg


# ServerReady ACS
#  -drive file=../disks/sr_acs_live_image-v23.01_2.0.0_BETA-0.img,format=raw,if=ide

# userspace networking
#-net nic
#-net user

# usb for graphical console
#-usb
-device usb-kbd
-device usb-tablet
-device usb-mouse

-watchdog-action none

# exit instead of rebooting
#-no-reboot

# have a way to check internals
-monitor telnet::45454,server,nowait

# output on console
-serial stdio

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

# lspci -nn
# 00:00.0 Host bridge [0600]: Red Hat, Inc. QEMU PCIe Host bridge [1b36:0008]
# 00:01.0 Ethernet controller [0200]: Intel Corporation 82574L Gigabit Network Connection [8086:10d3]
# 00:02.0 Display controller [0380]: Device [1234:1111] (rev 02)
# 00:03.0 PCI bridge [0604]: Red Hat, Inc. QEMU PCIe Root port [1b36:000c]
# 00:04.0 PCI bridge [0604]: Red Hat, Inc. QEMU PCIe Root port [1b36:000c]
# 00:05.0 PCI bridge [0604]: Red Hat, Inc. QEMU PCIe Root port [1b36:000c]
# 00:06.0 PCI bridge [0604]: Red Hat, Inc. QEMU PCIe Root port [1b36:000c]
# 00:07.0 PCI bridge [0604]: Red Hat, Inc. QEMU PCIe Root port [1b36:000c]
# 00:08.0 PCI bridge [0604]: Red Hat, Inc. QEMU PCIe Root port [1b36:000c]
# 00:09.0 Host bridge [0600]: Red Hat, Inc. QEMU PCIe Expander bridge [1b36:000b]
# 01:00.0 PCI bridge [0604]: Red Hat, Inc. QEMU PCIe Root port [1b36:000c]
# 02:00.0 SATA controller [0106]: Intel Corporation 82801IR/IO/IH (ICH9R/DO/DH) 6 port SATA Controller [AHCI mode] [8086:2922] (rev 02)
# 03:00.0 Non-Volatile memory controller [0108]: Red Hat, Inc. QEMU NVM Express Controller [1b36:0010] (rev 02)
# 04:00.0 Ethernet controller [0200]: Intel Corporation 82576 Gigabit Network Connection [8086:10c9] (rev 01)
# 05:00.0 USB controller [0c03]: Red Hat, Inc. QEMU XHCI Host Controller [1b36:000d] (rev 01)
# 06:00.0 Unclassified device [00ff]: Red Hat, Inc. Virtio 1.0 RNG [1af4:1044] (rev 01)
# 07:00.0 PCI bridge [0604]: Red Hat, Inc. Device [1b36:000e]
# 08:09.0 Multimedia audio controller [0401]: Ensoniq ES1370 [AudioPCI] [1274:5000]
# 08:10.0 Ethernet controller [0200]: Intel Corporation 82540EM Gigabit Ethernet Controller [8086:100e] (rev 03)
#
# lspci -tv
# -[0000:00]-+-00.0  Red Hat, Inc. QEMU PCIe Host bridge
#            +-01.0  Intel Corporation 82574L Gigabit Network Connection
#            +-02.0  Device 1234:1111
#            +-03.0-[01-02]----00.0-[02]----00.0  Intel Corporation 82801IR/IO/IH (ICH9R/DO/DH) 6 port SATA Controller [AHCI mode]
#            +-04.0-[03]----00.0  Red Hat, Inc. QEMU NVM Express Controller
#            +-05.0-[04]----00.0  Intel Corporation 82576 Gigabit Network Connection
#            +-06.0-[05]----00.0  Red Hat, Inc. QEMU XHCI Host Controller
#            +-07.0-[06]----00.0  Red Hat, Inc. Virtio 1.0 RNG
#            +-08.0-[07-08]----00.0-[08]--+-09.0  Ensoniq ES1370 [AudioPCI]
#            |                            \-10.0  Intel Corporation 82540EM Gigabit Ethernet Controller
#            \-09.0  Red Hat, Inc. QEMU PCIe Expander bridge

# 104c:8232 x3130-upstream  
# 1274:5000 es1370          
# 1af4:1044 virtio-rng-pci  
# 1b36:000b pxb-pcie
# 1b36:000c pcie-root-port  
# 1b36:000d qemu-xhci
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

# is iso file hdd image?
ISOHDD=0

case $OS in
	"alpine")
		ISO="disks/alpine-standard-3.17.2-aarch64.iso"
		;;
	"centos")
		ISO="disks/CentOS-Stream-9-20230918.0-aarch64-boot.iso"
		;;
	"centos8s")
		ISO="disks/CentOS-Stream-8-aarch64-latest-boot.iso"
		;;
	"debian")
		ISO="disks/debian-12.1.0-arm64-netinst.iso"
		;;
	"fedora")
		ISO="disks/Fedora-Server-netinst-aarch64-39_Beta-1.1.iso"
		;;
	"freebsd")
		ISO="disks/FreeBSD-13.2-RELEASE-arm64-aarch64-bootonly.iso"
		;;
	"freebsd14")
		ISO="disks/FreeBSD-14.0-BETA4-arm64-aarch64-bootonly.iso"
		;;
	"freebsd15")
		ISO="disks/FreeBSD-15.0-CURRENT-arm64-aarch64-20230921-febba4622b60-265435-bootonly.iso"
		;;
	"netbsd")
		ISO="disks/NetBSD-10.0_BETA-evbarm-aarch64.iso"
		;;
	"netbsd9")
		ISO="disks/NetBSD-9.3-evbarm-arm64.img"
		ISOHDD=1
		;;
	"openbsd")
		ISO="disks/openbsd-miniroot73.img"
		ISOHDD=1
		;;
	"rhel")
		ISO="disks/rhel-9.2-aarch64-boot.iso"
		;;
	"sr-acs")
		ISO="disks/SystemReady-ACS-23.09-2.0.0-sr_acs_live_image.img"
		ISOHDD=1
		DISABLE_NO_REBOOT=1
		;;
	*)
		if [ ! -z $OS ]; then
			echo "Unknown OS: >${OS}<"
			exit 1
		fi
		;;
esac

if [ ! -z $ISO ];then
	if [ 0 == $ISOHDD ];then
		ISO="${ISO},media=cdrom"
	else
		ISO="${ISO},format=raw"
	fi
	qemu_args="${qemu_args} -drive file=${ISO}"
fi

# virt does not have USB host controller
if [ $MACHINE == "virt" ]; then
        qemu_args="${qemu_args} -device qemu-xhci,id=usb"
fi

qemu_args="${qemu_args} ${common_qemu_args[@]}"

if [ -z $DISABLE_NO_REBOOT ]; then
	qemu_args="${qemu_args} --no-reboot"
fi

if [ -z $NOITS ]; then
	qemu_args="${qemu_args[@]} ${its_pci_setup[@]}"
fi

if [ ! -z $GDB ]; then
	qemu_args="${qemu_args} -s -S"
fi

if [ -z $GFX ]; then
        qemu_args="${qemu_args} -nographic"
fi

qemu_args="${qemu_args} ${firmware_args[@]}"

echo "QEMU command line arguments:"
echo "${qemu_args}" | sed -e "s/ -/\n-/g"
echo ""

../code/qemu/build/aarch64-softmmu/qemu-system-aarch64 $qemu_args

if [ ! -z "$CMD" ]; then
        rm disks/virtual/startup.nsh
fi
