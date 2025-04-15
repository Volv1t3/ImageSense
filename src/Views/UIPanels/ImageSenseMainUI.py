#!-------------------------------------------
# * Descripcion del Contenido
# * @authors: Maria Granda Anazco, Santiago Arellano
# * @date: 13-Apr-2025
# * @description: El presente archivo implementa la interface visual principal, de la aplicacion, la idea de este archivo es
# * incluir un layout en el que se pueda enchufar las instancias de los diversos paneles directamente al programa principal
# * aqui.
# !-------------------------------------------
from PyQt5.QtWidgets import (QMainWindow, QToolBar, QPushButton, QLabel,
                             QHBoxLayout, QVBoxLayout, QWidget, QSplitter,
                             QFrame, QSizePolicy)
from PyQt5.QtCore import Qt, QSize, QMargins
from PyQt5.QtGui import QFont

import ImagePreviewCenterPane
import ImageAnalysisRightPane
import ImageModificationLeftPane


class ImageSenseMainUIApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set window title and size
        self.setWindowTitle('ImageSense Application')
        self.resize(1024, 768)

        # Set margin/padding (10px on each side)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Create toolbar with buttons aligned left and title aligned right
        self.setupToolbar()

        # Create main content area with three panes
        self.setupMainContentArea(main_layout)

        # Set status bar
        self.statusBar().showMessage('Ready')

    def setupToolbar(self):
        # Create toolbar
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        toolbar.setIconSize(QSize(16, 16))

        # Add buttons to the left
        file_controls_btn = QPushButton("File Controls")
        preview_controls_btn = QPushButton("Preview Controls")

        toolbar.addWidget(file_controls_btn)
        toolbar.addWidget(preview_controls_btn)

        # Add spacer to push the title to the right
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        toolbar.addWidget(spacer)

        # Add title to the right
        title_label = QLabel("ImageSense")
        title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        toolbar.addWidget(title_label)

        # Add toolbar to the main window
        self.addToolBar(toolbar)

    def setupMainContentArea(self, main_layout):
        # Create a horizontal splitter for the three panes
        splitter = QSplitter(Qt.Horizontal)

        # Left pane - Image Modification
        left_pane = ImageModificationLeftPane.LeftSideImageModificationPane()

        # Center pane - Image Preview
        center_pane = ImagePreviewCenterPane.CenterSidePreview()

        # Right pane - Image Analysis
        right_pane = ImageAnalysisRightPane.RightSideImageAnalysisPane()

        # Add the panes to the splitter
        splitter.addWidget(left_pane)
        splitter.addWidget(center_pane)
        splitter.addWidget(right_pane)

        # Set initial sizes (ratio like 1:2:1)
        splitter.setSizes([250, 500, 250])

        # Add the splitter to the main layout
        main_layout.addWidget(splitter)