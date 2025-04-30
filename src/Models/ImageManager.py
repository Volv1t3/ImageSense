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
        """
        Handles the communication between the toolbar and image loading functionality. This method is responsible for loading
        an image from a specified file path and storing it in the application's internal image holders. The method performs
        various validation checks to ensure the image can be properly loaded and handled by the system.
    
        The method first validates if the provided path exists and is accessible. If the path is invalid, both internal
        image holders are set to None. If the path is valid, it attempts to load the image using QImage. If the initial
        loading fails, the method attempts to load the image using different formats (PNG, JPG, JPEG, BMP, TIFF) until
        successful. If no format works, the internal holders are set to None. On successful load, the image is stored
        in both internal holders through the _setter_internal_normal_image_holder method.
    
        Parameters:
            image_path (str): The file system path to the image that needs to be loaded.
    
        Returns:
            None
        """
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
        """
        Manages the saving functionality of images within the application. This method is responsible for storing
        the current preview image to a specified location in the user's file system. The method operates by checking
        if there is a valid image in the internal preview holder before attempting to save it.
    
        The method first validates the existence of an image in the internal preview holder. If an image exists,
        it proceeds to save it to the specified path using the QImage's built-in save functionality. Upon successful
        saving, it prints a confirmation message with the storage location. If no image is present in the preview
        holder, the method silently fails without performing any operation.
    
        Parameters:
            image_to_store_path (str): The complete file system path where the image should be saved, including
                                      the filename and extension.
    
        Returns:
            None
        """
        #? Guardamos la imagen directamente dentro del sistema del usuario, guardando la imagen de la preview interna
        if self.internal_preview_image_holder:
            self.internal_preview_image_holder.save(image_to_store_path)
            print(f'Image saved successfully at {image_to_store_path}')
    def connect_to_toolbar_clear_image_register(self):
        """
        Handles the clearing of image data within the application's image management system. This method is responsible for
        resetting both the normal and preview image holders to their initial state and notifying the application of this
        change. The method is typically triggered through the toolbar's clear functionality, providing a way to reset the
        application's image state.
    
        The method performs two primary operations: First, it clears both internal image holders by setting them to None,
        effectively removing any previously loaded images from memory. Second, it emits a signal to notify other parts of
        the application that the images have been cleared, allowing them to update their displays accordingly. This signal
        emission ensures that all components depending on the image data are properly synchronized after the clearing
        operation.
    
        Parameters:
            None
    
        Returns:
            None
        """
        self.internal_normal_image_holder = None
        self.internal_preview_image_holder = None
        self.image_manager_orders_image_and_preview_update_after_clearing_signal.emit()
    def connect_to_left_pane_modification_image_storage(self, image_from_exterior: QImage):
        """
        Manages the communication between the left pane modifications and the application's image storage system. This method 
        is responsible for updating the preview image holder with a modified image received from external image processing 
        operations, typically initiated from the left pane of the application interface.
    
        The method performs two primary operations: First, it updates the internal preview image holder with the new modified
        image while maintaining the original image in the normal image holder. This allows the application to maintain both 
        the original and modified versions of the image. Second, it emits a signal to notify other components of the 
        application about the preview image update, ensuring that all dependent components can update their displays 
        accordingly.
    
        Parameters:
            image_from_exterior (QImage): The modified image received from external processing operations that will replace
                                        the current preview image.
    
        Returns:
            None
        """
        self.internal_preview_image_holder = image_from_exterior
        self.image_manager_dictates_preview_image_update.emit(image_from_exterior)