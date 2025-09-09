# FAN1 Service BOM (SBOM) - PPP Domain

<!-- UTCS-MI Standard Header -->
**EstándarUniversal**: Artefacto-CatalogoPiezas-ATA+S1000D-72.10-ServiceBOM-0001-v9.0-Aerospace and Quantum United Advanced Venture-GeneracionHybrida-ppp-Amedeo Pelliccia-c18e04d3-RestoDeVidaUtil

**DET Reference**: DET:CAS:ppp:72-10:FAN1-SBOM:V9.0

<a id="cas-ppp"></a><a id="sbom-fan1"></a><a id="ipc-ppp"></a>

## Overview

This document operationalizes the FAN1 Fan Section Assembly Service Bill of Materials (SBOM) for the BWB-Q100 propulsion system, providing comprehensive Field Replaceable Unit (FRU) catalog, S1000D integration, vendor supply chain data, and MRO procedures following UTCS-MI standards.

## Service Assembly Structure

### Primary Assembly
- **Assembly P/N**: Q100-72-10-01-FAN1
- **Description**: Fan Section Assembly - Service BOM  
- **ATA Chapter**: 72.10 (Engine Fan Section)
- **Domain**: PPP (Propulsion and Fuels)
- **Service Criticality**: DAL-B
- **Program**: BWB-Q100

## EBOM → MBOM → SBOM Transformation Rules

### Service Mapping Philosophy
The SBOM transforms manufacturing perspective ([MBOM](../../../CAM-MANUFACTURING/H2-BWB-Q100-CONF0000/PPP-PROPULSION_AND_FUEL/FAN1_MBOM.md)) into service maintenance perspective, focusing on Field Replaceable Units (FRUs), maintenance levels, and operational procedures.

### Transformation Matrix
| EBOM Item | MBOM Items | SBOM FRU | Service Level | Replacement Unit | Service Notes |
|-----------|------------|----------|---------------|------------------|---------------|
| [CWL3](../../../CAD-DESIGN/H2-BWB-Q100-CONF0000/PPP-PROPULSION_AND_FUELS/CE-CAD-Q100-PPP-ATA-72-ENGINE/CC/CE-CC-CAD-Q100-PPP-ATA-72-10-FAN-SECTION/CI/CE-CC-CI-CAD-Q100-PPP-ATA-72-10-01-FAN1/EBOM.yaml) | CWL3 ×2 | CWL3-SVC | O-Level | paired | Suministro pareado (matcheado en fabricación) |
| [SPN4](../../../CAD-DESIGN/H2-BWB-Q100-CONF0000/PPP-PROPULSION_AND_FUELS/CE-CAD-Q100-PPP-ATA-72-ENGINE/CC/CE-CC-CAD-Q100-PPP-ATA-72-10-FAN-SECTION/CI/CE-CC-CI-CAD-Q100-PPP-ATA-72-10-01-FAN1/EBOM.yaml) | SPN4 ×1 | SPN4-SVC | O-Level | individual | FRU O-Level |
| [SHR8](../../../CAD-DESIGN/H2-BWB-Q100-CONF0000/PPP-PROPULSION_AND_FUELS/CE-CAD-Q100-PPP-ATA-72-ENGINE/CC/CE-CC-CAD-Q100-PPP-ATA-72-10-FAN-SECTION/CI/CE-CC-CI-CAD-Q100-PPP-ATA-72-10-01-FAN1/EBOM.yaml) | SHR8 ×1 | SHR8-SVC | O-Level | individual | Inspección térmica previa (nota SBOM) |
| [BLD1](../../../CAD-DESIGN/H2-BWB-Q100-CONF0000/PPP-PROPULSION_AND_FUELS/CE-CAD-Q100-PPP-ATA-72-ENGINE/CC/CE-CC-CAD-Q100-PPP-ATA-72-10-FAN-SECTION/CI/CE-CC-CI-CAD-Q100-PPP-ATA-72-10-01-FAN1/EBOM.yaml) | BLD1 ×24 (rotor) | BLD1-SVC | O-Level | individual | Re-equilibrar si >2 palas cambiadas |
| [FST7](../../../CAD-DESIGN/H2-BWB-Q100-CONF0000/PPP-PROPULSION_AND_FUELS/CE-CAD-Q100-PPP-ATA-72-ENGINE/CC/CE-CC-CAD-Q100-PPP-ATA-72-10-FAN-SECTION/CI/CE-CC-CI-CAD-Q100-PPP-ATA-72-10-01-FAN1/EBOM.yaml) | FST7-B/N/W (96 c/u) | KIT-BLD-FST-01 | O-Level | Kit | EBOM "set" → MBOM piezas; SBOM → Kit |
| [QSN5](../../../CAD-DESIGN/H2-BWB-Q100-CONF0000/PPP-PROPULSION_AND_FUELS/CE-CAD-Q100-PPP-ATA-72-ENGINE/CC/CE-CC-CAD-Q100-PPP-ATA-72-10-FAN-SECTION/CI/CE-CC-CI-CAD-Q100-PPP-ATA-72-10-01-FAN1/EBOM.yaml) | QSN5 ×4 | QSN5-SVC | I-Level | individual | Requiere recalibración T-QCAL-100 |
| [QIC9](../../../CAD-DESIGN/H2-BWB-Q100-CONF0000/PPP-PROPULSION_AND_FUELS/CE-CAD-Q100-PPP-ATA-72-ENGINE/CC/CE-CC-CAD-Q100-PPP-ATA-72-10-FAN-SECTION/CI/CE-CC-CI-CAD-Q100-PPP-ATA-72-10-01-FAN1/EBOM.yaml) | QIC9 ×2 | QIC9-SVC | I-Level | individual | Verif. conectores/prior routing |
| [HUB2](../../../CAD-DESIGN/H2-BWB-Q100-CONF0000/PPP-PROPULSION_AND_FUELS/CE-CAD-Q100-PPP-ATA-72-ENGINE/CC/CE-CC-CAD-Q100-PPP-ATA-72-10-FAN-SECTION/CI/CE-CC-CI-CAD-Q100-PPP-ATA-72-10-01-FAN1/EBOM.yaml) | HUB2 ×1 | HUB2-NR | D-Level | No-Reemplazable | En SBOM como No-Reemplazable (D-Level) |
| [BRH6](../../../CAD-DESIGN/H2-BWB-Q100-CONF0000/PPP-PROPULSION_AND_FUELS/CE-CAD-Q100-PPP-ATA-72-ENGINE/CC/CE-CC-CAD-Q100-PPP-ATA-72-10-FAN-SECTION/CI/CE-CC-CI-CAD-Q100-PPP-ATA-72-10-01-FAN1/EBOM.yaml) | BRH6 ×24 | BRH6-NR | D-Level | No-Reemplazable | Integrado al cubo en servicio; D-Level |

