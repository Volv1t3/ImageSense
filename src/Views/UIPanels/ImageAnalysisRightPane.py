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
from PyQt5.QtCore import pyqtSignal, Qt, QThread
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import (QWidget, QSizePolicy, QPushButton, QVBoxLayout, QSlider, QLabel, QHBoxLayout, QGridLayout)
import cv2
import numpy as np
from Models.ImageManager import ImageManager


class RightSideImageAnalysisPane(QWidget):
    # ? 1. Signals para manejar transferencia de informacion e imagenes
    preview_image_needs_to_be_updated: pyqtSignal = pyqtSignal(QImage)

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
        # ? 1. Calculamos los valores del tresh para el canny edge detection
        self.edge_detection_min_thresh = self.min_threshold_slider.value() / 100.0
        self.edge_detection_max_thresh = self.max_threshold_slider.value() / 100.0
        # ? 2. Enviamos un request a la UI principal para recoger la imagen de afuera
        self.image_from_storage: QImage = self.imageManager.internal_normal_image_holder
        print("Canny Edge Analysis Requested")

        # ? Aqui va la implementacion del canny edge detection.
        if self.image_from_storage:
            self.background_worker: CannyEdgeDetectionWorkerThread = CannyEdgeDetectionWorkerThread(
                self.image_from_storage,
                self.edge_detection_min_thresh,
                self.edge_detection_max_thresh)
            self.background_worker.onCannyEdgeResult.connect(self.onCannyEdgeResult)
            self.background_worker.onError.connect(self.onError)
            self.background_worker.start()

    def handle_object_detetion_analysis_request(self) -> None:
        print("Object Detection Analysis Requested")
        image_from_storage: QImage = self.imageManager.internal_normal_image_holder

        if image_from_storage:
            # ? Realizamos la llamada al background thread
            self.background_worker: ObjectDetectionWorkerThread = ObjectDetectionWorkerThread(image_from_storage)
            self.background_worker.onObjectDetectionResult.connect(self.onObjectDetectionResult)
            self.background_worker.onError.connect(self.onError)
            self.background_worker.start()

    def onCannyEdgeResult(self, returnedImage: QImage):
        print("Canny Edge Result Received")
        self.preview_image_needs_to_be_updated.emit(returnedImage)

    def onError(self, error_message):
        print("Error in the effect")
        print(error_message)

    def onObjectDetectionResult(self, returnedImage: QImage):
        print("Object Detection Result Received")
        self.preview_image_needs_to_be_updated.emit(returnedImage)


class CannyEdgeDetectionWorkerThread(QThread):
    # https://pytutorial.com/python-opencv-cv2canny-edge-detection-guide/
    # ? Signals for changes and their emission
    onCannyEdgeResult: pyqtSignal = pyqtSignal(QImage)
    onError: pyqtSignal = pyqtSignal(str)

    def __init__(self, image_to_analize: QImage, min_thresh: float = 50.0, max_thresh: float = 50.0):
        super().__init__()
        self.image_to_analize = image_to_analize
        self.min_thresh = min_thresh
        self.max_thresh = max_thresh

    def run(self):
        try:
            # ? 1. Inicializamos el modulo de Canny Edge Detection utilizando la informacion del arreglo de numpy de la
            # ? imagen general, esto porque al final, cv2 utiliza arrays de numpy para manejarse cuando se tiene que pasar de
            # ? openCV hacia QImage y viceversa
            to_process_image_width = self.image_to_analize.width()
            to_process_image_height = self.image_to_analize.height()

            # ? 1.1. Convertimos la imagen a escala de grises
            image_in_bits = self.image_to_analize.bits();
            image_in_bits.setsize(to_process_image_height * to_process_image_width * 4)
            image_as_array = np.frombuffer(image_in_bits, np.uint8).copy()
            image_as_array = image_as_array.reshape((to_process_image_height, to_process_image_width, 4))

            # ? 2. Convertimos la imagen al formato BGR que se utiliza en open CV y luego hacia grayscale
            bgr_image = cv2.cvtColor(image_as_array, cv2.COLOR_RGBA2BGR)
            gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)

            # ? 3. Aplicamos el algoritmo de Canny Edge Detection
            edges = cv2.Canny(gray_image, int(max(0, int(self.min_thresh * 255))),
                              int(max(0, int(self.max_thresh * 255))))

            # ? 4. Convertimos la imagen de vuelta a RGBA para poder mostrarla en el widget
            rgba_edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGBA)
            height, width, channel = rgba_edges.shape
            bytes_per_line = 4 * width
            q_image = QImage(rgba_edges.data, width, height, bytes_per_line, QImage.Format_RGBA8888).copy()
            # ? 5. Emitimos el resultado
            self.onCannyEdgeResult.emit(q_image)
        except Exception as e:
            self.onError.emit(str(e))


