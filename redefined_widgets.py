from enum import Enum, auto
from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QSize
from PyQt5.QtGui import QFont, QColor, QPixmap, QIcon, QPainter, QPen, QEnterEvent
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy, \
    QPushButton, QDialog, QCalendarWidget


class Calendar(QCalendarWidget):
    def __init__(self, parent=None):
        super().__init__(parent)


# noinspection PyPep8Naming
class TitleBar(QWidget):
    windowMinimumed = pyqtSignal()
    windowMaximumed = pyqtSignal()
    windowNormaled = pyqtSignal()
    windowClosed = pyqtSignal()
    windowMoved = pyqtSignal(QPoint)

    # noinspection PyArgumentList
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.header: QWidget
        self.setAttribute(Qt.WA_StyledBackground)
        self._old_pos = None
        self.iconSize = 20

        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(palette.Window, QColor(240, 240, 240))
        self.setPalette(palette)

        self.iconLabel = QLabel()

        self.titleLabel = QLabel()
        self.titleLabel.setMargin(2)
        font = self.font() or QFont()
        font.setFamily('Webdings')

        self.buttonMinimum = QPushButton('0', font=font, objectName='buttonMinimum')
        self.buttonMinimum.clicked.connect(self.windowMinimumed.emit)
        self.buttonMaximum = QPushButton('1', font=font, objectName='buttonMaximum')
        self.buttonMaximum.clicked.connect(self.showMaximized)
        self.buttonClose = QPushButton('r', font=font, objectName='buttonClose')
        self.buttonClose.clicked.connect(self.windowClosed.emit)

        layout = QHBoxLayout(spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.iconLabel)
        layout.addWidget(self.titleLabel)

        layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.layout_custom_widget = QHBoxLayout()
        self.layout_custom_widget.setContentsMargins(0, 0, 0, 0)

        self.conn_state = QPushButton(objectName='buttonConnect')

        layout.addWidget(self.conn_state)
        layout.addWidget(self.buttonMinimum)
        layout.addWidget(self.buttonMaximum)
        layout.addWidget(self.buttonClose)
        self.setLayout(layout)
        self.show()
        self.setHeight()

    def showMaximized(self):
        if self.buttonMaximum.text() == '1':
            # Максимизировать
            self.buttonMaximum.setText('2')
            self.windowMaximumed.emit()
        else:  # Восстановить
            self.buttonMaximum.setText('1')
            self.windowNormaled.emit()

    def setHeight(self, height=38):
        """ Установка высоты строки заголовка """
        self.setMinimumHeight(height)
        self.setMaximumHeight(height)
        # Задайте размер правой кнопки  ?
        self.buttonMinimum.setMinimumSize(height, height)
        self.buttonMinimum.setMaximumSize(height, height)
        self.buttonMaximum.setMinimumSize(height, height)
        self.buttonMaximum.setMaximumSize(height, height)
        self.buttonClose.setMinimumSize(height, height)
        self.buttonClose.setMaximumSize(height, height)

    def setTitle(self, title):
        """ Установить заголовок """
        self.titleLabel.setText(title)

    def setIcon(self, icon):
        """ настройки значокa """
        self.iconLabel.setPixmap(icon.pixmap(self.iconSize, self.iconSize))

    def setIconSize(self, size):
        """ Установить размер значка """
        self.iconSize = size

    def enterEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        super().enterEvent(event)

    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        self.showMaximized()

    def mousePressEvent(self, event):
        """ Событие клика мыши """
        if event.button() == Qt.LeftButton:
            self._old_pos = event.pos()
        event.accept()

    def mouseReleaseEvent(self, event):
        """ Событие отказов мыши """
        self._old_pos = None
        event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self._old_pos:
            self.windowMoved.emit(self.mapToGlobal(event.pos() - self._old_pos))
        event.accept()


class Direction(Enum):
    LEFT = auto()
    TOP = auto()
    RIGHT = auto()
    BOTTOM = auto()

    LEFT_TOP = auto()
    RIGHT_TOP = auto()
    LEFT_BOTTOM = auto()
    RIGHT_BOTTOM = auto()


