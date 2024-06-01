from typing import Any

from nortech.derivers.values.physical_units_schema import PhysicalQuantity


def get_physical_quantity(deriver_io: Any) -> PhysicalQuantity:
    return PhysicalQuantity(
        **deriver_io[1].json_schema_extra["physicalQuantity"] # type: ignore
    )