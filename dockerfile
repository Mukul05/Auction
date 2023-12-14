FROM python:3.10.8-slim

WORKDIR /app

# RUN mkdir cacerts

COPY . /app
# COPY cacerts /app/cacerts

# ENV REQUESTS_CA_BUNDLE=/app/cacerts/WellPoint_Internal_Root_CA.cer
# RUN pip config set global.cert /app/cacerts/WellPoint_Internal_Root_CA.cer

# COPY ../extras/cacerts/ /app/cacerts
# ENV REQUESTS_CA_BUNDLE=/app/cacerts/WellPoint_Internal_Root_CA.cer
# RUN pip config set global.cert /app/cacerts/WellPoint_Internal_Root_CA.ceryes

RUN pip install fastapi typer uvicorn pydantic python-multipart toml minio pymongo pyjwt[crypto] python-dotenv pandas Jinja2 mysql-connector-python


# CMD ['python','-m http.server']
#CMD ["python","./app.py","--host","0.0.0.0"]
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]