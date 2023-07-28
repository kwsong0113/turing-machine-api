import uvicorn

from app.core.config import settings


def main() -> None:
    """Entrypoint of the application."""
    uvicorn.run(
        "app.main:app",
        workers=1,
        host="0.0.0.0",
        port=8000,
        reload=settings.DEV,
    )


if __name__ == "__main__":
    main()
