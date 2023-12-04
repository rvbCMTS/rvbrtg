from dataclasses import dataclass
import logging
from math import exp
from typing import Optional

from numpy import log

import pandas as pd
from rich.logging import RichHandler

logger = logging.getLogger()
logger.addHandler(RichHandler())


@dataclass
class BarrierMaterial:
    lead: str = "lead"
    concrete: str = "concrete"
    gypsum: str = "gypsum"
    steel: str = "steel"
    wood: str = "wood"
    plate_glass: str = "plate_glass"


BARRIER_TRANSMISSION_TABLE_DATA: pd.DataFrame = pd.DataFrame(
    [
        {
            "material": "lead",
            "phase": 3,
            "kVp": 50,
            "alpha": 8.801,
            "beta": 2.728e1,
            "gamma": 2.97e-1,
        },
        {
            "material": "lead",
            "phase": 3,
            "kVp": 60,
            "alpha": 6.951,
            "beta": 2.489e1,
            "gamma": 4.198e-1,
        },
        {
            "material": "lead",
            "phase": 3,
            "kVp": 70,
            "alpha": 5.369,
            "beta": 2.349e1,
            "gamma": 5.881e-1,
        },
        {
            "material": "lead",
            "phase": 3,
            "kVp": 80,
            "alpha": 4.404,
            "beta": 2.169e1,
            "gamma": 7.187e-1,
        },
        {
            "material": "lead",
            "phase": 3,
            "kVp": 90,
            "alpha": 3.067,
            "beta": 1.883e1,
            "gamma": 7.726e-1,
        },
        {
            "material": "lead",
            "phase": 3,
            "kVp": 100,
            "alpha": 2.500,
            "beta": 1.528e1,
            "gamma": 7.557e-1,
        },
        {
            "material": "concrete",
            "phase": 3,
            "kVp": 50,
            "alpha": 9.032e-2,
            "beta": 1.712e-1,
            "gamma": 2.324e-1,
        },
        {
            "material": "concrete",
            "phase": 3,
            "kVp": 60,
            "alpha": 6.251e-2,
            "beta": 1.692e-1,
            "gamma": 2.733e-1,
        },
        {
            "material": "concrete",
            "phase": 3,
            "kVp": 70,
            "alpha": 5.087e-2,
            "beta": 1.696e-1,
            "gamma": 3.847e-1,
        },
        {
            "material": "concrete",
            "phase": 3,
            "kVp": 80,
            "alpha": 4.583e-2,
            "beta": 1.549e-1,
            "gamma": 4.926e-1,
        },
        {
            "material": "concrete",
            "phase": 3,
            "kVp": 90,
            "alpha": 4.228e-2,
            "beta": 1.137e-1,
            "gamma": 4.690e-1,
        },
        {
            "material": "concrete",
            "phase": 3,
            "kVp": 100,
            "alpha": 3.295e-2,
            "beta": 8.567e-2,
            "gamma": 4.273e-1,
        },
        {
            "material": "steel",
            "phase": 3,
            "kVp": 50,
            "alpha": 1.817,
            "beta": 4.840,
            "gamma": 4.021e-1,
        },
        {
            "material": "steel",
            "phase": 3,
            "kVp": 60,
            "alpha": 1.183,
            "beta": 4.219,
            "gamma": 4.571e-1,
        },
        {
            "material": "steel",
            "phase": 3,
            "kVp": 70,
            "alpha": 7.149e-1,
            "beta": 3.798,
            "gamma": 5.378e-1,
        },
        {
            "material": "steel",
            "phase": 3,
            "kVp": 80,
            "alpha": 4.921e-1,
            "beta": 3.428,
            "gamma": 6.427e-1,
        },
        {
            "material": "steel",
            "phase": 3,
            "kVp": 90,
            "alpha": 3.971e-1,
            "beta": 2.913,
            "gamma": 7.204e-1,
        },
        {
            "material": "steel",
            "phase": 3,
            "kVp": 100,
            "alpha": 3.415e-1,
            "beta": 2.420,
            "gamma": 7.645e-1,
        },
        {
            "material": "gypsum",
            "phase": 3,
            "kVp": 50,
            "alpha": 3.883e-2,
            "beta": 8.730e-2,
            "gamma": 5.105e-1,
        },
        {
            "material": "gypsum",
            "phase": 3,
            "kVp": 60,
            "alpha": 2.985e-2,
            "beta": 7.961e-2,
            "gamma": 6.169e-1,
        },
        {
            "material": "gypsum",
            "phase": 3,
            "kVp": 70,
            "alpha": 2.302e-2,
            "beta": 7.163e-2,
            "gamma": 7.299e-1,
        },
        {
            "material": "gypsum",
            "phase": 3,
            "kVp": 80,
            "alpha": 1.886e-2,
            "beta": 6.093e-2,
            "gamma": 8.103e-1,
        },
        {
            "material": "gypsum",
            "phase": 3,
            "kVp": 90,
            "alpha": 1.633e-2,
            "beta": 5.039e-2,
            "gamma": 8.585e-1,
        },
        {
            "material": "gypsum",
            "phase": 3,
            "kVp": 100,
            "alpha": 1.466e-2,
            "beta": 4.171e-2,
            "gamma": 8.939e-1,
        },
        {
            "material": "wood",
            "phase": 3,
            "kVp": 50,
            "alpha": 1.076e-2,
            "beta": 1.862e-3,
            "gamma": 1.170,
        },
        {
            "material": "wood",
            "phase": 3,
            "kVp": 60,
            "alpha": 9.512e-3,
            "beta": 9.672e-4,
            "gamma": 1.333,
        },
        {
            "material": "wood",
            "phase": 3,
            "kVp": 70,
            "alpha": 8.550e-3,
            "beta": 5.390e-4,
            "gamma": 1.194,
        },
        {
            "material": "wood",
            "phase": 3,
            "kVp": 80,
            "alpha": 7.903e-3,
            "beta": 8.640e-4,
            "gamma": 9.703e-1,
        },
        {
            "material": "wood",
            "phase": 3,
            "kVp": 90,
            "alpha": 7.511e-3,
            "beta": 1.159e-3,
            "gamma": 1.081,
        },
        {
            "material": "wood",
            "phase": 3,
            "kVp": 100,
            "alpha": 7.230e-3,
            "beta": 9.343e-4,
            "gamma": 1.309,
        },
        {
            "material": "plate_glass",
            "phase": 3,
            "kVp": 50,
            "alpha": 9.721e-2,
            "beta": 1.799e-1,
            "gamma": 4.912e-1,
        },
        {
            "material": "plate_glass",
            "phase": 3,
            "kVp": 60,
            "alpha": 7.452e-2,
            "beta": 1.539e-1,
            "gamma": 5.304e-1,
        },
        {
            "material": "plate_glass",
            "phase": 3,
            "kVp": 70,
            "alpha": 5.791e-2,
            "beta": 1.357e-1,
            "gamma": 5.967e-1,
        },
        {
            "material": "plate_glass",
            "phase": 3,
            "kVp": 80,
            "alpha": 4.955e-2,
            "beta": 1.208e-1,
            "gamma": 7.097e-1,
        },
        {
            "material": "plate_glass",
            "phase": 3,
            "kVp": 90,
            "alpha": 4.550e-2,
            "beta": 1.077e-1,
            "gamma": 8.522e-1,
        },
        {
            "material": "plate_glass",
            "phase": 3,
            "kVp": 100,
            "alpha": 4.278e-2,
            "beta": 9.466e-2,
            "gamma": 9.791e-1,
        },
        {
            "material": "lead",
            "phase": 1,
            "kVp": 50,
            "alpha": 6.046,
            "beta": 3.290e1,
            "gamma": 2.357e-1,
        },
        {
            "material": "lead",
            "phase": 1,
            "kVp": 70,
            "alpha": 4.241,
            "beta": 2.683e1,
            "gamma": 4.814e-1,
        },
        {
            "material": "lead",
            "phase": 1,
            "kVp": 100,
            "alpha": 2.017,
            "beta": 1.315e1,
            "gamma": 4.835e-1,
        },
        {
            "material": "wood",
            "phase": 1,
            "kVp": 50,
            "alpha": 1.131e-2,
            "beta": 3.770e-3,
            "gamma": 1.133,
        },
        {
            "material": "wood",
            "phase": 1,
            "kVp": 70,
            "alpha": 9.010e-3,
            "beta": 1.610e-3,
            "gamma": 1.176,
        },
        {
            "material": "wood",
            "phase": 1,
            "kVp": 100,
            "alpha": 7.200e-3,
            "beta": 9.500e-4,
            "gamma": 1.207,
        },
        {
            "material": "gypsum",
            "phase": 1,
            "kVp": 50,
            "alpha": 3.856e-2,
            "beta": 1.078e-1,
            "gamma": 5.047e-1,
        },
        {
            "material": "gypsum",
            "phase": 1,
            "kVp": 70,
            "alpha": 2.245e-2,
            "beta": 8.524e-2,
            "gamma": 7.112e-1,
        },
        {
            "material": "gypsum",
            "phase": 1,
            "kVp": 100,
            "alpha": 1.478e-2,
            "beta": 5.277e-2,
            "gamma": 8.006e-1,
        },
        {
            "material": "steel",
            "phase": 1,
            "kVp": 50,
            "alpha": 1.642,
            "beta": 6.073,
            "gamma": 4.118e-1,
        },
        {
            "material": "steel",
            "phase": 1,
            "kVp": 70,
            "alpha": 7.744e-1,
            "beta": 5.243,
            "gamma": 6.268e-1,
        },
        {
            "material": "steel",
            "phase": 1,
            "kVp": 100,
            "alpha": 3.695e-1,
            "beta": 3.663,
            "gamma": 8.572e-1,
        },
        {
            "material": "plate_glass",
            "phase": 1,
            "kVp": 50,
            "alpha": 8.721e-2,
            "beta": 2.221e-1,
            "gamma": 4.430e-1,
        },
        {
            "material": "plate_glass",
            "phase": 1,
            "kVp": 70,
            "alpha": 5.713e-2,
            "beta": 1.693e-1,
            "gamma": 6.117e-1,
        },
        {
            "material": "plate_glass",
            "phase": 1,
            "kVp": 100,
            "alpha": 3.984e-2,
            "beta": 1.058e-1,
            "gamma": 6.793e-1,
        },
    ]
)


