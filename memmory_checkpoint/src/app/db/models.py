from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import BigInteger, ForeignKey, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))


class Sailing(Base):
    __tablename__ = "sailings"

    id: Mapped[int] = mapped_column(primary_key=True)
    ship_name: Mapped[str] = mapped_column(String(120), index=True)
    departure_port: Mapped[str] = mapped_column(String(120))
    arrival_port: Mapped[str] = mapped_column(String(120))
    departure_date: Mapped[date]
    adult_fare: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    currency: Mapped[str] = mapped_column(String(3))


class ConversationThread(Base):
    __tablename__ = "conversation_threads"

    thread_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    summary_mode: Mapped[str] = mapped_column(String(32), default="manual")
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    thread_id: Mapped[str] = mapped_column(
        ForeignKey("conversation_threads.thread_id"), index=True
    )
    role: Mapped[str] = mapped_column(String(16))  # 'user' | 'assistant' | 'tool' | 'system'
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class Summary(Base):
    __tablename__ = "summaries"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    thread_id: Mapped[str] = mapped_column(
        ForeignKey("conversation_threads.thread_id"), index=True
    )
    summary_text: Mapped[str] = mapped_column(Text)
    covered_until_message_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("messages.id"))
    strategy: Mapped[str] = mapped_column(String(32))  # 'manual' | 'langmem'
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class LongTermMemory(Base):
    __tablename__ = "long_term_memories"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    memory_type: Mapped[str] = mapped_column(String(32))
    content: Mapped[str] = mapped_column(Text)
    confidence: Mapped[Decimal] = mapped_column(Numeric(3, 2))
    source_thread_id: Mapped[str] = mapped_column(
        ForeignKey("conversation_threads.thread_id"), index=True
    )
    status: Mapped[str] = mapped_column(String(16), default="active")
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
