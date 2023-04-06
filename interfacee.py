from PyQt6.QtCore import *
from solution import *
from visual import *
from scrolllabel import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class MainWindow(QMainWindow):
    """
    Клас головного вікна програми.

    ---

    Атрибути
    --------
    equation1     : Equation
        Перше рівняння системи.
    equation2     : Equation
        Друге рівняння системи.
    greetLabel   : QLabel
        Текстове поле "Оберіть тип рівнянь"
    combotype   : QComboBox
        Випадний список для обрання типу рівнянь
    windowView  : Visual
        Атрибут для обробки взаємодії користувача з вікном.
    equations   : QLabel
        Текстове поле для виведення загального виду системи
    filledEq    : QLabel
        Текстове поле для виведення введеної системи
    method  : QComboBox
        Випадний список для обрання методу розв'язання
    precision   : QLineEdit
        Поле для введення точности розв'язання
    polya1  : QLineEdit[]
        Список полів для введення коефієцінтів 1 рівняння
    polya2  : QLineEdit[]
        Список полів для введення коефієцінтів 2 рівняння
    labels1  : QLabel[]
        Список текстових полів для змінних біля коефіцієнтів 1 рівняння
    labels2  : QLabel[]
        Список текстових полів для змінних біля коефіцієнтів 2 рівняння
    startX  : QLineEdit
        Поле для введення початкового наближення першої змінної
    startY  : QLineEdit
        Поле для введення початкового наближення другої змінної
    confirm : QPushButton
        Кнопка для розв'язання системи.
    equationSolve   : Solution
        Атрибут для розв'язання системи і взаємодії його з вікном
    iterations  : ScrollLabel
        Текстове поле з прокручуванням для виведення ітерацій й кінцевого розв'язку
    figure  : Figure
        Фігура, де буде намальований графік системи
    canvas  : FigureCanvas
        Віджет полотна, де буде розташований графік
    msg : QMessageBox
        Вікно з питанням про запис у файл

    Методи
    ------
    """

    def __init__(self):
        """
        Створює усі елементи вікна, розташовує їх, надає їм функціонал.
        
        Аргументи:
        ---------
            немає.
        """

        super().__init__()

        self.equation1 = None
        self.equation2 = None

        self.setWindowTitle("Системи нелінійних рівнянь")

        self.greetLabel = QLabel()
        self.greetLabel.setText("Оберіть тип рівнянь:")

        self.comboType = QComboBox()
        self.comboType.addItems(["Оберіть тип рівнянь", "Алгебраїчні", "Тригонометричні", "Трансцендентні"])
        self.windowView = Visual(self)

        # Під'єднуємо зміну обраного елементу в списку до виклику відповідного методу в класі Visual
        self.comboType.currentIndexChanged.connect(self.windowView.showDefEquation)

        self.equations = QLabel()
        self.filledEq = QLabel()

        self.method = QComboBox()
        self.method.addItems(["Метод простих ітерацій (Якобі)", "Метод Гауса-Зейделя"])

        self.precision = QLineEdit()
        self.precision.setPlaceholderText("Введіть точність")

        self.polya1 = [QLineEdit() for i in range(3)]
        self.labels1 = [QLabel() for i in range(3)]
        self.polya2 = [QLineEdit() for i in range(3)]
        self.labels2 = [QLabel() for i in range(3)]

        self.startX = QLineEdit()
        self.startY = QLineEdit()
        self.startX.setPlaceholderText("Введіть початкове наближення для x₁")
        self.startY.setPlaceholderText("Введіть початкове наближення для x₂")

        self.confirm = QPushButton("Розв'язати")
        self.confirm.setCheckable(True)
        self.equationSolve = Solution(self)

        # Під'єднумо натискання кнопки до виклику відповідного методу в класі Solution
        self.confirm.clicked.connect(self.equationSolve.getCoeffs)

        self.iterations = ScrollLabel()

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Icon.Question)

        self.msg.setText("Записати розв'язок у файл?")
        self.msg.setInformativeText("Розв'язок буде записано у файл 'solution.txt' поточної теки")
        self.msg.setWindowTitle("Розв'язано.")
        self.msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        # Макети для того, щоб зібрати усі віджети так, як вони мають знаходитися
        outerLayout = QVBoxLayout()
        chooseLayout = QHBoxLayout()
        eqLayout = QGridLayout()
        gridLayout = QGridLayout()
        startLayout = QHBoxLayout()
        enterLayout = QVBoxLayout()
        downLayout = QHBoxLayout()

        chooseLayout.addWidget(self.greetLabel)
        chooseLayout.addWidget(self.comboType)

        eqLayout.addWidget(self.equations, 0, 0)
        eqLayout.addWidget(self.filledEq, 0, 1)
        eqLayout.addWidget(self.method, 1, 0)
        eqLayout.addWidget(self.precision, 1, 1)

        for i in range(3):
            gridLayout.addWidget(self.polya1[i], 0, i * 2)
            gridLayout.addWidget(self.labels1[i], 0, i * 2 + 1)
        for i in range(3):
            gridLayout.addWidget(self.polya2[i], 1, i * 2)
            gridLayout.addWidget(self.labels2[i], 1, i * 2 + 1)

        startLayout.addWidget(self.startX)
        startLayout.addWidget(self.startY)

        # Встановлюється фіксований розмір вікна
        self.setFixedSize(QSize(1000, 700))
        enterLayout.addLayout(chooseLayout)
        enterLayout.addLayout(eqLayout)
        enterLayout.addLayout(gridLayout)
        enterLayout.addLayout(startLayout)
        enterLayout.addWidget(self.confirm)
        downLayout.addWidget(self.iterations)
        downLayout.addWidget(self.canvas)
        outerLayout.addLayout(enterLayout)
        outerLayout.addLayout(downLayout)

        container = QWidget()
        container.setLayout(outerLayout)

        self.setCentralWidget(container)
