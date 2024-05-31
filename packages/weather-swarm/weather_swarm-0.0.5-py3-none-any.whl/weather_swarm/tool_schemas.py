from swarms import get_openai_function_schema_from_func

from weather_swarm.tools.tools import (
    request_metar_nearest,
    point_query,
    request_ndfd_basic,
    point_query_region,
    request_ndfd_hourly,
)


def get_schemas_for_funcs(funcs):
    schemas = []
    for func in funcs:
        name = func.__name__
        description = func.__doc__
        schema = get_openai_function_schema_from_func(
            func, name=name, description=description
        )
        schemas.append(schema)
    merged_schemas = "\n".join(schemas)
    return merged_schemas


funcs = [
    request_metar_nearest,
    point_query,
    request_ndfd_basic,
    point_query_region,
    request_ndfd_hourly,
]

schemas = get_schemas_for_funcs(funcs)
print(schemas)