def air_kerma_per_image_at_1_m_from_source(
    tube_voltage: float = 70.0, tube_current: float = 8.0, exposure_time: float = 100.0
) -> float:
    """Calculate the air KERMA per image at 1 m from the source in mGy/image

    Parameters
    ----------
    tube_voltage
        Operating voltage for the tube in kV
    tube_current
        Operating current for the tube in mA
    exposure_time
        The exposure time in ms

    Returns
    -------
    float
        Air KERMA (in mGy) per image at 1 m from the source
    """
    air_kerma = (
        -0.37
        - 2.58e-3 * tube_voltage
        + (5.37e-4) * (tube_voltage**2)
        - 1.02e-6 * (tube_voltage**3)
    )  # mGy mA-1 min-1
    return air_kerma * tube_current * (exposure_time / 1000 / 60)


def get_barrier_transmission_data(
    material: str, tube_voltage: int, phase: int = 1
) -> tuple[float, float, float]:
    """Extract barrier transmission data (alpha, beta, and gamma) for the specification of the input arguments.

    Parameters
    ----------
    material
        The material of the barrier. Should be one of the materials in the BarrierMaterial dataclass
    tube_voltage
        The tube voltage for the calculation in kV
    phase
        1 for single phase, 3 for three-phase or constant potential

    Returns
    -------
    tuple[float, float, float]
        The alpha, beta, and gamma values of the transmission data
    """
    transmission_data = BARRIER_TRANSMISSION_TABLE_DATA[
        (BARRIER_TRANSMISSION_TABLE_DATA.material == material)
        & (BARRIER_TRANSMISSION_TABLE_DATA.kVp == tube_voltage)
        & (BARRIER_TRANSMISSION_TABLE_DATA.phase == phase)
    ]
    return (
        float(transmission_data.alpha.values[0]),
        float(transmission_data.beta.values[0]),
        float(transmission_data.gamma.values[0]),
    )


