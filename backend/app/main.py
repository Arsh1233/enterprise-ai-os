import uvicorn

from app.config.settings import settings
from app.core.factory import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG
    )
