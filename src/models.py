from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, ForeignKey, Integer

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

    favorites: Mapped[list["Favorite"]] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
        }


class Character(db.Model):
    __tablename__ = 'characters'
    id: Mapped[int] = mapped_column(primary_key=True)
    name_character: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    gender: Mapped[str] = mapped_column(String(120), nullable=False)
    hair: Mapped[str] = mapped_column(String(120), nullable=False)

    def __repr__(self):
     return f'<Character {self.name_character}>'

    favorites: Mapped[list["Favorite"]] = relationship(
        back_populates="character")

    def serialize(self):
        return {
            "id": self.id,
            "name_character": self.name_character,
            "gender": self.gender,
            "hair": self.hair,
        }


class Planet(db.Model):
    __tablename__ = 'planets'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    climate: Mapped[str] = mapped_column(String(120), nullable=False)
    population: Mapped[str] = mapped_column(String(120), nullable=False)

    def __repr__(self):
        return f'<Planet {self.name}>'

    favorites: Mapped[list["Favorite"]] = relationship(back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population,
        }


class Favorite(db.Model):
    __tablename__ = 'favorite'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    planet_id: Mapped[int] = mapped_column(
        ForeignKey("planets.id"), nullable=True)
    character_id: Mapped[int] = mapped_column(
        ForeignKey("characters.id"), nullable=True)

    planet: Mapped["Planet"] = relationship(back_populates="favorites")
    character: Mapped["Character"] = relationship(back_populates="favorites")
    user: Mapped["User"] = relationship(back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "character_id": self.character_id,
        }
