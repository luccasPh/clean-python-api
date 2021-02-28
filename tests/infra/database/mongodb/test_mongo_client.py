from app.infra import get_collection


def test_should_return_a_mongodb_collection():
    collection = get_collection("test")
    assert collection
