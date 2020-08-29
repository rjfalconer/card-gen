#!/usr/bin/env python

# Copyright 2020, Richard Falconer @rjfalconer / https://github.com/rjfalconer

import os
import math
from wand.image import Image


class Config:
    def __init__(self):
        self.card_values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        self.total_suits = 4

        # Dimensions of indicator for the Ace card
        self.ace_size = 250

        #  Margin between frame.jpg and rest of printable area
        self.frame_horizontal_margin = 100
        self.frame_vertical_margin = 100

        #  Vertical margin between the corner suit-indicators and the numerical card values
        self.indicator_number_margin = 10

        #  Dimension of the smaller corner suit-indicator (scaled down from the suit art)
        self.mini_suit_width = 60
        self.mini_suit_height = 70
        self.number_width = 54
        self.number_height = 74

        #  Dimension of the larger central suit-indicator
        self.suit_indicator_width = 170
        self.suit_indicator_height = 170  # In regular playing cards this is about 17.5% the height of the card

        #  Margins for the indicators, relative to the frame (not the box)
        self.horizontal_margin = 15
        self.vertical_margin = 60

        #  Render card indicators on all four corners, not just top left and bottom right
        self.support_left_handed = True


class Box:
    #  Defines printable area within card for use with suit-indicators
    def __init__(self, width, height, margin_left, margin_top):
        self.width = width
        self.height = height
        self.margin_left = margin_left
        self.margin_top = margin_top

    def insert(self, canvas, image, x, y):
        #  Insert image onto canvas, positioned at x,y offset relative to canvas indicator box
        corner_x = math.floor(x + self.margin_left)
        corner_y = math.floor((y + self.margin_top))
        canvas.composite(image, corner_x, corner_y)


def draw_suit_marker_ace(canvas, suit, box):
    with Image(suit) as big_suit:
        big_suit.resize(config.ace_size, config.ace_size)
        corner_x = (box.width / 2) - (big_suit.width / 2)
        corner_y = (box.height / 2) - (big_suit.height / 2)
        box.insert(canvas, big_suit, corner_x, corner_y)


def draw_suit_marker_single_solo(canvas, suit, box):
    #  The centre of a 3, 5, or 9
    corner_x = (box.width / 2) - (suit.width / 2)
    corner_y = (box.height / 2) - (suit.height / 2)
    box.insert(canvas, suit, corner_x, corner_y)


def draw_suit_pair_solo(canvas, suit, box):
    #  The middle row of a 6, 7, or 8
    corner_x = 0
    corner_y = (box.height / 2) - (suit.height / 2)
    box.insert(canvas, suit, corner_x, corner_y)
    box.insert(canvas, suit, box.width - suit.width, corner_y)


def draw_suit_marker_single_top(half_canvas, suit, box):
    #  The top row of a 2 or a 3
    corner_x = (box.width / 2) - (suit.width / 2)
    corner_y = 0
    box.insert(half_canvas, suit, corner_x, corner_y)


def draw_suit_marker_single_offset(half_canvas, suit, box):
    #  Half of the middle column of an 8
    corner_x = (box.width / 2) - (suit.width / 2)
    corner_y = (box.height / 5)
    box.insert(half_canvas, suit, corner_x, corner_y)


def draw_suit_marker_single_mid(half_canvas, suit, box):
    #  Half of the middle column of a 10
    corner_x = (box.width / 2) - (suit.width / 2)
    corner_y = (half_canvas.height / 4)
    box.insert(half_canvas, suit, corner_x, corner_y)


def draw_suit_marker_pair(half_canvas, suit, box):
    #  The top row of a 4, 5, 6, 7, or 8
    corner_x = 0
    corner_y = 0
    box.insert(half_canvas, suit, corner_x, corner_y)
    box.insert(half_canvas, suit, box.width - suit.width, corner_y)


def draw_suit_marker_quad(half_canvas, suit, box):
    #  The top two rows of a 9 or 10
    corner_x = 0
    corner_y = 0
    box.insert(half_canvas, suit, corner_x, corner_y)
    box.insert(half_canvas, suit, box.width - suit.width, corner_y)

    buffer_space = box.height - (4 * suit.height)
    corner_y = suit.height + (buffer_space / 3)
    box.insert(half_canvas, suit, corner_x, corner_y)
    box.insert(half_canvas, suit, box.width - suit.width, corner_y)


def insert_mirror(canvas, half_canvas):
    with Image(half_canvas) as mirror:
        mirror.flip()
        mirror.flop()
        canvas.composite(mirror, 0, math.floor(canvas.height / 2))


