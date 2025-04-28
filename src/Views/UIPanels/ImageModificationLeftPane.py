#!-------------------------------------------
# * Descripcion del Contenido
# * @authors: Maria Granda Anazco, Santiago Arellano
# * @date: 13-Apr-2025
# * @description: El presente archivo una clase estandar de PyQT5 que permite generar y
# * controlar una vista completa dentro de la aplicacion. La idea de este archivo es contener la clase estandar que define
# * el layout general para el lado izquierdo de la app, es decir la seccion de manipulacion de imagenes simples con
# * librerias estandares de python como openCV, etc.
# !-------------------------------------------
import threading

from PyQt5.QtCore import pyqtSignal, Qt, QThread
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import (QWidget, QSizePolicy, QPushButton, QVBoxLayout)
# Mini librerias para poder trabajar con imagenes y open cv por los efectos
import cv2
import numpy as np
from Models.ImageManager import ImageManager


class LeftSideImageModificationPane(QWidget):
    # ! Signals para manejar comunicacion entre metodos de la UI
    image_needs_to_be_updated_signal: pyqtSignal = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self.imageManager: ImageManager = ImageManager()
        self.__init_UI__()

    def __init_UI__(self) -> None:
        # Create the main container widget
        self.effectsPanel = QWidget(self)
        self.effectsPanel.setMinimumWidth(325)
        self.effectsPanel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.effectsPanel.setStyleSheet("""
                   background-color: #273B65;
                   border-radius: 15px;
                   padding: 10px 10px
               """)

        self.mainLayout = QVBoxLayout(self.effectsPanel)
        self.mainLayout.setContentsMargins(20, 20, 20, 20)
        self.mainLayout.setSpacing(32)
        self.mainLayout.setAlignment(Qt.AlignCenter)
        self.mainLayout.setDirection(QVBoxLayout.Direction.TopToBottom)

        self.mainLayout.addStretch(1)
        self.blurButton = QPushButton("Apply Image Blur")
        self.noiseButton = QPushButton("Apply Image Noise Effect")
        self.bwButton = QPushButton("Apply Black & White Effect")
        self.distortionButton = QPushButton("Apply Distortion Effect")

        # Style all buttons
        buttonStyle = """
                   QPushButton {
                       background-color: #BED6DF;
                       color: #273B65;
                       font-family: 'Microsoft JhengHei UI', sans-serif;
                       font-size:  15px;
                       font-weight: bold;
                       border-radius: 10px;
                
                       text-align: center;
                   }
                   QPushButton:hover {
                       background-color: #84979E;
                   }
                   QPushButton:pressed {
                       background-color: #6B7D84;
                   }
               """

        for button in [self.blurButton, self.noiseButton, self.bwButton, self.distortionButton]:
            button.setStyleSheet(buttonStyle)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
            self.mainLayout.addWidget(button)

        # Add a stretch at the end to push all content up
        self.mainLayout.addStretch(1)

        # Connect signals for each button
        self.blurButton.clicked.connect(self.applyBlurEffect)
        self.noiseButton.clicked.connect(self.applyNoiseEffect)
        self.bwButton.clicked.connect(self.applyBWEffect)
        self.distortionButton.clicked.connect(self.applyDistortionEffect)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.effectsPanel)
        main_layout.setAlignment(Qt.AlignHCenter)
        main_layout.setAlignment(Qt.AlignVCenter)
        self.setLayout(main_layout)

    def applyBlurEffect(self):
        """Apply a blur effect to the image"""
        print("Applying blur effect")
        # ? Aqui debe empezar la implementacion del efecto de Blur
        imageModifiedWithin: QImage = self.imageManager.internal_normal_image_holder

        # ? Si la imagen existe entonces hacemos el analisis
        if imageModifiedWithin:
            # ? 1. Realizamos la manipulacion de la imagen usango la transformacion primaria hacia
            # ? open cv compatible formats
            cv_image_from_q_image = self.helperQImageToOpenCV(imageModifiedWithin)

            # ? 2. Aplicamos el efecto de burring mediante open cv
            background_worker: BlurWorkerForBackgroundWork = BlurWorkerForBackgroundWork(cv_image_from_q_image);

            background_worker.onSuccessfullyFinished.connect(self.onBlurResult)
            background_worker.onErrorCondition.connect(self.onError)

            background_worker.start()

            # ? 3. Desactivamos el boton de blur
            self.blurButton.setEnabled(False)

    def applyNoiseEffect(self):
        """Apply a noise effect to the image"""
        print("Applying noise effect")
        # ? Aqui debe empezar la implementacion del efecto de Noise
        imageModifiedWithin: QImage = self.imageManager.internal_normal_image_holder
        if imageModifiedWithin:
            #? Realizamos la manipulacion de la imagen hacia open cv
            cv_image_from_q_image = self.helperQImageToOpenCV(imageModifiedWithin)

            # ? Aplicamos el efecto de noise mediante open cv
            background_worker: NoiseWorkerForBackgroundWork = NoiseWorkerForBackgroundWork(cv_image_from_q_image)
            background_worker.onSuccessfullyFinished.connect(self.onNoiseResult)
            background_worker.onErrorCondition.connect(self.onError)
            background_worker.start()
            # ? Desactivamos el boton de noise
            self.noiseButton.setEnabled(False)
    def applyBWEffect(self):
        """Apply a black and white effect to the image"""
        print("Applying black & white effect")
        # ? Aqui debe empezar la implementacion del efecto de blanco y negro
        imageModifiedWithin: QImage = self.imageManager.internal_normal_image_holder
        if imageModifiedWithin:
            # ? Realizamos la manipulacion de la imagen hacia open cv
            cv_image_from_q_image = self.helperQImageToOpenCV(imageModifiedWithin)

            # ? Aplicamos el efecto de blanco y negro mediante open cv
            background_worker: BlackAndWhiteForBackgroundWork = BlackAndWhiteForBackgroundWork(cv_image_from_q_image)
            background_worker.onSuccessfullyFinished.connect(self.onBWResult)
            background_worker.onErrorCondition.connect(self.onError)
            background_worker.start()
            # ? Desactivamos el boton de blanco y negro
            self.bwButton.setEnabled(False)
    def applyDistortionEffect(self):
        """Apply a distortion effect to the image"""
        print("Applying distortion effect")
        # ? Aqui debe empezar la implementacion del efecto de distorcion
        imageModifiedWithin: QImage = self.imageManager.internal_normal_image_holder
        if imageModifiedWithin:
            # ? Realizamos la manipulacion de la imagen hacia open cv
            cv_image_from_q_image = self.helperQImageToOpenCV(imageModifiedWithin)

            # ? Aplicamos el efecto de distorcion mediante open cv
            background_worker: DistortionWorkerForBackgroundWork = DistortionWorkerForBackgroundWork(cv_image_from_q_image)
            background_worker.onSuccessfullyFinished.connect(self.onDistortionResult)
            background_worker.onErrorCondition.connect(self.onError)
            background_worker.start()
            # ? Desactivamos el boton de distorcion
            self.distortionButton.setEnabled(False)
    def helperQImageToOpenCV(self, image: QImage) -> np.ndarray:
        """Method defined such that our project is capable of handling transformations between open cv and
        Qt, one is for image processing and another is for image displaying"""
        # ? 1. Debemos de revisar que la imagen que tengamos este en el formato adecuado, en donde los canales de
        # ? RBG son RGB888
        if image.format() != QImage.Format_RGBA8888:
            image = image.convertToFormat(QImage.Format_RGBA8888)

        # ? 2. Para trabajar con open cv, necesitamos tener el tamano de la pantalla
        image_width: float = image.width()
        image_height: float = image.height()

        # ? 3.Tomamos pos bits de la imagen y  contamos
        color_bits = image.constBits()
        color_bits.setsize(image.byteCount())

        # ? 4. Armamos el array interno
        array_of_bits = np.array(color_bits).reshape(image_height, image_width, 4)

        return array_of_bits

    def helperOpenCVToQImage(self, cv_image: np.ndarray) -> QImage:
        """Method defined such that our project is capable of converting between a modifid nd array into a
        UI friendly QImage such that it can be displayed on the user's side."""
        new_qimage_height, new_qimage_width = cv_image.shape[:2]
        new_qimage_from_array = QImage(cv_image.data, new_qimage_width, new_qimage_height, (4 * new_qimage_width),
                                       QImage.Format_RGBA8888)

        return new_qimage_from_array.copy()

    def onBlurResult(self, result_cv_image: np.ndarray):
        """Method used to communicate the returned image from the worker thread back to the main thread and
        transform that image into a QImage"""
        try:
            # ? 1. Convertir el resultado de la imagen de open cv a QImage
            new_qimage_from_cv = self.helperOpenCVToQImage(result_cv_image)
            # ? 2. Activamos de nuevo el boton
            self.blurButton.setEnabled(True)
            # ? 2. Emitir el resultado de la imagen
            self.image_needs_to_be_updated_signal.emit(new_qimage_from_cv)
        except Exception as e:
            print("Error in the result of the blur effect")
            print(e)

    def onError(self, error_message):
        print("Error in the effect")
        print(error_message)
    def onNoiseResult(self, result_cv_image: np.ndarray):
        """Method used to communicate the returned image from the worker thread back to the main thread and
        transform that image into a QImage"""
        try:
            # ? 1. Convertir el resultado de la imagen de open cv a QImage
            new_qimage_from_cv = self.helperOpenCVToQImage(result_cv_image)
            # ? 2. Activamos de nuevo el boton
            self.noiseButton.setEnabled(True)
            # ? 2. Emitir el resultado de la imagen
            self.image_needs_to_be_updated_signal.emit(new_qimage_from_cv)
        except Exception as e:
            print("Error in the result of the noise effect")
            print(e)

    def onBWResult(self, result_cv_image: np.ndarray):
        """Method used to communicate the returned image from the worker thread back to the main thread and
        transform that image into a QImage"""
        try:
            # ? 1. Convertir el resultado de la imagen de open cv a QImage
            new_qimage_from_cv = self.helperOpenCVToQImage(result_cv_image)
            # ? 2. Activamos de nuevo el boton
            self.bwButton.setEnabled(True)
            # ? 2. Emitir el resultado de la imagen
            self.image_needs_to_be_updated_signal.emit(new_qimage_from_cv)
        except Exception as e:
            print("Error in the result of the black and white effect")
            print(e)

    def onDistortionResult(self, result_cv_image: np.ndarray):
        """Method used to communicate the returned image from the worker thread back to the main thread and
        transform that image into a QImage"""
        try:
            # ? 1. Convertir el resultado de la imagen de open cv a QImage
            new_qimage_from_cv = self.helperOpenCVToQImage(result_cv_image)
            # ? 2. Activamos de nuevo el boton
            self.distortionButton.setEnabled(True)
            # ? 2. Emitir el resultado de la imagen
            self.image_needs_to_be_updated_signal.emit(new_qimage_from_cv)
        except Exception as e:
            print("Error in the result of the distortion effect")
            print(e)
