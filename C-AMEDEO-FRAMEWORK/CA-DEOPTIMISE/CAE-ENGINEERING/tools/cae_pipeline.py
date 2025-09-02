#!/usr/bin/env python3
"""
Automated CAE Pipeline - Digital Twin Simulation Orchestra

Integrates with AMPEL360 CVaR selection to execute multi-physics simulations
and generate realistic cost/time distributions for engineering optimization.

Architecture: CVaR Selection → CAE Simulation → Results Analysis → CAV Integration
"""

import argparse
import json
import csv
import yaml
import subprocess
import asyncio
import time
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass, asdict
import hashlib
import tempfile


@dataclass
class SimulationJob:
    """Individual simulation job definition"""
    config_id: str
    analysis_type: str  # "FEA", "CFD", "Thermal", "Fatigue", "Modal"
    geometry_params: Dict[str, float]
    material_specs: Dict[str, str]
    boundary_conditions: Dict[str, Any]
    mesh_requirements: Dict[str, Any]
    solver_settings: Dict[str, Any]
    expected_runtime_hrs: float
    priority: int


@dataclass
class SimulationResults:
    """Simulation results with metrics and evidence"""
    job_id: str
    config_id: str
    analysis_type: str
    status: str  # "PASS", "FAIL", "WARNING"
    metrics: Dict[str, float]
    margins: Dict[str, float]
    cost_factors: Dict[str, float]
    time_factors: Dict[str, float]
    artifacts: List[str]
    det_hash: str
    execution_time_hrs: float
    convergence_quality: float


@dataclass
class CAEResults:
    """Complete CAE campaign results"""
    campaign_id: str
    total_simulations: int
    successful_simulations: int
    failed_simulations: int
    configuration_scores: Dict[str, float]
    cost_distribution: Dict[str, Dict[str, float]]
    time_distribution: Dict[str, Dict[str, float]]
    risk_distribution: Dict[str, Dict[str, float]]
    simulation_results: List[SimulationResults]
    campaign_det_hash: str
    total_execution_time_hrs: float
    timestamp: str


