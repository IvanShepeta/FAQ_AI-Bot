import logging
import time
from fastapi import Request, FastAPI
from app.routers import agent


app = FastAPI()


# Settings for logging
logging.basicConfig(level=logging.INFO)

# Middleware for logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logging.info(f"{request.method} {request.url.path} {response.status_code} {process_time:.2f}s")
    return response


# Register the router
app.include_router(agent.router)


@app.get("/")
def root():
    """
    Simple health-check endpoint to verify that the service is running.
    """
    return {"Hello": "World"}
