from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes.user import router as user_router
from src.api.routes.users import router as users_router

app = FastAPI(
    title="GymDash", description="API for managing a gym database.", version="0.0.1"
)

# CORS middleware to allow React frontend to make requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with API prefix
app.include_router(user_router, prefix="/api/v1/user", tags=["user"])
app.include_router(users_router, prefix="/api/v1/users", tags=["users"])


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/")
def root():
    return {"message": "API is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
