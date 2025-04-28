#!-------------------------------------------
# * Descripcion del Contenido
# * @authors: Maria Granda Anazco, Santiago Arellano
# * @date: 13-Apr-2025
# * @description: El presente archivo una clase estandar de PyQT5 que permite generar y
# * controlar una vista completa dentro de la aplicacion. La idea de este archivo es contener la clase estandar que define
# * el layout general para el centro de la app, es decir la seccion en donde tiene que verse la base del layout y de los
# * previews de las imagenes generadas internamente
#!-------------------------------------------
import os

from PyQt5.QtCore import pyqtSignal, Qt, QSize, QEvent
from PyQt5.QtGui import QBitmap, QImage, QPixmap, QResizeEvent
from PyQt5.QtHelp import QHelpLink
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QSizePolicy, QLabel)


class CenterSidePreview(QWidget):

    def __init__(self):
        super().__init__()
        self.actual_image: QImage = None
        self.transformed_image: QImage = None
        self.__init_UI__()
    def __init_UI__(self) -> None:
        """
        Este metodo se encarga de definir el formato de la UI interna para el panel del centro, la idea es seguir un layout
        prestablecido en donde se tiene dos imagenes, la primera imagen representa la entrada y la segunda la salida
        """
        self.mainLayoutWidget = QWidget(self)
        self.mainLayoutWidget.setMinimumWidth(325)
        self.mainLayoutWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.mainLayoutWidget.setStyleSheet("""
            QWidget {
                background-color: #273B65;
                border-radius: 16px;
                padding: 10px 10px;
            }
        """)

        self.layout_for_Images = QVBoxLayout(self.mainLayoutWidget)
        self.layout_for_Images.setDirection(QVBoxLayout.Direction.TopToBottom)
        self.layout_for_Images.setSpacing(15)
        self.layout_for_Images.setContentsMargins(20, 20, 20, 20)

        self.original_image_container = QWidget()
        self.original_image_container.setMinimumHeight(250)
        self.original_image_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.original_image_container.setStyleSheet("""
            QWidget {
                background-color: #BED6DF;
                border-radius: 30px;
            }
        """)

        original_image_layout = QVBoxLayout(self.original_image_container)
        original_image_layout.setContentsMargins(10, 10, 10, 10)
        original_image_layout.setAlignment(Qt.AlignCenter)

        self.original_image_label = QLabel("No Image Loaded")
        self.original_image_label.setAlignment(Qt.AlignCenter)
        self.original_image_label.setStyleSheet("""
            QLabel {
                color: #273B65;
                font-size: 18px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        self.original_image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        original_image_layout.addWidget(self.original_image_label)

        self.layout_for_Images.addWidget(self.original_image_container)

        self.transformation_message = QLabel("was transformed into")
        self.transformation_message.setAlignment(Qt.AlignCenter)
        self.transformation_message.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
                font-style: normal;
                background-color: transparent;
            }
        """)

        self.layout_for_Images.addWidget(self.transformation_message)

        self.transformed_image_container = QWidget()
        self.transformed_image_container.setMinimumHeight(250)
        self.transformed_image_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.transformed_image_container.setStyleSheet("""
            QWidget {
                background-color: #BED6DF;
                border-radius: 30px;
            }
        """)


        transformed_image_layout = QVBoxLayout(self.transformed_image_container)
        transformed_image_layout.setContentsMargins(10, 10, 10, 10)
        transformed_image_layout.setAlignment(Qt.AlignCenter)

        self.transformed_image_label = QLabel("No Image Preview")
        self.transformed_image_label.setAlignment(Qt.AlignCenter)
        self.transformed_image_label.setStyleSheet("""
            QLabel {
                color: #273B65;
                font-size: 18px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        self.transformed_image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        transformed_image_layout.addWidget(self.transformed_image_label)

        self.layout_for_Images.addWidget(self.transformed_image_container)

        self.layout_for_Images.setStretchFactor(self.original_image_container, 10)
        self.layout_for_Images.setStretchFactor(self.transformation_message, 1)
        self.layout_for_Images.setStretchFactor(self.transformed_image_container, 10)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.mainLayoutWidget)

        self.setLayout(main_layout)

    def resizeEvent(self, a0: QResizeEvent):
        super().resizeEvent(a0)

        #? 1. Si tenemos cargada una imagen entonces intentemos cambiar su tamano
        if self.actual_image and not self.actual_image.isNull():
            container_size = self.original_image_container.size()
            display_size = QSize(container_size.width() - 20, container_size.height() - 20)
            pixmap_from_original_image = QPixmap.fromImage(self.actual_image)
            scaled_pixmap = pixmap_from_original_image.scaled(
                display_size,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.original_image_label.setPixmap(scaled_pixmap)
        if self.transformed_image and not self.transformed_image.isNull():
            container_size = self.transformed_image_container.size()
            display_size = QSize(container_size.width() - 20, container_size.height() - 20)
            pixmap_from_transformed_image = QPixmap.fromImage(self.transformed_image)
            scaled_pixmap = pixmap_from_transformed_image.scaled(
                display_size,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.transformed_image_label.setPixmap(scaled_pixmap)


    def updateDisplay(self, preview_image_from_the_outide: QImage) -> None:
        if preview_image_from_the_outide and not preview_image_from_the_outide.isNull():
            print(f"Displaying image: {preview_image_from_the_outide.width()}x{preview_image_from_the_outide.height()}")
            self.actual_image = preview_image_from_the_outide
            self.transformed_image = preview_image_from_the_outide
            pixmap = QPixmap.fromImage(preview_image_from_the_outide)
            container_size = self.original_image_container.size()
            display_size = QSize(container_size.width(), container_size.height())
            scaled_pixmap = pixmap.scaled(
                display_size,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.original_image_label.setPixmap(scaled_pixmap)
            self.transformed_image_label.setPixmap(scaled_pixmap)
            self.original_image_label.setText("")
            self.original_image_label.setAlignment(Qt.AlignCenter)
        else:
            self.original_image_label.setText("No Image Loaded")
            self.transformed_image_label.setText("No Image Preview")

    def resetActualImageAndPreview(self) -> None:
        """
        Este metodo se encarga de resetear la imagen actual y la
        imagen de preview, ademas de actualizar el texto de los
        labels de las imagenes.
        """
        self.original_image_label.setText("No Image Loaded")
        self.transformed_image_label.setText("No Image Preview")
        self.updateDisplay(None)
    def updatePreviewImage(self, image: QImage):
        """
        Este metodo se encarga de actualizar la imagen de preview, ademas de actualizar el texto de los labels de las
        imagenes.
        """
        if image and not image.isNull():
            self.transformed_image = image
            pixmap = QPixmap.fromImage(image)
            container_size = self.original_image_container.size()
            display_size = QSize(container_size.width(), container_size.height())
            scaled_pixmap = pixmap.scaled(
                display_size,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.transformed_image_label.setPixmap(scaled_pixmap)
            self.original_image_label.setText("")
            self.original_image_label.setAlignment(Qt.AlignCenter)
        else:
            self.original_image_label.setText("No Image Loaded")
            self.transformed_image_label.setText("No Image Preview")
