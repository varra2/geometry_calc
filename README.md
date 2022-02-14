"# geometry_calc"

**Начальные требования**

Наличие python (тестировалось на версии 3.8) и pip

**Установка**


* Скачайте репозиторий \

* Перейдите в папку с проектом и создайте виртуальную среду
    * python -m venv .venv
    * Активируйте среду

    В Windows:

    * .venv\Scripts\activate

	В Linux:

    * source .venv/bin/activate

* Установите необходимые для работы программы модули
    * pip install -r requirements.txt

**Использование**

Программа запускает веб-приложение "калькулятор" по локальному адресу http://localhost:8000

Команда запуска:

* python manage.py runserver

Калькулятор запрашивает параметры фигуры, выдаёт изображение и вычисляет, в зависимости от выбранного типа фигуры, такие свойства как периметр (все фигуры или основания), площадь (всей фигуры или основания), высота (для пирамиды так же высота стороны - апофема, может посчитать длину стороны трапеции, сторон ромба и объём. Поддерживаются такие фигуры, как круг, квадрат, прямоугольник, треугольник, трапеция, ромб, сфера, куб, параллелепипед, пирамида, цилиндр и конус.
Выберите фигуру среди предложенных вверху, введите запрашиваемые параметры и нажмите "submit". Внизу под рисунком вы надёте расчитанные значения или сообщение об ошибке, в случае, если программе не удалось построить фигуру по предложенным данным.

Приложение выполнено в фремворке django, для отрисовки фигур использована библиотека matplotlib.
