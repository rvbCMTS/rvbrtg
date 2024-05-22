from dataclasses import dataclass

from io_calculation import BarrierMaterial, wall_thickness_requirement
from rich.console import Console
from rich.progress import track
from rich.style import Style
from rich.table import Table


@dataclass
class CalculationSite:
    site: str
    datum: str
    distance_tube_to_barrier: float
    images_per_year: int = 3200
    tube_current: float = 7.0
    tube_voltage: float = 70.0


CALCULATION_SITES: list[CalculationSite] = [
    CalculationSite(site="Stenbergska", datum="2023-01-25", images_per_year=300, distance_tube_to_barrier=1.58),
    CalculationSite(site="Bergvattengården", datum="2023-03-03", distance_tube_to_barrier=1.6),
    CalculationSite(site="Nordmaling", datum="2023-09-22", distance_tube_to_barrier=1.8),
    CalculationSite(site="Vännäs", datum="2023-11-06", images_per_year=2110, distance_tube_to_barrier=3.35),
]

barrier_material = BarrierMaterial()


def calculate_barrier_material_thickness_requirement(calc_site: CalculationSite) -> tuple[str, str, str, str, str, str]:
    need_gypsum = (
        wall_thickness_requirement(
            tube_voltage=calc_site.tube_voltage,
            tube_current=calc_site.tube_current,
            barrier_material=barrier_material.gypsum,
            images_per_year=calc_site.images_per_year,
            distance_to_tube=calc_site.distance_tube_to_barrier,
        )
        * 1000
    )

    need_concrete = (
        wall_thickness_requirement(
            tube_voltage=calc_site.tube_voltage,
            tube_current=calc_site.tube_current,
            barrier_material=barrier_material.concrete,
            images_per_year=calc_site.images_per_year,
            distance_to_tube=calc_site.distance_tube_to_barrier,
        )
        * 1000
    )

    need_lead = (
        wall_thickness_requirement(
            tube_voltage=calc_site.tube_voltage,
            tube_current=calc_site.tube_current,
            barrier_material=barrier_material.lead,
            images_per_year=calc_site.images_per_year,
            distance_to_tube=calc_site.distance_tube_to_barrier,
        )
        * 1000
    )

    return (
        calc_site.site,
        calc_site.datum,
        f"{need_gypsum:.2f}",
        f"{need_concrete:.2f}",
        f"{need_lead:.2f}",
        str(calc_site.images_per_year),
    )


def main():
    table = Table(
        title="Behov strålskärmningstjocklek",
        header_style=Style(bold=True),
        row_styles=[Style(italic=False), Style(italic=True)],
    )
    table.add_column("Sajt", justify="left", no_wrap=True)
    table.add_column("Datum", justify="left", no_wrap=True)
    table.add_column("Gips (mm)", justify="right", no_wrap=True)
    table.add_column("Betong (mm)", justify="right", no_wrap=True)
    table.add_column("Bly (mm)", justify="right", no_wrap=True)
    table.add_column("Bilder/år", justify="right", no_wrap=True)

    for ind, calc_site in track(enumerate(CALCULATION_SITES), description="Beräknar behov..."):
        table.add_row(*calculate_barrier_material_thickness_requirement(calc_site))

    console = Console(width=120)
    console.print(table)


if __name__ == "__main__":
    main()