def get_barrier_transmission(
    barrier_thickness: float,
    barrier_material: str,
    tube_voltage: float,
    phase: Optional[int] = 1,
) -> float:
    """Calculate the barrier transmission factor and return it as a float

    Parameters
    ----------
    barrier_thickness
        The barrier thickness in mm
    barrier_material
        lead, concrete, steel, plate_glass, or wood
    tube_voltage
        Operating voltage for the tube in kV
    phase
        1 for single phase, 3 for three-phase or constant potential

    Returns
    -------
    float
        Barrier transmission factor

    """
    if phase not in [1, 3]:
        raise ValueError("Invalid phase value. Must be wither 1 or 3")

    alpha, beta, gamma = get_barrier_transmission_data(
        material=barrier_material, tube_voltage=int(tube_voltage), phase=phase
    )

    barrier_transmission = (
        (1 + beta / alpha) * exp(alpha * gamma * barrier_thickness) - beta / alpha
    ) ** (-1 / gamma)

    return barrier_transmission


def total_shielded_primary_air_kerma_in_uGy_per_image(
    air_kerma_per_unit_workload,
    average_transmission_through_patient_and_image_receptors: float,
    distance_from_tube: float,
    primary_barrier_transmission: float,
    workload: float = 1.0,
    use_factor: float = 1.0,
) -> float:
    """Calculate the total shielded primary beam air KERMA in µGy per image

    Parameters
    ----------
    air_kerma_per_unit_workload
        Air KERMA in µGy per unit workload
    average_transmission_through_patient_and_image_receptors
        A factor giving the average transmission through the patient and image receptors
    distance_from_tube
        Distance from the tube in meters
    primary_barrier_transmission
        The primary barrier transmission factor
    workload
        The workload factor
    use_factor
        The use factor of the point in space where for which the calculation is performed

    Returns
    -------
    float
        Total shielded primary beam air KERMA in µGy per image

    """
    return (
        air_kerma_per_unit_workload
        * workload
        * average_transmission_through_patient_and_image_receptors
        * use_factor
        / (distance_from_tube**2)
        * primary_barrier_transmission
    )


