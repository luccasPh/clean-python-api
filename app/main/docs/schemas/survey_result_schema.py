save_survey_result_schema = dict(
    type="object", properties=dict(answer=dict(type="string")), required=["answer"]
)

load_survey_result_schema = dict(
    type="object",
    properties=dict(
        survey_id=dict(type="string"),
        question=dict(type="string"),
        answers=dict(
            type="array",
            items=dict(
                type="object",
                properties=dict(
                    image=dict(type="string"),
                    answers=dict(type="string"),
                    count=dict(type="number"),
                    percent=dict(type="number"),
                ),
            ),
        ),
        date=dict(type="string"),
    ),
)
