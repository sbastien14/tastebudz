# Tastebudz
A web application that leverages machine learning to recommend local restaurants to the user based on their swipes.

## Backend
Backend is based on Flask and wrapped in an ASGI application through the Connexion library that delivers automatic routing and request verification based on OpenAPI 3.0 specifications.

### Installation
  1. Ensure that you have Python 3 installed and run `pip install -r requirements.txt`
  2. API keys and other variables may be modified in `config.py` but this is not necessary at this time.

### Running the Backend
  1. In the parent directory of this project, run the command `uvicorn tastebudz:create_app --factory --port 5000`
  __Note:__ if you would like the backend to automatically reload the server when its component files are modified (for development purposes), append the following to the above command: `--reload --reload-dir tastebudz`
  2. You may send requests according to the OpenAPI 3.0 specifications, which can be found in the `tastebudz/openapi/` folder. You may also access the specifications from a web page automatically generated for each. See the section below for more information.

### API Specifications
| API | Specification File | Interactive URL |
| :--: | :--: | :--: |
| Auth | [auth.yaml](./tastebudz/openapi/auth.yaml) | http://127.0.0.1:5000/auth/ui |
| Restaurant | [restaurants.yaml](./tastebudz/openapi/restaurants.yaml) | http://127.0.0.1:5000/restaurant/ui |

### Testing
I have implemented testing using the Pytest framework. To run through all tests, use the command `pytest --disable-warnings`. Additional information:
- Configuration of the framework can be found in [conftest.py](conftest.py)
- Some additional testing configuration is done in the corresponding section of [pyproject.toml](pyproject.toml)
- Test cases, setup, and additional code needed for testing are under the `tests/` directory.