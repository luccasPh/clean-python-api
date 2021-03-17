survey_result_path = dict(
    put=dict(
        security=[dict(ApiKeyAuth=[])],
        tags=["Survey"],
        summary="Endpoint para salvar a resposta de uma enquete",
        requestBody=dict(
            content={
                "application/json": dict(
                    schema={"$ref": "#/schemas/save_survey_result"}
                )
            },
        ),
        parameters=[
            {
                "in": "path",
                "name": "survey_id",
                "description": "ID da enquete a ser respondida",
                "type": "string",
                "required": True,
            }
        ],
        responses={
            "200": dict(
                description="Sucesso",
                content={
                    "application/json": dict(
                        schema={"$ref": "#/schemas/load_survey_result"}
                    )
                },
            ),
            "403": {"$ref": "#/components/forbidden"},
            "500": {"$ref": "#/components/server_error"},
        },
    ),
    get=dict(
        security=[dict(ApiKeyAuth=[])],
        tags=["Survey"],
        summary="Endpoint para consultar resultado de uma enquete",
        parameters=[
            {
                "in": "path",
                "name": "survey_id",
                "description": "ID da enquete para consultar",
                "type": "string",
                "required": True,
            }
        ],
        responses={
            "200": dict(
                description="Sucesso",
                content={
                    "application/json": dict(
                        schema=dict(
                            type="array", items={"$ref": "#/schemas/load_survey_result"}
                        )
                    )
                },
            ),
            "403": {"$ref": "#/components/forbidden"},
            "500": {"$ref": "#/components/server_error"},
        },
    ),
)
