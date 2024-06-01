from collections.abc import Sequence
from functools import lru_cache
from pathlib import Path

from sqlalchemy import create_engine, or_, select
from sqlalchemy.orm import sessionmaker

from mtgcdb.card import Base, Card
from mtgcdb.db import clean_old_dbs, download_card_definitions_db, update_or_pass


class MTGCDB:
    """Magic: The Gathering card database singleton"""

    __instance: "MTGCDB | None" = None

    def __init__(self, force_update: bool = False):
        if (
            MTGCDB.__instance is not None
            and hasattr(self, "engine")
            and hasattr(self, "Session")
        ):
            return MTGCDB.__instance  # type: ignore

        self.db_path = update_or_pass() if not force_update else self.update_db()
        self.engine = create_engine(f"sqlite:///{self.db_path}", echo=False)
        self.Session = sessionmaker(bind=self.engine)
        Base.prepare(self.engine)

        MTGCDB.__instance = self

    def update_db(self) -> Path:
        clean_old_dbs()
        return download_card_definitions_db()

    @lru_cache(maxsize=1024)
    def get_card_by_name(self, name: str, set_code: str | None = None) -> Card:
        """Get a card by its name

        Args:
            name (str): exact card name
            set_code (str | None, optional): 3 letters of the set code. Defaults to None.

        Returns:
            Card:
        """
        with self.Session() as session:
            query = select(Card).where(Card.name == name)
            if set_code:
                query = query.where(Card.setCode == set_code)
            card = session.scalars(query).first()
            if not card:
                card = self.get_card_by_face_name(name, set_code=set_code)
            return card

    @lru_cache(maxsize=1024)
    def get_card_by_face_name(
        self, face_name: str, set_code: str | None = None
    ) -> Card:
        """Get a card by its front face name

        Args:
            face_name (str): exact front face name
            set_code (str | None, optional): 3 letters of the set code. Defaults to None.

        Returns:
            Card:
        """
        with self.Session() as session:
            query = select(Card).where(Card.faceName == face_name)
            if set_code:
                query = query.where(Card.setCode == set_code)
            card = session.scalars(query).first()
            if not card:
                raise ValueError(f"Card faceName={face_name} not found in database")
            return card

    def get_card_image_url_from_name(
        self, name: str, set_code: str | None = None, img_type: str = "normal"
    ) -> str:
        """Get the image URL of a card by its name

        Args:
            name (str): exact card name
            set_code (str | None, optional):  3 letters of the set code. Defaults to None.
            img_type (str, optional): One of "png", "normal", "large" or "small". Defaults to "normal".
              See https://scryfall.com/docs/api/images for more info.

        Returns:
            str: URL of the card image
        """
        c = self.get_card_by_name(name, set_code=set_code)
        img_format = "png" if img_type == "png" else "jpg"
        scryfall_id = c.identifier.scryfallId
        url = f"https://cards.scryfall.io/{img_type}/front/{scryfall_id[0]}/{scryfall_id[1]}/{scryfall_id}.{img_format}"
        return url

    def get_cards_by_names(self, names: list[str]) -> list[Card]:
        """Get a list of cards by their names

        Args:
            names (list[str]): List of exact card names

        Returns:
            list[Card]: List of cards
        """
        with self.Session() as session:
            query = select(Card).where(
                or_(Card.name.in_(names), Card.faceName.in_(names))
            )
            results = session.scalars(query).all()
        return _deduplicate_cards_by_name(results)

    @lru_cache(maxsize=8)
    def get_cards_by_set_code(self, setCode: str) -> list[Card]:
        """Get all cards from a set by its set code

        Args:
            setCode (str): Set code (3 letters)

        Returns:
            list[Card]: List of cards from the set
        """
        with self.Session() as session:
            query = select(Card).where(Card.setCode == setCode)
            results = session.scalars(query).all()
        return _deduplicate_cards_by_name(results)


def _deduplicate_cards_by_name(cards: Sequence[Card]) -> list[Card]:
    """Deduplicate a list of cards by their names

    Args:
        cards (Sequence[Card]): List of cards

    Returns:
        list[Card]: Deduplicated list of cards
    """
    card_names = set()
    dedup_cards = []
    for card in cards:
        if card.name not in card_names:
            dedup_cards.append(card)
            card_names.add(card.name)
    return dedup_cards
