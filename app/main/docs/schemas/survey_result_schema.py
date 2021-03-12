save_survey_result_schema = dict(
    type="object", properties=dict(answer=dict(type="string"))
)

load_survey_result_schema = dict(
    type="object",
    properties=dict(
        id=dict(type="string"),
        survey_id=dict(type="string"),
        account_id=dict(type="string"),
        answer=dict(type="string"),
        date=dict(type="string"),
    ),
)
