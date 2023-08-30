import uiautomator2 as u2
import cv2 as cv
from PIL import Image
import numpy as np
import os
import time


base_dir = os.path.dirname(os.path.abspath(__file__))


def crop_image(base_image_path, left, top, right, bottom):
    crop_dir = os.path.join(base_dir, "data/images/crop")
    os.makedirs(crop_dir, exist_ok=True)
    cropped_image_path = os.path.join(
        crop_dir,
        f"crop_{left}_{top}_{right}_{bottom}_{os.path.basename(base_image_path)}"
    )
    if not os.path.exists(cropped_image_path):
        image = Image.open(base_image_path)
        cropped_image = image.crop((left, top, right, bottom))
        cropped_image.save(cropped_image_path)
    return cropped_image_path


def screenshot(file_name=None):
    d = u2.connect()
    screenshot_dir = os.path.join(base_dir, "data/images/screenshot")
    os.makedirs(screenshot_dir, exist_ok=True)
    if file_name is None:
        file_name = f"{time.time()}.png"
    screenshot_path = os.path.join(screenshot_dir, file_name)
    d.screenshot(screenshot_path)
    with Image.open(screenshot_path) as im:
        if im.mode == "RGBA":
            # TODO: 为什么一会儿RBGA 一会儿RBG，并且为什么格式一定要RBG？
            img = cv.imread(screenshot_path, 1)
            jpg_img = cv.cvtColor(img, cv.COLOR_BGRA2BGR)
            cv.imwrite(screenshot_path, jpg_img)
    return screenshot_path


def click_base(button, cropped_image_path=None, threshold=.5):
    if cropped_image_path is None or not os.path.exists(cropped_image_path) and isinstance(button, dict):
        # setup
        # crop
        base_image_path = button.get("page")
        cropped_image_path = crop_image(
            base_image_path,
            *button.get("loc")
        )

    # get screenshot  and detect object
    screenshot_path = screenshot()
    loc = loc_needle_in_haystack(cropped_image_path, screenshot_path, threshold=threshold)
    os.remove(screenshot_path)
    if loc:
        x = (loc[0] + loc[2]) // 2
        y = (loc[1] + loc[3]) // 2
        d = u2.connect()
        print(x, y)
        d.click(x, y)
    else:
        raise Exception("button missions not found.")


def loc_needle_in_haystack(image_path_needle, image_path_haystack, threshold=0.8):
    if not os.path.exists(image_path_needle):
        raise FileNotFoundError(image_path_needle)
    if not os.path.exists(image_path_haystack):
        raise FileNotFoundError(image_path_haystack)

    haystack_img = cv.imread(image_path_haystack, cv.IMREAD_UNCHANGED)
    needle_img = cv.imread(image_path_needle, cv.IMREAD_UNCHANGED)

    result = cv.matchTemplate(haystack_img, needle_img, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    print('Best match top left position: %s' % str(max_loc))
    print('Best match confidence: %s' % max_val)

    if max_val >= threshold:
        print('Found needle.')

        needle_w = needle_img.shape[1]
        needle_h = needle_img.shape[0]

        top_left = max_loc
        bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)
        return *top_left, *bottom_right

    else:
        print('Needle not found.')
        return False


def locations_needle_in_haystack(image_path_needle, image_path_haystack, threshold=0.8):
    if not os.path.exists(image_path_needle):
        raise FileNotFoundError(image_path_needle)
    if not os.path.exists(image_path_haystack):
        raise FileNotFoundError(image_path_haystack)

    haystack_img = cv.imread(image_path_haystack, cv.IMREAD_UNCHANGED)
    needle_img = cv.imread(image_path_needle, cv.IMREAD_UNCHANGED)

    result = cv.matchTemplate(haystack_img, needle_img, cv.TM_CCOEFF_NORMED)
    print(result)
    locations = np.where(result >= threshold)
    print(locations)
    locations = list(zip(*locations[::-1]))
    print(f"len of locations: {len(locations)}")
    if locations:
        print('Found needles.')

        needle_w = needle_img.shape[1]
        needle_h = needle_img.shape[0]
        line_color = (0, 255, 0)
        line_type = cv.LINE_4

        # Loop over all the locations and draw their rectangle
        for index, loc in enumerate(locations):

            # Determine the box positions
            top_left = loc
            bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)
            # print(top_left)
            # Draw the box
            cv.rectangle(haystack_img, top_left, bottom_right, line_color, line_type)
            print(f"#{index} loc{loc}: confidence='{result[loc[1],loc[0]]}'")
        cv.imwrite('result.jpg', haystack_img)
        return locations
    else:
        print('Needle not found.')
