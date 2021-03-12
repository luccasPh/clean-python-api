login_schema = dict(
    type="object",
    properties=dict(
        email=dict(type="string"),
        password=dict(type="string"),
    ),
    required=["email", "password"],
)
