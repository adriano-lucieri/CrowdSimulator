import PySimpleGUI as sg
from pathlib import Path
from PIL import Image, ImageOps
import base64
from io import BytesIO
import sys
import tkinter
from tkinter import filedialog
import os

root = tkinter.Tk()
root.withdraw()

TRANSPARENT_COLOR = 'green'


# Convert Image to String
def im_2_b64(image):
    buff = BytesIO()
    image.save(buff, format="PNG")
    img_str = base64.b64encode(buff.getvalue())
    return img_str


def get_image_from_path(path):
    img = Image.open(path)
    img_w, img_h = img.size
    print('Image Size: (%d,%d)' % (img_w, img_h))
    factor = w / img_w
    print('Crop Factor: %.2f' % factor)
    new_h = min(int(img_h * factor), h)
    new_w = min(int(img_w * factor), w)
    img = img.resize((new_w, new_h))
    base64_image = im_2_b64(img)
    return base64_image


def get_new_image_data():
    currdir = os.getcwd()
    tempdir = filedialog.askopenfilename(parent=root, initialdir=currdir, title='Please select a directory')
    if os.path.exists(tempdir):
        image_data = get_image_from_path(tempdir)
        return image_data
    else:
        return None


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


w, h = sg.Window.get_screen_size()
print('Window Size: (%d,%d)' % (w, h))

# if getattr(sys, 'frozen', False):
#     filepath = Path(os.path.join(sys._MEIPASS, "images/RH.png"))
#     image_data, im_height = get_image_from_path(filepath)
# else:
filepath = resource_path("images\\default.png")

if os.path.exists(filepath):
    image_data = get_image_from_path(filepath)
else:
    image_data = get_new_image_data()

layout = [[sg.Image(
    data=image_data,
    key='__IMAGE__',
    size=(w, h),
    pad=((0, 0), (0, 0)),
    background_color=TRANSPARENT_COLOR,
    right_click_menu=['&Right', ['!CrowdSimulator', '---', '&Select Image', '&Toggle Movable', '&Reset Position', 'E&xit']]
    )],
]

window = sg.Window('Window Title', layout,
                   location=(0, 0),
                   size=(w, h),
                   no_titlebar=True,
                   keep_on_top=True,
                   grab_anywhere=False,
                   background_color='black',
                   transparent_color=TRANSPARENT_COLOR
                   )

grab_status = False

while True:
    event, values = window.read()

    if event is None or event == 'Exit':
        break
    if event == 'Select Image':
        img_data = get_new_image_data()
        window['__IMAGE__'].Update(data=img_data)
        # currdir = os.getcwd()
        # tempdir = filedialog.askopenfilename(parent=root, initialdir=currdir, title='Please select a directory')
        # if os.path.exists(tempdir):
        #     image_data = get_image_from_path(tempdir)
        #     window['__IMAGE__'].Update(data=image_data)
    elif event == 'Toggle Movable':
        if grab_status:
            window.GrabAnyWhereOff()
        else:
            window.GrabAnyWhereOn()
        grab_status = not grab_status
    elif event == 'Reset Position':
        window.move(0, 0)
