bad_request = dict(
    description="Requisição invalida",
    content={"application/json": dict(schema={"$ref": "#/schemas/error"})},
)
