from axiom.context.models import ExpansionBudget, RetrievalUnit


def expand(
        initial_units: list[RetrievalUnit],
        project,
        budget: ExpansionBudget,
) -> list[RetrievalUnit]:

    all_units = list(initial_units)
    current_units = list(initial_units)

    visited = {unit.id for unit in initial_units}

    for _ in range(budget.max_rounds):

        new_units = expand_round(
            current_units,
            project,
            visited,
        )

        if not new_units:
            break

        all_units.extend(new_units)

        for unit in new_units:
            visited.add(unit.id)

        current_units = new_units

    return all_units

def expand_round(
        units: list[RetrievalUnit],
        project,
        visited: set[str],
) -> list[RetrievalUnit]:

    discovered: list[RetrievalUnit] = []
    discovered_ids: set[str] = set()

    for unit in units:

        relationships = analyze_relationships(
            unit,
            project,
        )

        for relationship in relationships:

            candidates = resolve_relationship(
                relationship,
                project,
            )

            for candidate in candidates:

                if candidate.id in visited:
                    continue

                if candidate.id in discovered_ids:
                    continue

                discovered.append(candidate)
                discovered_ids.add(candidate.id)

    return discovered

def analyze_relationships(unit, project):
    raise NotImplementedError


def resolve_relationship(relationship, project):
    raise NotImplementedError