signup_path = dict(
    post=dict(
        tags=["Auth"],
        summary="Endpoint para cria conta de um usuário",
        requestBody=dict(
            content={"application/json": dict(schema={"$ref": "#/schemas/signup"})},
        ),
        responses={
            "204": dict(description="Sucesso"),
            "400": {"$ref": "#/components/bad_request"},
            "403": {"$ref": "#/components/forbidden"},
            "500": {"$ref": "#/components/server_error"},
        },
    )
)