## Field Replaceable Units (FRU) Catalog

### O-Level Parts (Organizational Maintenance)

#### BLD1-SVC - Fan Blade Assembly
- **Quantity per Assembly**: 24
- **Service Action**: Remove/Install
- **S1000D DMC**: [72-10-01-020-801-A](#s1000d-dmc-01)
- **AMM Reference**: AMM 72-10-01
- **Service Time**: 2.5 hrs
- **Special Tools**: T-BAL-015
- **Service Notes**: Re-equilibrar si >2 palas cambiadas
- **Vendor**: [CompositeWorks (7C9L1)](#vendor-compositeworks)

#### CWL3-SVC - Cowl Assembly (Pair)
- **Quantity per Assembly**: 1 pair
- **Service Action**: Remove/Install
- **S1000D DMC**: [72-10-02-020-801-A](#s1000d-dmc-02)
- **AMM Reference**: AMM 72-10-02
- **Service Time**: 1.5 hrs
- **Special Tools**: Útil posicionamiento
- **Service Notes**: Suministro pareado (matching required)
- **Vendor**: [CompositeWorks (7C9L1)](#vendor-compositeworks)

#### SPN4-SVC - Spinner Assembly
- **Quantity per Assembly**: 1
- **Service Action**: Remove/Install
- **S1000D DMC**: [72-10-03-020-801-A](#s1000d-dmc-03)
- **AMM Reference**: AMM 72-10-03
- **Service Time**: 1.0 hrs
- **Special Tools**: None
- **Service Notes**: Revisión de holguras
- **Vendor**: [AeroSpin Corp (2B4X9)](#vendor-aerospin)

#### SHR8-SVC - Shroud Assembly
- **Quantity per Assembly**: 1
- **Service Action**: Remove/Install
- **S1000D DMC**: [72-10-04-020-801-A](#s1000d-dmc-04)
- **AMM Reference**: AMM 72-10-04
- **Service Time**: 2.0 hrs
- **Special Tools**: None
- **Service Notes**: Inspección térmica previa (nota SBOM)
- **Vendor**: [CompositeWorks (7C9L1)](#vendor-compositeworks)

#### KIT-BLD-FST-01 - Blade Fastener Kit
- **Quantity per Assembly**: 1 kit (96 complete sets)
- **Service Action**: Replace complete kit
- **S1000D DMC**: [72-10-05-020-801-A](#s1000d-dmc-05)
- **AMM Reference**: AMM 72-10-05
- **Service Time**: 3.0 hrs
- **Special Tools**: T-TORQ-150
- **Kit Contents**: FST7-B/N/W (bolts, nuts, washers)
- **Service Notes**: Kit completo FST7-B/N/W
- **Vendor**: [HiLock Aero (1XK21)](#vendor-hilock)

### I-Level Parts (Intermediate Maintenance)

#### QSN5-SVC - Quantum Sensor Node
- **Quantity per Assembly**: 4
- **Service Action**: Test/Calibrate
- **S1000D DMC**: [72-10-10-720-801-A](#s1000d-dmc-10-720)
- **FIM Reference**: FIM 72-10-F01
- **Service Time**: 4.0 hrs
- **Special Tools**: T-QCAL-100
- **Facility Requirements**: CLEANROOM-ISO7
- **Service Notes**: [Quantum sensor calibration con T-QCAL-100](#quantum-calibration)
- **Vendor**: [Q-Sense NV (3F7Q2)](#vendor-qsense)

#### QIC9-SVC - Quantum Interface Cable
- **Quantity per Assembly**: 2
- **Service Action**: Remove/Install
- **S1000D DMC**: [72-10-10-020-801-A](#s1000d-dmc-10-020)
- **AMM Reference**: AMM 72-10-10
- **Service Time**: 1.5 hrs
- **Special Tools**: None
- **Facility Requirements**: CLEANROOM-ISO7
- **Service Notes**: [Verificación de conectividad cuántica post-instalación](#quantum-verification)
- **Vendor**: [Q-Sense NV (3F7Q2)](#vendor-qsense)

### D-Level Parts (Depot Maintenance - Non-Repairable)

#### HUB2-NR - Hub Assembly (Non-Repairable)
- **Quantity per Assembly**: 1
- **Service Action**: Depot overhaul only
- **Service Level**: D-Level
- **Service Notes**: No field replacement - return to depot
- **Overhaul Cycle**: 20,000 flight hours

#### BRH6-NR - Blade Root Housing (Non-Repairable)
- **Quantity per Assembly**: 24
- **Service Action**: Depot overhaul only
- **Service Level**: D-Level
- **Service Notes**: Integrated with hub - depot service only
- **Overhaul Cycle**: 20,000 flight hours

## Overhaul Modules

### FAN-MOD-OH - Fan Module Overhaul Exchange
- **Service Action**: Complete module swap
- **S1000D DMC**: [72-10-00-040-801-A](#s1000d-dmc-00-040)
- **AMM Reference**: AMM 72-10-00
- **Service Time**: 8.0 hrs
- **Core Return Policy**: Mandatory
- **Turnaround Time**: 30 days
- **Service Notes**: Devolver core con etiquetas completas

## Vendor Information and Supply Chain (CV)

### Q-Sense NV (CAGE: 3F7Q2) <a id="vendor-qsense"></a>
- **Products**: QSN5-SVC, QIC9-SVC
- **CV P/N**: QSN5-NV-2026, QIC9-QF-2026
- **Requirements**: Certif. DO-160G Sec. 20, Trazas QA lot/wafer
- **Lead Time**: 12 weeks
- **MOQ**: 10 units
- **Special Requirements**: Quantum component certification chain

### HiLock Aero (CAGE: 1XK21) <a id="vendor-hilock"></a>
- **Products**: KIT-BLD-FST-01
- **CV P/N**: FST7-KIT-01
- **Requirements**: Coating Ti, lote único por rotor
- **Lead Time**: 6 weeks
- **MOQ**: 50 kits
- **Special Requirements**: Matched set certification

### CompositeWorks (CAGE: 7C9L1) <a id="vendor-compositeworks"></a>
- **Products**: CWL3-SVC, SHR8-SVC, BLD1-SVC
- **CV P/N**: CWL3-PAIR-M, SHR8-CFRP-01, BLD1-CF-24
- **Requirements**: Par emparejado con cert. emparejamiento
- **Lead Time**: 16 weeks
- **MOQ**: 2 pairs (CWL3), 1 unit (others)
- **Special Requirements**: Composite material traceability

### AeroSpin Corp (CAGE: 2B4X9) <a id="vendor-aerospin"></a>
- **Products**: SPN4-SVC
- **CV P/N**: SPN4-AL-01
- **Requirements**: Aluminum forging certification
- **Lead Time**: 8 weeks
- **MOQ**: 5 units
- **Special Requirements**: Dynamic balance certification

## Service Procedures and S1000D Mapping

### Remove/Install Procedures

#### Fan Blade Removal <a id="s1000d-dmc-01"></a>
- **DMC**: 72-10-01-020-801-A
- **AMM Section**: AMM 72-10-01
- **Estimated Time**: 2.5 hrs
- **Skill Level**: Technician
- **Prerequisites**: Engine shutdown, safety locks
- **Post-Removal**: Blade indexing documentation required

#### Fan Blade Installation
- **DMC**: 72-10-01-030-801-A
- **AMM Section**: AMM 72-10-01  
- **Estimated Time**: 3.0 hrs
- **Skill Level**: Technician
- **Post-Install**: [Dynamic balance check required](#post-install-balance)

#### Cowl Assembly Service <a id="s1000d-dmc-02"></a>
- **DMC**: 72-10-02-020-801-A
- **AMM Section**: AMM 72-10-02
- **Estimated Time**: 1.5 hrs
- **Skill Level**: Technician
- **Special Note**: Paired installation mandatory

#### Spinner Service <a id="s1000d-dmc-03"></a>
- **DMC**: 72-10-03-020-801-A
- **AMM Section**: AMM 72-10-03
- **Estimated Time**: 1.0 hrs
- **Skill Level**: Technician

#### Shroud Service <a id="s1000d-dmc-04"></a>
- **DMC**: 72-10-04-020-801-A
- **AMM Section**: AMM 72-10-04
- **Estimated Time**: 2.0 hrs
- **Skill Level**: Technician
- **Prerequisites**: Thermal inspection required

#### Fastener Kit Replacement <a id="s1000d-dmc-05"></a>
- **DMC**: 72-10-05-020-801-A
- **AMM Section**: AMM 72-10-05
- **Estimated Time**: 3.0 hrs
- **Skill Level**: Technician
- **Special Tools**: T-TORQ-150 torque wrench

### Test/Calibration Procedures

#### Quantum Sensor Calibration <a id="s1000d-dmc-10-720"></a>
- **DMC**: 72-10-10-720-801-A
- **FIM Section**: FIM 72-10-F01
- **Estimated Time**: 4.0 hrs
- **Skill Level**: Specialist
- **Facility**: CLEANROOM-ISO7
- **Equipment**: T-QCAL-100 quantum calibrator
- **Procedure**: [Quantum calibration protocol](#quantum-calibration)

#### Quantum Interface Verification <a id="s1000d-dmc-10-020"></a>
- **DMC**: 72-10-10-020-801-A
- **AMM Section**: AMM 72-10-10
- **Estimated Time**: 1.5 hrs
- **Skill Level**: Specialist
- **Facility**: CLEANROOM-ISO7
- **Procedure**: [Connectivity verification protocol](#quantum-verification)

### Module Overhaul <a id="s1000d-dmc-00-040"></a>
- **DMC**: 72-10-00-040-801-A
- **AMM Section**: AMM 72-10-00
- **Estimated Time**: 8.0 hrs
- **Skill Level**: Certified technician
- **Prerequisites**: Core return completed

## Quantum Service Integration

### Quantum Sensor Calibration <a id="quantum-calibration"></a>
- **Equipment**: T-QCAL-100 quantum calibrator
- **Environment**: CLEANROOM-ISO7
- **Calibration Standard**: NIST quantum reference
- **Calibration Interval**: 6 months or 1000 flight hours
- **Documentation**: QS.Published event emission required

### Quantum Connectivity Verification <a id="quantum-verification"></a>
- **Test Equipment**: DAS-Q quantum analyzer
- **Test Standard**: DO-160G Section 20
- **Acceptance Criteria**: Connectivity >99.9%, EMI compliance
- **Documentation**: [QS.Published event emission](#qal-bus-integration) required

## Core Return and RMA Policies

### FAN-MOD-OH Core Policy
- **Policy**: Core return mandatory within 30 days
- **RMA Process**: [DET de recepción required](#det-rma)
- **Turnaround Time**: 30 days from receipt
- **Shipping**: Quantum components require special handling

### Serviceable Component RMA
- **QSN5-SVC**: Return for recalibration if drift >5%
- **QIC9-SVC**: Return if connectivity <99.9%
- **Standard Components**: Standard aerospace RMA procedures

## IPC (Illustrated Parts Catalog) References

### Figure Structure
- **Figure 01**: Fan assembly overview - [AMM 72-10-00](#amm-ref-01)
- **Figure 02**: Blade installation detail - [AMM 72-10-01](#amm-ref-02)
- **Figure 03**: Quantum sensor locations - [FIM 72-10-F01](#fim-ref-03)
- **Figure 04**: Service access points - [AMM 72-10-00](#amm-ref-04)

## Post-Installation Requirements

### Dynamic Balance Check <a id="post-install-balance"></a>
- **Required After**: >2 blade changes, any rotor component change
- **Equipment**: T-BAL-015 balancing equipment
- **Acceptance**: Residual imbalance < 0.25 g·cm
- **Documentation**: Balance report required in maintenance log

### Quantum System Verification
- **Required After**: Any quantum component service
- **Tests**: Connectivity, calibration, EMI compliance
- **Documentation**: [QS.Published event](#qal-bus-integration) required

## QAL Bus Integration <a id="qal-bus-integration"></a>

### CAS.SBOMReleased Event
- **Event File**: [../../../../../../events/out/CAS.SBOMReleased.json](../../../../../../events/out/CAS.SBOMReleased.json)
- **DET Reference**: [DET:CAS:ppp:72-10:FAN1-SBOM:V9.0](#det-cas-sbom)
- **Meta**: IPC structure, FRU count, S1000D DMCs, vendor count

### Service Event Emissions
- **QS.Published**: Quantum component calibration/verification
- **Service.Completed**: Maintenance action completion
- **RMA.Initiated**: Return material authorization

## DET Evidence Links <a id="det-cas-sbom"></a>

### Primary DET
- **DET ID**: [DET:CAS:ppp:72-10:FAN1-SBOM:V9.0](../../../../../UTCS-BLOCKCHAIN/DET/CAS/ppp/72-10/FAN1-SBOM/V9.0/)
- **Linked MBOM**: [DET:CAM:ppp:72-10:FAN1-MBOM:V9.0](../../../CAM-MANUFACTURING/H2-BWB-Q100-CONF0000/PPP-PROPULSION_AND_FUEL/FAN1_MBOM.md)
- **Service Manual**: [DET:CAS:ppp:72-10:FAN1-SVC:V9.0](#det-service-manual)

### RMA DET Reference <a id="det-rma"></a>
- **DET ID**: [DET:CAS:ppp:72-10:FAN1-RMA:V9.0](../../../../../UTCS-BLOCKCHAIN/DET/CAS/ppp/72-10/FAN1-RMA/V9.0/)

### AMM References
- **AMM 72-10-00**: [DET:CAS:ppp:72-10:AMM-00:V9.0](#amm-ref-01)
- **AMM 72-10-01**: [DET:CAS:ppp:72-10:AMM-01:V9.0](#amm-ref-02)
- **FIM 72-10-F01**: [DET:CAS:ppp:72-10:FIM-F01:V9.0](#fim-ref-03)

---

**Documento controlado por QAL Bus**  
**Próxima revisión**: En cambio de configuración FAN1  
**Responsable**: CAS Authority & MRO Engineering Lead  
**QAUDIT**: [QAUDIT:CAS:ppp:SBOM:V9.0](../../../../../UTCS-BLOCKCHAIN/QAUDIT/CAS/ppp/SBOM-V9.0.yaml)

**Validation Status**: ✅ UTCS-MI compliant ✅ S1000D integrated ✅ QAL Bus compatible ✅ FRU catalog complete