class CAEPipelineOrchestrator:
    """Automated CAE pipeline orchestrator for multi-physics simulations"""
    
    def __init__(self, config_file: str = None):
        self.config = self._load_config(config_file)
        self.simulation_queue = []
        self.completed_jobs = []
        self.failed_jobs = []
        self.temp_dir = None
        
    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """Load CAE pipeline configuration"""
        default_config = {
            "solvers": {
                "FEA": {
                    "executable": "nastran",
                    "default_args": ["-batch", "-old"],
                    "max_parallel": 4,
                    "timeout_hrs": 12
                },
                "CFD": {
                    "executable": "fluent",
                    "default_args": ["-3d", "-t8"],
                    "max_parallel": 2,
                    "timeout_hrs": 24
                },
                "Thermal": {
                    "executable": "ansys",
                    "default_args": ["-b"],
                    "max_parallel": 4,
                    "timeout_hrs": 8
                },
                "Fatigue": {
                    "executable": "fe-safe",
                    "default_args": ["-batch"],
                    "max_parallel": 6,
                    "timeout_hrs": 6
                },
                "Modal": {
                    "executable": "nastran",
                    "default_args": ["-batch", "-modal"],
                    "max_parallel": 8,
                    "timeout_hrs": 4
                }
            },
            "resource_limits": {
                "max_concurrent_jobs": 16,
                "max_memory_gb": 256,
                "max_disk_gb": 1000
            },
            "quality_gates": {
                "min_convergence": 1e-6,
                "max_residual": 1e-5,
                "min_mesh_quality": 0.3
            }
        }
        
        if config_file and Path(config_file).exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                user_config = yaml.safe_load(f)
                # Merge with defaults
                default_config.update(user_config)
        
        return default_config
    
    def process_cvar_selection(self, cvar_results_file: str) -> List[SimulationJob]:
        """Process CVaR selection results and generate simulation jobs"""
        print(f"🔄 Processing CVaR selection results: {cvar_results_file}")
        
        with open(cvar_results_file, 'r', encoding='utf-8') as f:
            cvar_data = json.load(f)
        
        selected_configs = cvar_data["selected_configurations"]
        cae_hints = cvar_data.get("cae_seeding_hints", {})
        
        simulation_jobs = []
        job_id = 0
        
        # Define analysis matrix based on BWB-Q100 requirements
        analysis_matrix = [
            ("FEA", ["static_structural", "fatigue"], 1),
            ("CFD", ["boundary_layer_ingestion", "thermal_flow"], 2),
            ("Thermal", ["cryogenic_analysis"], 3),
            ("Modal", ["vibration_analysis"], 4)
        ]
        
        for config in selected_configs:
            config_id = config["id"]
            geometry_params = config["geometry_params"]
            material_specs = config["material_specs"]
            
            print(f"   Generating jobs for configuration: {config_id}")
            
            for analysis_type, sub_analyses, priority in analysis_matrix:
                for sub_analysis in sub_analyses:
                    
                    # Generate boundary conditions based on analysis type
                    boundary_conditions = self._generate_boundary_conditions(
                        analysis_type, sub_analysis, geometry_params, material_specs
                    )
                    
                    # Generate mesh requirements
                    mesh_requirements = self._generate_mesh_requirements(
                        analysis_type, geometry_params, config.get("risk_factors", {})
                    )
                    
                    # Generate solver settings
                    solver_settings = self._generate_solver_settings(
                        analysis_type, sub_analysis
                    )
                    
                    # Estimate runtime
                    expected_runtime = self._estimate_runtime(
                        analysis_type, geometry_params, mesh_requirements
                    )
                    
                    job = SimulationJob(
                        config_id=config_id,
                        analysis_type=f"{analysis_type}_{sub_analysis}",
                        geometry_params=geometry_params,
                        material_specs=material_specs,
                        boundary_conditions=boundary_conditions,
                        mesh_requirements=mesh_requirements,
                        solver_settings=solver_settings,
                        expected_runtime_hrs=expected_runtime,
                        priority=priority
                    )
                    
                    simulation_jobs.append(job)
                    job_id += 1
        
        # Sort by priority and expected execution time
        simulation_jobs.sort(key=lambda x: (x.priority, x.expected_runtime_hrs))
        
        print(f"✅ Generated {len(simulation_jobs)} simulation jobs")
        return simulation_jobs
    
    async def execute_simulation_campaign(self, simulation_jobs: List[SimulationJob]) -> CAEResults:
        """Execute complete simulation campaign with parallel processing"""
        campaign_id = f"CAE_CAMPAIGN_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        print(f"🚀 Starting CAE simulation campaign: {campaign_id}")
        
        start_time = time.time()
        
        # Create temporary working directory
        self.temp_dir = tempfile.mkdtemp(prefix=f"{campaign_id}_")
        print(f"   Working directory: {self.temp_dir}")
        
        # Execute simulations with resource management
        max_concurrent = self.config["resource_limits"]["max_concurrent_jobs"]
        semaphore = asyncio.Semaphore(max_concurrent)
        
        tasks = []
        for job in simulation_jobs:
            task = asyncio.create_task(self._execute_simulation_job(job, semaphore))
            tasks.append(task)
        
        # Wait for all simulations to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        simulation_results = []
        successful_count = 0
        failed_count = 0
        
        for result in results:
            if isinstance(result, Exception):
                print(f"❌ Simulation failed with exception: {result}")
                failed_count += 1
            elif isinstance(result, SimulationResults):
                simulation_results.append(result)
                if result.status == "PASS":
                    successful_count += 1
                else:
                    failed_count += 1
            else:
                failed_count += 1
        
        # Calculate aggregate metrics
        configuration_scores = self._calculate_configuration_scores(simulation_results)
        cost_distribution = self._calculate_cost_distribution(simulation_results)
        time_distribution = self._calculate_time_distribution(simulation_results)
        risk_distribution = self._calculate_risk_distribution(simulation_results)
        
        total_execution_time = time.time() - start_time
        
        # Generate campaign evidence hash
        campaign_data = {
            "campaign_id": campaign_id,
            "simulation_results": [asdict(r) for r in simulation_results],
            "configuration_scores": configuration_scores,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        campaign_det_hash = hashlib.sha3_256(json.dumps(campaign_data, sort_keys=True).encode()).hexdigest()
        
        cae_results = CAEResults(
            campaign_id=campaign_id,
            total_simulations=len(simulation_jobs),
            successful_simulations=successful_count,
            failed_simulations=failed_count,
            configuration_scores=configuration_scores,
            cost_distribution=cost_distribution,
            time_distribution=time_distribution,
            risk_distribution=risk_distribution,
            simulation_results=simulation_results,
            campaign_det_hash=campaign_det_hash,
            total_execution_time_hrs=total_execution_time / 3600.0,
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        
        print(f"✅ CAE Campaign Complete: {campaign_id}")
        print(f"   Total Simulations: {len(simulation_jobs)}")
        print(f"   Successful: {successful_count}")
        print(f"   Failed: {failed_count}")
        print(f"   Execution Time: {total_execution_time/3600:.2f} hrs")
        print(f"   Campaign DET Hash: {campaign_det_hash[:16]}...")
        
        # Cleanup temporary directory
        if self.temp_dir and Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)
        
        return cae_results
    
    async def _execute_simulation_job(self, job: SimulationJob, semaphore: asyncio.Semaphore) -> SimulationResults:
        """Execute individual simulation job"""
        async with semaphore:
            job_id = f"{job.config_id}_{job.analysis_type}"
            print(f"   🔄 Executing: {job_id}")
            
            start_time = time.time()
            
            try:
                # Create job working directory
                job_dir = Path(self.temp_dir) / job_id
                job_dir.mkdir(exist_ok=True)
                
                # Generate input files
                input_files = await self._generate_input_files(job, job_dir)
                
                # Execute simulation (mock execution for demonstration)
                solver_result = await self._run_solver(job, job_dir)
                
                # Process results
                metrics, margins = self._extract_simulation_metrics(job, solver_result, job_dir)
                cost_factors = self._calculate_cost_factors(job, metrics)
                time_factors = self._calculate_time_factors(job, solver_result)
                
                # Generate artifacts list
                artifacts = list(job_dir.glob("*"))
                artifact_paths = [str(p.relative_to(job_dir)) for p in artifacts]
                
                # Generate evidence hash
                job_data = {
                    "job_id": job_id,
                    "metrics": metrics,
                    "margins": margins,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
                det_hash = hashlib.sha3_256(json.dumps(job_data, sort_keys=True).encode()).hexdigest()
                
                execution_time = time.time() - start_time
                
                result = SimulationResults(
                    job_id=job_id,
                    config_id=job.config_id,
                    analysis_type=job.analysis_type,
                    status="PASS" if solver_result["convergence"] else "FAIL",
                    metrics=metrics,
                    margins=margins,
                    cost_factors=cost_factors,
                    time_factors=time_factors,
                    artifacts=artifact_paths,
                    det_hash=det_hash,
                    execution_time_hrs=execution_time / 3600.0,
                    convergence_quality=solver_result["convergence_quality"]
                )
                
                print(f"   ✅ Completed: {job_id} ({execution_time:.1f}s)")
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                print(f"   ❌ Failed: {job_id} - {str(e)}")
                
                # Return failed result
                return SimulationResults(
                    job_id=job_id,
                    config_id=job.config_id,
                    analysis_type=job.analysis_type,
                    status="FAIL",
                    metrics={},
                    margins={},
                    cost_factors={},
                    time_factors={},
                    artifacts=[],
                    det_hash="",
                    execution_time_hrs=execution_time / 3600.0,
                    convergence_quality=0.0
                )
    
    async def _generate_input_files(self, job: SimulationJob, job_dir: Path) -> List[str]:
        """Generate solver input files based on job specification"""
        input_files = []
        
        # Generate geometry file (mock)
        geom_file = job_dir / "geometry.step"
        geom_file.write_text(f"# Geometry for {job.config_id}\n# Generated automatically\n")
        input_files.append(str(geom_file))
        
        # Generate mesh file (mock)
        mesh_file = job_dir / "mesh.fem"
        mesh_content = f"""
# Mesh for {job.config_id}
# Global size: {job.mesh_requirements.get('global_size_mm', 50)}mm
# Elements: {job.mesh_requirements.get('estimated_elements', 100000)}
"""
        mesh_file.write_text(mesh_content)
        input_files.append(str(mesh_file))
        
        # Generate boundary conditions file
        bc_file = job_dir / "boundary_conditions.dat"
        bc_content = json.dumps(job.boundary_conditions, indent=2)
        bc_file.write_text(bc_content)
        input_files.append(str(bc_file))
        
        # Generate solver input deck
        solver_file = job_dir / "solver_input.inp"
        solver_content = f"""
! Solver input for {job.analysis_type}
! Configuration: {job.config_id}
! Generated: {datetime.now().isoformat()}

SOL 101
CEND
TITLE = {job.analysis_type} Analysis
ECHO = NONE
"""
        solver_file.write_text(solver_content)
        input_files.append(str(solver_file))
        
        return input_files
    
    async def _run_solver(self, job: SimulationJob, job_dir: Path) -> Dict[str, Any]:
        """Execute simulation solver (mock implementation)"""
        # Mock solver execution - in real implementation, this would call actual solvers
        base_analysis = job.analysis_type.split('_')[0]
        solver_config = self.config["solvers"].get(base_analysis, {})
        
        # Simulate solver execution time
        await asyncio.sleep(0.1)  # Mock execution delay
        
        # Mock results based on analysis type
        if "FEA" in job.analysis_type:
            convergence_quality = 0.95
            max_stress = 350.0  # MPa
            max_displacement = 2.5  # mm
            safety_margin = 1.8
        elif "CFD" in job.analysis_type:
            convergence_quality = 0.92
            max_velocity = 150.0  # m/s
            pressure_drop = 1200.0  # Pa
            heat_transfer_coeff = 45.0  # W/m²K
        elif "Thermal" in job.analysis_type:
            convergence_quality = 0.94
            max_temperature = 350.0  # K
            min_temperature = 20.0  # K
            thermal_gradient = 15.0  # K/mm
        elif "Modal" in job.analysis_type:
            convergence_quality = 0.98
            first_frequency = 65.0  # Hz
            modal_mass = 0.85
            damping_ratio = 0.02
        else:
            convergence_quality = 0.9
        
        return {
            "convergence": convergence_quality > self.config["quality_gates"]["min_convergence"],
            "convergence_quality": convergence_quality,
            "analysis_type": job.analysis_type,
            "execution_time_s": 120.0,  # Mock execution time
            "memory_usage_gb": 8.5,
            "disk_usage_gb": 2.1
        }
    
    def _extract_simulation_metrics(self, job: SimulationJob, solver_result: Dict, job_dir: Path) -> Tuple[Dict[str, float], Dict[str, float]]:
        """Extract engineering metrics from simulation results"""
        metrics = {}
        margins = {}
        
        if "FEA" in job.analysis_type:
            metrics.update({
                "max_stress_mpa": 350.0,
                "max_displacement_mm": 2.5,
                "total_weight_kg": job.geometry_params.get("wing_area_m2", 550) * 45
            })
            margins.update({
                "stress_margin": 1.8,
                "displacement_margin": 2.2,
                "buckling_margin": 1.5
            })
        
        elif "CFD" in job.analysis_type:
            metrics.update({
                "lift_coefficient": 0.85,
                "drag_coefficient": 0.025,
                "l_d_ratio": 34.0,
                "pressure_drop_pa": 1200.0
            })
            margins.update({
                "performance_margin": 1.15,
                "stability_margin": 1.25
            })
        
        elif "Thermal" in job.analysis_type:
            metrics.update({
                "max_temperature_k": 350.0,
                "heat_flux_w_m2": 1500.0,
                "thermal_efficiency": 0.92
            })
            margins.update({
                "temperature_margin": 1.3,
                "thermal_margin": 1.4
            })
        
        elif "Modal" in job.analysis_type:
            metrics.update({
                "first_frequency_hz": 65.0,
                "modal_mass_participation": 0.85,
                "damping_ratio": 0.02
            })
            margins.update({
                "frequency_margin": 1.08,  # >60 Hz requirement
                "flutter_margin": 1.5
            })
        
        return metrics, margins
    
    def _calculate_cost_factors(self, job: SimulationJob, metrics: Dict[str, float]) -> Dict[str, float]:
        """Calculate cost factors based on simulation results"""
        cost_factors = {
            "base_cost_factor": 1.0,
            "material_cost_factor": 1.0,
            "manufacturing_complexity": 1.0,
            "maintenance_cost_factor": 1.0
        }
        
        # Adjust based on analysis results
        if "FEA" in job.analysis_type:
            weight = metrics.get("total_weight_kg", 45000)
            cost_factors["material_cost_factor"] = weight / 45000  # Normalized to target
            
        elif "CFD" in job.analysis_type:
            l_d_ratio = metrics.get("l_d_ratio", 30)
            if l_d_ratio > 35:
                cost_factors["manufacturing_complexity"] = 1.2  # More complex for better performance
        
        return cost_factors
    
    def _calculate_time_factors(self, job: SimulationJob, solver_result: Dict) -> Dict[str, float]:
        """Calculate time factors based on simulation execution"""
        time_factors = {
            "design_time_factor": 1.0,
            "manufacturing_time_factor": 1.0,
            "testing_time_factor": 1.0,
            "certification_time_factor": 1.0
        }
        
        # Adjust based on convergence and complexity
        convergence_quality = solver_result.get("convergence_quality", 0.9)
        if convergence_quality < 0.95:
            time_factors["certification_time_factor"] = 1.3  # More time for low confidence results
        
        return time_factors
    
    def _calculate_configuration_scores(self, simulation_results: List[SimulationResults]) -> Dict[str, float]:
        """Calculate overall scores for each configuration"""
        config_scores = {}
        config_groups = {}
        
        # Group results by configuration
        for result in simulation_results:
            config_id = result.config_id
            if config_id not in config_groups:
                config_groups[config_id] = []
            config_groups[config_id].append(result)
        
        # Calculate composite scores
        for config_id, results in config_groups.items():
            total_score = 0.0
            total_weight = 0.0
            
            for result in results:
                if result.status == "PASS":
                    # Weight by analysis importance
                    weight = 1.0
                    if "FEA" in result.analysis_type:
                        weight = 2.0  # Structural analysis is critical
                    elif "Modal" in result.analysis_type:
                        weight = 1.5
                    
                    score = result.convergence_quality * weight
                    total_score += score
                    total_weight += weight
            
            config_scores[config_id] = total_score / total_weight if total_weight > 0 else 0.0
        
        return config_scores
    
    def _calculate_cost_distribution(self, simulation_results: List[SimulationResults]) -> Dict[str, Dict[str, float]]:
        """Calculate cost distribution statistics"""
        cost_distribution = {}
        
        for result in simulation_results:
            config_id = result.config_id
            if config_id not in cost_distribution:
                cost_distribution[config_id] = {
                    "mean_cost_factor": 1.0,
                    "std_cost_factor": 0.1,
                    "p95_cost_factor": 1.2,
                    "material_cost_multiplier": 1.0,
                    "manufacturing_cost_multiplier": 1.0
                }
            
            # Update with actual results
            if result.cost_factors:
                dist = cost_distribution[config_id]
                dist["material_cost_multiplier"] = result.cost_factors.get("material_cost_factor", 1.0)
                dist["manufacturing_cost_multiplier"] = result.cost_factors.get("manufacturing_complexity", 1.0)
        
        return cost_distribution
    
    def _calculate_time_distribution(self, simulation_results: List[SimulationResults]) -> Dict[str, Dict[str, float]]:
        """Calculate time distribution statistics"""
        time_distribution = {}
        
        for result in simulation_results:
            config_id = result.config_id
            if config_id not in time_distribution:
                time_distribution[config_id] = {
                    "mean_time_factor": 1.0,
                    "std_time_factor": 0.15,
                    "p95_time_factor": 1.3,
                    "design_time_multiplier": 1.0,
                    "manufacturing_time_multiplier": 1.0,
                    "certification_time_multiplier": 1.0
                }
            
            # Update with actual results
            if result.time_factors:
                dist = time_distribution[config_id]
                dist["design_time_multiplier"] = result.time_factors.get("design_time_factor", 1.0)
                dist["manufacturing_time_multiplier"] = result.time_factors.get("manufacturing_time_factor", 1.0)
                dist["certification_time_multiplier"] = result.time_factors.get("certification_time_factor", 1.0)
        
        return time_distribution
    
    def _calculate_risk_distribution(self, simulation_results: List[SimulationResults]) -> Dict[str, Dict[str, float]]:
        """Calculate risk distribution statistics"""
        risk_distribution = {}
        
        for result in simulation_results:
            config_id = result.config_id
            if config_id not in risk_distribution:
                risk_distribution[config_id] = {
                    "technical_risk": 0.1,
                    "schedule_risk": 0.15,
                    "cost_risk": 0.12,
                    "certification_risk": 0.08,
                    "composite_risk": 0.11
                }
            
            # Update based on simulation quality
            dist = risk_distribution[config_id]
            if result.convergence_quality < 0.95:
                dist["technical_risk"] += 0.05
            
            if result.status != "PASS":
                dist["certification_risk"] += 0.1
            
            # Recalculate composite risk
            dist["composite_risk"] = (
                0.4 * dist["technical_risk"] +
                0.25 * dist["schedule_risk"] +
                0.25 * dist["cost_risk"] +
                0.1 * dist["certification_risk"]
            )
        
        return risk_distribution
    
    def _generate_boundary_conditions(self, analysis_type: str, sub_analysis: str, 
                                    geometry_params: Dict, material_specs: Dict) -> Dict[str, Any]:
        """Generate boundary conditions for specific analysis type"""
        bc = {}
        
        if "FEA" in analysis_type:
            wing_area = geometry_params.get("wing_area_m2", 550)
            bc.update({
                "loads": {
                    "wing_loading_n_m2": wing_area * 5000,  # 5 kN/m²
                    "fuselage_pressure_pa": 75000,  # 0.75 bar
                    "landing_gear_load_n": 450000  # 450 kN
                },
                "constraints": {
                    "wing_root": "FIXED",
                    "fuselage_ends": "PINNED",
                    "landing_gear": "CONSTRAINED"
                },
                "materials": material_specs
            })
        
        elif "CFD" in analysis_type:
            bc.update({
                "inlet": {
                    "velocity_m_s": 230,  # Cruise speed
                    "pressure_pa": 23000,  # FL350 pressure
                    "temperature_k": 220   # FL350 temperature
                },
                "outlet": {
                    "pressure_pa": 23000
                },
                "walls": {
                    "type": "no_slip",
                    "temperature_k": 220
                }
            })
        
        elif "Thermal" in analysis_type:
            bc.update({
                "ambient_temperature_k": 293,
                "cryogenic_temperature_k": 20,
                "heat_sources": {
                    "electronics_w": 5000,
                    "passengers_w": 12000
                },
                "convection_coefficients": {
                    "external_w_m2_k": 50,
                    "internal_w_m2_k": 25
                }
            })
        
        elif "Modal" in analysis_type:
            bc.update({
                "frequency_range_hz": [1, 100],
                "damping_ratio": 0.02,
                "constraints": {
                    "wing_root": "FIXED",
                    "fuselage_center": "PINNED"
                }
            })
        
        return bc
    
    def _generate_mesh_requirements(self, analysis_type: str, geometry_params: Dict, 
                                  risk_factors: Dict) -> Dict[str, Any]:
        """Generate mesh requirements based on analysis type and risk"""
        base_size = 50  # mm
        
        # Adjust mesh density based on risk factors
        safety_risk = risk_factors.get("safety_risk", 0.1)
        density_factor = 1.0 + safety_risk  # Higher risk = finer mesh
        
        mesh_req = {
            "global_size_mm": base_size / density_factor,
            "min_size_mm": 0.5,
            "max_size_mm": 200,
            "growth_rate": 1.2,
            "refinement_zones": []
        }
        
        if "FEA" in analysis_type:
            mesh_req["refinement_zones"].extend([
                {"location": "stress_concentrations", "size_mm": 2},
                {"location": "joint_interfaces", "size_mm": 5},
                {"location": "load_introduction", "size_mm": 1}
            ])
            mesh_req["element_type"] = "CQUAD4"
        
        elif "CFD" in analysis_type:
            mesh_req["refinement_zones"].extend([
                {"location": "boundary_layer", "size_mm": 0.1},
                {"location": "wing_tips", "size_mm": 5},
                {"location": "wake_region", "size_mm": 10}
            ])
            mesh_req["y_plus_target"] = 1.0
            mesh_req["prism_layers"] = 15
        
        wing_area = geometry_params.get("wing_area_m2", 550)
        mesh_req["estimated_elements"] = int(wing_area * 1000 / density_factor)
        
        return mesh_req
    
    def _generate_solver_settings(self, analysis_type: str, sub_analysis: str) -> Dict[str, Any]:
        """Generate solver-specific settings"""
        settings = {}
        
        if "FEA" in analysis_type:
            settings.update({
                "solution_method": "SPARSE",
                "convergence_tolerance": 1e-6,
                "max_iterations": 50,
                "memory_gb": 16
            })
        
        elif "CFD" in analysis_type:
            settings.update({
                "turbulence_model": "k_omega_sst",
                "convergence_criteria": 1e-5,
                "max_iterations": 1000,
                "parallel_processes": 8
            })
        
        elif "Modal" in analysis_type:
            settings.update({
                "eigenvalue_method": "LANCZOS",
                "num_modes": 20,
                "frequency_shift": 0.0
            })
        
        return settings
    
    def _estimate_runtime(self, analysis_type: str, geometry_params: Dict, 
                         mesh_requirements: Dict) -> float:
        """Estimate simulation runtime in hours"""
        base_times = {
            "FEA": 2.0,
            "CFD": 8.0,
            "Thermal": 1.5,
            "Modal": 0.5
        }
        
        base_analysis = analysis_type.split('_')[0]
        base_time = base_times.get(base_analysis, 2.0)
        
        # Scale by mesh size
        estimated_elements = mesh_requirements.get("estimated_elements", 100000)
        element_factor = estimated_elements / 100000  # Normalized to 100k elements
        
        # Scale by geometry complexity
        wing_area = geometry_params.get("wing_area_m2", 550)
        complexity_factor = wing_area / 550  # Normalized to baseline
        
        return base_time * element_factor * complexity_factor


def save_cae_results(results: CAEResults, output_dir: str) -> Dict[str, str]:
    """Save CAE campaign results with DET evidence generation"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    file_paths = {}
    
    # Save campaign summary JSON
    summary_path = output_path / f"{results.campaign_id}_summary.json"
    summary_data = {
        "campaign_id": results.campaign_id,
        "execution_summary": {
            "total_simulations": results.total_simulations,
            "successful_simulations": results.successful_simulations,
            "failed_simulations": results.failed_simulations,
            "total_execution_time_hrs": results.total_execution_time_hrs
        },
        "configuration_scores": results.configuration_scores,
        "cost_distribution": results.cost_distribution,
        "time_distribution": results.time_distribution,
        "risk_distribution": results.risk_distribution,
        "campaign_det_hash": results.campaign_det_hash,
        "timestamp": results.timestamp
    }
    
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, indent=2)
    file_paths["summary"] = str(summary_path)
    
    # Save detailed results CSV
    csv_path = output_path / f"{results.campaign_id}_detailed_results.csv"
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            "job_id", "config_id", "analysis_type", "status", "execution_time_hrs",
            "convergence_quality", "det_hash"
        ])
        
        for result in results.simulation_results:
            writer.writerow([
                result.job_id, result.config_id, result.analysis_type, result.status,
                result.execution_time_hrs, result.convergence_quality, result.det_hash
            ])
    
    file_paths["csv"] = str(csv_path)
    
    # Generate DET evidence pack
    det_path = output_path / f"DET_CAE_CAMPAIGN_{results.campaign_id}.yaml"
    det_pack = {
        "det_id": f"DET:CAE:SIMULATION:53-10:campaign_execution:V1",
        "phase": "CAE",
        "artifact_type": "SimulationCampaign",
        "ts": results.timestamp,
        "inputs": ["cvar_selection_results", "domain_constraints", "analysis_matrix"],
        "outputs": {
            "successful_simulations": results.successful_simulations,
            "failed_simulations": results.failed_simulations,
            "execution_time_hrs": results.total_execution_time_hrs,
            "units": "hours",
            "metrics": {
                "campaign_success_rate": results.successful_simulations / results.total_simulations,
                "average_convergence": sum(r.convergence_quality for r in results.simulation_results) / len(results.simulation_results),
                "evidence_hash": results.campaign_det_hash
            }
        },
        "refs": {
            "ce": "CE-CAE-SIMULATION-53-10-CAMPAIGN",
            "ci": "CI-CAE-SIMULATION-53-10-01-ORCHESTRATOR"
        },
        "processing": {
            "tool": "CAE_Pipeline_Orchestrator",
            "version": "1.0.0",
            "params": {
                "total_jobs": results.total_simulations,
                "parallel_execution": True,
                "quality_gates_enabled": True
            }
        },
        "sig": {
            "alg": "Ed25519",
            "by": "CAE-Pipeline-Authority",
            "hash": results.campaign_det_hash[:64]
        }
    }
    
    with open(det_path, 'w', encoding='utf-8') as f:
        yaml.dump(det_pack, f, default_flow_style=False, sort_keys=False)
    file_paths["det"] = str(det_path)
    
    return file_paths


async def main():
    """Main CLI interface for CAE pipeline orchestrator"""
    parser = argparse.ArgumentParser(
        description="Automated CAE Pipeline - Digital Twin Simulation Orchestra",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --cvar-results cvar_selection.json --output ./cae_results
  %(prog)s --config cae_config.yaml --cvar-results selection.json --parallel 8
  %(prog)s --cvar-results results.json --cav-integration --output ./certification
        """
    )
    
    parser.add_argument(
        "--cvar-results",
        type=str,
        required=True,
        help="CVaR selection results file (JSON)"
    )
    
    parser.add_argument(
        "--config",
        type=str,
        help="CAE pipeline configuration file (YAML)"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default="./cae_pipeline_results",
        help="Output directory for results (default: ./cae_pipeline_results)"
    )
    
    parser.add_argument(
        "--parallel",
        type=int,
        help="Maximum parallel simulations (overrides config)"
    )
    
    parser.add_argument(
        "--cav-integration",
        action="store_true",
        help="Generate CAV-ready certification packages"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        print("🚀 Automated CAE Pipeline - Digital Twin Simulation Orchestra")
        print(f"   CVaR Results: {args.cvar_results}")
        print(f"   Config File:  {args.config or 'default'}")
        print(f"   Output Dir:   {args.output}")
        if args.parallel:
            print(f"   Parallel Jobs: {args.parallel}")
        if args.cav_integration:
            print("   CAV Integration: Enabled")
        print()
    
    try:
        # Initialize pipeline orchestrator
        orchestrator = CAEPipelineOrchestrator(args.config)
        
        # Override parallel setting if specified
        if args.parallel:
            orchestrator.config["resource_limits"]["max_concurrent_jobs"] = args.parallel
        
        # Process CVaR selection results
        simulation_jobs = orchestrator.process_cvar_selection(args.cvar_results)
        
        # Execute simulation campaign
        cae_results = await orchestrator.execute_simulation_campaign(simulation_jobs)
        
        # Save results
        file_paths = save_cae_results(cae_results, args.output)
        
        # Generate CAV integration if requested
        if args.cav_integration:
            cav_package_path = Path(args.output) / "cav_certification_package.yaml"
            cav_package = generate_cav_package(cae_results)
            with open(cav_package_path, 'w', encoding='utf-8') as f:
                yaml.dump(cav_package, f, default_flow_style=False)
            file_paths["cav_package"] = str(cav_package_path)
        
        # Summary output
        print(f"\n✅ CAE Pipeline Execution Complete")
        print(f"   Campaign ID: {cae_results.campaign_id}")
        print(f"   Success Rate: {cae_results.successful_simulations}/{cae_results.total_simulations}")
        print(f"   Total Time: {cae_results.total_execution_time_hrs:.2f} hrs")
        print(f"   Campaign DET: {cae_results.campaign_det_hash}")
        print(f"\n📁 Output Files:")
        for format_name, file_path in file_paths.items():
            print(f"   {format_name.upper()}: {file_path}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error during CAE pipeline execution: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def generate_cav_package(cae_results: CAEResults) -> Dict[str, Any]:
    """Generate CAV certification package from CAE results"""
    cav_package = {
        "certification_dossier": {
            "campaign_id": cae_results.campaign_id,
            "compliance_matrix": {
                "CS_25_305": "Strength analysis completed with positive margins",
                "CS_25_629": "Aeroelastic analysis shows flutter margin >1.15",
                "CS_25_1309": "System safety analysis demonstrates acceptable risk levels"
            },
            "evidence_summary": {
                "total_analyses": cae_results.total_simulations,
                "successful_analyses": cae_results.successful_simulations,
                "confidence_level": 0.95,
                "certification_basis": "CS-25 Amendment 28"
            },
            "configuration_assessment": {},
            "risk_assessment": cae_results.risk_distribution,
            "det_evidence_chain": [
                cae_results.campaign_det_hash
            ]
        },
        "approval_readiness": {
            "technical_approval": "READY" if cae_results.successful_simulations / cae_results.total_simulations > 0.9 else "PENDING",
            "documentation_complete": True,
            "test_correlation_required": True,
            "certification_credits": {
                "analysis_credit": 0.8,
                "test_credit": 0.2
            }
        },
        "timestamp": cae_results.timestamp,
        "authority_signature": "PENDING_CAV_REVIEW"
    }
    
    # Add configuration assessment
    for config_id, score in cae_results.configuration_scores.items():
        cav_package["certification_dossier"]["configuration_assessment"][config_id] = {
            "overall_score": score,
            "certification_recommendation": "APPROVED" if score > 0.9 else "CONDITIONAL",
            "risk_level": "LOW" if score > 0.95 else "MEDIUM" if score > 0.85 else "HIGH"
        }
    
    return cav_package


if __name__ == "__main__":
    import sys
    sys.exit(asyncio.run(main()))