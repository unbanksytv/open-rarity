from open_rarity.models.token import Token
from open_rarity.models.token_identifier import (
    EVMContractTokenIdentifier,
    SolanaMintAddressTokenIdentifier,
)
from open_rarity.models.token_metadata import (
    NumericAttribute,
    StringAttribute,
    TokenMetadata,
)
from open_rarity.models.token_standard import TokenStandard
from tests.helpers import create_evm_token


class TestToken:
    def test_create_metaplex_non_fungible(self):
        token = Token(
            token_identifier=SolanaMintAddressTokenIdentifier(
                mint_address="AsjdsskDso..."
            ),
            token_standard=TokenStandard.METAPLEX_NON_FUNGIBLE,
            metadata=TokenMetadata.from_attributes({"hat": "cap", "shirt": "blue"}),
        )
        token_equal = Token.from_metaplex_non_fungible(
            mint_address="AsjdsskDso...",
            attributes={"hat": "cap", "shirt": "blue"},
        )

        assert token == token_equal

        token_not_equal = Token.from_metaplex_non_fungible(
            mint_address="DiffMintAddresss...",
            attributes={"hat": "cap", "shirt": "blue"},
        )

        assert token != token_not_equal

    def test_create_erc721(self):
        token = Token(
            token_identifier=EVMContractTokenIdentifier(
                contract_address="0xa3049...", token_id=1
            ),
            token_standard=TokenStandard.ERC721,
            metadata=TokenMetadata.from_attributes({"hat": "cap", "shirt": "blue"}),
        )
        token_equal = Token.from_erc721(
            contract_address="0xa3049...",
            token_id=1,
            metadata_dict={"hat": "cap", "shirt": "blue"},
        )

        assert token == token_equal

        token_not_equal = Token.from_erc721(
            contract_address="0xmew...",
            token_id=1,
            metadata_dict={"hat": "cap", "shirt": "blue"},
        )

        assert token != token_not_equal

    def test_token_init_metadata_non_matching_attribute_names(self):
        token = create_evm_token(
            token_id=1,
            metadata=TokenMetadata(
                string_attributes={
                    "hat": StringAttribute(name="big hat", value="blue"),
                    "shirt": StringAttribute(name=" shirt", value="red"),
                }
            ),
        )
        assert token.metadata.string_attributes == {
            "hat": StringAttribute(name="hat", value="blue"),
            "shirt": StringAttribute(name="shirt", value="red"),
        }

    def test_token_attribute_normalization(self):
        expected_equal_metadata_tokens = [
            create_evm_token(
                token_id=1,
                metadata=TokenMetadata(
                    string_attributes={
                        "hat ": StringAttribute(name="hat", value="blue"),
                        "Shirt ": StringAttribute(name="shirt", value="red"),
                    },
                    numeric_attributes={
                        "level": NumericAttribute(name="level", value=1),
                    },
                ),
            ),
            create_evm_token(
                token_id=1,
                metadata=TokenMetadata(
                    string_attributes={
                        "hat": StringAttribute(name="hat", value="blue"),
                        "Shirt ": StringAttribute(name=" shirt", value="red"),
                    },
                    numeric_attributes={
                        "Level": NumericAttribute(name="level", value=1),
                    },
                ),
            ),
            create_evm_token(
                token_id=1,
                metadata=TokenMetadata(
                    string_attributes={
                        "Hat": StringAttribute(name=" hat ", value="blue"),
                        "shirt": StringAttribute(name="shirt", value="red"),
                    },
                    numeric_attributes={
                        "Level": NumericAttribute(name=" level ", value=1),
                    },
                ),
            ),
            create_evm_token(
                token_id=1,
                metadata=TokenMetadata(
                    string_attributes={
                        "  hat ": StringAttribute(name=" hat ", value="blue"),
                        "   shirt": StringAttribute(name="shirt", value="red"),
                    },
                    numeric_attributes={
                        "level": NumericAttribute(name="level ", value=1),
                    },
                ),
            ),
        ]

        assert all(
            t.metadata == expected_equal_metadata_tokens[0].metadata
            for t in expected_equal_metadata_tokens
        )

        expected_not_equal = [
            create_evm_token(
                token_id=1,
                metadata=TokenMetadata(
                    string_attributes={
                        " big hat ": StringAttribute(name=" hat ", value="blue"),
                        "   shirt": StringAttribute(name="shirt", value="red"),
                    },
                    numeric_attributes={
                        "level": NumericAttribute(name="level", value=1),
                    },
                ),
            ),
            create_evm_token(
                token_id=1,
                metadata=TokenMetadata(
                    string_attributes={
                        "hat": StringAttribute(name="hat", value="blue"),
                        "shirt": StringAttribute(name="shirt", value="red"),
                    },
                    numeric_attributes={
                        "big level": NumericAttribute(name="level", value=1),
                    },
                ),
            ),
        ]

        assert all(
            t.metadata != expected_equal_metadata_tokens[0].metadata
            for t in expected_not_equal
        )
