from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Mapped, mapped_column, relationship

Base = automap_base()


class Card(Base):  # type: ignore
    __tablename__ = "cards"
    extend_existing = True

    uuid: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    faceName: Mapped[str]
    types: Mapped[str]
    subtypes: Mapped[str]
    setCode: Mapped[str]
    power: Mapped[Optional[str]]
    toughness: Mapped[Optional[str]]
    text: Mapped[str]
    manaValue: Mapped[float]
    manaCost: Mapped[str]
    colors: Mapped[str]
    colorIdentity: Mapped[str]
    rarity: Mapped[str]

    def __repr__(self) -> str:
        return f"Card(name={self.name}, types={self.types}, manaCost={self.manaCost})"

    identifier: Mapped["CardIdentifier"] = relationship(
        back_populates="card", viewonly=True, lazy="joined"
    )


class CardIdentifier(Base):  # type: ignore
    __tablename__ = "cardIdentifiers"

    uuid = mapped_column(ForeignKey("cards.uuid"), primary_key=True)
    scryfallId: Mapped[str]

    card: Mapped[Card] = relationship(back_populates="identifier", viewonly=True)
