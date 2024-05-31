# directly select out a basic derivation
from typing import List

from preql.core.models import (
    Concept,
)
from preql.core.processing.nodes import (
    StrategyNode,
    SelectNode,
)
from preql.core.processing.node_generators.common import (
    resolve_function_parent_concepts,
)
from preql.constants import logger

LOGGER_PREFIX = "[GEN_BASIC_NODE]"


def gen_basic_node(
    concept: Concept,
    local_optional: List[Concept],
    environment,
    g,
    depth: int,
    source_concepts,
):
    parent_concepts = resolve_function_parent_concepts(concept)
    depth_prefix = "\t" * depth
    if not parent_concepts:
        raise ValueError(
            f"concept {concept} has basic lineage {concept.derivation} {type(concept.lineage)} {str(concept.lineage)}  but no parents!"
        )
    output_concepts = [concept] + local_optional
    partials = []

    enriched = source_concepts(
        mandatory_list=parent_concepts + local_optional,
        environment=environment,
        g=g,
        depth=depth + 1,
    )
    if not enriched:
        logger.info(
            f"{depth_prefix}{LOGGER_PREFIX} Could not find enrichment node for {concept} with local_optional {local_optional}"
        )
        return None
    parents: List[StrategyNode] = [enriched]
    for x in output_concepts:
        sources = [p for p in parents if x in p.output_concepts]
        if not sources:
            continue
        if all(x in source.partial_concepts for source in sources):
            partials.append(x)
    logger.info(f"{depth_prefix}{LOGGER_PREFIX} Returning basic select node")
    return SelectNode(
        input_concepts=parent_concepts + local_optional,
        output_concepts=output_concepts,
        environment=environment,
        g=g,
        parents=parents,
        depth=depth,
        partial_concepts=partials,
    )