def total_shielded_scatter_radiation_air_kerma_in_uGy_per_image(
    primary_beam_air_kerma,
    tube_voltage: float = 70,
    distance_from_patient_to_point_calculation: float = 2.0,
    primary_field_size_in_cm2: float = 12.0,
    distance_from_primary_source_in_m: float = 0.2,  # PID length
    scattering_angle: float = 180.0,
    workload_per_image: float = 1.0,
    fraction_of_exposures_towards_primary_barrier: float = 0.999,
    primary_beam_transmission: float = 0.073
) -> float:
    """Calculate the total shielded scattered radiation air KERMA per image in µGy

    Parameters
    ----------
    primary_beam_air_kerma
    tube_voltage
        Operating voltage of the tube in kV
    distance_from_patient_to_point_calculation
        Distance from the patient to the point fo calculation in meters
    primary_field_size_in_cm2
        Field size of the primary beam in cm2
    distance_from_primary_source_in_m
        Distance from the primary source in meters
    scattering_angle
        Scattering angle in degrees
    workload_per_image
        The workload per image
    fraction_of_exposures_towards_primary_barrier
        Fractions of the exposures that are aimed towards the primary barrier
    primary_beam_transmission

    Returns
    -------
    float
        Total shielded scattered radiation air KERMA per image in µGy

    """
    scaled_scatter_fraction_per_unit_beam_area_in_cm2_at_1m_from_scatter_source = (
        1.60e-2 * (tube_voltage - 125)
        + 8.434
        - 1.105e-1 * scattering_angle
        + 9.828e-4 * (scattering_angle ** 2)
        - 1.741e-6 * (scattering_angle ** 3)
    )

    if fraction_of_exposures_towards_primary_barrier >= 1:
        fraction_of_exposures_towards_primary_barrier = 0.999

    return (
        (
            scaled_scatter_fraction_per_unit_beam_area_in_cm2_at_1m_from_scatter_source / 1000000
            * primary_beam_air_kerma
            * (1 - fraction_of_exposures_towards_primary_barrier)
            * workload_per_image
        ) / (distance_from_patient_to_point_calculation ** 2)
        * (
            primary_beam_transmission * primary_field_size_in_cm2 / (distance_from_primary_source_in_m ** 2)
        )
    )