def draw_suit_markers(canvas, card_number, suit):
    box_width = canvas.width - (2 * config.frame_horizontal_margin)
    box_height = canvas.height - (2 * config.frame_vertical_margin)
    box = Box(box_width, box_height, config.frame_horizontal_margin, config.frame_vertical_margin)

    with Image(width=canvas.width, height=math.floor(canvas.height / 2)) as half_canvas:
        if card_number == 'A':
            #  Uncomment if you do not want to special-case Ace, and instead render it like the middle of a 3.
            # draw_suit_marker_single_solo(canvas, suit, box)
            draw_suit_marker_ace(canvas, suit, box)
        elif card_number == '2':
            draw_suit_marker_single_top(half_canvas, suit, box)
            canvas.composite(half_canvas)
            insert_mirror(canvas, half_canvas)
        elif card_number == '3':
            draw_suit_marker_single_solo(canvas, suit, box)
            draw_suit_marker_single_top(half_canvas, suit, box)
            canvas.composite(half_canvas)
            insert_mirror(canvas, half_canvas)
        elif card_number == '4':
            draw_suit_marker_pair(half_canvas, suit, box)
            canvas.composite(half_canvas)
            insert_mirror(canvas, half_canvas)
        elif card_number == '5':
            draw_suit_marker_pair(half_canvas, suit, box)
            canvas.composite(half_canvas)
            insert_mirror(canvas, half_canvas)
            draw_suit_marker_single_solo(canvas, suit, box)
        elif card_number == '6':
            draw_suit_marker_pair(half_canvas, suit, box)
            canvas.composite(half_canvas)
            insert_mirror(canvas, half_canvas)
            draw_suit_pair_solo(canvas, suit, box)
        elif card_number == '7':
            draw_suit_marker_pair(half_canvas, suit, box)
            canvas.composite(half_canvas)
            insert_mirror(canvas, half_canvas)
            draw_suit_pair_solo(canvas, suit, box)
            draw_suit_marker_single_offset(half_canvas, suit, box)
            canvas.composite(half_canvas)
        elif card_number == '8':
            draw_suit_marker_pair(half_canvas, suit, box)
            canvas.composite(half_canvas)
            insert_mirror(canvas, half_canvas)
            draw_suit_pair_solo(canvas, suit, box)
            draw_suit_marker_single_offset(half_canvas, suit, box)
            canvas.composite(half_canvas)
            insert_mirror(canvas, half_canvas)
        elif card_number == '9':
            draw_suit_marker_quad(half_canvas, suit, box)
            draw_suit_marker_single_solo(canvas, suit, box)
            canvas.composite(half_canvas)
            insert_mirror(canvas, half_canvas)
        elif card_number == '10':
            draw_suit_marker_quad(half_canvas, suit, box)
            canvas.composite(half_canvas)
            insert_mirror(canvas, half_canvas)
            draw_suit_marker_single_mid(half_canvas, suit, box)
            canvas.composite(half_canvas)
            insert_mirror(canvas, half_canvas)

    return


def build_card(canvas, frame, card_number, suit_number, suit):
    canvas.composite(frame)
    draw_suit_markers(canvas, card_number, suit)

    number = Image(filename=f"numbers/suit-{suit_number}/{card_number}.png")
    number.resize(config.number_width, config.number_height)
    indicator = build_indicator(number, suit)
    number.close()

    top_y = config.vertical_margin
    bottom_y = canvas.height - config.vertical_margin - indicator.height
    left_x = config.horizontal_margin
    right_x = canvas.width - config.horizontal_margin - indicator.width

    canvas.composite(indicator, left_x, top_y)
    if config.support_left_handed:
        canvas.composite(indicator, right_x, top_y)
    indicator.flip()
    indicator.flop()
    canvas.composite(indicator, right_x, bottom_y)
    if config.support_left_handed:
        canvas.composite(indicator, left_x, bottom_y)

    indicator.close()
    return


def build_indicator(number, suit):
    indicator_height = number.height + config.mini_suit_height + config.indicator_number_margin
    indicator_width = max(number.width, config.mini_suit_width)

    # Transparent
    indicator = Image(background="#f000", width=indicator_width, height=indicator_height)
    number_centre_x = math.floor((indicator_width / 2) - (config.number_width / 2))
    indicator.composite(number, number_centre_x)
    mini_suit = Image(suit)
    mini_suit.resize(config.mini_suit_width, config.mini_suit_height)

    centre_x = math.floor((indicator_width / 2) - (config.mini_suit_width / 2))
    indicator.composite(mini_suit, centre_x, number.height + config.indicator_number_margin)
    mini_suit.close()
    indicator.save(filename='bin/debug_card_indicator.png')

    return indicator


def build_suit(frame, preview, suit_number):
    with Image(filename=f"art/suit-{suit_number}.png") as suit:
        suit.resize(config.suit_indicator_width, config.suit_indicator_height)
        for i, card_value in enumerate(config.card_values):
            canvas = Image(width=frame.width, height=frame.height)
            build_card(canvas, frame, card_value, suit_number, suit)
            canvas.save(filename=f"bin/suit_{suit_number}_card_{card_value}.png")
            preview.composite(canvas, i * canvas.width, suit_number * canvas.height)


def main():
    if not os.path.exists("bin"):
        os.mkdir("bin")

    with Image(filename='art/frame.png') as frame:
        total_width = frame.width * len(config.card_values)
        total_height = frame.height * config.total_suits
        with Image(width=total_width, height=total_height) as preview:
            for suit_number in range(config.total_suits):
                build_suit(frame, preview, suit_number)

            preview.save(filename="bin/preview.png")


config = Config()
main()
