# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'windowbaseUpOvCv.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGraphicsView, QHBoxLayout,
    QMainWindow, QMenuBar, QSizePolicy, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1740, 1171)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.LeftWorkArea = QVBoxLayout()
        self.LeftWorkArea.setObjectName(u"LeftWorkArea")
        self.PreviewViewportFrame = QFrame(self.centralwidget)
        self.PreviewViewportFrame.setObjectName(u"PreviewViewportFrame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.PreviewViewportFrame.sizePolicy().hasHeightForWidth())
        self.PreviewViewportFrame.setSizePolicy(sizePolicy1)
        self.PreviewViewportFrame.setMinimumSize(QSize(320, 320))
        self.PreviewViewportFrame.setMaximumSize(QSize(512, 16777215))
        self.PreviewViewportFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.PreviewViewportFrame.setFrameShadow(QFrame.Shadow.Raised)

        self.LeftWorkArea.addWidget(self.PreviewViewportFrame)

        self.PropertiesPanelFrame = QFrame(self.centralwidget)
        self.PropertiesPanelFrame.setObjectName(u"PropertiesPanelFrame")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.PropertiesPanelFrame.sizePolicy().hasHeightForWidth())
        self.PropertiesPanelFrame.setSizePolicy(sizePolicy2)
        self.PropertiesPanelFrame.setMinimumSize(QSize(320, 0))
        self.PropertiesPanelFrame.setMaximumSize(QSize(512, 16777215))
        self.PropertiesPanelFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.PropertiesPanelFrame.setFrameShadow(QFrame.Shadow.Raised)

        self.LeftWorkArea.addWidget(self.PropertiesPanelFrame)


        self.horizontalLayout.addLayout(self.LeftWorkArea)

        self.CenterWorkArea = QVBoxLayout()
        self.CenterWorkArea.setObjectName(u"CenterWorkArea")
        self.NodeGraphFrame = QFrame(self.centralwidget)
        self.NodeGraphFrame.setObjectName(u"NodeGraphFrame")
        sizePolicy.setHeightForWidth(self.NodeGraphFrame.sizePolicy().hasHeightForWidth())
        self.NodeGraphFrame.setSizePolicy(sizePolicy)
        self.NodeGraphFrame.setBaseSize(QSize(0, 0))
        self.NodeGraphFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.NodeGraphFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.NodeGraphFrame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.NodeGraphView = QGraphicsView(self.NodeGraphFrame)
        self.NodeGraphView.setObjectName(u"NodeGraphView")
        self.NodeGraphView.setAutoFillBackground(True)
        self.NodeGraphView.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.NodeGraphView.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        brush = QBrush(QColor(61, 56, 70, 255))
        brush.setStyle(Qt.Dense4Pattern)
        self.NodeGraphView.setBackgroundBrush(brush)

        self.verticalLayout_2.addWidget(self.NodeGraphView)


        self.CenterWorkArea.addWidget(self.NodeGraphFrame)

        self.OutputViewFrame = QFrame(self.centralwidget)
        self.OutputViewFrame.setObjectName(u"OutputViewFrame")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.OutputViewFrame.sizePolicy().hasHeightForWidth())
        self.OutputViewFrame.setSizePolicy(sizePolicy3)
        self.OutputViewFrame.setMinimumSize(QSize(0, 120))
        self.OutputViewFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.OutputViewFrame.setFrameShadow(QFrame.Shadow.Raised)

        self.CenterWorkArea.addWidget(self.OutputViewFrame)


        self.horizontalLayout.addLayout(self.CenterWorkArea)

        self.RightWorkArea = QVBoxLayout()
        self.RightWorkArea.setObjectName(u"RightWorkArea")
        self.PaletteFrame = QFrame(self.centralwidget)
        self.PaletteFrame.setObjectName(u"PaletteFrame")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.PaletteFrame.sizePolicy().hasHeightForWidth())
        self.PaletteFrame.setSizePolicy(sizePolicy4)
        self.PaletteFrame.setMinimumSize(QSize(200, 0))
        self.PaletteFrame.setMaximumSize(QSize(320, 16777215))
        self.PaletteFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.PaletteFrame.setFrameShadow(QFrame.Shadow.Raised)

        self.RightWorkArea.addWidget(self.PaletteFrame)


        self.horizontalLayout.addLayout(self.RightWorkArea)


        self.verticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1740, 23))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
    # retranslateUi
