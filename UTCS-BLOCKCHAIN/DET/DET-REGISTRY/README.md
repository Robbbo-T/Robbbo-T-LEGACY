# DET Registry - Digital Evidence Twin

## Overview
Complete registry of Digital Evidence Twin templates for the CAX framework.

- **Total Domains**: 15
- **Total CAX Pillars**: 7  
- **Total Combinations**: 105 DET template sets

## Domain Structure
- **AAA** - [ARCHITECTURES_AIRFRAMES_AERODYNAMICS](AAA/)
- **AAP** - [AIRPORTS_ADAPTATIONS](AAP/)
- **CCC** - [COCKPIT_CABIN_CARGO_SYSTEMS](CCC/)
- **CQH** - [CRYOGENICS_QUANTUM_INTERFACES_HYDROGEN_CELLS](CQH/)
- **DDD** - [DEFENCE_CYBERSECURITY_SAFETY](DDD/)
- **EDI** - [ELECTRONICS_DIGITAL_INSTRUMENTS](EDI/)
- **EEE** - [ENVIRONMENTAL_REMEDIATION_CIRCULARITY](EEE/)
- **EER** - [ENERGY_AND_RENEWABLE](EER/)
- **IIF** - [INFRASTRUCTURES_AND_FACILITIES_VALUE_CHAINS](IIF/)
- **IIS** - [INTELLIGENT_SYSTEMS_ONBOARD_AI](IIS/)
- **LCC** - [LINKS_COMMUNICATIONS_CONTROL_IoT](LCC/)
- **LIB** - [LOGISTICS_INTEGRATED_BLOCKCHAIN](LIB/)
- **MMM** - [MECHANICAL_MATERIAL_MONITORING](MMM/)
- **OOO** - [OPERATING_SYSTEMS_NAVIGATION_HPC](OOO/)
- **PPP** - [PROPULSION_AND_FUEL](PPP/)

## CAX Pillars
- **CAD** - Computer-Aided Design
- **CAE** - Computer-Aided Engineering
- **CAM** - Computer-Aided Manufacturing
- **CAT** - Computer-Aided Testing
- **CAI** - Computer-Aided Integration
- **CAS** - Computer-Aided Sustainment
- **CAO** - Computer-Aided Organization

## Registry Files
- [registry-index.json](registry-index.json) - Complete registry index
- Domain directories contain CAX pillar subdirectories
- Each CAX-Domain combination contains DET templates for relevant ATA SNS codes

## Namespacing
```
DET:<CAX>:<DOMAIN>:<SNS>:<activity>:<version>
```

Example: `DET:CAD:AAA:52-10:design:V3`
