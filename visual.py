from math import *
import numpy as np


class Visual:
    """
    Клас, призначений для взаємодії з користувачем у графічному інтерфейсі

    ---

    Атрибути
    --------
    windowGiven : MainWindow
        Вікно, за яким відбуватиметься взаємодія.

    Методи
    ------
    showDefEquation(i):
        Виводить у вікно формат рівнянь відповідно до того, який обраний в випадному списку.

    setGrids(i)
        Виводить на екран потрібні поля для введення коефіцієнтів і змінні біля них.

    plotEq(check, xs, ys)
        Будує графік розв'язаної системи і виводить його на екран.
    """

    def __init__(self, windowGiven):
        """
        Конструктор класу.

        Аргументи
        ---------
            windowGiven  : MainWindow
                Вікно, з яким буде взаємодія
        """

        self.window = windowGiven

    def showDefEquation(self, i):
        """
        Виводить у вікно формат рівнянь відповідно до того, який обраний в випадному списку.

        Аргументи
        ---------
        i    : int
            Індекс обраного типу рівнянь у випадному списку.

        Повертає
        --------
        None
        """

        text = "Обраний формат рівнянь:\n"
        if i == 1:
            text += "{a}x₁⁵ - {b}x₂² + {c} = 0 \n {d}x₁³ + {e}x₁² + {f}x₂³ = 0"
        elif i == 2:
            text += "{a}*ctg³(x₁) + {b}*sin({c}x₂) = 0 \n {d}*cos(x₁) - {e}*tg(x₂) = 0"
        elif i == 3:
            text += "{a}*log₂(x₁) + {b}*cos(x₂) - {c} = 0 \n {d}*2ˣ₁ + {e}*log₂(x₂) = 0"

        # Задаємо текст відповідному текстовому полю
        self.window.equations.setText(text)

        # Викликаємо наступний метод
        self.setGrids(i)

    def setGrids(self, i):
        """
        Виводить на екран потрібні поля для введення коефіцієнтів і змінні біля них.

        Аргументи
        ---------
        i    : int
            Індекс обраного типу рівнянь у випадному списку.

        Повертає
        --------
        None
        """

        # У тригон. і трансц. рівняннях нема 6-го коефіцієнту, тому приховуємо його.
        if i == 1:
            self.window.labels1[0].setText("x₁⁵ - ")
            self.window.labels1[1].setText("x₂² + ")
            self.window.labels1[2].setText(" = 0")
            self.window.labels2[0].setText("x₁³ + ")
            self.window.labels2[1].setText("x₁² + ")
            self.window.polya2[2].show()
            self.window.labels2[2].show()
            self.window.labels2[2].setText("x₂³ = 0")
        elif i == 2:
            self.window.labels1[0].setText("ctg³(x₁) + ")
            self.window.labels1[1].setText("*sin(")
            self.window.labels1[2].setText("x₂) = 0")
            self.window.labels2[0].setText("cos(x₁) - ")
            self.window.labels2[1].setText("tg(x₂) = 0")
            self.window.polya2[2].hide()
            self.window.labels2[2].hide()
        elif i == 3:
            self.window.labels1[0].setText("log₂(x₁) + ")
            self.window.labels1[1].setText("cos(x₂) -")
            self.window.labels1[2].setText(" = 0")
            self.window.labels2[0].setText("2ˣ₁ + ")
            self.window.labels2[1].setText("log₂(x₂) = 0")
            self.window.polya2[2].hide()
            self.window.labels2[2].hide()

    def plotEq(self, check, xs, ys):
        """
        Будує графік розв'язаної системи і виводить його на екран.

        Аргументи
        ---------
        check    : int
            Показує, розв'язано окремим випадком чи загальним (ітераційно).
        xs   : float
            Перший розв'язок системи.
        ys   : float
            Другий розв'язок системи.

        Повертає
        --------
        None
        """

        # Виділяємо коефіцієнти рівнянь
        a, b, c = self.window.equation1.parameters
        d, e, f = self.window.equation2.parameters
        x11, x21, x12, x22 = [], [], [], []

        '''Якщо розв'язано ітераційно, то на проміжку
        10 в обидва боки від розв'язку шукаємо значення функцій і
        збіерігаємо їх в окремі списки'''
        '''Якщо ж розв'язано неітераційно, то перевіряємо, 
        чи має система числовий розв'язок:
        якщо так, то маємо точку перетину на графіку'''

        if check == 0:
            x21 = np.arange(int(ys) - 10, 10 + int(ys),0.1)
            x12 = np.arange(int(xs) - 10, 10 + int(xs),0.01)
            if self.window.equation1.index == 1:
                for i in x21:
                    w = -1 if ((b * i ** 2 - c) / a) < 0 else 1
                    x11.append(w * abs((b * i ** 2 - c) / a) ** (1 / 5))
                for i in x12:
                    w = -1 if ((-d * i ** 3 - e * i ** 2) / f) < 0 else 1
                    x22.append(w * abs((-d * i ** 3 - e * i ** 2) / f) ** (1 / 3))
            elif self.window.equation1.index == 2:
                if 0 in x21:
                    x21.remove(0)
                for i in x21:
                    print(i)
                    if i>int(ys)+10 or i<int(ys)-10:
                        x21.remove(i)
                    else:
                        w = -1 if (-b * sin(c * i) / a) < 0 else 1
                        x11.append(1/(atan((w * abs(-b * sin(c * i) / a) ** (1 / 3)))))
                x22 = [atan((d * cos(i)) / e) for i in x12]
            elif self.window.equation1.index == 3:
                x11 = [2 ** ((c - b * cos(i)) / a) for i in x21]
                x22 = [2 ** ((-d * 2 ** i) / e) for i in x12]
        elif type(xs) == int or type(xs) == float and type(ys) == int or type(ys) == float:
            x11, x21 = xs, ys
            x12, x22 = xs, ys
        self.window.figure.clear()

        '''Якщо розв'язок існує, то малюємо окремо графіки і позначаємо
        окремо їх точку перетину'''

        if x11 != []:
            ax = self.window.figure.add_subplot(111)
            labels = (self.window.filledEq.text()[17:]).split("\n")
            ax.plot(x11, x21, label=labels[0])
            ax.plot(x12, x22, label=labels[1])
            ax.plot(xs, ys, marker="o")
            ax.grid()
            ax.legend()

        self.window.canvas.draw()
