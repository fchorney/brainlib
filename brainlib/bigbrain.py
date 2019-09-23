import textwrap

from os.path import join
from PIL import Image, ImageFont, ImageDraw
from imgurpython import ImgurClient


def bigbrain(
    messages,
    imgdir="./",
    bgcolour=[255, 255, 255, 255],
    fontpath="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    fontsize=22,
    fontcolour=[0, 0, 0, 255],
    wraplength=20,
    heightpadding=5,
    client_id=None,
    client_secret=None,
    upload=False,
):

    # Make sure messages is the correct length
    if len(messages) > 10:
        print("Messages must be 10 items or less")
        return None, None

    # If upload is set, make sure we have client id and secret
    if upload and (client_id is None or client_secret is None):
        print("Must supply client_id and client_secret if upload is set")
        return None, None

    # Set image paths
    brain_img_path = join(imgdir, "10-brain-template.png")
    output_img_path = join(imgdir, "new-brain.png")

    # Open up Base Image
    base_img = Image.open(brain_img_path)

    # Grab Font
    font = ImageFont.truetype(fontpath, fontsize)

    # Panel Config: X, Y, Width, Height
    configs = [
        [4, 2, 414, 294],
        [4, 304, 414, 298],
        [4, 612, 412, 268],
        [4, 895, 413, 304],
        [4, 1214, 413, 368],
        [4, 1600, 416, 364],
        [4, 1983, 416, 430],
        [4, 2440, 418, 492],
        [4, 2960, 418, 585],
        [4, 3575, 418, 253],
    ]

    # Cutoffs
    cutoffs = [299, 607, 885, 1204, 1592, 1974, 2430, 2950, 3565]

    for msg, config in zip(messages, configs):
        # Grab image config
        X, Y, MAX_W, MAX_H = config

        # Create a new image
        img = Image.new("RGB", (MAX_W, MAX_H), tuple(bgcolour))
        draw = ImageDraw.Draw(img)

        # Separate our message with textwrap
        wrapped_msg = textwrap.wrap(msg, width=wraplength)

        # Determine message height
        line_count = len(wrapped_msg)
        message_height = (fontsize * line_count) + (heightpadding * (line_count - 1))

        # Vertically allign the message to be in the centre
        current_height = ((MAX_H - message_height) / 2) - (fontsize / 2)

        for line in wrapped_msg:
            w, h = font.getsize(line)
            draw.text(
                ((MAX_W - w) / 2, current_height), line, tuple(fontcolour), font=font
            )
            current_height += h + heightpadding

        # Paste image into base image
        base_img.paste(img, (X, Y))

    # Crop the image if necessary,
    # and save it
    msg_length = len(messages)
    if msg_length < 10:
        result_img = base_img.crop((0, 0, 862, cutoffs[msg_length - 1]))
        result_img.save(output_img_path)
    else:
        base_img.save(output_img_path)

    # Upload to imgur if flags have been set
    if upload:
        imgur_client = ImgurClient(client_id, client_secret)
        data = imgur_client.upload_from_path(output_img_path, anon=True)
        imgur_link = data["link"]

        # Return the output image path, and the imgur link
        return output_img_path, imgur_link

    # Return the output image path
    return output_img_path, None
