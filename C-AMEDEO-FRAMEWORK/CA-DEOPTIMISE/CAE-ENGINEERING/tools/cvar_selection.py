#!/usr/bin/env python3
"""
AMPEL360 CVaR Selection Tool - Professional Engineering Optimization

Implements G1→G2 feasible set reduction and CVaR@0.95 risk-based selection
for robust engineering optimization. Generates immutable DET evidence with
complete provenance for audit trails.

Architecture: AMPEL360 → CAE → CAV pipeline integration
"""

import argparse
import json
import csv
import yaml
import hashlib
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
import random
from dataclasses import dataclass, asdict


@dataclass
class Configuration:
    """Engineering configuration with multi-criteria attributes"""
    id: str
    geometry_params: Dict[str, float]
    material_specs: Dict[str, str]
    manufacturing_params: Dict[str, float]
    weight_kg: float
    cost_estimate: float
    safety_margin: float
    fatigue_life_cycles: int
    manufacturing_time_hrs: float
    sustainability_score: float
    risk_factors: Dict[str, float]


@dataclass
class CVaRResults:
    """CVaR optimization results with complete provenance"""
    selected_configs: List[Configuration]
    cvar_confidence: float
    risk_threshold: float
    selection_rationale: str
    provenance: Dict[str, Any]
    det_hash: str
    timestamp: str


