class Equation:
    """
    Клас, призначений для зберігання даних, пов'язаних з рівняннями.

    ---

    Атрибути
    --------

    index : int
        Індекс, що відповідає за тип рівнянь.
    parameters  : float[]
        Список коефіцієнтів у цьому рівнянні.
    meth  : int
        Індекс, що відповідає за метод розв'язання.
    prec    : float
        Точність розв'язання.

    Методи
    ------
    """

    def __init__(self, index, parameter, method, precision):
        """
        Конструктор класу.

        Аргументи
        ---------
        index : int
            Індекс, що відповідає за тип рівнянь.
        parameter  : float[]
            Список коефіцієнтів у цьому рівнянні.
        method  : int
            Індекс, що відповідає за метод розв'язання.
        precision    : float
            Точність розв'язання.
        """

        self.index = index
        self.parameters = parameter
        self.meth = method
        self.prec = precision