# noinspection PyPep8Naming
class Window(QDialog):
    def __init__(self, setup_ui):
        super().__init__()
        self.setup_ui = setup_ui
        setup_ui(self)
        self.MARGINS = 7
        self._old_pos = None
        self._direction = None
        self._widget = None
        self.header.conn_state.setIconSize(QSize(30, 30))

        self.setWindowFlags(Qt.FramelessWindowHint)

        self.window().setMouseTracking(True)

        self.header.windowMinimumed.connect(self.showMinimized)
        self.header.windowMaximumed.connect(self.showMaximized)
        self.header.windowNormaled.connect(self.showNormal)
        self.header.windowClosed.connect(self.close)
        self.header.windowMoved.connect(self.move)
        self.windowTitleChanged.connect(self.header.setTitle)
        self.windowIconChanged.connect(self.header.setIcon)

        self.header.resize(self.width(), self.header.height())
        self.header.setIcon(QIcon(QPixmap('System Files/Logo.png')))
        self.setWindowTitle('AREA: Student')

    def move(self, pos):
        if self.windowState() == Qt.WindowMaximized or self.windowState() == Qt.WindowFullScreen:
            # Максимизировать или полноэкранный режим не допускается
            return

        super().move(pos)

    def eventFilter(self, obj, event):
        """ Фильтр событий, используемый для решения мыши в других элементах
            управления и восстановления стандартного стиля мыши """
        if isinstance(event, QEnterEvent):
            self.setCursor(Qt.ArrowCursor)

        return super().eventFilter(obj, event)

    def paintEvent(self, event):
        """ Поскольку это полностью прозрачное фоновое окно, жесткая для поиска граница с
        прозрачностью 1 рисуется в событии перерисовывания, чтобы отрегулировать размер окна. """
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setPen(QPen(QColor(255, 255, 255, 1), 2 * self.MARGINS))
        painter.drawRect(self.rect())

    def mousePressEvent(self, event):
        """ Событие клика мыши """
        super().mousePressEvent(event)

        if event.button() == Qt.LeftButton:
            self._old_pos = event.pos()

    def mouseReleaseEvent(self, event):
        """ Событие отказов мыши """
        super().mouseReleaseEvent(event)

        self._old_pos = None
        self._direction = None

    def mouseMoveEvent(self, event):
        """ Событие перемещения мыши """
        super().mouseMoveEvent(event)

        pos = event.pos()
        x_pos, y_pos = pos.x(), pos.y()
        wm, hm = self.width() - self.MARGINS, self.height() - self.MARGINS

        if self.isMaximized() or self.isFullScreen():
            self._direction = None
            self.setCursor(Qt.ArrowCursor)
            return

        if event.buttons() == Qt.LeftButton and self._old_pos:
            self.resize_window(pos)
            return

        if x_pos <= self.MARGINS and y_pos <= self.MARGINS:
            # Верхний левый угол
            self._direction = Direction.LEFT_TOP
            self.setCursor(Qt.SizeFDiagCursor)

        elif wm <= x_pos <= self.width() and hm <= y_pos <= self.height():
            # Нижний правый угол
            self._direction = Direction.RIGHT_BOTTOM
            self.setCursor(Qt.SizeFDiagCursor)

        elif wm <= x_pos and y_pos <= self.MARGINS:
            # верхний правый угол
            self._direction = Direction.RIGHT_TOP
            self.setCursor(Qt.SizeBDiagCursor)

        elif x_pos <= self.MARGINS and hm <= y_pos:
            # Нижний левый угол
            self._direction = Direction.LEFT_BOTTOM
            self.setCursor(Qt.SizeBDiagCursor)

        elif 0 <= x_pos <= self.MARGINS <= y_pos <= hm:
            # Влево
            self._direction = Direction.LEFT
            self.setCursor(Qt.SizeHorCursor)

        elif wm <= x_pos <= self.width() and self.MARGINS <= y_pos <= hm:
            # Право
            self._direction = Direction.RIGHT
            self.setCursor(Qt.SizeHorCursor)

        elif wm >= x_pos >= self.MARGINS >= y_pos >= 0:
            # выше
            self._direction = Direction.TOP
            self.setCursor(Qt.SizeVerCursor)

        elif self.MARGINS <= x_pos <= wm and hm <= y_pos <= self.height():
            # ниже
            self._direction = Direction.BOTTOM
            self.setCursor(Qt.SizeVerCursor)

        else:
            # Курсор по умолчанию
            self.setCursor(Qt.ArrowCursor)

    def resize_window(self, pos):
        """ Отрегулируйте размер окна """
        if self._direction is None:
            return

        mpos = pos - self._old_pos
        x_pos, y_pos = mpos.x(), mpos.y()
        geometry = self.geometry()
        x, y, w, h = geometry.x(), geometry.y(), geometry.width(), geometry.height()

        if self._direction == Direction.LEFT_TOP:  # Верхний левый угол
            if w - x_pos > self.minimumWidth():
                x += x_pos
                w -= x_pos

            if h - y_pos > self.minimumHeight():
                y += y_pos
                h -= y_pos

        elif self._direction == Direction.RIGHT_BOTTOM:  # Нижний правый угол
            if w + x_pos > self.minimumWidth():
                w += x_pos
                self._old_pos = pos

            if h + y_pos > self.minimumHeight():
                h += y_pos
                self._old_pos = pos

        elif self._direction == Direction.RIGHT_TOP:  # верхний правый угол
            if h - y_pos > self.minimumHeight():
                y += y_pos
                h -= y_pos

            if w + x_pos > self.minimumWidth():
                w += x_pos
                self._old_pos.setX(pos.x())

        elif self._direction == Direction.LEFT_BOTTOM:  # Нижний левый угол
            if w - x_pos > self.minimumWidth():
                x += x_pos
                w -= x_pos

            if h + y_pos > self.minimumHeight():
                h += y_pos
                self._old_pos.setY(pos.y())

        elif self._direction == Direction.LEFT:  # Влево
            if w - x_pos > self.minimumWidth():
                x += x_pos
                w -= x_pos
            else:
                return

        elif self._direction == Direction.RIGHT:  # Право
            if w + x_pos > self.minimumWidth():
                w += x_pos
                self._old_pos = pos
            else:
                return

        elif self._direction == Direction.TOP:  # выше
            if h - y_pos > self.minimumHeight():
                y += y_pos
                h -= y_pos
            else:
                return

        elif self._direction == Direction.BOTTOM:  # ниже
            if h + y_pos > self.minimumHeight():
                h += y_pos
                self._old_pos = pos
            else:
                return

        self.setGeometry(x, y, w, h)
