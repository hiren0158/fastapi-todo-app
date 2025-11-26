"""
Background jobs for emailing daily summaries and resetting todos.
"""
from __future__ import annotations

import asyncio
import logging
import smtplib
from datetime import datetime
from email.message import EmailMessage
from textwrap import dedent
from typing import List, Sequence
from zoneinfo import ZoneInfo

from ..config import settings
from ..models_beanie import Todo, User

logger = logging.getLogger(__name__)

try:
    APP_TZ = ZoneInfo(settings.timezone)
except Exception:  # pragma: no cover - fallback path
    logger.warning("Invalid timezone '%s'. Falling back to UTC.", settings.timezone)
    APP_TZ = ZoneInfo("UTC")


async def send_daily_summaries_and_reset():
    """
    Send end-of-day summaries to every user and purge todos for a fresh start.
    """
    if not settings.daily_reset_enabled:
        logger.debug("Daily reset disabled; skipping scheduled purge.")
        return

    summary_date = datetime.now(tz=APP_TZ)
    logger.info("Running daily summary + purge for %s", summary_date.date())

    users: List[User] = await User.find_all().to_list()

    if settings.summary_email_enabled and not _email_configured():
        logger.error("Summary email enabled but SMTP credentials missing. Skipping emails.")

    for user in users:
        await _send_summary_for_user(user, summary_date)

    delete_result = await Todo.find_all().delete()
    deleted_count = getattr(delete_result, "deleted_count", delete_result)
    logger.info("Daily purge complete. Deleted %s todos.", deleted_count)


async def _send_summary_for_user(user: User, summary_date: datetime) -> None:
    if not settings.summary_email_enabled or not _email_configured():
        return

    todos = await Todo.find(Todo.owner_id == str(user.id)).to_list()
    subject = f"Your Todo Summary · {summary_date.strftime('%b %d, %Y')}"
    body = _build_email_body(user, todos, summary_date)
    recipient = user.email
    if recipient:
        try:
            await _send_email(subject, body, recipient)
            logger.info("Sent daily summary email to %s", recipient)
        except Exception as exc:  # pragma: no cover - logging only
            logger.exception("Failed to send summary email to %s: %s", recipient, exc)
    else:
        logger.warning("User %s missing email address; skipping summary.", user.id)


def _build_email_body(user: User, todos: Sequence[Todo], summary_date: datetime) -> str:
    total = len(todos)
    completed = len([todo for todo in todos if todo.complete])
    pending = total - completed

    lines = [
        f"Hey {user.first_name or user.username},",
        "",
        f"Here is your todo snapshot for {summary_date.strftime('%A, %d %B %Y')}:",
        f"• Total tasks: {total}",
        f"• Completed: {completed}",
        f"• Pending: {pending}",
        "",
    ]

    if todos:
        lines.append("Tasks:")
        for idx, todo in enumerate(todos, start=1):
            status = "Done" if todo.complete else "Pending"
            lines.append(
                f"{idx}. {todo.title} [{status}] (Priority {todo.priority})"
                f"\n   {todo.description}"
            )
    else:
        lines.append("Looks like you had a clean slate today. Great job!")

    lines.extend(
        [
            "",
            "Tomorrow is a fresh start — all tasks have been cleared.",
            "Keep up the great work!",
            "",
            f"{settings.app_name} Bot",
        ]
    )

    return dedent("\n".join(lines))


def _email_configured() -> bool:
    sender = settings.email_from or settings.smtp_username
    return bool(
        settings.smtp_host
        and settings.smtp_port
        and sender
    )


async def _send_email(subject: str, body: str, recipient: str) -> None:
    message = EmailMessage()
    sender = settings.email_from or settings.smtp_username
    if not sender:
        raise RuntimeError("Missing sender email address.")

    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    await asyncio.to_thread(_send_email_blocking, message)


def _send_email_blocking(message: EmailMessage) -> None:
    smtp_class = smtplib.SMTP_SSL if not settings.smtp_use_tls else smtplib.SMTP
    with smtp_class(settings.smtp_host, settings.smtp_port, timeout=30) as server:
        if settings.smtp_use_tls:
            server.starttls()
        if settings.smtp_username and settings.smtp_password:
            server.login(settings.smtp_username, settings.smtp_password)
        server.send_message(message)


__all__ = ["send_daily_summaries_and_reset"]


