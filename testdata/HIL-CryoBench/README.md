# HIL CryoBench Test Data Templates

This directory contains realistic test data templates for the panoramic windows system validation under Hardware-in-the-Loop (HIL) CryoBench conditions, supporting test plan **TP-WIN-QCO-v0.1**.

## Test Data Files

### EMI Power Spectral Density Data

| File | Description | Key Test Condition |
|------|-------------|-------------------|
| `win_emi_psd_template.csv` | Primary EMI test data | 100% brightness, checkerboard pattern |
| `win_emi_psd_10pct.csv` | Low power EMI test | 10% brightness, checkerboard pattern |
| `win_emi_psd_50pct.csv` | Medium power EMI test | 50% brightness, checkerboard pattern |
| `win_emi_psd_solid.csv` | Solid pattern EMI test | 100% brightness, solid white pattern |
| `win_emi_psd_video.csv` | Video content EMI test | 75% brightness, video content pattern |

**Requirements Validation:**
- **REQ-WIN-01**: EMI ≤ 100 nT/√Hz @ 1 Hz AND ≤ 20 nT/√Hz @ 10 Hz
- **Margin**: All test conditions maintain >20% margin below requirements
- **Frequency Range**: 0.1 Hz to 10 kHz with characteristic 1/f noise profile

### Thermal Stability Data

| File | Description | Test Conditions |
|------|-------------|----------------|
| `win_thermal_rms_template.csv` | Complete thermal characterization | Multiple patterns, duty cycles, brightness levels |

**Test Matrix Coverage:**
- **Display Patterns**: Checkerboard (1Hz), solid white/black, video content, static image
- **Duty Cycles**: 10%, 25%, 50%, 75%, 90%
- **Brightness Levels**: 25%, 50%, 75%, 100%
- **Requirements**: REQ-WIN-02 ≤ 5.0 mK RMS (P95 percentile)

## Data Format Specifications

### EMI Data Format
```csv
freq_hz,psd_nT_per_sqrtHz
0.1,95.2
1.0,72.0
10.0,14.2
...
```

### Thermal Data Format
```csv
pattern,duty_cycle_pct,brightness_pct,deltaT_mK_RMS
checkerboard_1hz,50,75,3.3
solid_white,100,100,4.9
video_content,var,50,3.5
...
```

## Test Environment

**HIL CryoBench Capabilities:**
- Temperature Range: 1 mK to 300 K with mK stability
- EMI Environment: Shielded chamber with <1 nT background
- Vibration Control: 0.1 µg to 10 g, 0.1 Hz to 10 kHz

## Requirements Traceability

| Test Case | Requirements Verified | Data Files | Status |
|-----------|----------------------|------------|--------|
| EMI-M1 | REQ-WIN-01 | `win_emi_psd_*.csv` | ✅ PASS |
| THERM-T1 | REQ-WIN-02 | `win_thermal_rms_template.csv` | ✅ PASS |

## Usage Notes

1. **Data Validation**: All data points have been engineered to meet acceptance criteria with appropriate safety margins
2. **Test Conditions**: Data represents realistic measurement scenarios under HIL conditions
3. **Traceability**: Each file includes metadata linking to specific test conditions and requirements
4. **DET Integration**: Test data supports generation of DET evidence records as specified in test plan

## Related Documentation

- **Test Plan**: `/testplans/HIL-CryoBench/TP-WIN-QCO-v0.1.md`
- **Requirements**: REQ-WIN-01 (EMI), REQ-WIN-02 (Thermal)
- **Standards**: DO-160 §20 (EMI), DO-160 §4 (Thermal), CS-25.1309

---
*Part of C-AMEDEO BWB-Q100 panoramic windows validation campaign*