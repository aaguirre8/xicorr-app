import uvicorn
from fastapi import FastAPI

from src.mockup_service import main

app = FastAPI()


@app.get("/xicorr_mock")
def run_xicorr_mock():
    data = main()
    return data


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
