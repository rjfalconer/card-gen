"""Generate face card artwork programmatically."""

from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color


class FaceCardArtwork:
    """Generate J, Q, K artwork programmatically using simple geometric shapes."""

    def __init__(self, width: int = 54, height: int = 74) -> None:
        """Initialize face card artwork generator.

        Args:
            width: Width of the generated artwork
            height: Height of the generated artwork
        """
        self.width = width
        self.height = height

    def generate_jack(self, color: str = "black") -> Image:
        """Generate Jack artwork with simple geometric representation.

        Args:
            color: Color for the artwork

        Returns:
            Wand Image object containing the Jack artwork
        """
        img = Image(
            width=self.width, height=self.height, background=Color("transparent")
        )

        with Drawing() as draw:
            draw.fill_color = Color(color)
            draw.stroke_color = Color(color)
            draw.stroke_width = 2

            # Simple "J" shape with decorative elements
            # Vertical line
            draw.line(
                (self.width * 0.6, self.height * 0.2),
                (self.width * 0.6, self.height * 0.7),
            )

            # Hook at bottom
            draw.arc(
                (self.width * 0.3, self.height * 0.6),
                (self.width * 0.7, self.height * 0.8),
                (180, 270),
            )

            # Crown/hat decoration
            draw.rectangle(
                self.width * 0.4,
                self.height * 0.1,
                self.width * 0.8,
                self.height * 0.25,
            )

            draw(img)

        return img

    def generate_queen(self, color: str = "black") -> Image:
        """Generate Queen artwork with crown and elegant design.

        Args:
            color: Color for the artwork

        Returns:
            Wand Image object containing the Queen artwork
        """
        img = Image(
            width=self.width, height=self.height, background=Color("transparent")
        )

        with Drawing() as draw:
            draw.fill_color = Color(color)
            draw.stroke_color = Color(color)
            draw.stroke_width = 2

            # Crown with points
            crown_points = [
                (self.width * 0.2, self.height * 0.3),
                (self.width * 0.3, self.height * 0.15),
                (self.width * 0.4, self.height * 0.25),
                (self.width * 0.5, self.height * 0.1),
                (self.width * 0.6, self.height * 0.25),
                (self.width * 0.7, self.height * 0.15),
                (self.width * 0.8, self.height * 0.3),
                (self.width * 0.2, self.height * 0.3),
            ]

            draw.polygon(crown_points)

            # Face (circle)
            draw.fill_color = Color("transparent")
            draw.circle(
                (self.width * 0.5, self.height * 0.5),
                (self.width * 0.6, self.height * 0.5),
            )

            # Dress/body (triangle)
            draw.fill_color = Color(color)
            dress_points = [
                (self.width * 0.5, self.height * 0.6),
                (self.width * 0.3, self.height * 0.9),
                (self.width * 0.7, self.height * 0.9),
            ]
            draw.polygon(dress_points)

            draw(img)

        return img

    def generate_king(self, color: str = "black") -> Image:
        """Generate King artwork with crown and regal design.

        Args:
            color: Color for the artwork

        Returns:
            Wand Image object containing the King artwork
        """
        img = Image(
            width=self.width, height=self.height, background=Color("transparent")
        )

        with Drawing() as draw:
            draw.fill_color = Color(color)
            draw.stroke_color = Color(color)
            draw.stroke_width = 2

            # Crown base
            draw.rectangle(
                self.width * 0.25,
                self.height * 0.2,
                self.width * 0.75,
                self.height * 0.3,
            )

            # Crown cross decoration
            # Vertical line of cross
            draw.line(
                (self.width * 0.5, self.height * 0.1),
                (self.width * 0.5, self.height * 0.25),
            )
            # Horizontal line of cross
            draw.line(
                (self.width * 0.4, self.height * 0.15),
                (self.width * 0.6, self.height * 0.15),
            )

            # Face (circle)
            draw.fill_color = Color("transparent")
            draw.circle(
                (self.width * 0.5, self.height * 0.45),
                (self.width * 0.6, self.height * 0.45),
            )

            # Beard (triangle below face)
            draw.fill_color = Color(color)
            beard_points = [
                (self.width * 0.4, self.height * 0.55),
                (self.width * 0.6, self.height * 0.55),
                (self.width * 0.5, self.height * 0.7),
            ]
            draw.polygon(beard_points)

            # Body (rectangle)
            draw.rectangle(
                self.width * 0.35,
                self.height * 0.65,
                self.width * 0.65,
                self.height * 0.9,
            )

            draw(img)

        return img

    def save_face_cards(self, output_dir: str, suit_number: int) -> None:
        """Generate and save J, Q, K artwork for a specific suit.

        Args:
            output_dir: Directory to save the images
            suit_number: Suit number (0-3) for filename generation
        """
        import os

        # Determine color based on suit (0,2 = red suits, 1,3 = black suits)
        color = "red" if suit_number in [0, 2] else "black"

        face_cards = {
            "J": self.generate_jack(color),
            "Q": self.generate_queen(color),
            "K": self.generate_king(color),
        }

        suit_dir = os.path.join(output_dir, f"suit-{suit_number}")
        os.makedirs(suit_dir, exist_ok=True)

        for card_name, artwork in face_cards.items():
            filename = os.path.join(suit_dir, f"{card_name}.png")
            artwork.save(filename=filename)
            artwork.close()
