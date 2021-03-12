login_path = dict(
    post=dict(
        tags=["Auth"],
        summary="Endpoint para autenticar usuário",
        requestBody=dict(
            content={"application/json": dict(schema={"$ref": "#/schemas/login"})},
        ),
        responses={
            "200": dict(
                description="Sucesso",
                content={"application/json": dict(schema={"$ref": "#/schemas/token"})},
            ),
            "400": {"$ref": "#/components/bad_request"},
            "401": {"$ref": "#/components/unauthorized"},
            "500": {"$ref": "#/components/server_error"},
        },
    )
)
