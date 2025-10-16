from __future__ import annotations

from typing import Optional

from flask_login import UserMixin
from sqlalchemy import Integer, String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from slugify import slugify
from sqlalchemy.exc import IntegrityError

from . import db, login_manager


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(80), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    posts: Mapped[list[Post]] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(user_id: int) -> Optional["User"]:
        return db.session.get(User, user_id)

    @staticmethod
    def get_by_email(email: str) -> Optional["User"]:
        return User.query.filter_by(email=email).first()


@login_manager.user_loader
def load_user(user_id: str) -> Optional[User]:
    return User.get_by_id(int(user_id))


class Post(db.Model):
    __tablename__ = "posts"
    __table_args__ = (UniqueConstraint("slug", name="uq_posts_slug"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(80), nullable=True)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    author: Mapped[User] = relationship(back_populates="posts")

    def _generate_unique_slug(self) -> str:
        base = slugify(self.title)
        if not base:
            base = "post"
        candidate = base
        counter = 1
        while Post.query.filter_by(slug=candidate).first() is not None:
            candidate = f"{base}-{counter}"
            counter += 1
        return candidate

    def save(self) -> None:
        if not self.slug:
            self.slug = self._generate_unique_slug()
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            # Retry with a new slug if collision happened
            self.slug = self._generate_unique_slug()
            db.session.add(self)
            db.session.commit()

    def public_url(self) -> str:
        from flask import url_for

        return url_for("post_detail", slug=self.slug)

    @staticmethod
    def get_by_slug(slug: str) -> Optional["Post"]:
        return Post.query.filter_by(slug=slug).first()

    @staticmethod
    def get_all() -> list["Post"]:
        return Post.query.order_by(Post.id.desc()).all()

