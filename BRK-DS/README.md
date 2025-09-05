# Base Regulatory Knowledge Data Set (BRK‑DS) Requirements Library

## Overview
This library provides a structured **Base Regulatory Knowledge Data Set (BRK‑DS)** that can be dropped straight into your SRS/SDD and compliance matrix. It is organized as **domain packs** with terse, testable **"shall"** requirements and **trace hooks** to the governing EU/EASA sources.

## Structure
Each domain pack is kept tight (3–7 requirements) to remain actionable. Requirements can be expanded per programme as needed.

## Notation
- IDs use `BRK-<DOMAIN>-###` format
- "Evidence" means the artefact logged in your **Digital Evidence Twin (DET)** to show objective compliance
- "AltMoC/AMOC" hooks provided wherever substitution or alternative compliance might be needed

## Integration with C-AMEDEO Framework
All BRK-DS requirements integrate seamlessly with:
- **DET (Digital Evidence Twin)** patterns for compliance tracking
- **TRACES** framework for bidirectional traceability  
- **CADET** circular assurance metrics
- **ATA SNS** compliance mapping

## Usage
1. Select applicable domain packs for your project
2. Copy relevant requirements.yaml files to your component/system requirements
3. Map to appropriate DET patterns for evidence tracking
4. Link to EASA regulatory sources for audit trail

## Domain Packs
- [GOV](GOV/requirements.yaml) - Global governance (5 requirements)
- [BASIC](BASIC/requirements.yaml) - Basic Regulation EU 2018/1139 (2 requirements)  
- [IA](IA/requirements.yaml) - Initial Airworthiness Part 21 (3 requirements)
- [CS](CS/requirements.yaml) - Additional Airworthiness Specifications (1 requirement)
- [CAW](CAW/requirements.yaml) - Continuing Airworthiness (2 requirements)
- [OPS](OPS/requirements.yaml) - Air Operations (2 requirements)
- [FCL](FCL/requirements.yaml) - Aircrew & Medical (1 requirement)
- [FSTD](FSTD/requirements.yaml) - Flight Simulation Training Devices (1 requirement)
- [ATCO](ATCO/requirements.yaml) - ATCO Licensing (1 requirement)
- [ATM](ATM/requirements.yaml) - ATM/ANS (1 requirement)
- [ATMGND](ATMGND/requirements.yaml) - ATM/ANS Ground Equipment (1 requirement)
- [AIRSPACE](AIRSPACE/requirements.yaml) - Airspace Usage Requirements (1 requirement)
- [ADR](ADR/requirements.yaml) - Aerodromes (1 requirement)
- [UAS](UAS/requirements.yaml) - Drones (1 requirement)
- [TCO](TCO/requirements.yaml) - Third Country Operators (1 requirement)
- [LOI](LOI/requirements.yaml) - Level of Involvement (1 requirement)
- [IS](IS/requirements.yaml) - Information Security (1 requirement)
- And 22 additional regulatory domains...

## Sources
All requirements anchored to EASA official pages and EU regulations for primary sourcing during audits.

## Generated
*This library was generated to support C-AMEDEO regulatory compliance activities.*