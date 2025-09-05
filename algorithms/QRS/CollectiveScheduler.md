# CollectiveScheduler: Quantum Resource Scheduler Algorithm Design

## State Vector

The QRS maintains a comprehensive state vector **x(t)** representing the system's quantum and classical resource allocation state:

```
x(t) = [
  q_states[N_qubits],           // Quantum computer states (idle/active/coherent/error)
  thermal_powers[N_zones],      // Power dissipation per thermal zone [mW]
  emi_levels[N_sensors],        // EMI measurements per sensor location [nT/√Hz]
  vibration_levels[N_axes],     // Vibration levels per measurement axis [µg]
  queue_depths[N_queues],       // Number of pending requests per queue class
  resource_utilization[N_res],  // Classical computing resource usage [%]
  cbf_margins[N_barriers],      // Control Barrier Function safety margins
  mode_state,                   // System operational mode (nominal/degraded/emergency)
  fairness_metrics[N_queues]    // Weighted fair queuing performance indicators
]
```

**Dimensions**: 
- N_qubits = 100 (quantum processing units)
- N_zones = 8 (thermal management zones)  
- N_sensors = 12 (EMI monitoring positions)
- N_axes = 6 (vibration measurement directions)
- N_queues = 4 (priority classes: safety/passenger/optimization/research)
- N_res = 16 (classical computing resources)
- N_barriers = 4 (thermal/EMI/vibration/coherence CBFs)

## Invariants (CBFs)

Control Barrier Functions ensure the system remains within safe operating bounds:

### 1. Thermal CBF
```
h_thermal(x) = P_cooling_max - Σ(thermal_powers) - P_safety_margin
```
**Invariant**: h_thermal(x) ≥ 0 (total power < cooling capacity)
**Parameters**: P_cooling_max = 50 mW, P_safety_margin = 5 mW

### 2. EMI CBF
```  
h_emi(x) = EMI_threshold - max(emi_levels)
```
**Invariant**: h_emi(x) ≥ 0 (EMI below QCO compatibility limit)
**Parameters**: EMI_threshold = 100 nT/√Hz @ 1 Hz

### 3. Vibration CBF
```
h_vibration(x) = Vib_threshold - RMS(vibration_levels[10:100 Hz])
```
**Invariant**: h_vibration(x) ≥ 0 (vibration within quantum coherence limits)
**Parameters**: Vib_threshold = 10 µg RMS

### 4. Coherence CBF
```
h_coherence(x) = T_coherence_min - max(predicted_decoherence_time)
```
**Invariant**: h_coherence(x) ≥ 0 (quantum coherence maintained)
**Parameters**: T_coherence_min = 100 µs

**CBF Class K Functions**: All CBFs use exponential class K functions α(r) = λr with λ = 0.1 s⁻¹ for smooth constraint enforcement.

## MPC Objective

The Model Predictive Control objective balances performance optimization with safety constraint satisfaction over prediction horizon T_horizon = 10 seconds:

### Primary Objective
```
J_primary(x, u) = Σ(t=0 to T_horizon) [
  w_throughput * throughput(x(t), u(t)) +
  w_latency * (-expected_latency(x(t), u(t))) +  
  w_fairness * fairness_index(x(t))
]
```

### CBF Safety Constraints
```
J_safety(x, u) = Σ(CBF violations) * penalty_weight
```

**Total Objective**:
```
J_total = J_primary + J_safety
```

**Weights**:
- w_throughput = 0.4 (quantum operations per second)
- w_latency = 0.3 (minimize response time)
- w_fairness = 0.3 (ensure equitable resource allocation)
- penalty_weight = 1000 (safety violation penalty)

## Fairness Rule

Weighted Fair Queuing (WFQ) implementation with dynamic weight adaptation:

### Base Queue Weights
```
weights = {
  safety_critical: 0.60,    // Flight systems, navigation
  passenger_exp: 0.25,      // Entertainment, UI, personalization
  optimization: 0.10,       // Route planning, fuel optimization  
  research: 0.05            // Algorithm development, characterization
}
```

### Dynamic Weight Adjustment
```
effective_weight[i](t) = base_weight[i] * priority_multiplier[i](t) * deadline_urgency[i](t)

where:
priority_multiplier[i] = 1.0 + 0.5 * (10 - avg_response_time[i]) / 10
deadline_urgency[i] = min(2.0, deadline_remaining / expected_execution_time)
```

