from dataclasses import dataclass, field
from enum import Enum

from openrarity.models.token_metadata import TokenMetadata
from openrarity.models.collection import Collection


class RankProvider(Enum):
    # external ranks
    TRAITS_SNIPER = 1
    RARITY_SNIFFER = 2
    # open rarity scorring
    OR_ARITHMETIC = 3
    OR_GEOMETRIC = 4
    OR_HARMONIC = 5
    OR_SUM = 6


Rank = tuple[RankProvider, int]


@dataclass
class Token:
    """Class represents Token class

    Attributes
    ----------
    token_id : int
        id of the token
    token_standard : str
        name of token standard (e.g. EIP-721 or EIP-1155)
    """

    token_id: int
    token_standard: str
    collection: Collection
    metadata: TokenMetadata
    ranks: list[Rank] = field(default_factory=list)