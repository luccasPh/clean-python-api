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
                        schema=dict(type="array", items={"$ref": "#/schemas/survey"})
                    )
                },
            ),
            "403": {"$ref": "#/components/forbidden"},
            "500": {"$ref": "#/components/server_error"},
        },
    )
)
