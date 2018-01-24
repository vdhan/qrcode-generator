"""
QR Code Generator.
Copyright (C) 2018 Vũ Đắc Hoàng Ân.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import argparse

from PIL import Image
from qrcode import QRCode, ERROR_CORRECT_H


def create_qrcode(params):
    qr = QRCode(error_correction=ERROR_CORRECT_H, box_size=params.size, border=params.border)
    qr.add_data(params.content)
    qr.make()

    output = params.output
    img = qr.make_image(fill_color=params.background, back_color=params.foreground)
    img.save(output)
    print('Created file: {}'.format(output))


def embed_image(params):
    qrcode = params.qrcode
    image = params.image
    output = params.output
    size = params.size

    try:
        Image.open(qrcode).verify()
    except Exception:
        print('Image is not found, invalid or corrupted: {}'.format(qrcode))
    else:
        try:
            Image.open(image).verify()
        except Exception:
            print('Image is not found, invalid or corrupted: {}'.format(image))
        else:
            img = Image.open(qrcode)
            img = img.convert('RGBA')
            img_w, img_h = img.size

            logo = Image.open(image)
            logo_w, logo_h = logo.size
            if logo_w >= logo_h:
                width = size
                height = logo_h * size // logo_w
            else:
                height = size
                width = logo_w * size // logo_h

            x1 = (img_w - width) // 2
            x2 = x1 + width
            y1 = (img_h - height) // 2
            y2 = y1 + height

            box = (x1, y1, x2, y2)
            region = logo.resize((width, height))
            img.paste(region, box)
            img.save(output)
            print('Created file: {}'.format(output))


if __name__ == '__main__':
    parser = argparse.ArgumentParser('qrcode-generator', description='QR Code Generator')
    subparsers = parser.add_subparsers(title='commands', dest='command')

    create_parser = subparsers.add_parser('create', help='Generate QR Code')
    create_parser.add_argument('content', help='QR Code content')
    create_parser.add_argument('-b', '--border', help='QR Code image border (default 1)', default=1, type=int)
    create_parser.add_argument('-f', '--foreground', help='foreground color', default='#000')
    create_parser.add_argument('-g', '--background', help='background color', default='#fff')
    create_parser.add_argument('-o', '--output', help='output file', default='output.png')
    create_parser.add_argument('-s', '--size', help='box size (default 10)', default=10, type=int)

    embed_parser = subparsers.add_parser('embed', help='Embed image to QR Code')
    embed_parser.add_argument('image', help='embedded image')
    embed_parser.add_argument('qrcode', help='QR Code')
    embed_parser.add_argument('-o', '--output', help='output file', default='output.png')
    embed_parser.add_argument('-s', '--size', help='embedded size (px)', default=100, type=int)

    parser.add_argument('-V', '--version', action='version', version='1.0')
    args = parser.parse_args()
    command = args.command
    if command == 'create':
        create_qrcode(args)
    elif command == 'embed':
        embed_image(args)
    else:
        parser.print_help()
