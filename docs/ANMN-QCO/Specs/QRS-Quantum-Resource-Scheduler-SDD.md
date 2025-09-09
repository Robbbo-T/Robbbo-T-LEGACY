# QRS Quantum Resource Scheduler Software Design Document

## QRS Overview (slots, refresh, CVaR risk)

The Quantum Resource Scheduler (QRS) manages computational resources across the Quantum Cryogenic Oasis (QCO) to ensure:
- **Fair resource allocation** using Weighted Fair Queuing (WFQ)
- **Thermal stability** through intelligent workload distribution  
- **Risk management** using Conditional Value at Risk (CVaR) methodology
- **System protection** via Control Barrier Functions (CBFs)

### Resource Slots
- **Quantum Processing Slots**: Time-shared access to quantum computers (1-10 ms granularity)
- **Classical Processing**: Edge computing resources for hybrid algorithms
- **I/O Bandwidth**: Data transfer capacity for quantum state preparation and readout
- **Cooling Capacity**: Thermal budget allocation across competing workloads

### Refresh Rates
- **Real-time Applications**: 1000 Hz refresh for flight-critical computations
- **Passenger Services**: 60 Hz for interactive quantum-enhanced experiences
- **Background Processing**: 1 Hz for optimization and machine learning tasks
- **Maintenance Mode**: 0.1 Hz for system diagnostics and calibration

### CVaR Risk Assessment
- **α = 0.95** confidence level for thermal management
- **α = 0.99** confidence level for safety-critical applications
- **Risk Metrics**: Thermal excursion probability, EMI interference likelihood, vibration sensitivity
- **Dynamic Adjustment**: Real-time risk parameter updates based on environmental conditions

## Control Barrier Functions (coherence/thermal/EMI/µg limits)

### Coherence Preservation CBF
```
h_coherence(x) = T_coherence_min - T_current_coherence(x)
```
**Constraint**: Maintains quantum coherence time > 100 µs minimum
**Action**: Reduces refresh rate and suspends non-critical operations when approaching limit

### Thermal Stability CBF  
```
h_thermal(x) = T_budget_remaining(x) - T_safety_margin
```
**Constraint**: Thermal power dissipation < 90% of cooling capacity
**Action**: Load shedding and workload migration to maintain thermal equilibrium

### EMI Protection CBF
```
h_emi(x) = EMI_threshold - EMI_current_level(x)
```
**Constraint**: EMI levels < 100 nT/√Hz in QCO environment
**Action**: Immediate suspension of sensitive quantum operations, switch to degraded mode

### Vibration Control CBF
```
h_vibration(x) = Vibration_limit - Vibration_measured(x)  
```
**Constraint**: Platform acceleration < 10 µg RMS in quantum-sensitive bands
**Action**: Suspend quantum processing, activate enhanced isolation system

## Fairness (WFQ)

### Weighted Fair Queuing Algorithm
**Queue Classes:**
1. **Safety-Critical** (Weight: 0.6): Flight systems, navigation, collision avoidance
2. **Passenger Experience** (Weight: 0.25): Entertainment, communication, personalization  
3. **Optimization** (Weight: 0.10): Route planning, fuel optimization, maintenance scheduling
4. **Research** (Weight: 0.05): Algorithm development, system characterization

**Scheduling Logic:**
```
service_rate_i = (weight_i / sum(active_weights)) * total_capacity
```

**Fairness Metrics:**
- **Max-Min Fairness**: Ensures no queue starves
- **Proportional Share**: Long-term resource allocation matches weights
- **Response Time**: Upper bounds on latency for each class

## Nominal/Degraded Modes (ABU-QuantumProtect)

### Nominal Mode
- **Full Capability**: All quantum computers operational at design parameters
- **Normal Refresh**: Standard refresh rates per application class
- **Complete Sensing**: Full sensor suite operational with redundancy
- **Optimal Performance**: Maximum computational throughput with thermal margins

