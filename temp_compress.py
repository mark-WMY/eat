#!/usr/bin/env python3
from PIL import Image
import os

img = Image.open('img/bg.jpg')
img.save('img/bg.jpg', quality=80, optimize=True)
print('bg.jpg: %.1f KB' % (os.path.getsize('img/bg.jpg') / 1024))

img = Image.open('img/logo.png')
img.save('img/logo.png', optimize=True)
print('logo.png: %.1f KB' % (os.path.getsize('img/logo.png') / 1024))
