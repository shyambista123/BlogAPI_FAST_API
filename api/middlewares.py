# FastAPI middlewares (e.g., CORS, logging)
from starlette.middleware.cors import CORSMiddleware

def setup_middlewares(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