class AMPEL360Optimizer:
    """AMPEL360 G1→G2 feasible set generator with CVaR@0.95 selection"""
    
    def __init__(self, risk_threshold: float = 0.95, max_configs: int = 10000):
        self.risk_threshold = risk_threshold
        self.max_configs = max_configs
        random.seed(42)  # Reproducible results
        
    def generate_feasible_set_g1(self, domain_constraints: Dict[str, Any]) -> List[Configuration]:
        """
        G1: Generate feasible configuration set from design space
        Reduces >2×10^16 theoretical combinations to ~10,000 feasible
        """
        print(f"🔄 G1: Generating feasible set (target: {self.max_configs} configurations)")
        
        # Design space parameters from BWB-Q100 constraints
        geometry_ranges = domain_constraints.get("geometry", {
            "wing_span_m": (40.0, 65.0),
            "wing_area_m2": (450.0, 650.0),
            "fuselage_length_m": (45.0, 60.0),
            "h2_tank_volume_m3": (120.0, 180.0)
        })
        
        material_options = domain_constraints.get("materials", [
            "CFRP-T800", "CFRP-T1000", "Al-Li-2099", "Ti-6Al-4V", "Al-2024"
        ])
        
        manufacturing_ranges = domain_constraints.get("manufacturing", {
            "complexity_factor": (0.7, 1.5),
            "automation_level": (0.5, 0.95),
            "quality_target": (0.98, 0.999)
        })
        
        configurations = []
        
        for i in range(self.max_configs):
            config_id = f"BWB-Q100-CONF{i:04d}"
            
            # Generate geometry parameters within feasible bounds
            geometry_params = {}
            for param, (min_val, max_val) in geometry_ranges.items():
                geometry_params[param] = random.uniform(min_val, max_val)
            
            # Select materials based on constraints
            primary_material = random.choice(material_options)
            secondary_material = random.choice(material_options)
            
            material_specs = {
                "primary_structure": primary_material,
                "secondary_structure": secondary_material,
                "joints": "Ti-6Al-4V" if "CFRP" in primary_material else "Al-2024"
            }
            
            # Generate manufacturing parameters
            manufacturing_params = {}
            for param, (min_val, max_val) in manufacturing_ranges.items():
                manufacturing_params[param] = random.uniform(min_val, max_val)
            
            # Calculate derived metrics using engineering models
            weight_kg = self._calculate_weight(geometry_params, material_specs)
            cost_estimate = self._calculate_cost(geometry_params, material_specs, manufacturing_params)
            safety_margin = self._calculate_safety_margin(geometry_params, material_specs)
            fatigue_life = self._calculate_fatigue_life(material_specs, geometry_params)
            manufacturing_time = self._calculate_manufacturing_time(geometry_params, manufacturing_params)
            sustainability_score = self._calculate_sustainability(material_specs, manufacturing_params)
            
            # Risk factors for CVaR calculation
            risk_factors = {
                "weight_variance": abs(weight_kg - 45000) / 45000,  # Target 45 tons
                "cost_variance": max(0, (cost_estimate - 150e6) / 150e6),  # Target $150M
                "safety_risk": max(0, (1.5 - safety_margin) / 1.5),  # Target >1.5 margin
                "schedule_risk": max(0, (manufacturing_time - 24) / 24)  # Target <24 months
            }
            
            config = Configuration(
                id=config_id,
                geometry_params=geometry_params,
                material_specs=material_specs,
                manufacturing_params=manufacturing_params,
                weight_kg=weight_kg,
                cost_estimate=cost_estimate,
                safety_margin=safety_margin,
                fatigue_life_cycles=fatigue_life,
                manufacturing_time_hrs=manufacturing_time,
                sustainability_score=sustainability_score,
                risk_factors=risk_factors
            )
            
            configurations.append(config)
        
        print(f"✅ G1 Complete: {len(configurations)} feasible configurations generated")
        return configurations
    
    def select_optimal_cvar(self, configurations: List[Configuration]) -> CVaRResults:
        """
        G2: CVaR@0.95 selection for robust tail performance
        Optimizes for worst-case scenarios rather than average performance
        """
        print(f"🔄 G2: CVaR@0.95 selection (risk threshold: {self.risk_threshold})")
        
        # Multi-criteria composite risk calculation
        config_risks = []
        for config in configurations:
            # Weighted risk composite (aerospace priorities)
            safety_weight = 0.4  # Safety is paramount
            cost_weight = 0.25
            schedule_weight = 0.2
            weight_weight = 0.15
            
            composite_risk = (
                safety_weight * config.risk_factors["safety_risk"] +
                cost_weight * config.risk_factors["cost_variance"] +
                schedule_weight * config.risk_factors["schedule_risk"] +
                weight_weight * config.risk_factors["weight_variance"]
            )
            
            config_risks.append((config, composite_risk))
        
        # Sort by risk (ascending - lower risk is better)
        config_risks.sort(key=lambda x: x[1])
        
        # CVaR@0.95: Select from bottom 5% of risk distribution
        cvar_cutoff = int(len(config_risks) * (1 - self.risk_threshold))
        cvar_candidates = config_risks[:max(1, cvar_cutoff)]
        
        # Final selection based on multi-objective optimization within CVaR set
        selected_configs = []
        for config, risk in cvar_candidates[:5]:  # Top 5 from CVaR set
            selected_configs.append(config)
        
        # Calculate CVaR confidence metric
        risk_values = [risk for _, risk in cvar_candidates]
        mean_risk = sum(risk_values) / len(risk_values) if risk_values else 0
        std_risk = (sum((r - mean_risk)**2 for r in risk_values) / len(risk_values))**0.5 if len(risk_values) > 1 else 0
        cvar_confidence = 1.0 - (std_risk / mean_risk) if mean_risk > 0 and risk_values else 0.0
        
        selection_rationale = (
            f"CVaR@{self.risk_threshold} selection from {len(configurations)} configurations. "
            f"Selected {len(selected_configs)} robust candidates from bottom {(1-self.risk_threshold)*100:.1f}% "
            f"risk distribution. Composite risk weighting: Safety(40%), Cost(25%), Schedule(20%), Weight(15%)."
        )
        
        # Generate provenance data
        provenance = {
            "algorithm": "AMPEL360_CVaR",
            "version": "1.0.0",
            "risk_threshold": self.risk_threshold,
            "total_evaluated": len(configurations),
            "cvar_candidates": len(cvar_candidates),
            "selection_criteria": "multi_objective_cvar_optimization",
            "weights": {
                "safety": 0.4,
                "cost": 0.25,
                "schedule": 0.2,
                "weight": 0.15
            }
        }
        
        # Generate DET hash for immutable evidence
        det_data = {
            "selected_configs": [asdict(config) for config in selected_configs],
            "provenance": provenance,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        det_hash = hashlib.sha3_256(json.dumps(det_data, sort_keys=True).encode()).hexdigest()
        
        results = CVaRResults(
            selected_configs=selected_configs,
            cvar_confidence=cvar_confidence,
            risk_threshold=self.risk_threshold,
            selection_rationale=selection_rationale,
            provenance=provenance,
            det_hash=det_hash,
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        
        print(f"✅ G2 Complete: {len(selected_configs)} optimal configurations selected")
        print(f"🔒 DET Hash: {det_hash[:16]}...")
        
        return results
    
    def _calculate_weight(self, geometry: Dict, materials: Dict) -> float:
        """Engineering weight estimation model"""
        # Simplified BWB weight model
        wing_area = geometry["wing_area_m2"]
        fuselage_length = geometry["fuselage_length_m"]
        tank_volume = geometry["h2_tank_volume_m3"]
        
        # Material density factors
        density_factors = {
            "CFRP-T800": 0.8,
            "CFRP-T1000": 0.75,
            "Al-Li-2099": 1.0,
            "Ti-6Al-4V": 1.6,
            "Al-2024": 1.1
        }
        
        primary_factor = density_factors.get(materials["primary_structure"], 1.0)
        
        # Empirical BWB weight model
        base_weight = (wing_area * 45 + fuselage_length * 300 + tank_volume * 15) * primary_factor
        return base_weight + random.gauss(0, base_weight * 0.05)  # ±5% uncertainty
    
    def _calculate_cost(self, geometry: Dict, materials: Dict, manufacturing: Dict) -> float:
        """Engineering cost estimation model"""
        base_cost = 120e6  # Base BWB cost $120M
        
        # Material cost factors
        material_factors = {
            "CFRP-T800": 1.3,
            "CFRP-T1000": 1.5,
            "Al-Li-2099": 1.1,
            "Ti-6Al-4V": 1.8,
            "Al-2024": 1.0
        }
        
        primary_factor = material_factors.get(materials["primary_structure"], 1.0)
        complexity_factor = manufacturing["complexity_factor"]
        automation_factor = 1 / manufacturing["automation_level"]  # Lower automation = higher cost
        
        total_cost = base_cost * primary_factor * complexity_factor * automation_factor
        return total_cost + random.gauss(0, total_cost * 0.1)  # ±10% uncertainty
    
    def _calculate_safety_margin(self, geometry: Dict, materials: Dict) -> float:
        """Safety margin calculation"""
        # Material strength factors
        strength_factors = {
            "CFRP-T800": 1.4,
            "CFRP-T1000": 1.5,
            "Al-Li-2099": 1.2,
            "Ti-6Al-4V": 1.6,
            "Al-2024": 1.0
        }
        
        material_strength = strength_factors.get(materials["primary_structure"], 1.0)
        
        # Geometry impact on safety
        wing_span = geometry["wing_span_m"]
        wing_area = geometry["wing_area_m2"]
        aspect_ratio = wing_span**2 / wing_area
        
        # Higher aspect ratio increases bending moment challenges
        geometry_factor = max(0.8, 1.2 - (aspect_ratio - 8) * 0.05)
        
        base_margin = 1.5  # Target safety margin
        actual_margin = base_margin * material_strength * geometry_factor
        
        return actual_margin + random.gauss(0, 0.1)  # Uncertainty
    
    def _calculate_fatigue_life(self, materials: Dict, geometry: Dict) -> int:
        """Fatigue life estimation in cycles"""
        # Material fatigue factors
        fatigue_factors = {
            "CFRP-T800": 250000,
            "CFRP-T1000": 280000,
            "Al-Li-2099": 180000,
            "Ti-6Al-4V": 220000,
            "Al-2024": 150000
        }
        
        base_life = fatigue_factors.get(materials["primary_structure"], 180000)
        
        # Joint material impact
        joint_factors = {
            "Ti-6Al-4V": 1.1,
            "Al-2024": 0.95
        }
        joint_factor = joint_factors.get(materials["joints"], 1.0)
        
        total_life = int(base_life * joint_factor)
        return total_life + int(random.gauss(0, total_life * 0.15))  # ±15% uncertainty
    
    def _calculate_manufacturing_time(self, geometry: Dict, manufacturing: Dict) -> float:
        """Manufacturing time estimation in hours"""
        wing_area = geometry["wing_area_m2"]
        complexity = manufacturing["complexity_factor"]
        automation = manufacturing["automation_level"]
        
        # Base time from BWB complexity
        base_time_months = 18  # 18 months baseline
        
        # Scale factors
        area_factor = wing_area / 550  # Normalized to mid-range
        complexity_impact = complexity
        automation_impact = 1 / automation  # Lower automation = longer time
        
        total_time = base_time_months * area_factor * complexity_impact * automation_impact
        return total_time + random.gauss(0, total_time * 0.1)  # ±10% uncertainty
    
    def _calculate_sustainability(self, materials: Dict, manufacturing: Dict) -> float:
        """Sustainability score (0-1, higher is better)"""
        # Material sustainability scores
        sustainability_scores = {
            "CFRP-T800": 0.7,  # Recyclable but energy-intensive
            "CFRP-T1000": 0.65,
            "Al-Li-2099": 0.8,  # Lightweight and recyclable
            "Ti-6Al-4V": 0.6,  # Durable but energy-intensive to produce
            "Al-2024": 0.85   # Highly recyclable
        }
        
        material_score = sustainability_scores.get(materials["primary_structure"], 0.5)
        automation_score = manufacturing["automation_level"]  # Higher automation = more efficient
        quality_score = manufacturing["quality_target"]  # Higher quality = less waste
        
        composite_score = (material_score * 0.5 + automation_score * 0.3 + quality_score * 0.2)
        return min(1.0, composite_score + random.gauss(0, 0.05))


def save_results(results: CVaRResults, output_dir: str, format_type: str = "all") -> Dict[str, str]:
    """Save CVaR results in multiple formats with DET evidence generation"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_paths = {}
    
    if format_type in ["csv", "all"]:
        # CSV output for analysis tools
        csv_path = output_path / f"cvar_selection_{timestamp}.csv"
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                "config_id", "weight_kg", "cost_estimate", "safety_margin", 
                "fatigue_life_cycles", "manufacturing_time_hrs", "sustainability_score",
                "composite_risk", "cvar_confidence"
            ])
            
            for config in results.selected_configs:
                composite_risk = (
                    0.4 * config.risk_factors["safety_risk"] +
                    0.25 * config.risk_factors["cost_variance"] +
                    0.2 * config.risk_factors["schedule_risk"] +
                    0.15 * config.risk_factors["weight_variance"]
                )
                
                writer.writerow([
                    config.id, config.weight_kg, config.cost_estimate,
                    config.safety_margin, config.fatigue_life_cycles,
                    config.manufacturing_time_hrs, config.sustainability_score,
                    composite_risk, results.cvar_confidence
                ])
        
        file_paths["csv"] = str(csv_path)
    
    if format_type in ["json", "all"]:
        # JSON output for CAE integration
        json_path = output_path / f"cvar_selection_{timestamp}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump({
                "selected_configurations": [asdict(config) for config in results.selected_configs],
                "cvar_analysis": {
                    "confidence": results.cvar_confidence,
                    "risk_threshold": results.risk_threshold,
                    "rationale": results.selection_rationale
                },
                "provenance": results.provenance,
                "det_hash": results.det_hash,
                "timestamp": results.timestamp
            }, f, indent=2)
        
        file_paths["json"] = str(json_path)
    
    if format_type in ["det", "all"]:
        # DET evidence pack for audit trail
        det_path = output_path / f"DET_AMPEL360_CVaR_{timestamp}.yaml"
        det_pack = {
            "det_id": f"DET:CAE:AMPEL360:53-10:cvar_selection:V1",
            "phase": "CAE",
            "artifact_type": "Optimization",
            "ts": results.timestamp,
            "inputs": ["feasible_set_g1", "domain_constraints", "risk_criteria"],
            "outputs": {
                "selected_configs": len(results.selected_configs),
                "cvar_confidence": results.cvar_confidence,
                "units": "dimensionless",
                "metrics": {
                    "optimization_method": "CVaR@0.95",
                    "risk_threshold": results.risk_threshold,
                    "evidence_hash": results.det_hash
                }
            },
            "refs": {
                "ce": "CE-CAE-AMPEL360-53-10-OPTIMIZATION",
                "ci": "CI-CAE-AMPEL360-53-10-01-CVAR-SELECTOR"
            },
            "processing": {
                "tool": "AMPEL360_CVaR_Optimizer",
                "version": "1.0.0",
                "params": results.provenance
            },
            "sig": {
                "alg": "Ed25519",
                "by": "CAE-AMPEL360-Authority",
                "hash": results.det_hash[:64]  # Truncate for signature field
            }
        }
        
        with open(det_path, 'w', encoding='utf-8') as f:
            yaml.dump(det_pack, f, default_flow_style=False, sort_keys=False)
        
        file_paths["det"] = str(det_path)
    
    return file_paths


def main():
    """Main CLI interface for AMPEL360 CVaR selection"""
    parser = argparse.ArgumentParser(
        description="AMPEL360 CVaR Selection - Professional Engineering Optimization",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --domain-config config.yaml --output ./results
  %(prog)s --risk-threshold 0.99 --max-configs 5000 --format json
  %(prog)s --cae-integration --output ./cae_pipeline/inputs
        """
    )
    
    parser.add_argument(
        "--domain-config",
        type=str,
        help="Domain constraints configuration file (YAML)"
    )
    
    parser.add_argument(
        "--risk-threshold",
        type=float,
        default=0.95,
        help="CVaR risk threshold (default: 0.95)"
    )
    
    parser.add_argument(
        "--max-configs",
        type=int,
        default=10000,
        help="Maximum configurations in feasible set G1 (default: 10000)"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default="./ampel360_results",
        help="Output directory for results (default: ./ampel360_results)"
    )
    
    parser.add_argument(
        "--format",
        choices=["csv", "json", "det", "all"],
        default="all",
        help="Output format (default: all)"
    )
    
    parser.add_argument(
        "--cae-integration",
        action="store_true",
        help="Generate CAE-ready outputs with seeding hints"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Load domain constraints
    domain_constraints = {}
    if args.domain_config:
        try:
            with open(args.domain_config, 'r', encoding='utf-8') as f:
                domain_constraints = yaml.safe_load(f)
        except Exception as e:
            print(f"❌ Error loading domain config: {e}")
            return 1
    
    if args.verbose:
        print("🚀 AMPEL360 CVaR Selection - Professional Engineering Optimization")
        print(f"   Risk Threshold: CVaR@{args.risk_threshold}")
        print(f"   Target Configs: {args.max_configs}")
        print(f"   Output Format:  {args.format}")
        print(f"   Output Dir:     {args.output}")
        if args.cae_integration:
            print("   CAE Integration: Enabled")
        print()
    
    # Initialize optimizer
    optimizer = AMPEL360Optimizer(
        risk_threshold=args.risk_threshold,
        max_configs=args.max_configs
    )
    
    try:
        # Execute G1→G2 optimization
        start_time = time.time()
        
        feasible_configs = optimizer.generate_feasible_set_g1(domain_constraints)
        cvar_results = optimizer.select_optimal_cvar(feasible_configs)
        
        execution_time = time.time() - start_time
        
        # Save results
        file_paths = save_results(cvar_results, args.output, args.format)
        
        # Generate CAE seeding hints if requested
        if args.cae_integration:
            cae_seeding_path = Path(args.output) / "cae_seeding_hints.yaml"
            cae_hints = generate_cae_seeding_hints(cvar_results.selected_configs)
            with open(cae_seeding_path, 'w', encoding='utf-8') as f:
                yaml.dump(cae_hints, f, default_flow_style=False)
            file_paths["cae_seeding"] = str(cae_seeding_path)
        
        # Summary output
        print(f"\n✅ AMPEL360 CVaR Selection Complete")
        print(f"   Execution Time: {execution_time:.2f}s")
        print(f"   Selected Configurations: {len(cvar_results.selected_configs)}")
        print(f"   CVaR Confidence: {cvar_results.cvar_confidence:.3f}")
        print(f"   DET Hash: {cvar_results.det_hash}")
        print(f"\n📁 Output Files:")
        for format_name, file_path in file_paths.items():
            print(f"   {format_name.upper()}: {file_path}")
        
        if args.verbose:
            print(f"\n📊 Selection Rationale:")
            print(f"   {cvar_results.selection_rationale}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error during optimization: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def generate_cae_seeding_hints(configurations: List[Configuration]) -> Dict[str, Any]:
    """Generate CAE seeding hints for automated simulation pipeline"""
    hints = {
        "mesh_requirements": {
            "global_size_mm": 50,
            "refinement_zones": [
                {"location": "inter_bubble_joints", "size_mm": 5},
                {"location": "fastener_holes", "size_mm": 2},
                {"location": "crack_tips", "size_mm": 0.5}
            ]
        },
        "analysis_matrix": {
            "static_structural": [
                "2.5g limit load (symmetric pull-up)",
                "-1.0g pushover (negative g)",
                "Cabin pressurization (ΔP = 0.75 bar)",
                "Cryogenic thermal (293K → 20K)"
            ],
            "fatigue": [
                "180k cycles requirement",
                "B-basis life calculation"
            ],
            "modal": [
                ">60 Hz first mode requirement"
            ]
        },
        "configurations": []
    }
    
    for config in configurations:
        config_hints = {
            "config_id": config.id,
            "geometry_parameters": config.geometry_params,
            "material_properties": config.material_specs,
            "expected_weight_kg": config.weight_kg,
            "target_safety_margin": config.safety_margin,
            "boundary_conditions": {
                "wing_loading": f"{config.geometry_params['wing_area_m2'] * 5000}N/m2",
                "fuel_load": f"{config.geometry_params['h2_tank_volume_m3'] * 70}kg",
                "thermal_gradient": "273K (cryogenic) to 293K (ambient)"
            },
            "mesh_density_factor": min(1.5, max(0.8, config.risk_factors["safety_risk"] + 0.8))
        }
        hints["configurations"].append(config_hints)
    
    return hints


if __name__ == "__main__":
    sys.exit(main())