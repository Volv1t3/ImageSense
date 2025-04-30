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
    """
    The following contains information about the right side, image analysis pane that handles the Canny
    edge detection used for the image, as well as Object Detection based on a YOLOv4 model pretrained for this
    task.
    
    As such, this class handles a series of background threads designed to extend the QThread class that handles 
    background tasks such as image processing.
    """
    # ? 1. Signals para manejar transferencia de informacion e imagenes
    preview_image_needs_to_be_updated: pyqtSignal = pyqtSignal(QImage)

    def __init__(self):
        """
        Initializes the RightSideImageAnalysisPane widget for image analysis functionality.
        
        This constructor sets up the initial state of the image analysis panel, including:
        1. Calls the parent QWidget constructor
        2. Creates an ImageManager instance for handling image operations
        3. Initializes edge detection threshold values (min and max)
        4. Declares UI control elements (sliders and buttons) that will be populated in __init_UI__
        5. Calls __init_UI__ to create and configure the user interface
        
        Instance Variables:
            - imageManager (ImageManager): Manages image loading and processing operations
            - edge_detection_min_thresh (float): Minimum threshold value for Canny edge detection
            - edge_detection_max_thresh (float): Maximum threshold value for Canny edge detection
            - min_threshold_slider (QSlider): Slider control for minimum threshold adjustment
            - max_threshold_slider (QSlider): Slider control for maximum threshold adjustment
            - edge_detection_button (QPushButton): Button to trigger edge detection analysis
            - object_detection_button (QPushButton): Button to trigger object detection analysis
            
        No parameters required.
        
        :return : None.
        """
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
        """
        Initializes and configures the user interface components of the image analysis panel.
        
        This method sets up a comprehensive UI layout for image analysis functionality, creating
        a right-side panel with various controls for image processing. The panel includes edge
        detection controls and object detection capabilities.
        
        The method constructs the following main components:
        
        - A main panel widget with custom styling and minimum width requirements
        - An edge detection button for triggering Canny edge analysis
        - Two threshold control groups (minimum and maximum) for edge detection sensitivity
        - Slider controls for adjusting the threshold values (0-100)
        - An object detection button for classification analysis
        
        The layout is organized vertically with proper spacing and margins, using a combination
        of QVBoxLayout and QHBoxLayout managers. All UI elements are styled consistently with
        a blue color scheme and modern design elements including rounded corners and hover effects.
        
        All components are connected to their respective event handlers and configured with
        appropriate size policies and alignments to ensure proper display and functionality.
        
        Parameters:
            None
            
        Returns:
            None
        """
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
        """
        Handles the request to perform Canny edge detection analysis on the currently loaded image.
        
        This method initiates the edge detection process by first calculating the threshold values
        from the UI slider controls, converting them from percentage values (0-100) to normalized
        values (0.0-1.0). It then retrieves the current image from storage and creates a background
        worker thread to perform the actual edge detection processing.
        
        The edge detection process is performed asynchronously using a CannyEdgeDetectionWorkerThread
        to prevent UI freezing during computation. The worker thread applies the Canny edge detection
        algorithm using the specified minimum and maximum threshold values.
        
        The method sets up the necessary signal connections to handle both successful results and
        errors from the background processing:
        
        - onCannyEdgeResult: Receives the processed image with detected edges
        - onError: Handles any errors that occur during processing
        
        No parameters are required as all necessary values are obtained from class instance variables
        and UI elements.
        
        Returns:
            None
            
        Signals:
        
            - Emits the processed image through preview_image_needs_to_be_updated signal when complete
            - Prints status messages to console for debugging purposes
        """
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
        """
        Handles the request to perform object detection analysis on the currently loaded image.
    
        This method initiates the object detection process by retrieving the current image from
        the ImageManager's internal storage. It utilizes a YOLOv4-based detection system implemented
        through OpenCV's deep neural network module.
    
        The actual processing is performed asynchronously in a background thread using the
        ObjectDetectionWorkerThread class to prevent UI freezing during computation. The worker
        thread processes the image through a pre-trained neural network model capable of
        detecting and classifying multiple objects within the image.
    
        The method sets up signal connections to handle both successful results and errors:
        
        - onObjectDetectionResult: Receives the processed image with detected objects
        - onError: Handles any errors that occur during processing
    
        No parameters are required as the image is obtained from the class's ImageManager instance.
    
        Returns:
            None
    
        Signals:
        
            - Emits the processed image through preview_image_needs_to_be_updated signal upon completion
            - Prints status messages to console for debugging purposes
        """
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
        print(f"Image is null={False if returnedImage else True}")
        self.preview_image_needs_to_be_updated.emit(returnedImage)


