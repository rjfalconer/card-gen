"""Main card generator class with refactored, pythonic code."""

import os
import math
from typing import Dict, Callable, Optional
from wand.image import Image

from .config import Config
from .face_cards import FaceCardArtwork


class Box:
    """Defines printable area within card for use with suit-indicators."""

    def __init__(
        self, width: int, height: int, margin_left: int, margin_top: int
    ) -> None:
        """Initialize box with dimensions and margins.

        Args:
            width: Width of the box
            height: Height of the box
            margin_left: Left margin offset
            margin_top: Top margin offset
        """
        self.width = width
        self.height = height
        self.margin_left = margin_left
        self.margin_top = margin_top

    def insert(self, canvas: Image, image: Image, x: float, y: float) -> None:
        """Insert image onto canvas at x,y offset relative to canvas indicator box.

        Args:
            canvas: Target canvas image
            image: Image to insert
            x: X coordinate relative to box
            y: Y coordinate relative to box
        """
        corner_x = math.floor(x + self.margin_left)
        corner_y = math.floor(y + self.margin_top)
        canvas.composite(image, corner_x, corner_y)


class CardGenerator:
    """Generate poker card images with configurable settings."""

    def __init__(self, config: Optional[Config] = None) -> None:
        """Initialize card generator.

        Args:
            config: Configuration object. If None, uses default config.
        """
        self.config = config or Config()
        self.config.validate()

        self.face_card_generator = FaceCardArtwork(
            self.config.number_width, self.config.number_height
        )

        # Map card numbers to their drawing functions
        self._card_drawing_functions: Dict[str, Callable] = {
            "A": self._draw_ace,
            "2": self._draw_two,
            "3": self._draw_three,
            "4": self._draw_four,
            "5": self._draw_five,
            "6": self._draw_six,
            "7": self._draw_seven,
            "8": self._draw_eight,
            "9": self._draw_nine,
            "10": self._draw_ten,
        }

    def _draw_ace(self, canvas: Image, suit: Image, box: Box) -> None:
        """Draw suit markers for Ace card."""
        with Image(suit) as big_suit:
            big_suit.resize(self.config.ace_size, self.config.ace_size)
            corner_x = (box.width / 2) - (big_suit.width / 2)
            corner_y = (box.height / 2) - (big_suit.height / 2)
            box.insert(canvas, big_suit, corner_x, corner_y)

    def _draw_single_center(self, canvas: Image, suit: Image, box: Box) -> None:
        """Draw a single suit marker in the center."""
        corner_x = (box.width / 2) - (suit.width / 2)
        corner_y = (box.height / 2) - (suit.height / 2)
        box.insert(canvas, suit, corner_x, corner_y)

    def _draw_pair_center(self, canvas: Image, suit: Image, box: Box) -> None:
        """Draw a pair of suit markers in the center row."""
        corner_x = 0
        corner_y = (box.height / 2) - (suit.height / 2)
        box.insert(canvas, suit, corner_x, corner_y)
        box.insert(canvas, suit, box.width - suit.width, corner_y)

    def _draw_single_top(self, half_canvas: Image, suit: Image, box: Box) -> None:
        """Draw single suit marker at top."""
        corner_x = (box.width / 2) - (suit.width / 2)
        corner_y = 0
        box.insert(half_canvas, suit, corner_x, corner_y)

    def _draw_single_offset(self, half_canvas: Image, suit: Image, box: Box) -> None:
        """Draw single suit marker with offset (for 8)."""
        corner_x = (box.width / 2) - (suit.width / 2)
        corner_y = box.height / 5
        box.insert(half_canvas, suit, corner_x, corner_y)

    def _draw_single_mid(self, half_canvas: Image, suit: Image, box: Box) -> None:
        """Draw single suit marker in middle (for 10)."""
        corner_x = (box.width / 2) - (suit.width / 2)
        corner_y = half_canvas.height / 4
        box.insert(half_canvas, suit, corner_x, corner_y)

    def _draw_pair_top(self, half_canvas: Image, suit: Image, box: Box) -> None:
        """Draw pair of suit markers at top."""
        corner_x = 0
        corner_y = 0
        box.insert(half_canvas, suit, corner_x, corner_y)
        box.insert(half_canvas, suit, box.width - suit.width, corner_y)

    def _draw_quad(self, half_canvas: Image, suit: Image, box: Box) -> None:
        """Draw four suit markers in two rows."""
        corner_x = 0
        corner_y = 0
        box.insert(half_canvas, suit, corner_x, corner_y)
        box.insert(half_canvas, suit, box.width - suit.width, corner_y)

        buffer_space = box.height - (4 * suit.height)
        corner_y = suit.height + (buffer_space / 3)
        box.insert(half_canvas, suit, corner_x, corner_y)
        box.insert(half_canvas, suit, box.width - suit.width, corner_y)

    def _insert_mirror(self, canvas: Image, half_canvas: Image) -> None:
        """Insert mirrored copy of half_canvas into bottom half of canvas."""
        with Image(half_canvas) as mirror:
            mirror.flip()
            mirror.flop()
            canvas.composite(mirror, 0, math.floor(canvas.height / 2))

    def _draw_two(self, canvas: Image, suit: Image, box: Box) -> None:
        """Draw suit markers for 2 card."""
        with Image(
            width=canvas.width, height=math.floor(canvas.height / 2)
        ) as half_canvas:
            self._draw_single_top(half_canvas, suit, box)
            canvas.composite(half_canvas)
            self._insert_mirror(canvas, half_canvas)

    def _draw_three(self, canvas: Image, suit: Image, box: Box) -> None:
        """Draw suit markers for 3 card."""
        with Image(
            width=canvas.width, height=math.floor(canvas.height / 2)
        ) as half_canvas:
            self._draw_single_center(canvas, suit, box)
            self._draw_single_top(half_canvas, suit, box)
            canvas.composite(half_canvas)
            self._insert_mirror(canvas, half_canvas)

    def _draw_four(self, canvas: Image, suit: Image, box: Box) -> None:
        """Draw suit markers for 4 card."""
        with Image(
            width=canvas.width, height=math.floor(canvas.height / 2)
        ) as half_canvas:
            self._draw_pair_top(half_canvas, suit, box)
            canvas.composite(half_canvas)
            self._insert_mirror(canvas, half_canvas)

    def _draw_five(self, canvas: Image, suit: Image, box: Box) -> None:
        """Draw suit markers for 5 card."""
        with Image(
            width=canvas.width, height=math.floor(canvas.height / 2)
        ) as half_canvas:
            self._draw_pair_top(half_canvas, suit, box)
            canvas.composite(half_canvas)
            self._insert_mirror(canvas, half_canvas)
            self._draw_single_center(canvas, suit, box)

    def _draw_six(self, canvas: Image, suit: Image, box: Box) -> None:
        """Draw suit markers for 6 card."""
        with Image(
            width=canvas.width, height=math.floor(canvas.height / 2)
        ) as half_canvas:
            self._draw_pair_top(half_canvas, suit, box)
            canvas.composite(half_canvas)
            self._insert_mirror(canvas, half_canvas)
            self._draw_pair_center(canvas, suit, box)

    def _draw_seven(self, canvas: Image, suit: Image, box: Box) -> None:
        """Draw suit markers for 7 card."""
        with Image(
            width=canvas.width, height=math.floor(canvas.height / 2)
        ) as half_canvas:
            self._draw_pair_top(half_canvas, suit, box)
            canvas.composite(half_canvas)
            self._insert_mirror(canvas, half_canvas)
            self._draw_pair_center(canvas, suit, box)
            self._draw_single_offset(half_canvas, suit, box)
            canvas.composite(half_canvas)

    def _draw_eight(self, canvas: Image, suit: Image, box: Box) -> None:
        """Draw suit markers for 8 card."""
        with Image(
            width=canvas.width, height=math.floor(canvas.height / 2)
        ) as half_canvas:
            self._draw_pair_top(half_canvas, suit, box)
            canvas.composite(half_canvas)
            self._insert_mirror(canvas, half_canvas)
            self._draw_pair_center(canvas, suit, box)
            self._draw_single_offset(half_canvas, suit, box)
            canvas.composite(half_canvas)
            self._insert_mirror(canvas, half_canvas)

    def _draw_nine(self, canvas: Image, suit: Image, box: Box) -> None:
        """Draw suit markers for 9 card."""
        with Image(
            width=canvas.width, height=math.floor(canvas.height / 2)
        ) as half_canvas:
            self._draw_quad(half_canvas, suit, box)
            self._draw_single_center(canvas, suit, box)
            canvas.composite(half_canvas)
            self._insert_mirror(canvas, half_canvas)

    def _draw_ten(self, canvas: Image, suit: Image, box: Box) -> None:
        """Draw suit markers for 10 card."""
        with Image(
            width=canvas.width, height=math.floor(canvas.height / 2)
        ) as half_canvas:
            self._draw_quad(half_canvas, suit, box)
            canvas.composite(half_canvas)
            self._insert_mirror(canvas, half_canvas)
            self._draw_single_mid(half_canvas, suit, box)
            canvas.composite(half_canvas)
            self._insert_mirror(canvas, half_canvas)

    def _draw_suit_markers(self, canvas: Image, card_number: str, suit: Image) -> None:
        """Draw suit markers for a given card number.

        Args:
            canvas: Canvas to draw on
            card_number: Card number/value (A, 2-10, J, Q, K)
            suit: Suit image to use for markers
        """
        box_width = canvas.width - (2 * self.config.frame_horizontal_margin)
        box_height = canvas.height - (2 * self.config.frame_vertical_margin)
        box = Box(
            box_width,
            box_height,
            self.config.frame_horizontal_margin,
            self.config.frame_vertical_margin,
        )

        # Use the appropriate drawing function based on card number
        if card_number in self._card_drawing_functions:
            self._card_drawing_functions[card_number](canvas, suit, box)
        # Face cards (J, Q, K) don't have suit markers in the main area

    def _build_indicator(self, number: Image, suit: Image) -> Image:
        """Build corner indicator with number and mini suit.

        Args:
            number: Number image
            suit: Suit image

        Returns:
            Combined indicator image
        """
        indicator_height = (
            number.height
            + self.config.mini_suit_height
            + self.config.indicator_number_margin
        )
        indicator_width = max(number.width, self.config.mini_suit_width)

        # Transparent background
        indicator = Image(
            background="#f000", width=indicator_width, height=indicator_height
        )

        number_centre_x = math.floor(
            (indicator_width / 2) - (self.config.number_width / 2)
        )
        indicator.composite(number, number_centre_x)

        mini_suit = Image(suit)
        mini_suit.resize(self.config.mini_suit_width, self.config.mini_suit_height)

        centre_x = math.floor((indicator_width / 2) - (self.config.mini_suit_width / 2))
        indicator.composite(
            mini_suit, centre_x, number.height + self.config.indicator_number_margin
        )
        mini_suit.close()

        return indicator

    def _build_card(
        self,
        canvas: Image,
        frame: Image,
        style: str,
        card_number: str,
        suit_number: int,
        suit: Image,
    ) -> None:
        """Build a complete card with frame, suit markers, and indicators.

        Args:
            canvas: Canvas to draw on
            frame: Frame image to composite
            style: Name of the folder in the art directory to read assets from
            card_number: Card number/value
            suit_number: Suit number (0-3)
            suit: Suit image
        """
        canvas.composite(frame)
        self._draw_suit_markers(canvas, card_number, suit)

        # Load existing number image
        number = Image(filename=f"art/{style}/suit-{suit_number}/{card_number}.png")
        number.resize(self.config.number_width, self.config.number_height)

        indicator = self._build_indicator(number, suit)
        number.close()

        # Position indicators in corners
        top_y = self.config.vertical_margin
        bottom_y = canvas.height - self.config.vertical_margin - indicator.height
        left_x = self.config.horizontal_margin
        right_x = canvas.width - self.config.horizontal_margin - indicator.width

        canvas.composite(indicator, left_x, top_y)
        if self.config.support_left_handed:
            canvas.composite(indicator, right_x, top_y)

        indicator.flip()
        indicator.flop()
        canvas.composite(indicator, right_x, bottom_y)
        if self.config.support_left_handed:
            canvas.composite(indicator, left_x, bottom_y)

        indicator.close()

    def _build_suit(self, frame: Image, style: str, preview: Image, suit_number: int) -> None:
        """Build all cards for a specific suit.

        Args:
            frame: Frame image to use
            style: Name of the folder in the art directory to read assets from
            preview: Preview image to composite cards onto
            suit_number: Suit number (0-3)
        """
        with Image(filename=f"art/{style}/suit-{suit_number}.png") as suit:
            suit.resize(
                self.config.suit_indicator_width, self.config.suit_indicator_height
            )

            for i, card_value in enumerate(self.config.card_values):
                canvas = Image(width=frame.width, height=frame.height)
                self._build_card(canvas, frame, style, card_value, suit_number, suit)
                canvas.save(filename=f"bin/suit_{suit_number}_card_{card_value}.png")
                preview.composite(canvas, i * canvas.width, suit_number * canvas.height)
                canvas.close()

    def generate_cards(self, style: str = "poker", output_dir: str = "bin") -> None:
        """Generate all playing cards.

        Args:
            output_dir: Directory to save generated cards
            :param style: Asset folder to use from the art directory
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        try:
            with Image(filename="art/frame.png") as frame:
                total_width = frame.width * len(self.config.card_values)
                total_height = frame.height * self.config.total_suits

                with Image(width=total_width, height=total_height) as preview:
                    for suit_number in range(self.config.total_suits):
                        self._build_suit(frame, style, preview, suit_number)

                    preview.save(filename=f"{output_dir}/preview.png")

        except Exception as e:
            raise RuntimeError(f"Failed to generate cards: {e}") from e
