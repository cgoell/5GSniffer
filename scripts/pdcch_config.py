#!/usr/bin/env python3
"""
5G CORESET / PDCCH Parameter Calculator
---------------------------------------

This script helps compute key parameters for the 5GSniffer `.toml` configuration,
given typical RRC/MIB values.

It calculates:
- The Point A frequency (lowest subcarrier of the carrier grid)
- The subcarrier offset for the CORESET (to center the PDCCH)
- The number of PRBs (num_prbs) for the PDCCH

References:
- 3GPP TS 38.211 (SSB definition)
- 3GPP TS 38.331 (ControlResourceSet)
- SpriteLab 5GSniffer documentation

Author: <Christian Goeller>
"""

# Constants
SUBCARRIERS_PER_RB = 12          # 12 subcarriers per Resource Block
SSB_SUBCARRIERS = 240            # SSB always spans 240 subcarriers (20 RBs)
SCS_KHZ = 15                     # subcarrier spacing in kHz (change if needed)
SCS_MHZ = SCS_KHZ / 1000.0       # 0.015 MHz per subcarrier

def main():
    print("=== 5GSniffer Parameter Calculator ===")
    print("All frequencies are in MHz.\n")

    # ---- Inputs ----
    ssb_center_freq = float(input("Enter SSB center frequency (e.g. 627.650): "))
    offset_to_pointA = int(input("Enter offsetToPointA (in PRBs): "))
    ssb_subcarrier_offset = int(input("Enter ssb-SubcarrierOffset (in subcarriers): "))
    k_ssb = int(input("Enter k_SSB (in subcarriers, from MIB): "))

    # Optional: known CORESET/PDCCH width
    bits_set = int(input("Number of '1' bits in frequencyDomainResources (e.g. 8 for 48 PRBs): "))

    # ---- Calculations ----

    # 1. Compute SSB bandwidth
    ssb_bw = SSB_SUBCARRIERS * SCS_MHZ  # in MHz

    # 2. Compute PointA frequency
    pointA_freq = (ssb_center_freq
                   - (ssb_bw / 2)
                   - (k_ssb * SCS_MHZ)
                   - (offset_to_pointA * SUBCARRIERS_PER_RB * SCS_MHZ))

    # 3. Compute PDCCH (CORESET) bandwidth
    num_prbs = bits_set * 6
    pdcch_bw = num_prbs * SUBCARRIERS_PER_RB * SCS_MHZ  # in MHz

    # 4. Compute subcarrier_offset (aligning PDCCH to SSB)
    pdcch_center = pointA_freq + pdcch_bw / 2
    freq_diff_mhz = ssb_center_freq - pdcch_center
    subcarrier_offset = round((freq_diff_mhz * 1000) / SCS_KHZ)

    # ---- Results ----
    print("\n--- Results ---")
    print(f"SSB Bandwidth          : {ssb_bw:.3f} MHz")
    print(f"PointA Frequency       : {pointA_freq:.3f} MHz")
    print(f"PDCCH Bandwidth (48PRBs): {pdcch_bw:.3f} MHz")
    print(f"Subcarrier Offset      : {subcarrier_offset} subcarriers")
    print(f"num_prbs (CORESET BW)  : {num_prbs} PRBs")
    print("-------------------------")
    print("Use these values in your .toml config:")
    print(f"subcarrier_offset = {subcarrier_offset}")
    print(f"num_prbs = {num_prbs}")

if __name__ == "__main__":
    main()
