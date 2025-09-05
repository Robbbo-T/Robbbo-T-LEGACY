#!/usr/bin/env python3
import json, sys
from datetime import datetime, timezone

def main():
    ts = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    evt = {
        "event": "QS.Published",
        "ts": ts,
        "program": "BWB-Q100",
        "domain": "AAA",
        "level": "CI",
        "entity": "WINCAL.HIL.RunFinished",
        "qs_type": "QML",
        "utcs_mi_id": "EstándarUniversal:EstadoCuantico-QML-56.01-PANORAMIC-WINDOWS-HIL-CRYOBENCH-RestoDeVidaUtil",
        "det_ref": "DET:QS:AAA:5601:hil_test_complete:V1.0",
        "signature": "PQC-Dilithium3",
        "meta": {
            "program": "WINCAL",
            "test_facility": "HIL-CryoBench",
            "test_type": "RunFinished",
            "window_id": "CE-CC-CI-CAD-Q100-AAA-ATA-56-01-PANORAMIC-WINDOWS",
            "pattern_id": "checkerboard_50hz",
            "B_psd_nT_per_sqrtHz": {"1Hz": 72.0, "10Hz": 14.2},
            "deltaT_mK_RMS": 4.2,
            "vibration_ug_RMS": 8.5,
            "ABU_protection": {"triggered": False, "response_time_ms": None, "recovery_time_s": None},
            "pass": True,
            "test_duration_s": 1800,
            "requirements_verified": ["REQ-WIN-01","REQ-WIN-02","REQ-WIN-03","REQ-WIN-04","REQ-WIN-05"],
            "thermal_gradient_K": {"cabin_side": 295, "mli_interface": 148, "cryo_buffer": 77.1},
            "security_test_status": {
                "pii_exfiltration_detected": False,
                "penetration_test_passed": True,
                "edge_processing_verified": True
            }
        }
    }
    out = "events/samples/WINCAL.HIL.RunFinished_generated.json"
    with open(out,"w",encoding="utf-8") as f:
        json.dump(evt, f, ensure_ascii=False, indent=2)
    print("Wrote", out)

if __name__ == "__main__":
    sys.exit(main())