from fastapi import FastAPI
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
import os
from fastapi.middleware.cors import CORSMiddleware

# Routers
from routes.purchase_router import router as purchase_router
from routes.auth_router import router as auth_router
from routes.store_router import router as store_router
from routes.cake_router import router as cake_router

app = FastAPI()

# # Mount Static Files (uploads/designs/)
# os.makedirs("uploads/designs", exist_ok=True)
# app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
# Create required directories if not exist
os.makedirs("uploads/designs", exist_ok=True)
os.makedirs("uploads/messages", exist_ok=True)
os.makedirs("uploads/audio", exist_ok=True)
os.makedirs("uploads/order_audio", exist_ok=True)

# Mount static files from 'uploads' folder
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include Routers
app.include_router(auth_router, prefix="/auth")
app.include_router(store_router, prefix="/store")
app.include_router(purchase_router, prefix="/purchase")
app.include_router(cake_router)

# Swagger Bearer Token Support
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Cake Shop API",
        version="1.0.0",
        description="API for Cake Shop Management",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
