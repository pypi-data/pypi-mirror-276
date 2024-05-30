from dataclasses import dataclass
from datetime import datetime
from typing import Callable

from IPython.display import Markdown, display

from nortech.derivers.gateways.customer_api import (
    CustomerAPI,
    CustomerWorkspace,
    create_deriver,
)
from nortech.derivers.services.schema import (
    get_deriver_schema_DAG,
)
from nortech.derivers.services.visualize import (
    create_deriver_schema_DAG_mermaid,
    create_deriver_schema_subgraph,
)
from nortech.derivers.values.instance import (
    Deriver,
)
from nortech.derivers.values.schema import (
    DeriverSchema,
)


@dataclass
class TimeWindow:
    start: datetime
    end: datetime

    def __post_init__(self):
        assert self.start <= self.end


def deploy_deriver(
    customer_API: CustomerAPI,
    customer_workspace: CustomerWorkspace,
    deriver: Deriver,
    dry_run: bool,
):
    deriver_schema_DAG = get_deriver_schema_DAG(deriver.create_deriver_schema)

    deriver_diffs = create_deriver(
        customer_API=customer_API,
        customer_workspace=customer_workspace,
        deriver=deriver,
        deriver_schema_DAG=deriver_schema_DAG,
        dry_run=dry_run,
    )

    return deriver_diffs


def visualize_deriver_schema(create_deriver_schema: Callable[[], DeriverSchema]):
    deriver_schema_DAG = get_deriver_schema_DAG(create_deriver_schema)

    mermaid = """
```mermaid
flowchart LR
"""

    mermaid = create_deriver_schema_DAG_mermaid(
        mermaid=mermaid, deriver_schema_DAG=deriver_schema_DAG
    )

    mermaid += """
```
"""

    display(Markdown(mermaid))


def visualize_deriver(deriver: Deriver):
    deriver_schema_DAG = get_deriver_schema_DAG(deriver.create_deriver_schema)

    mermaid = f"""
```mermaid
flowchart LR
    subgraph "Deriver ({deriver.name})"
"""

    mermaid += create_deriver_schema_subgraph(deriver_schema_DAG=deriver_schema_DAG)

    for input_name, input in deriver.inputs.items():
        mermaid += f"""
            {deriver.name.__hash__()}_{input.signal}["{input.signal}<br/>[{input.physicalUnit.symbol.replace(' ', '')}]"] --> {deriver_schema_DAG.name.__hash__()}_{input_name}
        """

    for output_name, output in deriver.outputs.items():
        mermaid += f"""
            {deriver_schema_DAG.name.__hash__()}_{output_name} --> {deriver.name.__hash__()}_{output_name}["{output_name}<br/>[{output.physicalUnit.symbol.replace(' ', '')}]"]
        """

    mermaid += """
end
```
"""

    display(Markdown(mermaid))
