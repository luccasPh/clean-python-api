survey_path = dict(
    get=dict(
        security=[dict(ApiKeyAuth=[])],
        tags=["Survey"],
        summary="Endpoint para lista as enquetes",
        responses={
            "200": dict(
                description="Sucesso",
                content={
                    "application/json": dict(
                        schema=dict(
                            type="array", items={"$ref": "#/schemas/load_survey"}
                        )
                    )
                },
            ),
            "401": {"$ref": "#/components/unauthorized"},
            "403": {"$ref": "#/components/forbidden"},
            "500": {"$ref": "#/components/server_error"},
        },
    ),
    post=dict(
        security=[dict(ApiKeyAuth=[])],
        tags=["Survey"],
        summary="Endpoint para criar uma enquete",
        description="Acesso apenas para administradores",
        requestBody=dict(
            content={"application/json": dict(schema={"$ref": "#/schemas/add_survey"})},
        ),
        responses={
            "204": dict(
                description="Sucesso",
            ),
            "403": {"$ref": "#/components/forbidden"},
            "500": {"$ref": "#/components/server_error"},
        },
    ),
)
