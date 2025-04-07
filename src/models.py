from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    comments: Mapped[list["Comment"]] = relationship(back_populates="user")
    posts: Mapped[list["Post"]] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(120), nullable=False)

    # Relationship User - MUCHOS A UNO
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="comments")

    # Relationship Post - MUCHOS A UNO
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    post: Mapped["Post"] = relationship(back_populates="comments")

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    # Relationship User - MUCHOS A UNO
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="posts")

    # Relationship Comment - UNO A MUCHOS
    comments: Mapped[list["Comment"]] = relationship(back_populates="post")

    # Relationship with Media - UNO A MUCHOS
    media: Mapped[list["Media"]] = relationship(back_populates="post")

class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(120), nullable=False)
    url: Mapped[str] = mapped_column(String(120), nullable=False)

    # Relationship with Post - MUCHOS A UNO
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    post: Mapped["Post"] = relationship(back_populates="media")

class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    user_from_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False)

    user_to_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False)