class BlurWorkerForBackgroundWork(QThread):
    # ? Signal to emit the processed image
    onSuccessfullyFinished: pyqtSignal = pyqtSignal(np.ndarray)
    onErrorCondition: pyqtSignal = pyqtSignal(str)

    def __init__(self, image: np.ndarray, kernel_size=(33, 33), sigma=0):
        super().__init__()
        self.image = image
        self.kernel_size = kernel_size
        self.sigma = sigma

    def run(self):
        try:
            blurred_image = cv2.GaussianBlur(self.image, self.kernel_size, self.sigma)
            self.onSuccessfullyFinished.emit(blurred_image)
        except Exception as e:
            self.onErrorCondition.emit(str(e))


class NoiseWorkerForBackgroundWork(QThread):
    # https://www.askpython.com/python/examples/adding-noise-images-opencv
    # ? Signals to emit the processed image
    onSuccessfullyFinished: pyqtSignal = pyqtSignal(np.ndarray)
    onErrorCondition: pyqtSignal = pyqtSignal(str)

    def __init__(self, image: np.ndarray, mean: int = 0, std: int = 25):
        super().__init__()
        self.image = image
        self.mean = mean
        self.std = std

    def run(self):
        try:
            # ? 1. Generamos el ruido
            noise = np.random.normal(self.mean, self.std, self.image.shape).astype(np.uint8)
            # ? 2. Aplicamos el ruido a la imagen
            noisy_image = cv2.add(self.image, noise)
            # ? 3. Emitimos el resultado
            self.onSuccessfullyFinished.emit(noisy_image)
        except Exception as e:
            self.onErrorCondition.emit(str(e))