### Degraded Mode 1: Thermal Limited
- **Reduced Capacity**: 50% quantum processing capability
- **Lower Refresh**: Maximum 10 Hz refresh for passenger services  
- **Load Shedding**: Non-essential computations suspended
- **Recovery Time**: < 60 seconds to return to nominal when thermal conditions improve

### Degraded Mode 2: EMI Interference
- **Shielded Operation**: Only EMI-tolerant classical processing active
- **Static Displays**: Panoramic windows switch to static content
- **Essential Only**: Safety-critical computations continue with increased error checking
- **Auto-Recovery**: Return to nominal when EMI levels return to acceptable range

### Degraded Mode 3: High Vibration
- **Suspended Quantum**: All quantum processing immediately halted
- **Classical Backup**: Fallback to conventional processing algorithms
- **Status Monitoring**: Continuous vibration monitoring for recovery conditions
- **Manual Override**: Ground-commanded return to operation after maintenance inspection

### Emergency Mode: ABU-QuantumProtect Active
- **Safe Shutdown**: Orderly quantum system shutdown in < 5 seconds
- **Isolation**: Complete thermal and electrical isolation of QCO
- **Maintenance Required**: Manual reset and inspection required before restart
- **Event Logging**: Full DET record generation for incident analysis

## Pseudo-API (inputs/outputs)

### Input Interface
```json
{
  "request_id": "string",
  "application_class": "safety|passenger|optimization|research", 
  "resource_requirements": {
    "quantum_slots": "integer",
    "classical_cpu": "percentage", 
    "memory_mb": "integer",
    "refresh_rate_hz": "float"
  },
  "priority": "1-10",
  "deadline_ms": "integer",
  "thermal_budget_mw": "float"
}
```

### Output Interface
```json
{
  "request_id": "string",
  "allocation_status": "granted|denied|queued|degraded",
  "allocated_resources": {
    "quantum_slots": "integer",
    "actual_refresh_hz": "float",
    "start_time_ms": "integer", 
    "duration_ms": "integer"
  },
  "system_status": {
    "mode": "nominal|degraded|emergency",
    "thermal_margin_percent": "float",
    "emi_level_nt_sqrt_hz": "float",
    "vibration_level_ug": "float"
  },
  "estimated_performance": {
    "quantum_fidelity": "float",
    "classical_throughput": "ops_per_sec", 
    "latency_ms": "float"
  }
}
```

## Logging to DET

### Standard Log Events
All QRS operations generate structured DET records:

```json
{
  "det_id": "DET:QRS:BWB:56-XX:scheduler_decision:V1.0",
  "timestamp": "2025-01-15T14:30:00.000Z",
  "event_type": "resource_allocation",
  "scheduler_state": {
    "mode": "nominal|degraded|emergency",
    "active_queues": "integer",
    "total_utilization": "percentage"
  },
  "allocation_decision": {
    "request_id": "string", 
    "granted_resources": "object",
    "rejection_reason": "string|null"
  },
  "system_metrics": {
    "thermal_power_mw": "float",
    "emi_level_nt_sqrt_hz": "float", 
    "vibration_ug_rms": "float",
    "quantum_coherence_us": "float"
  },
  "cbf_status": {
    "thermal_barrier": "float",
    "emi_barrier": "float",
    "vibration_barrier": "float", 
    "coherence_barrier": "float"
  },
  "performance_metrics": {
    "allocation_latency_ms": "float",
    "queue_depths": "object",
    "fairness_index": "float"
  },
  "signature": "PQC-Dilithium3"
}
```

### Critical Event Logging
- **CBF Violations**: Immediate DET generation when any control barrier function triggers
- **Mode Transitions**: Complete system state logging during nominal/degraded/emergency transitions
- **Performance Anomalies**: Statistical outliers and unexpected resource utilization patterns
- **Security Events**: Unauthorized access attempts and data exfiltration detection
- **Maintenance Triggers**: Predictive maintenance alerts and system health degradation