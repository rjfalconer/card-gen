"""Test face card artwork generation."""

from wand.image import Image
from card_gen.face_cards import FaceCardArtwork


class TestFaceCardArtwork:
    """Test cases for FaceCardArtwork class."""

    def test_initialization_default(self) -> None:
        """Test default initialization."""
        artwork = FaceCardArtwork()
        assert artwork.width == 54
        assert artwork.height == 74

    def test_initialization_custom(self) -> None:
        """Test initialization with custom dimensions."""
        artwork = FaceCardArtwork(width=100, height=150)
        assert artwork.width == 100
        assert artwork.height == 150

    def test_generate_jack(self) -> None:
        """Test Jack artwork generation."""
        artwork = FaceCardArtwork()
        jack_img = artwork.generate_jack()

        assert isinstance(jack_img, Image)
        assert jack_img.width == 54
        assert jack_img.height == 74

        jack_img.close()

    def test_generate_jack_with_color(self) -> None:
        """Test Jack artwork generation with custom color."""
        artwork = FaceCardArtwork()
        jack_img = artwork.generate_jack(color="red")

        assert isinstance(jack_img, Image)
        assert jack_img.width == 54
        assert jack_img.height == 74

        jack_img.close()

    def test_generate_queen(self) -> None:
        """Test Queen artwork generation."""
        artwork = FaceCardArtwork()
        queen_img = artwork.generate_queen()

        assert isinstance(queen_img, Image)
        assert queen_img.width == 54
        assert queen_img.height == 74

        queen_img.close()

    def test_generate_queen_with_color(self) -> None:
        """Test Queen artwork generation with custom color."""
        artwork = FaceCardArtwork()
        queen_img = artwork.generate_queen(color="blue")

        assert isinstance(queen_img, Image)
        assert queen_img.width == 54
        assert queen_img.height == 74

        queen_img.close()

    def test_generate_king(self) -> None:
        """Test King artwork generation."""
        artwork = FaceCardArtwork()
        king_img = artwork.generate_king()

        assert isinstance(king_img, Image)
        assert king_img.width == 54
        assert king_img.height == 74

        king_img.close()

    def test_generate_king_with_color(self) -> None:
        """Test King artwork generation with custom color."""
        artwork = FaceCardArtwork()
        king_img = artwork.generate_king(color="green")

        assert isinstance(king_img, Image)
        assert king_img.width == 54
        assert king_img.height == 74

        king_img.close()

    def test_save_face_cards(self, tmp_path) -> None:
        """Test saving face cards to directory."""
        artwork = FaceCardArtwork()

        # Save face cards for suit 0 (red suit)
        artwork.save_face_cards(str(tmp_path), 0)

        # Check that files were created
        suit_dir = tmp_path / "suit-0"
        assert suit_dir.exists()
        assert (suit_dir / "J.png").exists()
        assert (suit_dir / "Q.png").exists()
        assert (suit_dir / "K.png").exists()

    def test_save_face_cards_black_suit(self, tmp_path) -> None:
        """Test saving face cards for black suit."""
        artwork = FaceCardArtwork()

        # Save face cards for suit 1 (black suit)
        artwork.save_face_cards(str(tmp_path), 1)

        # Check that files were created
        suit_dir = tmp_path / "suit-1"
        assert suit_dir.exists()
        assert (suit_dir / "J.png").exists()
        assert (suit_dir / "Q.png").exists()
        assert (suit_dir / "K.png").exists()
