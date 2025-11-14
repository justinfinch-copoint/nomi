"""User model for authentication and user management."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class User(Base):
    """User model representing authenticated users in the system.

    Users are authenticated via Microsoft Entra ID (Azure AD) and stored
    in the database for session management and data ownership.

    Attributes:
        id: Unique identifier (UUID) for the user
        entraid_user_id: Microsoft Entra ID user identifier (unique)
        email: User's email address (unique, indexed for lookups)
        name: User's display name
        created_at: Timestamp when user record was created
        updated_at: Timestamp when user record was last updated
    """

    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        comment="Unique identifier for the user",
    )

    entraid_user_id = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
        comment="Microsoft Entra ID (Azure AD) user identifier",
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
        comment="User's email address",
    )

    name = Column(
        String(255),
        nullable=False,
        comment="User's display name",
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        comment="Timestamp when user was created",
    )

    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        comment="Timestamp when user was last updated",
    )

    def __repr__(self) -> str:
        """String representation of User."""
        return f"<User(id={self.id}, email={self.email}, name={self.name})>"
