# XiCorr FastAPI Server
This app computes the Xi Correlation between two arrays.

## Stack
- API: FastAPI
- Serverless: GCP Cloud Run

## Get started

1. Create venv.
    ```bash
    python3.12 -m venv .venv
    ```

2. Source venv

    Using Windows:
    ```bash
    .venv/Scripts/activate
    ```

    Using macOS and Linux:
    ```bash
    source .venv/bin/activate
    ```

3. Install the dependencies.
    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

## Usage

1. Run the server locally.

    ```bash
    $ python -m app
    ```
    To run xicorr process: Go to the fastapi docs and use your api endpoints - lhost:8080/xicorr_mock