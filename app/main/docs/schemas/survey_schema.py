load_survey_schema = dict(
    type="object",
    properties=dict(
        id=dict(type="string"),
        question=dict(type="string"),
        answers=dict(
            type="array",
            items=dict(
                type="object",
                properties=dict(image=dict(type="string"), answer=dict(type="string")),
            ),
        ),
        date=dict(type="string"),
    ),
)

add_survey_schema = dict(
    type="object",
    properties=dict(
        question=dict(type="string"),
        answers=dict(
            type="array",
            items=dict(
                type="object",
                properties=dict(image=dict(type="string"), answer=dict(type="string")),
            ),
        ),
    ),
    required=["question", "answers"],
)
