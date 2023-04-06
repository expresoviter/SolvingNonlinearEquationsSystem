from math import *
from PyQt6.QtWidgets import *
from equation import *


class Solution:
    """
    Клас, призначений для розв'язування введеної системи рівнянь.

    ---

    Атрибути
    --------
    window : MainWindow
        Вікно, за яким відбуватиметься взаємодія з інтерфейсом.
    startY  : float
        Початкове наближення другої змінної.
    startX  : float
        Початкове наближення першої змінної.

    Методи
    ------
    getCoeffs()
        Зчитує усі введені значення, створює об'єкти рівнянь, викликає подальші дії:
        розв'язання, будування графіку, запис у файл.

    convergence(det, x, y)
        Обраховує визначник матриці Якобі для поточної ітерації і число, що відповідає
        за збіжність ітераційного процесу.

    checkZero()
        Перевіряє, чи не потрібно обчислити систему окремо від загального ітераційного процесу,
        і, якщо так, то обчислює. Інакше переходить до звичайного розв'язання.

    solveIter()
        Розв'язує систему ітеративно відповідно до обраного методу.

    messageButton(reply)
        Якщо обрано, записує розв'язок системи у файл

    iterAlg(equation2, yl, start)
        Обчислює ітеративно змінну в кубічному рівнянні у випадку, коли інша змінна відома.
    """

    def __init__(self, windowGiven):
        """
        Конструктор класу.

        Аргументи
        ---------
            немає.
        """

        self.window = windowGiven
        self.startY = None
        self.startX = None

    def getCoeffs(self):
        """
        Зчитує усі введені значення, створює об'єкти рівнянь, викликає подальші дії:
        розв'язання, будування графіку, запис у файл.

        Аргументи
        --------
            немає.

        Повертає
        --------
        None
        """

        self.window.filledEq.setText("")
        try:
            ind = self.window.comboType.currentIndex()
            meth = self.window.method.currentIndex()
            prec = float(self.window.precision.displayText())
            a = [float(self.window.polya1[i].displayText()) for i in range(3)]
            b = [self.window.polya2[i].displayText() for i in range(3)]

            self.startX, self.startY = float(self.window.startX.displayText()), float(self.window.startY.displayText())
            if ind == 1:
                b = [float(i) for i in b]
            elif ind != 0:
                b = [float(i) for i in b[:2]]
                b.append(0)
            self.window.equation1, self.window.equation2 = Equation(ind, a, meth, prec), Equation(ind, b, meth, prec)
            s = self.window.equations.text()
            s = s.replace("{a}", str(self.window.equation1.parameters[0]))
            s = s.replace("{b}", str(self.window.equation1.parameters[1]))
            s = s.replace("{c}", str(self.window.equation1.parameters[2]))
            s = s.replace("{d}", str(self.window.equation2.parameters[0]))
            s = s.replace("{e}", str(self.window.equation2.parameters[1]))
            if ind == 1:
                s = s.replace("{f}", str(self.window.equation2.parameters[2]))
            self.window.filledEq.setText("Введена система:\n" + s[24:])
            check, x1, x2, press = self.checkZero()
            self.window.windowView.plotEq(check, x1, x2)
            reply = self.window.msg.exec()
            self.messageButton(reply)
        except (ValueError, TypeError):
            self.window.filledEq.setText(
                "Помилка. Переконайтеся, що: \n\t-введені коефіцієнти, початкові наближення та точність - це цілі або "
                "дійсні числа у форматі '0.0' .")
        except ZeroDivisionError:
            self.window.filledEq.setText("Помилка. Ділення на 0.")
        except OverflowError:
            self.window.filledEq.setText("Помилка переповнення. Спробуйте зменшити значення.")

    def convergence(self, det, x, y):
        """
        Обраховує визначник матриці Якобі для поточної ітерації і число, що відповідає
        за збіжність ітераційного процесу.

        Аргументи
        --------
            det    : float
                Число, що відповідає за збіжність, обчислене на попередній ітерації.
            x    : float
                Поточне наближення для першої змінної.
            y    : float
                Поточне наближення для другої змінної.

        Повертає
        --------
            temp (det)    : float
                Обчислене число, що відповідає за збіжність.
            a    : bool
                Вираз, що показує, збіжний процес (True) чи ні (False) на даній ітерації.
        """

        a, b, c = self.window.equation1.parameters
        d, e, f = self.window.equation2.parameters
        try:
            if self.window.equation1.index == 1:
                w = -1 if ((b * y ** 2 - c) / a) < 0 else 1
                temp = (2 * b * y) / (5 * w * (abs(a * (b * y ** 2 - c) ** 4) ** (1 / 5)))
                w = -1 if ((-d * x ** 3 - e * x ** 2) / f) < 0 else 1
                temp *= ((3 * d * x + 2 * e) * w * abs(((-d * x ** 3) - e * x ** 2) / f) ** (1 / 3)) / (
                        3 * d * x ** 2 + 3 * e * x)
            elif self.window.equation1.index == 2:
                w = -1 if (b * sin(c * y) / a) < 0 else 1
                temp = (a * b * c * cos(c * y)) / (
                        (3 * b ** 2 * sin(c * y) ** 2 + 3 * a ** 2) * atan(w * abs(b * sin(c * y)) / a) ** (-2 / 3))
                temp *= ((-e * d * sin(x)) / (e ** 2 + d ** 2 + (cos(x)) ** 2))
            else:
                temp = 2 ** ((c - b * cos(y)) / a) * log(2) * (b * sin(y) / a)
                temp *= (2 ** (x - (d * 2 ** x / e)) * log(2) ** 2 * (-d / e))
            temp *= -1
            temp *= det
            if abs(temp) <= abs(det):
                return temp, True
            else:
                return temp, False

        except:
            return det, True

    def checkZero(self):
        """
        Перевіряє, чи не потрібно обчислити систему окремо від загального ітераційного процесу,
        і, якщо так, то обчислює. Інакше переходить до звичайного розв'язання.

        Аргументи
        ---------
            немає.

        Повертає
        --------
            1    : const int
                Число, що означає, що розв'язано окремо від загального методу.
            sol[0]   : float
                Перший розв'язок системи.
            sol[1]   : float
                Другий розв'язок системи.
            0    : const int
                Точність розв'язання, окремим методом дорівнює 0.
        """

        a, b, c = self.window.equation1.parameters
        d, e, f = self.window.equation2.parameters
        sol = [0, 0]
        check = 0
        if self.window.equation1.index == 1:
            if a == 0:
                check = 1
                if b == 0:
                    if c == 0:
                        sol = ["b", "b"]
                    else:
                        sol = ["0", "0"]
                else:
                    if c / b >= 0:
                        x2 = sqrt(c / b)
                        x1 = self.iterAlg(self.window.equation2, x2, self.startX)
                        sol = [x1, x2]
                    else:
                        sol = ["0", "0"]
            if check == 0:
                if f == 0:
                    check = 1
                    if e == 0 and d == 0:
                        sol = ["b", "b"]
                    else:
                        if e == 0 and d != 0 or e != 0 and d == 0:
                            sol = [0, 0]
                        else:
                            sol = [self.iterAlg(self.window.equation2, 0, self.startX), 0]
                            try:
                                if (a * sol[0] ** 5 + c) / b >= 0:
                                    sol[1] = sqrt((a * sol[0] ** 5 + c) / b)
                                else:
                                    sol[1] = "0"
                            except TypeError:
                                sol[1] = "0"
        elif self.window.equation1.index == 2:
            if a == 0:
                check = 1
                if b == 0 or b != 0 and c == 0:
                    sol = ["b", "b"]
                else:
                    sol = [pi / 2, 0]
            if check == 0:
                if e == 0:
                    check = 1
                    if d == 0:
                        sol = ["b", "b"]
                    else:
                        sol = [pi / 2, 0]
        elif self.window.equation1.index == 3:
            if a == 0:
                check = 1
                if b == 0:
                    if c == 0:
                        sol = ["b", "b"]
                    else:
                        sol = ["0", "0"]
                else:
                    if -1 <= c / b <= 1:
                        sol = [0, acos(c / b)]
                        if sol[1] > 0 and -e * log2(sol[1]) / d > 0:
                            sol[0] = log2(-e * log2(sol[1]) / d)
                    else:
                        sol = ["0", "0"]
            if check == 0:
                if e == 0:
                    check = 1
                    if d == 0:
                        sol = ["b", "b"]
                    else:
                        sol = ["0", "0"]
        if check == 1:
            if sol[0] == "0" or sol[1] == "0":
                text = "Система розв'язків не має"
            elif sol[0] != "b" and sol[1] != "b":
                text = "Результат: x₁ =" + str(sol[0]) + ", x₂ =" + str(sol[1]) + ", точність = 0."
            else:
                text = "Система має безліч розв'язків"
            self.window.iterations.label.setText(text)
            return 1, sol[0], sol[1], 0
        else:
            return self.solveIter()

    def solveIter(self):
        """
        Розв'язує систему ітеративно відповідно до обраного методу.

        Аргументи
        ---------
            немає.

        Повертає
        --------
            0    : const int
                Число, що означає, що розв'язано ітеративним методом.
            x1[0]   : float
                Перший розв'язок системи.
            x2[0]   : float
                Другий розв'язок системи.
            precision    : float
                Точність розв'язання.
        """

        text = ""
        precision = self.window.equation1.prec + 1
        a, b, c = self.window.equation1.parameters
        d, e, f = self.window.equation2.parameters
        x1, x2 = [self.startX, 0], [self.startY, 0]
        k = 0
        det, boo = self.convergence(1, x1[0], x2[0])
        el = self.window.equation1.meth
        while precision >= abs(self.window.equation1.prec) and k <= 200:
            if self.window.equation1.index == 1:
                w = -1 if ((b * x2[0] ** 2 - c) / a) < 0 else 1
                x1[1] = w * abs((b * x2[0] ** 2 - c) / a) ** (1 / 5)
                w = -1 if ((-d * x1[el] ** 3 - e * x1[el] ** 2) / f) < 0 else 1
                x2[1] = w * abs((-d * x1[el] ** 3 - e * x1[el] ** 2) / f) ** (1 / 3)
            elif self.window.equation1.index == 2:
                if k == 0:
                    x1[1] = pi / 2
                else:
                    w = -1 if (-b * sin(c * x2[0]) / a) < 0 else 1
                    x1[1] = atan(1 / (w * abs(-b * sin(c * x2[0]) / a) ** (1 / 3)))
                x2[1] = atan((d * cos(x1[el])) / e)
            elif self.window.equation1.index == 3:
                x1[1] = 2 ** ((c - b * cos(x2[0])) / a)
                x2[1] = 2 ** ((-d * 2 ** x1[el]) / e)
            text += (str(k) + "-a ітерація: x₁ = " + str(x1[0]) + ", x₂ = " + str(x2[0]) + "\n")
            self.window.iterations.label.setText(text)
            precision = max(abs(x1[1] - x1[0]), abs(x2[1] - x2[0]))
            x1[0], x2[0] = x1[1], x2[1]
            det, boo = self.convergence(det, x1[0], x2[0])
            if not boo:
                kin = "Процес не збіжний, неможливо знайти розв'язок."
                break
            k += 1

        if boo:
            kin = ("Кінцевий результат: x₁ = " + str(x1[0]) + ", x₂ = " + str(x2[0]) + ", precision = " + str(
                precision))
        text += kin
        self.window.iterations.label.setText(text)
        return 0, x1[0], x2[0], precision

    def messageButton(self, reply):
        """
        Якщо обрано, записує розв'язок системи у файл

        Аргументи
        ---------
        reply    : QMessageBox.StandartButton
            Обрана кнопка у вікні запитання.

        Повертає
        --------
        None.
        """

        if reply == QMessageBox.StandardButton.Yes:
            text = self.window.filledEq.text()
            text += "\n\n"
            text += self.window.iterations.label.text()
            with open("solution.txt", "w", encoding="utf-8") as file:
                file.write(text)

    def iterAlg(self, equation2, yl, start):
        """
        Обчислює ітеративно змінну в кубічному рівнянні у випадку, коли інша змінна відома.

        Аргументи
        ---------
        equation2  : Equation
            Рівняння, яке треба розв'язати.
        yl   : float
            Друга змінна, вже відома.
        start    : float
            Початкове наближення для розв'язання.

        Повертає
        --------
            x    : float||string
                Значення обчисленої змінної.
        """

        d, c, f = equation2.parameters
        if d == 0:
            if e == 0:
                if f * yl ** 3 == 0:
                    return "b"
                else:
                    return "0"
            else:
                if (-f * yl ** 3) / e >= 0:
                    return sqrt((-f * yl ** 3) / e)
                else:
                    return "0"
        elif e == 0:
            w = -1 if (-f * yl ** 3) / d < 0 else 1
            return w * abs((f * yl ** 3) / d) ** (1 / 3)
        else:
            x = [start, 0]
            k = 0
            prec = equation2.prec + 1
            while prec > equation2.prec and k <= 100:
                w = -1 if (-f * yl ** 3 - e * x[0] ** 2) / d < 0 else 1
                x[1] = w * abs((-f * yl ** 3 - e * x[0] ** 2) / d) ** (1 / 3)
                prec = abs(x[1] - x[0])
                x[0] = x[1]
                k += 1
            return x[0]
