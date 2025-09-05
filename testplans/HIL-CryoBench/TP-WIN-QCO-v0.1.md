# TP-WIN-QCO-v0.1: HIL CryoBench Test Plan for QCO Windows Integration

## Overview

This test plan validates the integration of panoramic windows system with the Quantum Cryogenic Oasis (QCO) under Hardware-in-the-Loop (HIL) conditions. The CryoBench facility provides a representative thermal, EMI, and vibration environment for comprehensive system testing.

## Test Cases

### EMI-M1: EMI Compatibility Test (PWM sweep)

**Objective**: Verify panoramic windows EMI emissions compliance with QCO budget (REQ-WIN-01)

**Test Setup**:
- HIL CryoBench with QCO thermal simulator at 10 mK base temperature
- Panoramic windows OLED system under test
- EMI measurement system: Spectrum analyzer + calibrated magnetic field sensors
- PWM drive patterns: 1 Hz - 10 kHz sweep

**Inputs**:
- OLED display patterns: checkerboard, solid colors, video content at varying refresh rates
- PWM switching frequencies: 1 Hz, 10 Hz, 100 Hz, 1 kHz, 10 kHz
- Display brightness levels: 10%, 50%, 100%
- Ambient temperature: -40°C to +70°C

**Instruments**:
- **EMI Sensors**: Calibrated tri-axial magnetometer (1 nT/√Hz sensitivity)
- **Position**: 15 cm from OLED stack (QCO representative distance)  
- **Frequency Range**: 0.1 Hz - 100 kHz
- **Data Rate**: 1 kHz sampling for spectral analysis

**Acceptance Criteria** (aligned to REQ-WIN-01):
- **PASS**: Measured PSD ≤ 100 nT/√Hz @ 1 Hz AND ≤ 20 nT/√Hz @ 10 Hz  
- **PASS**: 20% margin maintained at all test conditions
- **FAIL**: Any frequency violation or insufficient margin

**DET Record Example**:
```cbor
{
  "det_id": "DET:HIL:BWB:56-01:emi_test:V1.0",
  "test_case": "EMI-M1",
  "results": {
    "pass": true,
    "B_psd_nT_per_sqrtHz": {"1Hz": 72.0, "10Hz": 14.2},
    "margin_percent": {"1Hz": 28.0, "10Hz": 29.0},
    "max_frequency_violation": null
  }
}
```

---

### THERM-T1: Thermal Stability Test (checkerboard duty)

**Objective**: Verify OLED thermal impact on QCO stability within 5 mK RMS (REQ-WIN-02)

**Test Setup**:
- QCO simulator with mK-stage temperature monitoring
- OLED display system with variable power dissipation
- Thermal gradient stack (300K → 150K → 77K)
- Calorimetry measurement system

**Inputs**:
- **Display Patterns**: Checkerboard at 50% duty cycle, varying frequency 1-60 Hz
- **Power Levels**: 25%, 50%, 75%, 100% brightness
- **Duty Cycles**: 10%, 25%, 50%, 75%, 90%
- **Test Duration**: 30 minutes per condition for thermal equilibrium

**Instruments**:
- **mK Thermometry**: Resistance thermometer (0.1 mK resolution)
- **Thermal Imaging**: IR camera for gradient stack temperature mapping
- **Power Measurement**: Precision power analyzer (0.1 mW accuracy)
- **Calorimeter**: Heat flow measurement through thermal barriers

**Acceptance Criteria** (aligned to REQ-WIN-02):
- **PASS**: ΔT_RMS at mK stage ≤ 5.0 mK (P95 percentile)
- **PASS**: Thermal gradient maintained: 300K ± 5K → 150K ± 10K → 77K ± 2K
- **FAIL**: Temperature excursion > 5.0 mK RMS or gradient stack failure

---

### VIB-V1: Vibration Isolation Test (10-20 Hz micro-g)

**Objective**: Verify vibration isolation maintains < 10 µg RMS in quantum-sensitive bands

**Test Setup**:  
- Vibration excitation system (10-1000 Hz capability)
- Panoramic windows mounted on isolation system
- QCO vibration-sensitive quantum simulator
- Multi-axis accelerometer array

**Inputs**:
- **Excitation Frequency**: Swept sine 10-1000 Hz, 0.1 Hz resolution
- **Excitation Amplitude**: 0.1g, 0.5g, 1.0g input at window mounting
- **Waveforms**: Sine, random, aircraft-representative turbulence
- **Test Duration**: 5 minutes per frequency/amplitude combination

**Instruments**:
- **Accelerometers**: MEMS sensors, 1 µg sensitivity, 0.1-2000 Hz bandwidth
- **Positions**: Window frame, QCO interface, thermal stack connections
- **Data Acquisition**: 5 kHz sampling, real-time spectral analysis
- **Vibration Source**: Electrodynamic shaker with <0.1% THD

**Acceptance Criteria**:
- **PASS**: QCO interface vibration ≤ 10 µg RMS in 10-100 Hz band
- **PASS**: Isolation system provides > 20 dB attenuation at resonant frequencies
- **FAIL**: Vibration budget exceeded or isolation system ineffective

