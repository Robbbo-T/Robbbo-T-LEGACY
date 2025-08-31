# IIS - Intelligent Systems Onboard AI

**Domain:** IIS - Intelligent Systems Onboard AI  
**Classification:** Domain Invariant (DI)  
**Configuration:** H2-BWB-Q100-CONF0000  

## Overview

This domain covers artificial intelligence systems, machine learning algorithms, and intelligent automation for the BWB aircraft.

## Scope

- AI-powered flight assistance
- Machine learning for predictive maintenance
- Intelligent system optimization
- AI safety and verification
- Autonomous system functions

## ATA iSpec 2200 Coverage

This domain includes Configuration Elements (CE) covering the following chapters:

- **ATA 22 - Auto Flight (AI control assist)**
- **ATA 31 - Indicating/Recording (AI analytics)**
- **ATA 34 - Navigation (AI assistance)**
- **ATA 46 - Information Systems (AI/RTOS)**

## Configuration Elements (CE)

Each CE follows the naming convention: `CE-CAD-Q100-IIS-ATA-XX-DESCRIPTION`

All CEs in this domain generate S1000D Data Module Codes (DMC) with:
- **MIC (Model Identification Code):** Q100
- **SNS (Subject Numbering System):** Per ATA iSpec 2200
- **Lifecycle Phase:** CA-DEOPTIMISE (Forward Creation Flow)

### Navigation — Configuration Elements

* [CE-CAD-Q100-IIS-ATA-22-AI-AF](https://github.com/Robbbo-T/Robbbo-T/tree/main/C-AMEDEO-FRAMEWORK/CA-DEOPTIMISE/CAD-DESIGN/H2-BWB-Q100-CONF0000/IIS-INTELLIGENT_SYSTEMS_ONBOARD_AI/CE-CAD-Q100-IIS-ATA-22-AI-AF) — Auto Flight (AI control assist)
* [CE-CAD-Q100-IIS-ATA-31-AI-IR](https://github.com/Robbbo-T/Robbbo-T/tree/main/C-AMEDEO-FRAMEWORK/CA-DEOPTIMISE/CAD-DESIGN/H2-BWB-Q100-CONF0000/IIS-INTELLIGENT_SYSTEMS_ONBOARD_AI/CE-CAD-Q100-IIS-ATA-31-AI-IR) — Indicating/Recording (AI analytics)
* [CE-CAD-Q100-IIS-ATA-34-AI-NAV](https://github.com/Robbbo-T/Robbbo-T/tree/main/C-AMEDEO-FRAMEWORK/CA-DEOPTIMISE/CAD-DESIGN/H2-BWB-Q100-CONF0000/IIS-INTELLIGENT_SYSTEMS_ONBOARD_AI/CE-CAD-Q100-IIS-ATA-34-AI-NAV) — Navigation (AI assistance)
* [CE-CAD-Q100-IIS-ATA-46-AI-RTOS](https://github.com/Robbbo-T/Robbbo-T/tree/main/C-AMEDEO-FRAMEWORK/CA-DEOPTIMISE/CAD-DESIGN/H2-BWB-Q100-CONF0000/IIS-INTELLIGENT_SYSTEMS_ONBOARD_AI/CE-CAD-Q100-IIS-ATA-46-AI-RTOS) — Information Systems (AI/RTOS)

## Dependencies

- **Digital Evidence Twin (DET):** All design changes and analyses generate DET evidence packs
- **CADET:** Circularity metrics for material reuse and lifecycle optimization

---

*This README is part of the C-AMEDEO framework for the AMPEL360-BWB-Q Program.*