def calculate_total_air_kerma_behind_barrier(
    tube_voltage: float = 70.0,
    tube_current: float = 8,
    exposure_time: float = 100,
    barrier_material: str = "gypsum",
    barrier_thickness: float = 4 * 13,  # thickness i mm
    phase: int = 1,
    average_transmission_through_patient: float = 0.7,
    distance_to_tube: float = 2.0,
    images_per_year: int = 3200,
    workload: float = 1.0,
    use_factor: float = 1.0,
) -> float:
    """Calculate the total air KERMA behind a barrier.

    Parameters
    ----------
    tube_voltage
        Operating voltage of the tube in kV
    tube_current
        Operating current of the tube in mA
    exposure_time
        Exposure time given in ms
    barrier_material
        Material of the barrier. Should be on of the values available as attributes in the BarrierMaterial dataclass
    barrier_thickness
        Thickness of the barrier given in mm
    phase
        1 for single phase, 3 for three-phase or constant potential
    average_transmission_through_patient
        A factor giving the average transmission through the patient and image receptor/-s
    distance_to_tube
        Distance to the caluclation point from the tube given in meters
    images_per_year
        Number of images taken with the X-ray tube per year
    workload
        The workload of the tube
    use_factor
        Use factor for the calculation point

    Returns
    -------
    float
        The total air KERMA behind the barrier, given in µGy
    """
    air_kerma = air_kerma_per_image_at_1_m_from_source(
        tube_voltage=tube_voltage,
        tube_current=tube_current,
        exposure_time=exposure_time,
    )
    logger.info(f"Air kerma @ 1 m = {air_kerma}")

    barrier_transmission = get_barrier_transmission(
        barrier_thickness=barrier_thickness,
        barrier_material=barrier_material,
        tube_voltage=tube_voltage,
        phase=phase,
    )

    logger.info(f"Primary barrier transmission = {barrier_transmission}")

    total_shielded_air_kerma_per_image = total_shielded_primary_air_kerma_in_uGy_per_image(
        air_kerma_per_unit_workload=air_kerma,
        average_transmission_through_patient_and_image_receptors=average_transmission_through_patient,
        distance_from_tube=distance_to_tube,
        primary_barrier_transmission=barrier_transmission,
        workload=workload,
        use_factor=use_factor,
    ) + total_shielded_scatter_radiation_air_kerma_in_uGy_per_image(
        primary_beam_air_kerma=air_kerma,
        tube_voltage=tube_voltage,
        distance_from_patient_to_point_calculation=distance_to_tube,
        primary_beam_transmission=barrier_transmission
    )

    total_shielded_air_kerma = total_shielded_air_kerma_per_image * images_per_year

    logger.info(f"Total shielded air KERMA = {total_shielded_air_kerma}")
    return total_shielded_air_kerma


def wall_thickness_requirement(
    tube_voltage: float = 70,
    tube_current: float = 8,
    exposure_time: float = 100,
    barrier_material: str = "gypsum",
    phase: int = 1,
    average_transmission_through_patient: float = 0.7,
    distance_to_tube: float = 2.0,
    images_per_year: int = 3200,
    use_factor: float = 1.0,
    permissible_dose_per_year: float = 0.1,
) -> float:
    """Calculate the required barrier thickness given a specified number of images per year and use factor of the area
    the calculation is run for.

    Parameters
    ----------
    tube_voltage
        Operating voltage of the tube in kV
    tube_current
        Operating current of the tube in mA
    exposure_time
        Exposure time given in ms
    barrier_material
        Material of the barrier. Should be on of the values available as attributes in the BarrierMaterial dataclass
    barrier_thickness
        Thickness of the barrier given in mm
    phase
        1 for single phase, 3 for three-phase or constant potential
    average_transmission_through_patient
        A factor giving the average transmission through the patient and image receptor/-s
    distance_to_tube
        Distance to the caluclation point from the tube given in meters
    images_per_year
        Number of images taken with the X-ray tube per year
    use_factor
        Use factor for the calculation point
    permissible_dose_per_year
        The permissible dose in mSv per year

    Returns
    -------
    float
        Required barrier thickness in meters
    """
    bm = BarrierMaterial()

    air_kerma = air_kerma_per_image_at_1_m_from_source(
        tube_voltage=tube_voltage,
        tube_current=tube_current,
        exposure_time=exposure_time,
    )

    barrier_transmission = (
        permissible_dose_per_year
        * distance_to_tube**2
        / (
            air_kerma
            * images_per_year
            * average_transmission_through_patient
            * use_factor
        )
    )

    if barrier_material == bm.concrete and phase == 1:
        logger.info(
            "Setting phase to 3 since we don't have data for concrete for single phase machines"
        )
        phase = 3

    alpha, beta, gamma = get_barrier_transmission_data(
        material=barrier_material, tube_voltage=int(tube_voltage), phase=phase
    )

    required_thickness_in_mm = log(
        (barrier_transmission ** (-gamma) + beta / alpha) / (1 + beta / alpha)
    ) / (alpha * gamma)

    logger.debug(
        f"Required thickness determined to {required_thickness_in_mm.real} mm {barrier_material}"
    )

    return required_thickness_in_mm.real / 1000
