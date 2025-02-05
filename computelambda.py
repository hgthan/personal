import numpy as np
# Given parameters
Vin = 0.5/(2 ** 0.5)  # Peak-to-peak voltage (1 Vpp); RMS value
tolerance = 0.05  # 5% resistor tolerance
dVin_tol = 0.01 # 1% is typical? depends on power source i think

# given instrument resistances
instrument_resistance = {
    "Multimeter": 10000000,  # 10MΩ
    "1x Scope Probe": 1000000,  # 1MΩ
    "10x Scope Probe": 10000000,  # 10MΩ
    "Teensy": 50000,  # 50kΩ
}

# measurement table (Z1, Z2, Instrument)
measurements = [
    {"Z1": 0, "Z2": 1e12, "Instrument": "Multimeter"},
    {"Z1": 0, "Z2": 1e12, "Instrument": "1x Scope Probe"},
    {"Z1": 0, "Z2": 1e12, "Instrument": "10x Scope Probe"},
    {"Z1": 0, "Z2": 1e12, "Instrument": "Teensy"},
    {"Z1": 10, "Z2": 20, "Instrument": "Multimeter"},
    {"Z1": 10, "Z2": 20, "Instrument": "Teensy"},
    {"Z1": 1_000, "Z2": 2_000, "Instrument": "Multimeter"},
    {"Z1": 1_000, "Z2": 2_000, "Instrument": "Teensy"},
    {"Z1": 100_000, "Z2": 200_000, "Instrument": "Multimeter"},
    {"Z1": 100_000, "Z2": 200_000, "Instrument": "1x Scope Probe"},
    {"Z1": 100_000, "Z2": 200_000, "Instrument": "Teensy"},
    {"Z1": 10_000_000, "Z2": 20_000_000, "Instrument": "Multimeter"},
    {"Z1": 10_000_000, "Z2": 20_000_000, "Instrument": "1x Scope Probe"},
    {"Z1": 10_000_000, "Z2": 20_000_000, "Instrument": "10x Scope Probe"},
    {"Z1": 10_000_000, "Z2": 20_000_000, "Instrument": "Teensy"},
]

def compute_lambda(Z1, Z2, instrument):
    R_inst = instrument_resistance[instrument]

    # Effective Z2 with instrument loading
    Z2_eff = (Z2 * R_inst) / (Z2 + R_inst) if Z2 else R_inst

    # Partial derivatives
    dVout_dZ1 = -Vin * (Z2_eff / (Z1 + Z2_eff)**2) if Z1 else 0
    dZ2_eff_dZ2 = (R_inst**2) / ((Z2 + R_inst)**2) if Z2 != float("inf") else 0
    dVout_dZ2 = Vin * (Z1 / (Z1 + Z2_eff)**2) * dZ2_eff_dZ2 if Z2 != float("inf") else 0
    dVout_dVin = Z2_eff / (Z1 + Z2_eff)

    # Error contributions based on partial derivatives and tolerance
    dVout_Z1 = abs(dVout_dZ1 * (Z1 * tolerance)) if Z1 else 0
    dVout_Z2 = abs(dVout_dZ2 * (Z2 * tolerance)) if Z2 != float("inf") else 0
    dVout_Vin = abs(dVout_dVin * (Vin * dVin_tol))

    # Total error (quadrature sum)
    lambda_total = np.sqrt(dVout_Z1**2 + dVout_Z2**2 + dVout_Vin**2)

    return {"Instrument": instrument, "Z1": Z1, "Z2": Z2, "Lambda": lambda_total}

# compute lambda for all cases
lambda_results = [compute_lambda(entry["Z1"], entry["Z2"], entry["Instrument"]) for entry in measurements]