import os
import time
import tempfile

import uiautomator2 as u2
from utils import (
    loc_needle_in_haystack,
    crop_image,
    screenshot,
    click_base,
    base_dir,
    locations_needle_in_haystack
)


def click_button():
    base_image = 'data/images/base/twd_page_main.png'
    button = {
        "name": "button.missions",
        "page": base_image,
        "loc": (2183, 878, 2370, 1060)
    }
    click_base(button)


def click_button_challenge():
    base_image = 'data/images/base/twd_page_missions.png'
    button = {
        "name": "button.challenge",
        "page": base_image,
        "loc": (914, 511, 1319, 1088)
    }
    
    click_base(button)

def click_button_challenge_select():
    base_image = 'data/images/base/twd_page_challenge.png'
    button = {
        "name": "button.challenge_select",
        "page": base_image,
        "loc": (750, 617, 890, 800)
    }

    click_base(button)


def click_button_challenge_select_start():
    base_image = 'data/images/base/twd_page_challenge_selected.png'
    button = {
        "name": "button.challenge_select_start",
        "page": base_image,
        "loc": (1015, 900, 1420, 1015)
    }

    click_base(button)


def click_button_select_your_team():
    base_image = 'data/images/base/twd_page_select_your_team.png'
    button = {
        "name": "button.select_your_team",
        "page": base_image,
        "loc": (1750, 950, 2327, 1060)
    }
    click_base(button)


def click_button_fighting_ready():
    base_image = 'data/images/base/twd_page_fighting_ready.png'
    button = {
        "name": "button.fighting_ready",
        "page": base_image,
        "loc": (915, 935, 1488, 1035)
    }
    click_base(button)


def fighting():
    base_image = 'data/images/base/twd_page_fighting_start.png'
    hero = {
        "name": "button.fighting",
        "page": base_image,
        "loc": (514, 435, 660, 560)
    }
    end_turn = {
        "name": "button.end_turn",
        "page": base_image,
        "loc": (1540, 957, 1800, 1074)
    }
    for _ in range(20):
        try:
            click_base(end_turn)
        except Exception as e:
            print(e)
        time.sleep(.5)


def continue_next():
    cropped_image_path = os.path.join(base_dir, 'data/images/crop/crop_continue.png')

    for _ in range(3):
        try:
            click_base(button=None, cropped_image_path=cropped_image_path, threshold=.3)
            break
        except Exception as e:
            print(e)
            time.sleep(.2)


def open_boxes():
    def open_boxes_can_open(number_box_can_open=3):
        while number_box_can_open >= 0:
            try:
                click_base(box, threshold=.3)
                number_box_can_open -= 1
                time.sleep(.1)
            except Exception as e:
                print(e)
                time.sleep(.5)

    base_image = 'data/images/base/twd_page_boxes.png'
    box = {
        "name": "button.box",
        "page": base_image,
        "loc": (1100, 400, 1326, 600)
    }

    open_boxes_can_open()

    base_image = 'data/images/base/twd_page_boxes_free_unlocks.png'
    free_unlocks = {
        "name": "button.free_unlocks",
        "page": base_image,
        "loc": (18, 517, 285, 625)
    }

    exist_free_unlocks = False
    for _ in range(1):
        try:
            click_base(free_unlocks)
            exist_free_unlocks = True
        except Exception as e:
            print(e)
        time.sleep(.2)

    if exist_free_unlocks:
        open_boxes_can_open()


def walkers():
    base_image_path = os.path.join(base_dir, "data/images/base/twd_page_fighting_start.png")
    loc = (1095, 250, 1190, 290)
    base_image_path = os.path.join(base_dir, "data/images/base/twd_page_fighting_start.png")
    loc = (1676, 518, 1776, 560)

    # setup
    # crop
    cropped_image_path = crop_image(
        base_image_path,
        *loc
    )

    # get screenshot  and detect object
    haystack_image_path = screenshot()
    locations = locations_needle_in_haystack(cropped_image_path, haystack_image_path, threshold=.4)
    print(locations)
    os.remove(haystack_image_path)
    return locations


def heroes():

    base_image_path = os.path.join(base_dir, "data/images/base/twd_page_fighting_start.png")
    # assault
    loc = (450, 345, 615, 406)
    #
    loc = (405, 460, 530, 525)
    #
    loc = (360, 605, 508, 660)
    heroes_locations = list()
    for loc in []:
        # setup
        # crop
        cropped_image_path = crop_image(
            base_image_path,
            *loc
        )

        # get screenshot  and detect object
        haystack_image_path = screenshot()
        locations = locations_needle_in_haystack(cropped_image_path, haystack_image_path, threshold=.5)
        heroes_locations.extend(locations)
    print(heroes_locations)
    return heroes_locations


def detect_current_page():
    page_image_path = os.path.join(base_dir, "data/images/base/the_city_of_dead_5/1_start.png")
    screenshot_path = os.path.join(base_dir, "data/images/screenshot/1693276655.195137.png")


if __name__ == '__main__':
    # click_button()
    # time.sleep(1)
    # click_button_challenge()
    # time.sleep(1)
    # click_button_challenge_select()
    #
    # time.sleep(1)
    # click_button_challenge_select_start()
    #
    # time.sleep(1)
    # click_button_select_your_team()

    # time.sleep(3)
    # click_button_fighting_ready()

    # fighting()
    # continue_next()
    # continue_next()
    # time.sleep(1)
    # open_boxes()
    # time.sleep(3)
    # continue_next()
    # continue_next()
    # walkers()
    # heroes()
    detect_current_page()
