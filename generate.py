#!/usr/bin/env python
"""Script for generating poker cards using suit images and ImageMagick."""

from card_gen import CardGenerator, Config


def main() -> None:
    """Generate poker cards with default configuration."""
    config = Config()
    generator = CardGenerator(config)
    generator.generate_cards()
    print(f"Generated {len(config.card_values) * config.total_suits} cards successfully!")
    print("Output saved to 'bin/' directory")


if __name__ == "__main__":
    main()