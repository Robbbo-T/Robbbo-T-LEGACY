#!/usr/bin/env python3

def resource_opt_score(normalized_energy_savings, delta_cvar, constraint_satisfaction_rate):
    """
    Compute resource optimization score based on energy savings, risk reduction, and constraint satisfaction.
    
    Args:
        normalized_energy_savings: Energy savings normalized to [0..1]
        delta_cvar: Risk reduction (positive is risk reduction, normalize to [0..1] beforehand)
        constraint_satisfaction_rate: Fraction [0..1] of constraints satisfied
    
    Returns:
        Resource optimization score [0..1]
    """
    # delta_cvar: positive is risk reduction (normalize to [0..1] beforehand)
    # constraint_satisfaction_rate: fraction [0..1]
    return (
        0.4 * float(normalized_energy_savings) +
        0.3 * float(max(0.0, 1.0 - delta_cvar)) +  # lower risk is better
        0.3 * float(constraint_satisfaction_rate)
    )

if __name__ == "__main__":
    # Example usage
    score = resource_opt_score(0.7, 0.2, 1.0)
    print(f"Resource optimization score: {score:.3f}")