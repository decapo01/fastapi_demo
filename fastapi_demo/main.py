import logging
import uvicorn
from fastapi import FastAPI

from fastapi_demo.routes import todo_routes

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(todo_routes.router, prefix="/todos")

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
