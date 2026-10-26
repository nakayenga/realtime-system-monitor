import threading

import uvicorn

from fastapi import FastAPI


app = FastAPI()


state = {
    "ready": False,
}


@app.get("/health/live")
def live():
    return {
        "status": "alive"
    }


@app.get("/health/ready")
def ready():
    if state["ready"]:
        return {
            "status": "ready"
        }

    return {
        "status": "starting"
    }


def mark_ready():
    state["ready"] = True


def start_health_server():
    thread = threading.Thread(
        target=uvicorn.run,

        kwargs={
            "app": app,
            "host": "0.0.0.0",
            "port": 8080,
            "log_level": "warning",
        },

        daemon=True,
    )

    thread.start()