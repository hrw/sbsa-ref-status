sbsa_level_checklist = {
    3: {
        "bsa": {
            51,     # B_PE_18 Check EL2 implementation
            52,     # B_PE_19 Check Stage 2 4KB Granule Support
            53,     # B_PE_20 Check Stage2 and Stage1 Granule match
            54,     # B_PE_21 Check for PMU counters
            55,     # B_PE_22 Check VMID breakpoint number
            76,     # B_PE_23, B_PE_24 Check EL3 implementation
            102,    # B_MEM_01 Mem Access Response in finite time
            103,    # B_MEM_05 PE must access all NS addr space
            203,    # B_GIC_03 If PCIe, GICv3 then ITS, LPI
            204,    # B_GIC_04 Check GICv3 Security States
            205,    # B_GIC_05 Non-secure SGIs are implemented
            206,    # B_PPI_01 Check PPI Assignments for OS
            226,    # B_PPI_02 Check NS EL2-Virt timer PPI Assignment
            227,    # B_PPI_02 Check NS EL2-Phy timer PPI Assignment
            228,    # B_PPI_02 Check GIC Maintenance PPI Assignment
            301,    # B_SMMU_01 All SMMUs have same Arch Revision
            302,    # B_SMMU_02 Check SMMU Granule Support
            303,    # B_SMMU_06 Check Large Physical Addr Support
            304,    # B_SMMU_08 SMMU revision and S-EL2 support
            352,    # B_SMMU_16, B_SMMU_17, B_SMMU_18 S-EL2 not implemented & SMMU stage2 support
            353,    # B_SMMU_19 SMMUv2 unique intr per ctxt bank
            354,    # B_SMMU_21, SMMU_01 SMMUv3 Integration compliance
            401,    # B_TIME_01, B_TIME_02 Check Counter Frequency
            402,    # B_TIME_06 SYS Timer if PE Timer not ON
            403,    # B_TIME_07, B_TIME_10 Memory mapped timer check
            404,    # B_TIME_08 Generate Mem Mapped SYS Timer Intr
            405,    # B_TIME_09 Restore PE timer on PE wake up
            501,    # B_WAK_06, B_WAK_07, B_WAK_10, B_WAK_11 Wake from EL1 PHY Timer Int
            502,    # B_WAK_06, B_WAK_07, B_WAK_10, B_WAK_11 Wake from EL1 VIR Timer Int
            503,    # B_WAK_06, B_WAK_07, B_WAK_10, B_WAK_11 Wake from EL2 PHY Timer Int
            504,    # B_WAK_06, B_WAK_07, B_WAK_10, B_WAK_11 Wake from Watchdog WS0 Int
            505,    # B_WAK_06, B_WAK_07, B_WAK_10, B_WAK_11 Wake from System Timer Int
            601,    # B_PER_01, B_PER_02 USB CTRL Interface
            602,    # B_PER_03 Check SATA CTRL Interface
            603,    # B_PER_05 Check Arm BSA UART register offsets
            604,    # B_PER_06, B_PER_07 Check Arm GENERIC UART Interrupt
            606,    # B_PER_05 16550 compatible UART
            701,    # B_WD_01, B_WD_02, S_L3WD_01 Non Secure Watchdog Access
            702     # B_WD_03, S_L3WD_01 Check Watchdog WS0 interrupt
        },
        "sbsa": {
            1,      # S_L3PE_01 Check PE Granule Support
            2,      # S_L3PE_02 Check for 16-bit ASID support
            3,      # S_L3PE_03 Check AARCH64 implementation
            4,      # S_L3PE_04 Check FEAT_LPA Requirements
            101,    # S_L3MM_01, S_L3MM_02 Check peripherals addr 64Kb apart
            201,    # S_L3GI_01 Check GIC version
            301     # S_L3SM_01 Check SMMU Version
        }
    },
    4: {
        "bsa": {
        },
        "sbsa": {
            5,      # S_L4PE_01 Check for RAS extension
            6,      # S_L4PE_02 Check DC CVAP support
            7,      # S_L4PE_03 Check for 16-Bit VMID
            8,      # S_L4PE_04 Check for Virtual host extensions
            601     # S_L4PCI_2 Check EA Capability
        }
    },
    5: {
        "bsa": {
        },
        "sbsa": {
            9,      # S_L5PE_01 Support Page table map size change
            10,     # S_L5PE_02 Check for pointer signing
            11,     # S_L5PE_04 Check Activity monitors extension
            12,     # S_L5PE_05 Check for SHA3 and SHA512 support
            13,     # S_L5PE_06 Stage 2 control of mem and cache
            14,     # S_L5PE_07 Check for nested virtualization
            15,     # S_MPAM_PE Check MPAM PE Requirements
            16,     # S_MPAM_PE Check MPAM LLC Requirements
            102     # S_L5PP_01 Check Reserved PPI Assignments
        }
    },
    6: {
        "bsa": {
        },
        "sbsa": {
            18,     # S_L6PE_02 Check Branch Target Support
            19,     # S_L6PE_03 Check Protect Against Timing Fault
            20,     # S_L6PE_04 Check PMU Version Support
            21,     # S_L6PE_05 Check AccessFlag DirtyState Update
            22,     # S_L6PE_06 Check Enhanced Virtualization Trap
            23,     # B_SEC_01 Check Speculation Restriction
            24,     # B_SEC_02 Check Speculative Str Bypass Safe
            25,     # B_SEC_03 Check PEs Impl CSDB,SSBB,PSSBB
            26,     # B_SEC_04 Check PEs Implement SB Barrier
            27,     # B_SEC_05 Check PE Impl CFP,DVP,CPP RCTX
            701     # S_L6WD_01 Check NS Watchdog Revision
        }
    },
    7: {
        "bsa": {
        },
        "sbsa": {
            28,     # S_L7PE_01 Check Fine Grain Trap Support
            29,     # S_L7PE_02 Check for ECV support
            30,     # S_L7PE_03 Check for AMU Support
            31,     # S_L7PE_04 Checks ASIMD Int8 matrix multiplc
            32,     # S_L7PE_05 Check for BFLOAT16 extension
            33,     # S_L7PE_06 Check for EnhancedPAC2 and FPAC
            34,     # S_L7PE_07 Check for SVE Int8 matrix multiplc
            35,     # S_L7PE_08 Check for data gathering hint
            36,     # S_L7PE_09 Check WFE Fine tune delay feature
            37,     # S_L7PE_10 Check for enhanced PAN feature
        }
    },
}
