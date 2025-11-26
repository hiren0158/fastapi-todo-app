"""
FastAPI Todo Application - Main Entry Point
"""
import logging
from typing import Optional
from zoneinfo import ZoneInfo
from contextlib import asynccontextmanager

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


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager for the FastAPI app.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting application...")
    
    # DEBUG: Print environment info
    mongo_url = settings.mongodb_url
    # Mask password for logs
    if "@" in mongo_url:
        # Attempt to mask the password part if present
        parts = mongo_url.split('@')
        if len(parts) > 1:
            protocol_and_auth = parts[0]
            host_port_db = parts[-1]
            
            protocol_end_idx = protocol_and_auth.find('://')
            if protocol_end_idx != -1:
                protocol = protocol_and_auth[:protocol_end_idx+3]
                masked_url = f"{protocol}***:***@{host_port_db}"
            else:
                # Fallback if no protocol or unexpected format
                masked_url = f"***:***@{host_port_db}"
            logger.info(f"DEBUG: Attempting to connect to MongoDB at: {masked_url}")
        else:
            logger.info(f"DEBUG: Attempting to connect to MongoDB at: {mongo_url}")
    else:
        logger.info(f"DEBUG: Attempting to connect to MongoDB at: {mongo_url}")
        
    logger.info(f"DEBUG: MONGODB_URL env var is set: {'MONGODB_URL' in os.environ}")
    
    await init_db()
    
    if settings.daily_reset_enabled:
        _schedule_daily_reset()
        if scheduler and not scheduler.running:
            scheduler.start()
            logger.info("Scheduler started")
    
    logger.info("Application started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    if scheduler and scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("Scheduler shutdown")
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