class CannyEdgeDetectionWorkerThread(QThread):
    """
    A worker thread class that performs Canny edge detection on images asynchronously.
    
    This class extends QThread to perform image processing operations in the background,
    preventing UI freezes during computation. It implements the Canny edge detection
    algorithm using OpenCV, converting between Qt and OpenCV image formats as needed.
    
    The class processes images through several steps:
    
    1. Converts QImage to numpy array format
    2. Transforms the image to grayscale
    3. Applies Canny edge detection with configurable thresholds
    4. Converts the result back to QImage format for display
    
    Signals:
        onCannyEdgeResult (QImage): Emitted when edge detection is complete
        onError (str): Emitted when an error occurs during processing
    """

    onCannyEdgeResult: pyqtSignal = pyqtSignal(QImage)
    onError: pyqtSignal = pyqtSignal(str)

    def __init__(self, image_to_analize: QImage, min_thresh: float = 50.0, max_thresh: float = 50.0):
        """
        Initialize the Canny edge detection worker thread.
    
        Parameters:
            image_to_analize (QImage): The source image to process
            min_thresh (float): Minimum threshold for edge detection (0.0-100.0)
            max_thresh (float): Maximum threshold for edge detection (0.0-100.0)
        """
        super().__init__()
        self.image_to_analize = image_to_analize
        self.min_thresh = min_thresh
        self.max_thresh = max_thresh

    def run(self):
        """
        Executes the Canny edge detection algorithm on the provided image in a background thread.
    
        This method performs a series of image processing operations to detect edges in the input image.
        The process begins by extracting the raw image data from the QImage format and converting it
        into a numpy array suitable for OpenCV operations. The image undergoes several transformations,
        including conversion to grayscale and application of the Canny edge detection algorithm with
        the specified threshold values.
    
        The method handles the complete pipeline of image processing:
        First, it extracts the dimensions of the input image and converts the QImage data into a numpy
        array format. This array is then reshaped according to the image dimensions and channel count.
        Next, it performs color space conversions, transforming the image from RGBA to BGR (OpenCV's
        preferred format) and then to grayscale. The Canny edge detection algorithm is applied using
        the pre-configured minimum and maximum threshold values, which are scaled from their normalized
        form (0-1) to the required pixel intensity range (0-255).
    
        Finally, the resulting edge map is converted back to RGBA format for compatibility with Qt's
        display system, and a new QImage is created from the processed data.
    
        The method uses instance variables:
            - self.image_to_analize: Source QImage to process
            - self.min_thresh: Minimum threshold for edge detection (0.0-1.0)
            - self.max_thresh: Maximum threshold for edge detection (0.0-1.0)
    
        Signals:
            - onCannyEdgeResult: Emits the processed QImage containing the detected edges
            - onError: Emits a string message if an error occurs during processing
    
        Raises:
            Any exceptions during processing are caught and emitted through the onError signal
        """
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
    """
    A worker thread class that performs object detection on images asynchronously using YOLOv4.
    
    This class extends QThread to perform complex image processing operations in the background,
    preventing UI freezes during computation. It implements the YOLOv4 object detection algorithm
    using OpenCV's deep neural network module to identify and classify objects within images.
    
    The class processes images through several steps:
    1. Converts QImage to OpenCV-compatible format
    2. Loads pre-trained YOLOv4 model and COCO dataset classes
    3. Processes image through neural network to detect objects
    4. Draws bounding boxes and labels around detected objects
    5. Converts results back to QImage format for display
    
    Signals:
        onObjectDetectionResult (QImage): Emitted when object detection is complete
        onError (str): Emitted when an error occurs during processing
    """
    onObjectDetectionResult: pyqtSignal = pyqtSignal(QImage)
    onError: pyqtSignal = pyqtSignal(str)

    def __init__(self, image_to_analize: QImage):
        """
        Initialize the object detection worker thread.
        
        This constructor sets up a new thread instance for processing images using
        YOLOv4 object detection. It stores the input image for later processing
        in the run method and initializes the base QThread functionality.
        
        Parameters:
            image_to_analize (QImage): The source image on which to perform object detection.
                                      This image will be processed when the thread is started.
        """
        super().__init__()
        self.image_to_analize = image_to_analize

    def run(self):
        """
        Execute the Canny edge detection processing in the background thread.
        
        This method performs the following operations:
        
        1. Converts the QImage to a numpy array format suitable for OpenCV
        2. Transforms the image from RGBA to BGR color space
        3. Converts the image to grayscale for edge detection
        4. Applies the Canny edge detection algorithm with normalized thresholds
        5. Converts the resulting edge map back to RGBA format
        6. Creates a new QImage from the processed data
        
        The method emits either:
        - onCannyEdgeResult signal with the processed image on success
        - onError signal with error message on failure
        
        No parameters required as it uses instance variables set in __init__.
        """
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

            layer_names = yolo_network.getLayerNames() #Obtenemos todas las layers dentro de la architectura del modelo de NN.
            output_layers = [layer_names[i - 1] for i in yolo_network.getUnconnectedOutLayers()]
            # esta linea toma el nombre de todas las layers que no estan contectadas con otras, es decir outputs.

            colors = np.random.uniform(250, 255, size=(len(class_labels), 3))
            # ? 4.1 Creamos un blob para la imagen analizada: Un blob es un Binary Large Object, el cual es una
            # ? estrcutura de tipo tensor que tiene dentro de si los valores de una cantidad de imagenes (batc size),
            # ? canales de colores, altura y ancho, etc. En este caso, normalizamos el tamano de los pixeles a un rango de 0 a
            # ? 1 dado que el scale es de 1/255.0. En si, este tipo de dato es util para comunicar datos a una Neural
            # ? Network prestablecida.
            blob = cv2.dnn.blobFromImage(
                bgr_image,
                size=(416, 416),
                scalefactor=1 / 255.0,
                swapRB=True,
                crop=False
            )

            # ? 5. Cargamos los parametros de la imagen a analizar dentro del sistema de YOLO para su anailsis,
            yolo_network.setInput(blob)
            output = yolo_network.forward(output_layers)
            class_ids = []
            confianzas = []
            boxes = []

            height, width = bgr_image.shape[:2]

            # ? 6. Analizamos los resultados moviendonos a traves de todas las capas de salida que tiene este modelo de
            # ? YOLO. Cada capa de salida tiene su propia "detection" que es un arreglo de valores que contiene informacion de
            # ? salida del modelo.
            for out in output:
                for detection in out:
                    #? Aqui tomamos los valores del cinco en adelante, los cuales son las probabilidades de cada categoria de
                    #? salida
                    scores = detection[5:]
                    class_id = np.argmax(scores) #index de la mayor probabilidad
                    confidence = scores[class_id] # tomamos el valor de la mayor probabilidad

                    #? Filtramos aquellos valores de confianza que sean mayores a 0.2 o 20% de fiabilidad.
                    if confidence > 0.2:
                        #? Aqui calculamos el centro de la deteccion, basandonos en la posicion retornada en el objeto de
                        #? deteccion de YOLO pasando de 0-1 al valor del pixel correcto.
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        #? Aqui calculamos el largo y ancho del objeto, que podemos usar para manejar el bounding boxes.
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)

                        #? Aqui calculamos la posicion real del bounding box que vamos a usar para modificar la imagen
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)

                        boxes.append([x, y, w, h])
                        confianzas.append(float(confidence))
                        class_ids.append(class_id)

            # ? 7. Aqui removemos aquellas boxes que esten en un overlap grande entre si,la idea es que no debemos tener
            # ? detecciones multiples en el mismo objeto
            indexes = cv2.dnn.NMSBoxes(boxes, confianzas, 0.5, 0.4)
            margin = 100
            #? Dbujmos las cajas que vamos a usar para demostrar la posicion de cada una de las detecciones, para esto
            #? iteramos sobre el arreglo de bounding boxes que se han detectado dentro del sistema.
            font = cv2.FONT_HERSHEY_SIMPLEX
            for i in range(len(boxes)):
                if i in indexes:
                    #? Aqui calculamos las posicioens maximas de cada una de los bounding boxes teniendo en cuenta que ponemos
                    #? un margen de 100 px de trabajo, esto lo hacemos ya que en algunos casos, teniamos el problema que
                    #? algunas cajas se salian del area de trabajo.
                    x, y, w, h = boxes[i]
                    x = max(margin, min(x, width - margin))
                    y = max(margin, min(y, height - margin))
                    w = max(margin, min(w, width - x - margin))
                    h = max(margin, min(h, height - y - margin))
                    label = str(class_labels[class_ids[i]])
                    confidence = confianzas[i]
                    color = colors[class_ids[i]].astype(int).tolist()

                    cv2.rectangle(
                        bgr_image,
                        (x, y),
                        (x + w, y + h),
                        color,
                        2
                    )

                    #? Aqui le colocamos la etiqueta a la cajita que acabamos de poner en la imagen
                    cv2.putText(
                        bgr_image,
                        f'{label} {confidence:.2f}',
                        (x, y - 10),
                        font,
                        0.5,
                        color,
                        2
                    )

            # ? 8. Pasamos la iamgen anterior a RGBA de nuevo para ser usada en QImage.
            rgba_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGBA)
            height, width, channel = rgba_image.shape
            bytes_per_line = 4 * width

            #? 9. Usamos la imagen transformada para crear una QImage
            q_image = QImage(
                rgba_image.data,
                width,
                height,
                bytes_per_line,
                QImage.Format_RGBA8888
            ).copy()

            #? Como ultimo paso enviamos la imagen reconstruida hacia la UI mediante signals para que se actualice
            #? la preview de la imagen modificada.
            self.onObjectDetectionResult.emit(q_image)
        except Exception as e:
            self.onError.emit(str(e))
