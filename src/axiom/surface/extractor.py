from axiom.scanner.models import TestSurface

def extract_test_surfaces(project) -> list[TestSurface]:
    surfaces = []

    for route in project.routes:
        # function = None
        #
        # for source_file in project.source_files:
        #     for candidate in source_file.functions:
        #         if candidate.name == route.function:
        #             function = candidate
        #             break
        #
        #     if function:
        #         break
        #
        # surfaces.append(
        #     TestSurface(
        #         route=route,
        #         function=function,
        #     )
        # )
        function = next(
            (
                function
                for function in project.functions
                if function.name == route.function
                and function.file == route.file
            ),
            None,
        )

        surfaces.append(
            TestSurface(
                route = route,
                function = function,
            )
        )


    return surfaces