from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

class HealthResponse(BaseModel):
    status: str
    components: Dict[str, str]

def check_system_health() -> Dict[str, str]:
    # This is a placeholder function to simulate checking system health.
    # In a real-world scenario, you would replace this with actual checks.
    return {
        "database": "healthy",
        "cache": "healthy",
        "api_service": "healthy"
    }

@app.get("/api/health", response_model=HealthResponse)
async def get_health(request: Request):
    """
    Endpoint to check the health status of system components.

    This endpoint returns a JSON object with the overall health status and
    detailed health statuses of individual components.

    Returns:
        HealthResponse: A dictionary containing the health status of each component.
    """
    try:
        components_status = check_system_health()
        status = "healthy" if all(value == "healthy" for value in components_status.values()) else "unhealthy"
        return {"status": status, "components": components_status}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve health status")

# Example of an error handling route
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Handler for HTTP exceptions.

    This function formats the exception into a JSON response with appropriate status codes.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )
