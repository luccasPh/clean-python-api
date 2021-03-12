signup_schema = dict(
    type="object",
    properties=dict(
        name=dict(type="string"),
        email=dict(type="string"),
        password=dict(type="string"),
        password_confirmation=dict(type="string"),
    ),
    required=["name", "email", "password", "password_confirmation"],
)
