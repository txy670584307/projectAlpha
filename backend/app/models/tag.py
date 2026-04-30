from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class Tag(Base):
    __tablename__ = "tags"
    __table_args__ = {"comment": "标签表，存储所有可用的标签"}

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键 ID")
    name = Column(String(50), unique=True, nullable=False, comment="标签名称，唯一")
    created_at = Column(DateTime, nullable=False, server_default=func.now(), comment="创建时间")

    tickets = relationship("Ticket", secondary="ticket_tags", back_populates="tags", lazy="selectin")

    def __repr__(self):
        return f"<Tag(id={self.id}, name='{self.name}')>"


ticket_tags = Table(
    "ticket_tags",
    Base.metadata,
    Column("ticket_id", Integer, ForeignKey("tickets.id", ondelete="CASCADE"), primary_key=True, comment="关联的 Ticket ID"),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True, comment="关联的 Tag ID"),
    comment="Ticket 和 Tag 的多对多关联表"
)
