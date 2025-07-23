"""Test configuration class."""

import pytest
from card_gen.config import Config


class TestConfig:
    """Test cases for Config class."""

    def test_default_initialization(self) -> None:
        """Test config initialization with default values."""
        config = Config()
        assert config.card_values == [
            "A",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "J",
            "Q",
            "K",
        ]
        assert config.total_suits == 4
        assert config.ace_size == 250
        assert config.support_left_handed is True

    def test_custom_initialization(self) -> None:
        """Test config initialization with custom values."""
        custom_values = ["A", "K", "Q"]
        config = Config(
            card_values=custom_values,
            total_suits=2,
            ace_size=300,
            support_left_handed=False,
        )
        assert config.card_values == custom_values
        assert config.total_suits == 2
        assert config.ace_size == 300
        assert config.support_left_handed is False

    def test_validation_success(self) -> None:
        """Test that valid configuration passes validation."""
        config = Config()
        config.validate()  # Should not raise any exception

    def test_validation_negative_total_suits(self) -> None:
        """Test validation fails for negative total_suits."""
        config = Config(total_suits=0)
        with pytest.raises(ValueError, match="total_suits must be at least 1"):
            config.validate()

    def test_validation_negative_ace_size(self) -> None:
        """Test validation fails for negative ace_size."""
        config = Config(ace_size=-10)
        with pytest.raises(ValueError, match="ace_size must be positive"):
            config.validate()

    def test_validation_empty_card_values_after_manual_clear(self) -> None:
        """Test validation fails when card_values is manually cleared after init."""
        config = Config()
        config.card_values = []  # Manually clear after init
        with pytest.raises(ValueError, match="card_values cannot be empty"):
            config.validate()

    def test_validation_negative_margins(self) -> None:
        """Test validation fails for negative margins."""
        config = Config(frame_horizontal_margin=-5)
        with pytest.raises(
            ValueError, match="frame_horizontal_margin cannot be negative"
        ):
            config.validate()

    def test_validation_zero_dimensions(self) -> None:
        """Test validation fails for zero dimensions."""
        config = Config(mini_suit_width=0)
        with pytest.raises(ValueError, match="mini_suit_width must be positive"):
            config.validate()

    def test_post_init_sets_default_card_values(self) -> None:
        """Test that __post_init__ sets default card values when empty."""
        config = Config(card_values=[])
        assert len(config.card_values) == 13
        assert "A" in config.card_values
        assert "K" in config.card_values
