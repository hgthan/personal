# Given parameters
Vin = 1  # Peak-to-peak voltage (1 Vpp)
tolerance = 0.05  # 5% resistor tolerance

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

def compute_vout(Z1, Z2, instrument):
    R_inst = instrument_resistance[instrument]
    
    # effective Z2 with instrument loading
    Z2_eff = (Z2 * R_inst) / (Z2 + R_inst) if Z2 else R_inst

    # nominal Vout
    Vout_nominal = Vin * (Z2_eff / (Z1 + Z2_eff))

    # compute min/max due to resistor tolerance
    Z1_min, Z1_max = Z1 * (1 - tolerance), Z1 * (1 + tolerance)
    Z2_min, Z2_max = Z2 * (1 - tolerance), Z2 * (1 + tolerance)

    # effective min/max with loading
    Z2_eff_min = (Z2_min * R_inst) / (Z2_min + R_inst) if Z2_min else R_inst
    Z2_eff_max = (Z2_max * R_inst) / (Z2_max + R_inst) if Z2_max else R_inst

    # min/max Vout
    Vout_min = Vin * (Z2_eff_min / (Z1_max + Z2_eff_min))
    Vout_max = Vin * (Z2_eff_max / (Z1_min + Z2_eff_max))

    return {"Instrument": instrument, "Z1": Z1, "Z2": Z2, "Vout_nominal": Vout_nominal, "Vout_min": Vout_min, "Vout_max": Vout_max}

# compute results for all cases
results = [compute_vout(entry["Z1"], entry["Z2"], entry["Instrument"]) for entry in measurements]

# results

def compute_lambda(Z1, Z2, instrument):
    R_inst = instrument_resistance[instrument]

    # Effective Z2 with instrument loading
    Z2_eff = (Z2 * R_inst) / (Z2 + R_inst) if Z2 else R_inst

    # Vout for nominal values
    Vout_nominal = Vin * (Z2_eff / (Z1 + Z2_eff))

    # Vout for perturbed values (5% tolerance)
    Z1_perturb = Z1 * 1.05  # +5%
    Z2_perturb = Z2 * 1.05  # +5%
    
    Z2_eff_perturb = (Z2_perturb * R_inst) / (Z2_perturb + R_inst) if Z2_perturb else R_inst

    Vout_perturb_Z1 = Vin * (Z2_eff / (Z1_perturb + Z2_eff))
    Vout_perturb_Z2 = Vin * (Z2_eff_perturb / (Z1 + Z2_eff_perturb))

    # compute lambda
    lambda_Z1 = abs((Vout_perturb_Z1 - Vout_nominal) / (Z1_perturb - Z1)) if Z1 else 0
    lambda_Z2 = abs((Vout_perturb_Z2 - Vout_nominal) / (Z2_perturb - Z2)) if Z2 else 0

    lambda_total = lambda_Z1 + lambda_Z2

    return {"Instrument": instrument, "Z1": Z1, "Z2": Z2, "Lambda": lambda_total}

# compute lambda for all cases
lambda_results = [compute_lambda(entry["Z1"], entry["Z2"], entry["Instrument"]) for entry in measurements]

lambda_results
