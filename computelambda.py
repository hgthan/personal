import numpy as np
# Given parameters
Vin = 0.5/(2 ** 0.5)  # Peak-to-peak voltage (1 Vpp); RMS value
tolerance = 0.05  # 5% resistor tolerance
dVin_tol = 0.02 # 2% verified w xavier yay

# given instrument resistances
instrument_resistance = {
    "Multimeter": 10000000,  # 10MΩ
    "1x Scope Probe": 1000000,  # 1MΩ
    "10x Scope Probe": 10000000,  # 10MΩ
    "Teensy": 636641348.4607166,  # xavier helped us
}

# measurement table (Z1, Z2, Instrument, Instrument Error)
measurements = [
    {"Z1": 0, "Z2": 1e12, "Instrument": "Multimeter", "Instrument Error": 0.01},
    {"Z1": 0, "Z2": 1e12, "Instrument": "1x Scope Probe", "Instrument Error": 0.02},
    {"Z1": 0, "Z2": 1e12, "Instrument": "10x Scope Probe", "Instrument Error": 0.02},
    {"Z1": 0, "Z2": 1e12, "Instrument": "Teensy", "Instrument Error": 0.0048},
    {"Z1": 10, "Z2": 20, "Instrument": "Multimeter", "Instrument Error": 0.01},
    {"Z1": 10, "Z2": 20, "Instrument": "Teensy", "Instrument Error": 0.0048},
    {"Z1": 1_000, "Z2": 2_000, "Instrument": "Multimeter", "Instrument Error": 0.01},
    {"Z1": 1_000, "Z2": 2_000, "Instrument": "Teensy", "Instrument Error": 0.0048},
    {"Z1": 100_000, "Z2": 200_000, "Instrument": "Multimeter", "Instrument Error": 0.01},
    {"Z1": 100_000, "Z2": 200_000, "Instrument": "1x Scope Probe", "Instrument Error": 0.02},
    {"Z1": 100_000, "Z2": 200_000, "Instrument": "Teensy", "Instrument Error": 0.0048},
    {"Z1": 10_000_000, "Z2": 20_000_000, "Instrument": "Multimeter", "Instrument Error": 0.01},
    {"Z1": 10_000_000, "Z2": 20_000_000, "Instrument": "1x Scope Probe", "Instrument Error": 0.02},
    {"Z1": 10_000_000, "Z2": 20_000_000, "Instrument": "10x Scope Probe", "Instrument Error": 0.02},
    {"Z1": 10_000_000, "Z2": 20_000_000, "Instrument": "Teensy", "Instrument Error": 0.0048},
]
def compute_vout_opampin(Z1, Z2, instrument):
    R_inst = instrument_resistance[instrument]
    
    # effective Z2 with instrument loading
    Z2_eff = (Z2 * R_inst) / (Z2 + R_inst) if Z2 else R_inst

    # nominal Vout
    Vout_nominal = Vin * (Z2_eff / (Z1 + Z2_eff))

    # compute min/max due to resistor tolerance
    Z1_min, Z1_max = (Z1) * (1 - tolerance), Z1 * (1 + tolerance)
    Z2_min, Z2_max = Z2 * (1 - tolerance), Z2 * (1 + tolerance)

    # effective min/max with loading
    Z2_eff_min = (Z2_min * R_inst) / (Z2_min + R_inst) if Z2_min else R_inst
    Z2_eff_max = (Z2_max * R_inst) / (Z2_max + R_inst) if Z2_max else R_inst

    # min/max Vout
    Vout_min = Vin * (Z2_eff_min / (Z1_max + Z2_eff_min))
    Vout_max = Vin * (Z2_eff_max / (Z1_min + Z2_eff_max))

    return {"Instrument": instrument, "Z1": Z1, "Z2_eff": Z2_eff, "Vout_nominal": Vout_nominal, "Vout_min": Vout_min, "Vout_max": Vout_max}

# compute results for all cases
results = [compute_vout_opampin(entry["Z1"], entry["Z2"], entry["Instrument"]) for entry in measurements]

