from PyQt5.QtGui import QImage
import numpy as np



class ImageToCVUtils:
    @staticmethod
    def helperQImageToOpenCV(image: QImage) -> np.ndarray:
        """Converts a QImage object to an OpenCV-compatible numpy array format.
        
        This method handles the transformation of Qt image formats to OpenCV format for image processing.
        It ensures proper color channel handling (RGBA8888) and creates a numpy array representation
        of the image data.
        
        Args:
            image (QImage): The source Qt image to be converted
            
        Returns:
            np.ndarray: A numpy array representing the image in RGBA format with shape (height, width, 4)
        """
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
    @staticmethod
    def helperOpenCVToQImage(cv_image: np.ndarray) -> QImage:
        """Converts an OpenCV numpy array to a QImage format.
        
        This method transforms an OpenCV-compatible numpy array into a Qt-compatible QImage
        for display purposes in the user interface. The conversion preserves the RGBA format
        and properly handles the image dimensions.
        
        Args:
            cv_image (np.ndarray): The source numpy array containing image data in RGBA format
            
        Returns:
            QImage: A Qt image object suitable for UI display
        """
        new_qimage_height, new_qimage_width = cv_image.shape[:2]
        new_qimage_from_array = QImage(cv_image.data, new_qimage_width, new_qimage_height, (4 * new_qimage_width),
                                       QImage.Format_RGBA8888)

        return new_qimage_from_array.copy()
