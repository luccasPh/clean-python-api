server_error = dict(
    description="Erro no servidor",
    content={"application/json": dict(schema={"$ref": "#/schemas/error"})},
)
