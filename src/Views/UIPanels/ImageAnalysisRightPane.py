#!-------------------------------------------
# * Descripcion del Contenido
# * @authors: Maria Granda Anazco, Santiago Arellano
# * @date: 13-Apr-2025
# * @description: El presente archivo una clase estandar de PyQT5 que permite generar y
# * controlar una vista completa dentro de la aplicacion. La idea de este archivo es contener la clase estandar que define
# * el layout general para el lado derechop de la app, es decir la seccion de analisis del contenido de una imagen a travges
# * de openCV y los modelos de Canny Edge Detection y Detection, ambos de la misma libreria para menejar mini modelos de
# * IA para identificar secciones de imagenes.
# !-------------------------------------------
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import (QWidget, QSizePolicy, QPushButton, QVBoxLayout, QSlider, QLabel, QHBoxLayout, QGridLayout)

from Models.ImageManager import ImageManager


class RightSideImageAnalysisPane(QWidget):

    #? 1. Signals para manejar transferencia de informacion e imagenes
    image_needs_to_be_updated_signal: pyqtSignal = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self.imageManager: ImageManager = ImageManager()
        self.edge_detection_min_thresh: float = 0.0
        self.edge_detection_max_thresh: float = 0.0
        self.min_threshold_slider: QSlider = None
        self.max_threshold_slider: QSlider = None
        self.edge_detection_button: QPushButton = None
        self.object_detection_button: QPushButton = None
        self.__init_UI__()

    def __init_UI__(self) -> None:
        # ? 1. Creamos el layout principal
        self.image_analysis_panel = QWidget(self)
        self.image_analysis_panel.setMinimumWidth(325)
        self.image_analysis_panel.setSizePolicy(QSizePolicy.Expanding,
                                                QSizePolicy.Expanding)
        self.image_analysis_panel.setStyleSheet("""
                   background-color: #273B65;
                   border-radius: 16px;
                   padding: 20px;
               """)

        # ? 2. Defnimos el contenido interno a traves
        # ? de un Layout manejado por el widget
        self.mainLayout = QVBoxLayout(self.image_analysis_panel)
        self.mainLayout.setContentsMargins(20, 20, 20, 20)
        self.mainLayout.setSpacing(2)  # Reduce overall spacing between elements

        self.mainLayout.setAlignment(Qt.AlignCenter)
        self.mainLayout.setDirection(QVBoxLayout.Direction.TopToBottom)

        # ? 2.1 Anadimos un poco de espacio antes de los elementos para que se alineen al centro
        self.mainLayout.addStretch(1)

        # Edge Detection button
        self.edge_detection_button = QPushButton("Analyze Image With Edge Detection")
        self.edge_detection_button.setStyleSheet("""
                    QPushButton {
                        background-color: #BED6DF;
                        color: #273B65;
                        text-align: center;
                        word-wrap: normal;
                        font-family: 'Microsoft JhengHei UI', sans-serif;
                        font-size: 14px;
                        font-style: normal;
                        font-weight: bold;
                        border-radius: 10px;
                        padding: 10px;
                        text-align: center;
                    }
                    QPushButton:hover {
                        background-color: #84979E;
                    }
                    QPushButton:pressed {
                        background-color: #6B7D84;
                    }
                """)
        self.edge_detection_button.clicked.connect(self.handle_canny_edge_analysis_request)
        self.edge_detection_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.mainLayout.addWidget(self.edge_detection_button)

        # ? 3. Create a grouped layout for Minimum threshold
        min_threshold_group = QWidget()
        min_group_layout = QVBoxLayout(min_threshold_group)
        min_group_layout.setContentsMargins(0, 10, 0, 0)
        min_group_layout.setSpacing(2)  # Minimal spacing within group

        # Header labels for Minimum threshold in a single compact layout
        header_layout = QVBoxLayout()
        header_layout.setSpacing(0)  # No spacing between the two labels

        mayor_informative_message_min_tresh_description = QLabel("Minimum Edge Detection Threshold")
        mayor_informative_message_min_tresh_description.setStyleSheet("""
            QLabel {
                color: #BED6DF;
                font-family: 'Microsoft JhengHei UI', sans-serif;
                font-size: 16px;
                font-style: normal;
                font-weight: bold;
            }
        """)
        mayor_informative_message_min_tresh_description.setWordWrap(True)
        mayor_informative_message_min_tresh_description.setAlignment(Qt.AlignLeft)
        header_layout.addWidget(mayor_informative_message_min_tresh_description)

        min_group_layout.addLayout(header_layout)

        # ? 3.1 Slider layout for minimum threshold
        min_slider_layout = QHBoxLayout()
        min_slider_layout.setSpacing(2)

        # ? Valor mínimo
        min_value_label = QLabel("0")
        min_value_label.setStyleSheet("""
            QLabel {
                color: #BED6DF;
                font-family: 'Microsoft JhengHei UI', sans-serif;
                font-size: 12px;
            }
        """)
        min_slider_layout.addWidget(min_value_label)

        # ? 3.2 Slider para el threshold minimo
        self.min_threshold_slider = QSlider(Qt.Horizontal)
        self.min_threshold_slider.setMinimum(0)
        self.min_threshold_slider.setMaximum(100)
        self.min_threshold_slider.setValue(50)
        self.min_threshold_slider.setTickPosition(QSlider.TicksBelow)
        self.min_threshold_slider.setTickInterval(10)
        self.min_threshold_slider.valueChanged.connect(self.update_min_threshold)
        self.min_threshold_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 8px;
                background: rgba(255, 255, 255, 0.2);
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: white;
                width: 16px;
                height: 16px;
                margin: -4px 0;
                border-radius: 8px;
            }
            QSlider::sub-page:horizontal {
                background: white;
                border-radius: 4px;
            }
        """)
        min_slider_layout.addWidget(self.min_threshold_slider, 0)

        # ? Valor máximo
        max_value_label = QLabel("100")
        max_value_label.setStyleSheet("""
            QLabel {
                color: #BED6DF;
                font-family: 'Microsoft JhengHei UI', sans-serif;
                font-size: 12px;
            }
        """)
        min_slider_layout.addWidget(max_value_label)

        min_group_layout.addLayout(min_slider_layout)
        self.mainLayout.addWidget(min_threshold_group)

        max_threshold_group = QWidget()
        max_group_layout = QVBoxLayout(max_threshold_group)
        max_group_layout.setContentsMargins(0, 10, 0, 0)
        max_group_layout.setSpacing(2)  # Minimal spacing within group

        max_header_layout = QVBoxLayout()
        max_header_layout.setSpacing(0)


        mayor_informative_message_max_tresh_description = QLabel("Maximum Edge Detection Threshold")
        mayor_informative_message_max_tresh_description.setStyleSheet("""
            QLabel {
                color: #BED6DF;
                font-family: 'Microsoft JhengHei UI', sans-serif;
                font-size: 16px;
                font-style: normal;
                font-weight: bold;
            }
        """)
        mayor_informative_message_max_tresh_description.setAlignment(Qt.AlignLeft)
        mayor_informative_message_max_tresh_description.setWordWrap(True)
        max_header_layout.addWidget(mayor_informative_message_max_tresh_description)

        max_group_layout.addLayout(max_header_layout)

        # ? 4.1 Slider layout for maximum threshold
        max_slider_layout = QHBoxLayout()
        max_slider_layout.setSpacing(2)

        # ? Valor mínimo
        min_value_label_max = QLabel("0")
        min_value_label_max.setStyleSheet("""
            QLabel {
                color: #BED6DF;
                font-family: 'Microsoft JhengHei UI', sans-serif;
                font-size: 12px;
            }
        """)
        max_slider_layout.addWidget(min_value_label_max)

        # ? 4.2 Slider para el threshold maximo
        self.max_threshold_slider = QSlider(Qt.Horizontal)
        self.max_threshold_slider.setMinimum(0)
        self.max_threshold_slider.setMaximum(100)
        self.max_threshold_slider.setValue(50)
        self.max_threshold_slider.setTickPosition(QSlider.TicksBelow)
        self.max_threshold_slider.setTickInterval(10)
        self.max_threshold_slider.valueChanged.connect(self.update_max_threshold)
        self.max_threshold_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 8px;
                background: rgba(255, 255, 255, 0.2);
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: white;
                width: 16px;
                height: 16px;
                margin: -4px 0;
                border-radius: 8px;
            }
            QSlider::sub-page:horizontal {
                background: white;
                border-radius: 4px;
            }
        """)
        max_slider_layout.addWidget(self.max_threshold_slider, 0)

        # ? Valor máximo
        max_value_label_max = QLabel("100")
        max_value_label_max.setStyleSheet("""
            QLabel {
                color: #BED6DF;
                font-family: 'Microsoft JhengHei UI', sans-serif;
                font-size: 12px;
            }
        """)
        max_slider_layout.addWidget(max_value_label_max)

        max_group_layout.addLayout(max_slider_layout)
        self.mainLayout.addWidget(max_threshold_group)

        # ? 5. Botón para clasificación de objetos with spacing to separate from sliders
        self.mainLayout.addSpacing(2)
        self.object_detection_button = QPushButton("Perform Object Classification")
        self.object_detection_button.setStyleSheet("""
            QPushButton {
                background-color: #BED6DF;
                color: #273B65;
                font-family: 'Microsoft JhengHei UI', sans-serif;
                font-size: 14px;
                font-style: normal;
                font-weight: bold;
                border-radius: 10px;
                padding: 10px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #84979E;
            }
            QPushButton:pressed {
                background-color: #6B7D84;
            }
        """)
        self.mainLayout.addWidget(self.object_detection_button)
        self.object_detection_button.clicked.connect(self.handle_object_detetion_analysis_request)

        # ? 6. Agregamos espacio al final para mantener el centrado
        self.mainLayout.addStretch(1)

        # ? 7. Asignamos el layout al widget principal
        layout = QVBoxLayout()
        layout.addWidget(self.image_analysis_panel)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def update_min_threshold(self) -> None:
        """Update the minimum threshold value"""
        self.edge_detection_min_thresh = self.min_threshold_slider.value() / 100.0

    def update_max_threshold(self) -> None:
        """Update the maximum threshold value"""
        self.edge_detection_max_thresh = self.max_threshold_slider.value() / 100.0

    def handle_canny_edge_analysis_request(self) -> None:
        #? 1. Calculamos los valores del tresh para el canny edge detection
        self.edge_detection_min_thresh = self.min_threshold_slider.value() / 100.0
        self.edge_detection_max_thresh = self.max_threshold_slider.value() / 100.0
        #? 2. Enviamos un request a la UI principal para recoger la imagen de afuera
        image_from_storage: QImage = self.imageManager.internal_normal_image_holder
        print("Canny Edge Analysis Requested")
        image_modified: QImage = None
        if image_from_storage:
            self.image_needs_to_be_updated_signal.emit(image_from_storage)
    def handle_object_detetion_analysis_request(self) -> None:
        print("Object Detection Analysis Requested")
        image_from_storage: QImage = self.imageManager.internal_normal_image_holder
        image_modified: QImage = None
        if image_from_storage:
            self.image_needs_to_be_updated_signal.emit(image_from_storage)