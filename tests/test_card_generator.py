"""Test card generator functionality."""

import pytest
from unittest.mock import Mock, patch

from card_gen.card_generator import CardGenerator, Box
from card_gen.config import Config


class TestBox:
    """Test cases for Box class."""

    def test_initialization(self) -> None:
        """Test Box initialization."""
        box = Box(100, 200, 10, 20)
        assert box.width == 100
        assert box.height == 200
        assert box.margin_left == 10
        assert box.margin_top == 20

    def test_insert(self) -> None:
        """Test Box insert method."""
        box = Box(100, 200, 10, 20)

        # Mock canvas and image
        canvas = Mock()
        image = Mock()

        box.insert(canvas, image, 5, 15)

        # Check that composite was called with correct coordinates
        canvas.composite.assert_called_once_with(image, 15, 35)  # 5+10, 15+20


class TestCardGenerator:
    """Test cases for CardGenerator class."""

    def test_initialization_default_config(self) -> None:
        """Test initialization with default config."""
        generator = CardGenerator()
        assert generator.config is not None
        assert len(generator.config.card_values) == 13

    def test_initialization_custom_config(self) -> None:
        """Test initialization with custom config."""
        config = Config(total_suits=2)
        generator = CardGenerator(config)
        assert generator.config.total_suits == 2

    def test_initialization_validates_config(self) -> None:
        """Test that initialization validates the config."""
        config = Config(total_suits=0)  # Invalid config
        with pytest.raises(ValueError):
            CardGenerator(config)

    def test_card_drawing_functions_mapping(self) -> None:
        """Test that all numeric cards have drawing functions."""
        generator = CardGenerator()
        expected_cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

        for card in expected_cards:
            assert card in generator._card_drawing_functions

    def test_insert_mirror_calculations(self) -> None:
        """Test the mirror insertion calculations."""
        generator = CardGenerator()

        # Mock canvas and half_canvas
        canvas = Mock()
        canvas.height = 300
        half_canvas = Mock()

        # Mock the Image context manager for the mirrored image
        mock_mirror = Mock()
        mock_mirror.__enter__ = Mock(return_value=mock_mirror)
        mock_mirror.__exit__ = Mock(return_value=None)

        with patch("card_gen.card_generator.Image", return_value=mock_mirror):
            generator._insert_mirror(canvas, half_canvas)

            # Verify flip and flop were called
            mock_mirror.flip.assert_called_once()
            mock_mirror.flop.assert_called_once()

            # Verify composite was called with correct y position (150 for height 300)
            canvas.composite.assert_called_once_with(mock_mirror, 0, 150)

    @patch("os.path.exists")
    @patch("os.makedirs")
    def test_generate_cards_creates_output_dir(
        self, mock_makedirs, mock_exists
    ) -> None:
        """Test that generate_cards creates output directory if it doesn't exist."""
        mock_exists.return_value = False

        generator = CardGenerator()

        # Mock the entire image processing to avoid ImageMagick issues
        with patch("card_gen.card_generator.Image") as mock_image:
            mock_image.side_effect = FileNotFoundError("Test file not found")

            with pytest.raises(RuntimeError, match="Failed to generate cards"):
                generator.generate_cards("test_output")

            mock_makedirs.assert_called_once_with("test_output")

    def test_generate_cards_error_handling(self) -> None:
        """Test error handling in generate_cards."""
        generator = CardGenerator()

        with patch("card_gen.card_generator.Image") as mock_image:
            mock_image.side_effect = Exception("Test error")

            with pytest.raises(
                RuntimeError, match="Failed to generate cards: Test error"
            ):
                generator.generate_cards()

    def test_face_cards_not_in_drawing_functions(self) -> None:
        """Test that face cards (J, Q, K) are not in drawing functions mapping."""
        generator = CardGenerator()

        face_cards = ["J", "Q", "K"]
        for card in face_cards:
            assert card not in generator._card_drawing_functions

    def test_config_validation_during_init(self) -> None:
        """Test that config is validated during initialization."""
        # This should work fine
        config = Config()
        generator = CardGenerator(config)
        assert generator.config == config

        # This should raise an error
        config.total_suits = -1
        with pytest.raises(ValueError):
            CardGenerator(config)
