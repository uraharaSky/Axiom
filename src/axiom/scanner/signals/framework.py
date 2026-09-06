from ast import List

from axiom.scanner.models import Project, FrameworkSignal

PYTHON_FRAMEWORKS = {
    "fastapi": "FastAPI",
    "flask": "Flask",
    "django": "Django",
}

JAVASCRIPT_FRAMEWORKS = {
    "express": "Express",
    "next": "Next.js",
}

def detect_frameworks(
        project: Project,
) -> list[FrameworkSignal]:

    signals: dict[tuple[str, str], FrameworkSignal] = {}

    for import_ in project.imports:

        module = import_.module

        if import_.file.suffix == ".py":

            frameworks = PYTHON_FRAMEWORKS

            language = "python"

        elif import_.file.suffix == ".js":

            frameworks = JAVASCRIPT_FRAMEWORKS

            language = "javascript"

        else:
            continue

        for package, name in frameworks.items():

            if not (
                    module == package
                    or module.startswith(f"{package}.")
                    or (
                            language == "javascript"
                            and module.startswith(f"{package}/")
                    )
            ):
                continue

            key = (name, language)

            if key not in signals:

                signals[key] = FrameworkSignal(
                    name=name,
                    language=language,
                    files=[],
                )

            if import_.file not in signals[key].files:

                signals[key].files.append(
                    import_.file
                )

    return list(signals.values())