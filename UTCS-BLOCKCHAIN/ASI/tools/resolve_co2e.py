#!/usr/bin/env python3
import yaml, json, sys

factors = yaml.safe_load(open("UTCS-BLOCKCHAIN/ASI/factors/co2e.yaml"))
country = (sys.argv[1] if len(sys.argv)>1 else "default").lower()
kwh = float(sys.argv[2]) if len(sys.argv)>2 else 0.0
factor = factors["electricity_kgco2_per_kwh"]["sources"].get(country,
          factors["electricity_kgco2_per_kwh"]["default"])
print(json.dumps({"co2e_kg": kwh * factor, "factor": factor}))