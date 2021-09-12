#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import mediapipe as mp
import utils


class Game:
    """Класс представляет собой одну игру"""

    def __init__(self, window_name="LOL", penis='penis.png'):
        # Сохраняем название нашего окна
        self.window_name = window_name

        # Загружаем пенис в память
        self.penis = cv2.imread('penis.png', cv2.IMREAD_UNCHANGED)

        # Загружаем отслеживателя рук
        self.hands_handler = mp.solutions.hands.Hands(
            min_detection_confidence=0.75,
            min_tracking_confidence=0.75)

    def __window_to_full_screen(self):
        """Создаём окно во весь экран"""
        cv2.namedWindow(self.window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(
            self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    def get_hands(self, img):
        """Определяет руки на изображении"""
        # Конвертируем изображение из схемы BGR в RGB
        # Нейроная сеть натренирована на схеме RGB
        # Иначе руки не определятся
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Для повышения производительности при необходимости помечаем
        # изображение как недоступное для записи
        img.flags.writeable = False

        # Находим руки на изображении
        hands = self.hands_handler.process(img)

        # Возвращаем все найденные руки на изображении
        return hands

    def draw_penis(self, img, hand, size=60):
        """Рисует член на картинке"""
        # Если размеры стандартной картинки
        # не соответствуют указанному
        if self.penis.shape[:2] != (size, size):
            # Приводим картику члена к нужному размеру
            self.penis = cv2.resize(self.penis, (size, size))

        # Получаем размеры основного изображения
        # На котором рисуются члены
        hight, width, _ = img.shape

        # получаем кончик СРЕДНЕГО пальца на руке
        ft = hand.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP]

        # Приводим относительные координаты к глобальным
        x = round(ft.x * width)
        y = round(ft.y * hight)

        # Получаем координаты точки, с которой будем рисовать член
        pos = (y-size//2, x-size//2)

        if (pos[0] >= 0 and pos[0] < hight and
            pos[1] >= 0 and pos[1] < width and
            pos[0] + size >= 0 and pos[0] + size < hight and
                pos[1] + size >= 0 and pos[1] + size < width):
            # Рисуем член из этой точки
            img = utils.overlayPNG(img, self.penis, pos)

        # Возвращаем изменённое, опороченное нами изображение
        return img

    def update(self, img):
        """Выполняется при каждом обновлении картинки с камеры"""
        # Отражаем изображение по горизонтали - тк оно снимается вебкамерой компьютера
        # Нужно для коректоного отслеживания рук
        img = cv2.flip(img, 1)

        # Получаем руки с изображения
        hands = self.get_hands(img)

        if hands.multi_hand_landmarks:
            for hand in hands.multi_hand_landmarks:
                img = self.draw_penis(img, hand)

        # Выводим изображение c членами на экран
        cv2.imshow(self.window_name, img)

    def mainloop(self, cap: cv2.VideoCapture):
        """Основной цикл работы программы"""
        while cap.isOpened():

            # Получаем изображение с камеры
            succes, img = cap.read()
            if not succes:
                print("Игнорируем пустой кадр с камеры")
                continue

            # Выполняем обработку каждоо кадра с картинки
            self.update(img)

            # Закрываем программу при нажати клавиши Esc
            if cv2.waitKey(1) & 0xFF == 27:
                break
        # Закрываем поток видео с камеры
        cap.release()

    def start(self):
        """Запуск работы программы"""
        # Создаём окно во весь экран
        self.__window_to_full_screen()
        # Подключаем камеру
        cap = cv2.VideoCapture(0)
        # Задаём размеры изображения
        cap.set(3, 1920)
        cap.set(4, 1080)

        # Запускаем основной цикл программы
        self.mainloop(cap)


def main():
    """Основная программа"""
    # Создаём новую игру
    game = Game()
    # Запускаем игру
    game.start()


# Стартовая точка программы
if __name__ == "__main__":
    main()
