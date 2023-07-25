import uvicorn

from app.settings import settings


def main() -> None:
    """Entrypoint of the application."""
    uvicorn.run(
        "app.main:app",
        # workers=settings.workers_count,
        workers=1,
        # host=settings.host,
        host="0.0.0.0",
        # port=settings.port,
        port=8000,
        # reload=settings.reload,
        reload=settings.dev,
        # log_level=settings.log_level.value.lower(),
        # factory=True,
    )


if __name__ == "__main__":
    main()
