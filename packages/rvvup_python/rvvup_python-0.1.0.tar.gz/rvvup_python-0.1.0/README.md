# python-sdk

python setup.py sdist bdist_wheel

pip install .

pipenv install -e .

~~~
from rvvup import RvvupClient

client = RvvupClient(
    endpoint="https://example.com/graphql",
    merchant_id="your_merchant_id",
    auth_token="your_auth_token",
    user_agent="your_user_agent"
)

methods = client.get_methods()
print(methods)
~~~

Development

~~~
poetry run black .
poetry run flake8
poetry run pre-commit install
~~~


# OpenAPI
~~~
poetry run openapi-python-client generate --path openapi/openapi.yaml --output rvvup_sdk
~~~

# TODO
* OpenAPI doc version isn't compatible with python generation