---

### SEC-S1: Security Exfiltration Test  

**Objective**: Verify zero PII exfiltration and edge-only processing (REQ-WIN-05)

**Test Setup**:
- Panoramic windows system with biometric calibration active
- Network monitoring and data flow analysis equipment
- Simulated passenger biometric input (synthetic datasets)
- Security test harness with penetration testing tools

**Inputs**:
- **Synthetic Biometrics**: Eye tracking, face recognition, voice patterns
- **Network Conditions**: Normal operation, degraded connectivity, disconnected
- **Attack Scenarios**: Network sniffing, man-in-the-middle, protocol analysis
- **Monitoring Duration**: 24 hours continuous operation

**Instruments**:
- **Network Analyzers**: Packet capture and deep protocol inspection
- **Security Scanners**: Vulnerability assessment tools
- **Data Flow Monitors**: Real-time data exfiltration detection
- **Forensic Tools**: Memory dumps and storage analysis

**Acceptance Criteria** (aligned to REQ-WIN-05):
- **PASS**: Zero PII detected in network traffic (confirmed by inspection)
- **PASS**: DET logs generated without PII content
- **PASS**: Penetration test report shows no data exfiltration paths
- **FAIL**: Any PII exfiltration detected or security vulnerability identified

---

### FALL-F1: Heater Fault Injection Test

**Objective**: Verify ABU-QuantumProtect response and recovery timing (REQ-WIN-03)

**Test Setup**:
- QCO thermal system with controllable fault injection
- ABU-QuantumProtect safety system integration  
- Panoramic windows with automated degradation capability
- Safety response timing measurement system

**Inputs**:
- **Fault Types**: Heater over-temperature, EMI injection, vibration impulse
- **Fault Timing**: Random injection during normal operation
- **Recovery Conditions**: Manual reset, automatic recovery, system override
- **Test Cycles**: 10 fault/recovery cycles per fault type

**Instruments**:
- **Safety Monitors**: ABU-QuantumProtect signal logging
- **Timing Analyzers**: μs-resolution event timing measurement
- **System Status**: Real-time monitoring of display mode and quantum status
- **Recovery Tracking**: Automated measurement of recovery time

**Acceptance Criteria** (aligned to REQ-WIN-03):
- **PASS**: Display refresh reduces to ≤ 10 Hz within protection response time
- **PASS**: Quantum tasks suspended immediately upon ABU trigger
- **PASS**: Recovery time ≤ 60 seconds after fault stimulus removal
- **FAIL**: Response timing exceeded or recovery failure

---

## CBOR/COSE DET Example Record

```cbor
{
  "det_id": "DET:HIL:BWB:56-01:test_complete:V1.0",
  "timestamp": "2025-01-15T16:45:00.000Z",
  "test_plan": "TP-WIN-QCO-v0.1",
  "facility": "HIL-CryoBench",
  "test_results": {
    "EMI-M1": {
      "status": "PASS",
      "B_field_nT_sqrt_hz": {"1Hz": 72, "10Hz": 14},
      "margin_percent": 25.0
    },
    "THERM-T1": {
      "status": "PASS", 
      "deltaT_mK_RMS": 4.2,
      "P95_temp_deviation": 4.8
    },
    "VIB-V1": {
      "status": "PASS",
      "vibration_ug_RMS": 8.5,
      "isolation_dB": 22.1
    },
    "SEC-S1": {
      "status": "PASS",
      "PII_exfiltration": false,
      "security_violations": 0
    },
    "FALL-F1": {
      "status": "PASS",
      "ABU_response_ms": 85,
      "recovery_time_s": 45
    }
  },
  "overall_status": "PASS",
  "requirements_verified": ["REQ-WIN-01", "REQ-WIN-02", "REQ-WIN-03", "REQ-WIN-05"],
  "signature": "PQC-Dilithium3",
  "cose_signature": "...base64encoded..."
}
```

## Test Environment Specifications

**HIL CryoBench Capabilities**:
- **Temperature Range**: 1 mK to 300 K with mK stability
- **EMI Environment**: Shielded chamber with <1 nT background
- **Vibration Control**: 0.1 µg to 10 g, 0.1 Hz to 10 kHz
- **Power Systems**: Clean power with EMI filtering
- **Data Acquisition**: 1 MHz sampling, quantum-limited noise floor

**Configuration Management**:
- All test configurations version controlled
- Calibration certificates maintained for all instrumentation  
- Test procedures peer-reviewed and approved
- Results archived with blockchain-anchored DET records

## Traceability Matrix

| Test Case | Requirements Verified | Standards Referenced | Evidence Generated |
|-----------|----------------------|---------------------|-------------------|
| EMI-M1    | REQ-WIN-01          | DO-160 §20, CS-25.1309 | EMI measurement data |
| THERM-T1  | REQ-WIN-02          | DO-160 §4, QCO Budget | Thermal stability data |  
| VIB-V1    | Vibration budget    | DO-160 §7           | Vibration isolation data |
| SEC-S1    | REQ-WIN-05          | DO-326A             | Security test report |
| FALL-F1   | REQ-WIN-03          | Safety requirements  | ABU response timing |