class ObjectDetectionWorkerThread(QThread):
    # ? Signals to update the UI
    onObjectDetectionResult: pyqtSignal = pyqtSignal(QImage)
    onError: pyqtSignal = pyqtSignal(str)

    def __init__(self, image_to_analize: QImage):
        super().__init__()
        self.image_to_analize = image_to_analize

    def run(self):
        try:
            # ? 1. Convertimos la QImage a un formato de numpy array para manejarlo con openCV
            to_process_image_width = self.image_to_analize.width()
            to_process_image_height = self.image_to_analize.height()

            # ? 1.1. Convertimos los bits de la imagen a un numpy array
            image_in_bits = self.image_to_analize.bits()
            image_in_bits.setsize(to_process_image_height * to_process_image_width * 4)
            image_as_array = np.frombuffer(image_in_bits, np.uint8).copy()
            image_as_array = image_as_array.reshape((to_process_image_height, to_process_image_width, 4))

            # ? 2. Convertimos la iamgen a BGR desde RGB para trabajar con openCV
            bgr_image = cv2.cvtColor(image_as_array, cv2.COLOR_RGBA2BGR)
            original_image = image_as_array.copy()
            # ? 3. Cargamos los modelos precargados en el sistema
            yolo_network = cv2.dnn.readNet("yolov4.weights", "yolov4.cfg")

            # ? 4. Cargamos todas las caracteristicas y objetos cargados en el modelo de COCO
            class_labels = []
            with open("coco.names", "r") as f:
                class_labels = [line.strip() for line in f.readlines()]

            layer_names = yolo_network.getLayerNames()
            output_layers = [layer_names[i - 1] for i in yolo_network.getUnconnectedOutLayers()]

            colors = np.random.uniform(250, 255, size=(len(class_labels), 3))
            # ? 4.1 Creamos un blob para la imagen analizada
            blob = cv2.dnn.blobFromImage(
                bgr_image,
                size=(416, 416),
                scalefactor=1 / 255.0,
                swapRB=True,
                crop=False
            )

            # ? 5. Realizamos la deteccion de objetos
            yolo_network.setInput(blob)
            output = yolo_network.forward(output_layers)
            class_ids = []
            confianza = []
            boxes = []

            height, width = bgr_image.shape[:2]

            for out in output:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]

                    if confidence > 0.2:
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)

                        # Rectangle coordinates
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)

                        boxes.append([x, y, w, h])
                        confianza.append(float(confidence))
                        class_ids.append(class_id)

            indexes = cv2.dnn.NMSBoxes(boxes, confianza, 0.5, 0.4)
            margin = 100
            # Draw boxes
            font = cv2.FONT_HERSHEY_SIMPLEX
            for i in range(len(boxes)):
                if i in indexes:
                    x, y, w, h = boxes[i]
                    x = max(margin, min(x, width - margin))
                    y = max(margin, min(y, height - margin))
                    w = max(margin, min(w, width - x - margin))
                    h = max(margin, min(h, height - y - margin))
                    label = str(class_labels[class_ids[i]])
                    confidence = confianza[i]
                    color = colors[class_ids[i]]

                    # Draw rectangle
                    cv2.rectangle(
                        original_image,
                        (x, y),
                        (x + w, y + h),
                        color,
                        2
                    )

                    # Draw label
                    cv2.putText(
                        original_image,
                        f'{label} {confidence:.2f}',
                        (x, y - 10),
                        font,
                        0.5,
                        color,
                        2
                    )

                    # Convert back to RGBA for Qt
            rgba_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGBA)
            height, width, channel = rgba_image.shape
            bytes_per_line = 4 * width

            # Create QImage from the processed image
            q_image = QImage(
                rgba_image.data,
                width,
                height,
                bytes_per_line,
                QImage.Format_RGBA8888
            ).copy()

            # Emit the result
            self.onObjectDetectionResult.emit(q_image)

        except Exception as e:
            self.onError.emit(str(e))
