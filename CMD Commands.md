# Run with CMD

### Installation

#### Cloning the Repository

1. Open PyCharm and click `Get from VCS` on the Welcome screen.
2. In the `Clone Repository` dialog, enter:
   - URL: `https://github.com/myusername/myproject.git` (replace this with your repository's URL)
   - Directory: Select your desired project directory.
3. Click `Clone`.
4. Open cmd and write given commands
```bash
venv\Scripts\activate
```
## Run the following command
```bash
pip install fastapi typer uvicorn pydantic python-multipart toml minio pymongo pyjwt[crypto] python-dotenv pandas Jinja2 mysql-connector-python itsdangerous

uvicorn app:app --reload
```
## to deactivate the environment
```bash
deactivate
```
