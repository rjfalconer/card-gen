"""Configuration class for card generation."""

from typing import List
from dataclasses import dataclass, field


@dataclass
class Config:
    """Configuration settings for card generation."""

    # Card values to generate
    card_values: List[str] = field(default_factory=list)
    total_suits: int = 4

    # Dimensions of indicator for the Ace card
    ace_size: int = 250

    # Margin between frame.jpg and rest of printable area
    frame_horizontal_margin: int = 100
    frame_vertical_margin: int = 100

    # Vertical margin between the corner suit-indicators and the numerical card values
    indicator_number_margin: int = 10

    # Dimension of the smaller corner suit-indicator (scaled down from the suit art)
    mini_suit_width: int = 60
    mini_suit_height: int = 70
    number_width: int = 54
    number_height: int = 74

    # Dimension of the larger central suit-indicator
    suit_indicator_width: int = 170
    suit_indicator_height: int = 170  # ~17.5% the height of the card

    # Margins for the indicators, relative to the frame (not the box)
    horizontal_margin: int = 15
    vertical_margin: int = 60

    # Render card indicators on all four corners, not just top left and bottom right
    support_left_handed: bool = True

    def __post_init__(self) -> None:
        """Initialize default values after dataclass creation."""
        if not self.card_values:
            self.card_values = [
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

    def validate(self) -> None:
        """Validate configuration settings."""
        if self.total_suits < 1:
            raise ValueError("total_suits must be at least 1")
        if self.ace_size <= 0:
            raise ValueError("ace_size must be positive")
        if not self.card_values:
            raise ValueError("card_values cannot be empty")

        # Validate margins are non-negative
        margin_attrs = [
            "frame_horizontal_margin",
            "frame_vertical_margin",
            "indicator_number_margin",
            "horizontal_margin",
            "vertical_margin",
        ]
        for attr in margin_attrs:
            if getattr(self, attr) < 0:
                raise ValueError(f"{attr} cannot be negative")

        # Validate dimensions are positive
        dimension_attrs = [
            "mini_suit_width",
            "mini_suit_height",
            "number_width",
            "number_height",
            "suit_indicator_width",
            "suit_indicator_height",
        ]
        for attr in dimension_attrs:
            if getattr(self, attr) <= 0:
                raise ValueError(f"{attr} must be positive")
