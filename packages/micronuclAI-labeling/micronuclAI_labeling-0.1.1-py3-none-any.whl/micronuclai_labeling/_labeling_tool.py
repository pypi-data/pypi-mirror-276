# labeling_tool.py
import PySimpleGUI as sg
from PIL import Image
from os.path import dirname, exists
from pathlib import Path
from matplotlib import colormaps as cm
from mask2bbox import BBoxes
import numpy as np
import io


def array2image(array, cmap="gray", size=(256, 256)):
    # https: // stackoverflow.com / questions / 10965417 / how - to - convert - a - numpy - array - to - pil - image - applying - matplotlib - colormap
    image = Image.fromarray(np.uint8(cm.get_cmap(cmap)(array) * 255))
    image = image.resize(size)
    byteIO = io.BytesIO()
    image.save(byteIO, format='PNG')
    byteArr = byteIO.getvalue()
    return byteArr


def updaterf(window, to_show, currentline, filelist):
    window["-IMAGE1-"].update(data=array2image(to_show, cmap="gray"))
    window["-IMAGE2-"].update(data=array2image(to_show, cmap="gray_r"))
    window["-IMAGE3-"].update(data=array2image(to_show, cmap="turbo"))
    window["-IMAGE4-"].update(data=array2image(to_show, cmap="prism"))
    window["-COUNT-"].update(f"{currentline}/{len(filelist)}")


def gui(args):
    # Constants and variables
    QT_ENTER_KEY1 = 'special 16777220'
    QT_ENTER_KEY2 = 'special 16777221'

    # Create output folder if it doesn't exist
    Path(dirname(args.out)).mkdir(parents=True, exist_ok=True)

    # Create layout
    layout = [
        [sg.Text("Press KEYs from 0-9 to specify the number of micronuclei on the image press r to go back one image",
                 key="-TEXT-")],

        [[sg.Image(key="-IMAGE1-"), sg.Image(key="-IMAGE2-")],
         [sg.Image(key="-IMAGE3-"), sg.Image(key="-IMAGE4-")]],

        [sg.Text("", key="-COUNT-")],

        [sg.Button("UNDERSTOOD", key="-OK-")]
    ]

    # Create window
    window = sg.Window(title="Labeling tool", layout=layout, return_keyboard_events=True, finalize=True)

    # Create output file if it does not exist
    if not exists(args.out):
        FILE = open(args.out, "w")
        currentline = 0
    else:
        # Open once to check what was the last line
        with open(args.out, "r") as F:
            currentline = len(F.readlines())

        #  Open in append mode.

    # Read in mask and image using mask2bbox
    boxes = BBoxes.from_mask(args.mask, args.input)
    rf = boxes.calculate_resizing_factor(0.6, 256)

    # Create list of all files
    boxes = boxes.expand(30)


    # Create a list of the output file
    filelist = list(boxes.idx())
    if currentline == 0:
        output_file_list = ["image,count,label"]
    else:
        output_file_list = []

    # Create an event loop
    while True:
        # Read the window
        event, values = window.read()

        # Close window
        if event == sg.WIN_CLOSED:
            break

        elif event in "0123456789":
            output_file_list.append(f"{filelist[currentline]+1},{event},{int(int(event)>0)}")

            with open(args.out, "w") as FILE:
                for f in output_file_list:
                    print(f, file=FILE)

            currentline += 1
            if currentline >= len(filelist):
                break
            to_show = boxes.grab_pixels_from(currentline, source="image", resize_factor=rf[currentline], size=(256, 256))
            updaterf(window, to_show, currentline, filelist)

        elif event in "b":
            output_file_list.append(f"{filelist[currentline]+1},{event},{0}")

            with open(args.out, "w") as FILE:
                for f in output_file_list:
                    print(f, file=FILE)

            currentline += 1
            if currentline >= len(filelist):
                break
            to_show = boxes.grab_pixels_from(currentline, source="image", resize_factor=rf[currentline], size=(256, 256))
            updaterf(window, to_show, currentline, filelist)

        elif event == "r":
            currentline -= 1
            to_show = boxes.grab_pixels_from(currentline, source="image", resize_factor=rf[currentline], size=(256, 256))
            updaterf(window, to_show, currentline, filelist)
            output_file_list.pop()

        elif event == "-OK-":
            to_show = boxes.grab_pixels_from(currentline, source="image", resize_factor=rf[currentline], size=(256, 256))
            updaterf(window, to_show, currentline, filelist)
            window["-OK-"].update(visible=False)

    window.close()