def compute_vout_opampout(Z1, Z2, instrument):
    Z1 = Z1 + 50
    R_inst = instrument_resistance[instrument]
    
    # effective Z2 with instrument loading
    Z2_eff = (Z2 * R_inst) / (Z2 + R_inst) if Z2 else R_inst

    # nominal Vout
    Vout_nominal = Vin * (Z2_eff / (Z1 + Z2_eff))

    return {"Instrument": instrument, "Z1": Z1, "Z2_eff": Z2_eff, "Vout_nominal": Vout_nominal, "Vout_min": Vout_min, "Vout_max": Vout_max}

# compute results for all cases
results = [compute_vout_opampout(entry["Z1"], entry["Z2"], entry["Instrument"]) for entry in measurements]

def compute_vout(Z1, Z2, instrument):
    Z1 = Z1 + 50 # Z1 + Vin
    R_inst = instrument_resistance[instrument]
    
    # effective Z2 with instrument loading
    Z2_eff = (Z2 * R_inst) / (Z2 + R_inst) if Z2 else R_inst

    # nominal Vout
    Vout_nominal = Vin * (Z2_eff / (Z1 + Z2_eff))

    # compute min/max due to resistor tolerance
    Z1_min, Z1_max = (Z1) * (1 - tolerance), Z1 * (1 + tolerance)
    Z2_min, Z2_max = Z2 * (1 - tolerance), Z2 * (1 + tolerance)

    # effective min/max with loading
    Z2_eff_min = (Z2_min * R_inst) / (Z2_min + R_inst) if Z2_min else R_inst
    Z2_eff_max = (Z2_max * R_inst) / (Z2_max + R_inst) if Z2_max else R_inst

    # return {"Instrument": instrument, "Z1": Z1, "Z2_eff": Z2_eff, "Vout_nominal": Vout_nominal, "Vout_min": Vout_min, "Vout_max": Vout_max}
    return Vout_nominal

# compute results for all cases
results = [compute_vout(entry["Z1"], entry["Z2"], entry["Instrument"]) for entry in measurements]

def compute_lambda1(Z1, Z2, instrument, instrument_error):
    R_inst = instrument_resistance[instrument]

    # effective Z2 with instrument loading
    Z2_eff = (Z2 * R_inst) / (Z2 + R_inst)
    Vout = compute_vout(Z1, Z2, instrument)

    # partial derivatives
    dVout_dZ1 = (Vin * (Z2_eff / (Z1 + Z2_eff)**2))
    # dZ2_eff_dZ2 = ((R_inst**2) / ((Z2 + R_inst)**2)) if Z2 != float("inf") else 0
    dVout_dZ2 = (Vin * ((Z2_eff) / (Z1 + Z2_eff)**2))
    dVout_dVin = (Z2_eff / (Z1 + Z2_eff))

    # error contributions based on partial derivatives and tolerance
    # dVout_Z1 = abs(dVout_dZ1 * (Z1 * tolerance)) if Z1 else 0
    # dVout_Z2 = abs(dVout_dZ2 * (Z2 * tolerance)) if Z2 != float("inf") else 0
    # dVout_Vin = abs(dVout_dVin * (Vin * dVin_tol))

    # total error (quadrature sum)
    #lambda_total = np.sqrt(dVout_Z1**2 + dVout_Z2**2 + dVout_Vin**2)
    lambda_total_in = np.sqrt(((dVout_dZ1**2)*((.05*Z1)**2)) + ((dVout_dZ2**2)*((.05*Z2)**2)) + ((dVout_dVin**2)*((.02*Vin)**2)) + (instrument_error*Vout)**2)
    lambda_wire = np.sqrt((dVout_dVin**2)*((.02*Vin)**2) + (instrument_error*Vout)**2)

    # return {"Instrument": instrument, "Z1": Z1, "Z2": Z2, "Lambda": lambda_total_in}
    return 

# compute lambda for all cases
lambda_results = [compute_lambda1(entry["Z1"], entry["Z2"], entry["Instrument"], entry["Instrument Error"]) for entry in measurements]

def compute_lambda2(Z1, Z2, instrument): # using numerical method
