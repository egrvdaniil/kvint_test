from fastapi import FastAPI


def setup_endpoints(app: FastAPI):
    app.get("/", response_model='')()  # type:ignore
    app.post("/", response_model='')()  # type:ignore
