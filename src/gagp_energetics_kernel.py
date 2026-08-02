import math
from dataclasses import dataclass


@dataclass(frozen=True)
class SystemConstants:
    """Core baseline reference bounds."""
    MITOCHONDRIAL_MEMBRANE_THICKNESS: float = 5.0e-9  # meters
    DIELECTRIC_BREAKDOWN_AIR: float = 3.0e6           # V/m
    DIELECTRIC_BREAKDOWN_MEMBRANE: float = 5.0e8      # V/m
    TARGET_DISCHARGE_POWER: float = 1.21e9            # Watts


@dataclass(frozen=True)
class Vector3D:
    """3D spatial magnitude vector for geometric directional calculations."""
    x: float
    y: float
    z: float

    def magnitude(self) -> float:
        """Calculates absolute vector magnitude."""
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def dot_product(self, other: 'Vector3D') -> float:
        """Computes dot product between two spatial vectors."""
        return (self.x * other.x) + (self.y * other.y) + (self.z * other.z)


class GAGPEnergeticsEngine:
    """
    Parametric throughput kernel evaluating spatial vector alignment,
    dielectric field metrics, and temporal compression limits.
    """

    def __init__(self, constants: SystemConstants = SystemConstants()):
        self.constants = constants

    def evaluate_membrane_field(self, voltage_millivolts: float) -> dict:
        """Evaluates electric field strength across the lipid bilayer membrane."""
        voltage_volts = voltage_millivolts * 1.0e-3
        thickness = self.constants.MITOCHONDRIAL_MEMBRANE_THICKNESS
        
        field_strength = voltage_volts / thickness if thickness > 0 else 0.0
        ratio_vs_air = field_strength / self.constants.DIELECTRIC_BREAKDOWN_AIR
        ratio_vs_membrane = field_strength / self.constants.DIELECTRIC_BREAKDOWN_MEMBRANE

        return {
            "membrane_voltage_volts": voltage_volts,
            "membrane_thickness_meters": thickness,
            "electric_field_volts_per_meter": field_strength,
            "multiplier_vs_air_breakdown": ratio_vs_air,
            "membrane_dielectric_capacity_used": ratio_vs_membrane
        }

    def evaluate_vector_work_power(self, force_vector: Vector3D, velocity_vector: Vector3D) -> dict:
        """
        Evaluates mechanical directional efficiency.
        Handles zero-vector edge cases safely without math domain errors.
        """
        force_mag = force_vector.magnitude()
        vel_mag = velocity_vector.magnitude()
        mag_product = force_mag * vel_mag
        
        aligned_power = force_vector.dot_product(velocity_vector)
        
        # Safe edge-case resolution for zero magnitude vectors
        if mag_product > 0:
            cos_theta_raw = aligned_power / mag_product
            cos_theta_clamped = max(-1.0, min(1.0, cos_theta_raw))
            theta_rad = math.acos(cos_theta_clamped)
        else:
            cos_theta_clamped = 0.0
            theta_rad = 0.0

        theta_deg = math.degrees(theta_rad)

        return {
            "force_magnitude_newtons": force_mag,
            "velocity_magnitude_m_per_s": vel_mag,
            "alignment_angle_radians": theta_rad,
            "alignment_angle_degrees": theta_deg,
            "directional_efficiency_cos_theta": cos_theta_clamped,
            "aligned_power_watts": aligned_power
        }

    def evaluate_high_power_temporal_compression(self, stored_energy_joules: float) -> dict:
        """Calculates compressed pulse duration required to hit target discharge power."""
        target_power = self.constants.TARGET_DISCHARGE_POWER
        pulse_duration = stored_energy_joules / target_power if target_power > 0 else 0.0

        return {
            "target_power_watts": target_power,
            "stored_energy_joules": stored_energy_joules,
            "required_pulse_duration_seconds": pulse_duration,
            "required_pulse_duration_microseconds": pulse_duration * 1.0e6
        }


def run_kernel_audit(
    membrane_mv: float = 200.0,
    force_tuple: tuple = (150.0, 200.0, 50.0),
    velocity_tuple: tuple = (10.0, 12.0, 2.0),
    energy_joules: float = 1210.0
) -> None:
    """Pipeline execution wrapper generating formal audit output."""
    engine = GAGPEnergeticsEngine()

    force = Vector3D(*force_tuple)
    velocity = Vector3D(*velocity_tuple)

    field_data = engine.evaluate_membrane_field(membrane_mv)
    work_data = engine.evaluate_vector_work_power(force, velocity)
    discharge_data = engine.evaluate_high_power_temporal_compression(energy_joules)

    print("==========================================================")
    print("       GAGP ENERGETICS THROUGHPUT KERNEL AUDIT           ")
    print("==========================================================")
    
    print("\n[SECTION 1: BIO-MEMBRANE DIELECTRIC FIELD DYNAMICS]")
    print(f"  Membrane Potential         : {field_data['membrane_voltage_volts']:.4f} V")
    print(f"  Membrane Thickness         : {field_data['membrane_thickness_meters']:.2e} m")
    print(f"  Field Strength             : {field_data['electric_field_volts_per_meter']:.4e} V/m")
    print(f"  Air Breakdown Multiplier   : {field_data['multiplier_vs_air_breakdown']:.4f}x")
    print(f"  Membrane Capacity Consumed : {field_data['membrane_dielectric_capacity_used'] * 100:.2f}%")

    print("\n[SECTION 2: MECHANICAL VECTOR ALIGNMENT & POWER]")
    print(f"  Force Vector Magnitude     : {work_data['force_magnitude_newtons']:.4f} N")
    print(f"  Velocity Vector Magnitude  : {work_data['velocity_magnitude_m_per_s']:.4f} m/s")
    print(f"  Vector Alignment Angle     : {work_data['alignment_angle_degrees']:.4f}° ({work_data['alignment_angle_radians']:.6f} rad)")
    print(f"  Directional Efficiency     : {work_data['directional_efficiency_cos_theta']:.6f}")
    print(f"  Net Aligned Power          : {work_data['aligned_power_watts']:.2f} W")

    print("\n[SECTION 3: HIGH-POWER TEMPORAL COMPRESSION]")
    print(f"  Target Power Threshold     : {discharge_data['target_power_watts']:.4e} W")
    print(f"  Stored Energy Capacity     : {discharge_data['stored_energy_joules']:.2f} J")
    print(f"  Required Pulse Duration    : {discharge_data['required_pulse_duration_seconds']:.4e} s ({discharge_data['required_pulse_duration_microseconds']:.4f} µs)")
    print("==========================================================")


if __name__ == "__main__":
    run_kernel_audit()
