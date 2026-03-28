"""Example demonstrating sus-inspector with a complex, nested object."""

from __future__ import annotations

import sys
from pathlib import Path

# Add src to path for local development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pydantic import BaseModel, Field

from sus_inspector import sus


class Moon(BaseModel):
    """Represents a moon orbiting a planet."""

    name: str
    radius_km: float


class Planet(BaseModel):
    """Represents a planet in a solar system."""

    name: str
    moons: list[Moon] = Field(default_factory=list)
    has_life: bool = False


class SolarSystem(BaseModel):
    """Represents a solar system with a star and planets."""

    star_name: str
    planets: list[Planet]


class BlackHole:
    """A custom class (non-Pydantic) to show how sus handles generic objects."""

    def __init__(self, name: str, mass_solar_masses: float) -> None:
        """Initialize a black hole.

        Args:
            name: The name of the black hole.
            mass_solar_masses: Mass in solar masses.

        """
        self.name = name
        self.mass = mass_solar_masses
        self.is_active = True

    def __repr__(self) -> str:
        """Return a string representation of the black hole.

        Returns:
            str: Representation string.

        """
        return f"BlackHole({self.name})"


def create_complex_universe() -> dict[str, object]:
    """Create a deeply nested dictionary for inspection.

    Returns:
        dict[str, object]: Deeply nested dictionary.

    """
    earth = Planet(
        name="Earth",
        moons=[Moon(name="The Moon", radius_km=1737.4)],
        has_life=True,
    )

    mars = Planet(
        name="Mars",
        moons=[
            Moon(name="Phobos", radius_km=11.2),
            Moon(name="Deimos", radius_km=6.2),
        ],
    )

    milky_way: dict[str, object] = {
        "metadata": {
            "age_gyr": 13.61,
            "type": "Spiral",
            "constellations": ["Sagittarius", "Cassiopeia", "Andromeda"],
        },
        "systems": [
            SolarSystem(star_name="Sun", planets=[earth, mars]),
        ],
        "anomalies": [
            BlackHole(name="Sagittarius A*", mass_solar_masses=4.1e6),
        ],
    }

    return milky_way


if __name__ == "__main__":
    universe = create_complex_universe()

    # Inspect the complex universe object
    sus / universe
