#!-------------------------------------------
# * Descripcion del Contenido
# * @authors: Maria Granda Anazco, Santiago Arellano
# * @date: 15-Apr-2025
# * @description: El presente archivo implementa la base de un Singleton para el manejo de imagenes dentro de la aplicacion.
# * La idea de esta clase es tener internamente las imagenes definidas por el usuario y un registro de aquellas imagenes que
# * tienen que ser guardadas dentro de la app
# !-------------------------------------------
import os

from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QBitmap, QImage


class ImageManager(QObject):
    Instance = None
    image_manager_dictates_preview_image_update: pyqtSignal = pyqtSignal(QImage)
    image_manager_dictates_actual_image_update: pyqtSignal = pyqtSignal(QImage)
    image_manager_orders_image_and_preview_update_after_clearing_signal: pyqtSignal = pyqtSignal()
    def __new__(cls, *args, **kwargs):
        """ Metodo base usado para manejar la creacion de un singleton o
        el regreso de informacion hacia el programa"""
        if not cls.Instance:
            cls.Instance = super(ImageManager, cls).__new__(cls)
        return cls.Instance

    def __init__(self):
        super().__init__()
        self.internal_normal_image_holder: QImage = None
        self.internal_preview_image_holder: QImage = None
    #? 1. Metodos para manejar la carga de imagenes al sistema
    def connect_to_toolbar_image_url_communication(self, image_path: str) -> None:
        if not image_path or not os.path.exists(image_path):
            self.internal_preview_image_holder = None
            self.internal_preview_image_holder = None
            print(f'Error: No image was loaded on incorrect url {image_path}')
            return
        #? Cargamos la imagen para ver si esta es nula o no
        image = QImage(image_path)
        if image.isNull():
            formats = ["PNG", "JPG", "JPEG", "BMP", "TIFF"]
            for fmt in formats:
                image = QImage(image_path, fmt)
                if not image.isNull():
                    break
        if image.isNull():
            print(f'Error: No image was loaded on incorrect url {image_path}')
            self.internal_normal_image_holder = None;
            self.internal_preview_image_holder = None;
            return
        else:
            self._setter_internal_normal_image_holder(image)
    def _setter_internal_normal_image_holder(self, image_from_exterior: QImage):
        """
        Este metodo permite settear una imagen dentro de los campos internos del singleton para
        que esta pueda ser accessible dentro de toda la aplicacion. La idea de esto es tener un solo
        punto de carga para la imagen al sistema
        :param image_from_exterior: Imagen cargada dentro del sistema a traves de un metodo adicional
        :return:
        """
        self.internal_normal_image_holder = image_from_exterior
        self.internal_preview_image_holder = image_from_exterior
        self.image_manager_dictates_preview_image_update.emit(image_from_exterior)
        self.image_manager_dictates_actual_image_update.emit(image_from_exterior)

    def connect_to_toolbar_save_image_information(self, image_to_store_path: str):
        #? Guardamos la imagen directamente dentro del sistema del usuario, guardando la imagen de la preview interna
        if self.internal_preview_image_holder:
            self.internal_preview_image_holder.save(image_to_store_path)
            print(f'Image saved successfully at {image_to_store_path}')
    def connect_to_toolbar_clear_image_register(self):
        self.internal_normal_image_holder = None
        self.internal_preview_image_holder = None
        self.image_manager_orders_image_and_preview_update_after_clearing_signal.emit()
    def connect_to_left_pane_modification_image_storage(self, image_from_exterior: QImage):
        self.internal_preview_image_holder = image_from_exterior
        self.image_manager_dictates_preview_image_update.emit(image_from_exterior)