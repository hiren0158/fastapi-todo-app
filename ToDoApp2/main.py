"""
FastAPI Todo Application - Main Entry Point
"""
import logging
from typing import Optional
from zoneinfo import ZoneInfo

from apscheduler.schedulers.asyncio import AsyncIOScheduler  # type: ignore
from apscheduler.triggers.cron import CronTrigger  # type: ignore
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from .config import settings
from .core.logging_config import setup_logging
from .database import close_db, init_db
from .routers import admin, auth, todos, users
from .services.notifications import send_daily_summaries_and_reset

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

# Mount static files
app.mount("/static", StaticFiles(directory="ToDoApp2/static"), name='static')

try:
    APP_TIMEZONE = ZoneInfo(settings.timezone)
except Exception:  # pragma: no cover - fallback path
    logger.warning("Invalid timezone '%s'. Falling back to UTC.", settings.timezone)
    APP_TIMEZONE = ZoneInfo("UTC")

scheduler: Optional[AsyncIOScheduler] = None


@app.on_event('startup')
async def on_startup():
    """Initialize database connection on startup."""
    logger.info("Starting application...")
    await init_db()
    if settings.daily_reset_enabled:
        _schedule_daily_reset()
    logger.info("Application started successfully")


@app.on_event('shutdown')
async def on_shutdown():
    """Close database connection on shutdown."""
    logger.info("Shutting down application...")
    if scheduler and scheduler.running:
        scheduler.shutdown(wait=False)
    await close_db()
    logger.info("Application shutdown complete")


@app.get('/')
def root(request: Request):
    """Redirect root to todos page."""
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)


@app.get('/healthy')
def health_check():
    """Health check endpoint."""
    return {'status': 'healthy', 'app': settings.app_name}


def _schedule_daily_reset() -> None:
    global scheduler
    if scheduler is None:
        scheduler = AsyncIOScheduler(timezone=APP_TIMEZONE)

    trigger = CronTrigger(hour=23, minute=59, timezone=APP_TIMEZONE)
    scheduler.add_job(
        send_daily_summaries_and_reset,
        trigger,
        id="daily-summary",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("Daily summary + purge scheduled for 23:59 (%s)", APP_TIMEZONE)

