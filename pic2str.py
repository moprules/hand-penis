#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import base64
import os
import numpy as np
import cv2


def pic2str(pic_path):
    """Преобразует изображение в строчное представление"""
    # имя картинки
    pic_name, ext = os.path.splitext(os.path.basename(pic_path))
    img = cv2.imread(pic_path, cv2.IMREAD_UNCHANGED)
    img_encode = cv2.imencode(ext, img)[1]
    pic_str = f"\n{pic_name}_str = {base64.b64encode(img_encode.tobytes())}\n"

    # Записываем в python файл переменную с полученным значением
    with open('images.py', 'a') as f:
        f.write(pic_str)
        pic_data = f"{pic_name}_img = str2data({pic_name}_str)\n"
        f.write(pic_data)


if __name__ == '__main__':
    pic2str('penis.png')