### Fairness Metrics
- **Max-Min Fairness**: min(allocation[i] / weight[i]) maximized
- **Proportional Share**: long_term_allocation[i] ≈ weight[i] (within 5%)
- **Jain's Index**: fairness = (Σ x_i)² / (n * Σ x_i²), target ≥ 0.95

## Degraded/Nominal Mode Table

| Mode | Trigger Conditions | Resource Limits | Recovery Criteria |
|------|-------------------|----------------|-------------------|
| **Nominal** | All CBFs > 10% margin | 100% quantum capacity, normal refresh rates | Default operational state |
| **Thermal Degraded** | h_thermal < 10% margin | 50% quantum capacity, passenger refresh ≤ 30 Hz | h_thermal > 20% for 60s |
| **EMI Degraded** | h_emi < 10% margin | Classical only, static windows | h_emi > 20% for 30s |
| **Vibration Degraded** | h_vibration < 10% margin | Quantum suspended, essential only | h_vibration > 20% for 10s |
| **Emergency** | Any CBF violated | Safe shutdown initiated | Manual reset + inspection |

### Mode Transition Logic
```python
def update_mode(current_mode, cbf_margins, time_in_mode):
    min_margin = min(cbf_margins)
    
    if min_margin < 0:  # CBF violation
        return "emergency"
    elif min_margin < 0.1:  # <10% margin
        if current_mode == "nominal":
            return determine_degraded_mode(cbf_margins)
        else:
            return current_mode  # Stay in current degraded mode
    elif min_margin > 0.2 and time_in_mode > recovery_time:  # >20% margin
        return "nominal"  # Recovery to nominal
    else:
        return current_mode  # No mode change
```

## DET Log Schema

All scheduler decisions generate structured DET records for audit and performance analysis:

```json
{
  "det_id": "DET:QRS:BWB:56-XX:scheduler_decision:V1.0",
  "timestamp": "ISO-8601 timestamp",
  "event_type": "allocation_decision|mode_transition|cbf_violation|fairness_alert",
  
  "system_state": {
    "mode": "nominal|thermal_degraded|emi_degraded|vibration_degraded|emergency",
    "total_utilization_percent": "float [0-100]",
    "active_queues": "integer",
    "quantum_computers_online": "integer [0-100]"
  },
  
  "cbf_status": {
    "thermal_margin_percent": "float",
    "emi_margin_nt_sqrt_hz": "float", 
    "vibration_margin_ug": "float",
    "coherence_margin_us": "float",
    "min_margin_percent": "float"
  },
  
  "allocation_decision": {
    "request_id": "uuid",
    "queue_class": "safety|passenger|optimization|research",
    "allocated_resources": {
      "quantum_slots": "integer",
      "classical_cpu_percent": "float",
      "memory_mb": "integer",
      "duration_ms": "integer"
    },
    "rejection_reason": "string|null"
  },
  
  "fairness_metrics": {
    "jain_index": "float [0-1]",
    "max_min_ratio": "float",
    "queue_utilizations": "array[float]",
    "weight_violations": "array[boolean]"
  },
  
  "performance_metrics": {
    "decision_latency_us": "float",
    "throughput_ops_per_sec": "float", 
    "avg_response_time_ms": "float",
    "cbf_computation_time_us": "float"
  },
  
  "mpc_solution": {
    "objective_value": "float",
    "horizon_steps": "integer",
    "solver_iterations": "integer", 
    "convergence_status": "optimal|suboptimal|infeasible"
  },
  
  "signature": "PQC-Dilithium3"
}
```

## Implementation Notes

### Real-Time Constraints
- **Decision Latency**: < 1 ms for safety-critical requests
- **CBF Evaluation**: < 100 µs per barrier function
- **MPC Solving**: < 10 ms for 10-second horizon
- **Fairness Update**: < 500 µs every scheduling epoch

### Fault Tolerance
- **Redundant CBF Calculation**: Dual-channel voting for safety
- **Graceful Degradation**: Fall back to simpler scheduling if MPC fails
- **State Persistence**: Critical state saved to non-volatile storage
- **Recovery Protocols**: Systematic restart procedures after emergency shutdown

### Scalability
- **Parallel Processing**: CBF evaluation parallelized across cores
- **Efficient Data Structures**: Priority heaps and balanced trees for queue management
- **Incremental Updates**: Only recompute changed portions of state vector
- **Memory Management**: Bounded memory usage with circular buffers for historical data