class BlackAndWhiteForBackgroundWork(QThread):
    # https://nulldog.com/opencv-image-to-black-and-white-conversion
    # ? Signals to emit the processed image
    onSuccessfullyFinished: pyqtSignal = pyqtSignal(np.ndarray)
    onErrorCondition: pyqtSignal = pyqtSignal(str)

    def __init__(self, image: np.ndarray):
        super().__init__()
        self.image = image

    def run(self):
        try:
            # ? 1. Convertir la imagen a escala de grises
            bgr_image = cv2.cvtColor(self.image, cv2.COLOR_RGBA2BGR)
            gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
            ret, bw_img = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
            rgba_bw = cv2.cvtColor(bw_img, cv2.COLOR_GRAY2RGBA)
            # ? 2. Emitir el resultado
            self.onSuccessfullyFinished.emit(rgba_bw)
        except Exception as e:
            self.onErrorCondition.emit(str(e))

class DistortionWorkerForBackgroundWork(QThread):
    # https://github.com/Eman-Bandesha/Wave-Effect-in-Images-using-OpenCV/blob/main/wave_efffects_using_opencv.ipynb
    #? Signals to emit the processed image
    onSuccessfullyFinished: pyqtSignal = pyqtSignal(np.ndarray)
    onErrorCondition: pyqtSignal = pyqtSignal(str)
    def __init__(self, image: np.ndarray, wave_amplitude: int = 10, wave_frequency: int = 10):
        super().__init__()
        self.image = image
        self.wave_amplitude = wave_amplitude
        self.wave_frequency = wave_frequency

    def run(self):
        try:
            # ? 1. Aplicar el efecto de distorsion
            rows, cols = self.image.shape[:2]
            map_y, map_x = np.indices((rows, cols), dtype=np.float32)
            map_x = map_x + self.wave_amplitude * np.sin(2 * np.pi * map_y / self.wave_frequency)
            distorted_image = cv2.remap(self.image, map_x, map_y, cv2.INTER_LINEAR)
            # ? 2. Emitir el resultado
            self.onSuccessfullyFinished.emit(distorted_image)
        except Exception as e:
            self.onErrorCondition.emit(str(e))