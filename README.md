# Online Auction System

This project is a comprehensive implementation of an online auction management system using FastAPI, complete with user authentication, item management, and real-time bidding functionalities.

## Getting Started

Follow these instructions to get this project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have the following installed:
- [PyCharm](https://www.jetbrains.com/pycharm/download/) (Community or Professional edition)
- [Git](https://git-scm.com/downloads)
- Python (usually included in PyCharm)

### Installation

#### Cloning the Repository

1. Open PyCharm and click `Get from VCS` on the Welcome screen.
2. In the `Clone Repository` dialog, enter:
   - URL: `https://github.com/myusername/myproject.git` (replace this with your repository's URL)
   - Directory: Select your desired project directory.
3. Click `Clone`.

#### Setting Up a Virtual Environment

1. After the project opens, navigate to `File` > `Settings` > `Project: myproject` > `Python Interpreter`.
2. Click the gear icon, select `Add`, and choose `Virtualenv Environment`.
3. In the dialog, select `New environment`. Set the base Python interpreter and specify the location for the new virtual environment.
4. Ensure `Inherit global site-packages` and `Make available to all projects` are unchecked.
5. Click `OK`.

#### Installing Dependencies

1. Open the integrated terminal in PyCharm.
2. Run the following command to install required packages :
```bash
pip install fastapi typer uvicorn pydantic python-multipart toml minio pymongo pyjwt[crypto] python-dotenv pandas Jinja2 mysql-connector-python itsdangerous

```
 ### Set up the Uvicorn Run Configuration:

1. Go to Run > Edit Configurations.
2. Click the + icon to add a new configuration.
3. Select Python.
4. Give your configuration a name, like "Uvicorn Server".
5. In the Script path or Module name field, type uvicorn.
6. In the Parameters field, type app:app --reload (replace app:app with your actual app module and instance if different).
7. Ensure the correct Python interpreter (your virtual environment) is selected.
8. Click OK to save the configuration.
9.   Run Your Uvicorn Server:

10. Select the Uvicorn run configuration you just created from the top-right dropdown menu.
11. Click the green play button to start the server.

### Access Your FastAPI Application:

Once the Uvicorn server is running, you should see output in the console indicating that the server is live (usually on localhost:8000).
Open a web browser and navigate to http://localhost:8000 to access your FastAPI application.



