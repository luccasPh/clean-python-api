forbidden = dict(
    description="Acesso negado",
    content={"application/json": dict(schema={"$ref": "#/schemas/error"})},
)
