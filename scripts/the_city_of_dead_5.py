# coding: utf-8
#
import time
import logging
import datetime
import uiautomator2 as u2
from main import open_boxes, continue_next, screenshot

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

d = u2.connect()

steps = [
    "",
    "start",
    "select_5",
    "select_5_2",
    "select_5_2_confirm",
    "select_5_2_team_select",
    "fighting_ready",
    "fighting_start_dialogue1",
    "fighting_start_dialogue2",
    "fighting_start_move1",
    "fighting_start_move2",
    "fighting_success_next",
    "open_boxes_and_free_unlocks",
    "open_boxes_next",
]


def screenshot_game_flow(step):
    file_name = f"{step}_" \
                f"{steps[step]}.png"
    logging.info(f"screenshot_game_flow #{step}, {steps[step]}")
    screenshot(file_name)
    step += 1
    return step


while True:
    start_time = datetime.datetime.now()
    # 记录
    screenshot()
    current_step = 1

    current_step = screenshot_game_flow(current_step)
    d.click(0.454, 0.888)
    time.sleep(0.5)

    current_step = screenshot_game_flow(current_step)
    d.click(0.394, 0.591)
    time.sleep(0.5)

    current_step = screenshot_game_flow(current_step)
    d.click(0.516, 0.884)
    time.sleep(0.5)

    current_step = screenshot_game_flow(current_step)
    d.click(0.85, 0.906)
    time.sleep(5)

    current_step = screenshot_game_flow(current_step)
    d.click(0.514, 0.902)
    time.sleep(5)

    current_step = screenshot_game_flow(current_step)
    d.click(0.506, 0.817)
    time.sleep(0.5)

    current_step = screenshot_game_flow(current_step)
    d.click(0.512, 0.364)
    time.sleep(0.5)

    current_step = screenshot_game_flow(current_step)
    d.click(0.512, 0.364)
    time.sleep(0.5)

    # 等待可以操作英雄
    current_step = screenshot_game_flow(current_step)
    d.swipe_points([(0.656, 0.355), (0.288, 0.346)], 0.2)
    time.sleep(8)

    current_step = screenshot_game_flow(current_step)
    d.swipe_points([(0.288, 0.346), (0.008, 0.444)], 0.2)
    time.sleep(3)

    current_step = screenshot_game_flow(current_step)
    d.click(0.502, 0.888)
    time.sleep(.5)
    d.click(0.502, 0.888)
    time.sleep(.5)

    current_step = screenshot_game_flow(current_step)
    open_boxes()
    time.sleep(1)

    current_step = screenshot_game_flow(current_step)
    continue_next()
    time.sleep(5)

    used_time = datetime.datetime.now() - start_time
    logging.info(f"used_time: {used_time.seconds}s")

