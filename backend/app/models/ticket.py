from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    CheckConstraint,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class Ticket(Base):
    __tablename__ = "tickets"
    __table_args__ = (
        CheckConstraint("status IN ('open', 'closed')", name="check_status"),
        {"comment": "Ticket 主表，存储所有工单信息"},
    )

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键 ID")
    title = Column(String(200), nullable=False, comment="Ticket 标题")
    description = Column(Text, nullable=True, comment="Ticket 详细描述")
    status = Column(
        String(20),
        nullable=False,
        default="open",
        comment="状态：open-未完成, closed-已完成",
    )
    created_at = Column(
        DateTime, nullable=False, server_default=func.now(), comment="创建时间"
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        comment="最后更新时间",
    )
    completed_at = Column(DateTime, nullable=True, comment="完成时间")

    tags = relationship(
        "Tag", secondary="ticket_tags", back_populates="tickets", lazy="selectin"
    )

    def __repr__(self):
        return f"<Ticket(id={self.id}, title='{self.title}', status='{self.status}')>"
