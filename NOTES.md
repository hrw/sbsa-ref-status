# Misc notes for my sbsa-ref work

## PCI Express cards

Vendor | Product | QEMU                | Name
-------|---------|---------------------|--------------------------------------------------------------------------------------------------------
 104c  |  8232   | x3130-upstream      | PCI bridge [0604]: Texas Instruments XIO3130 PCI Express Switch (Upstream)
 104c  |  8233   | xio3130-downstream  | PCI bridge [0604]: Texas Instruments XIO3130 PCI Express Switch (Downstream)
 1234  |  1111   | bochs-display       | Display controller [0380]: Device
 1274  |  5000   | es1370              | Multimedia audio controller [0401]: Ensoniq ES1370 [AudioPCI]
 1b36  |  0008   |                     | Host bridge [0600]: Red Hat, Inc. QEMU PCIe Host bridge
 1b36  |  000c   | pcie-root-port      | PCI bridge [0604]: Red Hat, Inc. QEMU PCIe Root port
 1b36  |  000e   | pcie-pci-bridge     | PCI bridge [0604]: Red Hat, Inc. Device
 1b36  |  0010   | nvme                | Non-Volatile memory controller [0108]: Red Hat, Inc. QEMU NVM Express Controller
 8086  |  100e   | e1000               | Ethernet controller [0200]: Intel Corporation 82540EM Gigabit Ethernet Controller
 8086  |  10c9   | igb                 | Ethernet controller [0200]: Intel Corporation 82576 Gigabit Network Connection
 8086  |  10d3   | e1000e              | Ethernet controller [0200]: Intel Corporation 82574L Gigabit Network Connection
 8086  |  2415   | ac97                | Multimedia audio controller [0401]: Intel Corporation 82801AA AC'97 Audio Controller
 8086  |  2922   | ahci                | SATA controller [0106]: Intel Corporation 82801IR/IO/IH (ICH9R/DO/DH) 6 port SATA Controller [AHCI mode]


### PCI Express types

Type    | Name
--------|-------------------
 0x01   | End Point
 0x02   | Legacy End Point
 0x10   | Root Port
 0x20   | Upstream Port
 0x40   | Downstream Port
 0x80   | PCI-Express to PCI/PCI-X Bridge
 0x100  | PCI/PCI-X to PCIe Bridge
 0x200  | Root Complex Integrated End Point
 0x400  | Root Complex Event Collector
 0x800  | iEP_RP
 0x1000 | iEP_EP
