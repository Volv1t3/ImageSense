from PyQt5.QtGui import QImage
import numpy as np



class ImageToCVUtils:
    @staticmethod
    def helperQImageToOpenCV(image: QImage) -> np.ndarray:
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
    @staticmethod
    def helperOpenCVToQImage(cv_image: np.ndarray) -> QImage:
        """Method defined such that our project is capable of converting between a modifid nd array into a
        UI friendly QImage such that it can be displayed on the user's side."""
        new_qimage_height, new_qimage_width = cv_image.shape[:2]
        new_qimage_from_array = QImage(cv_image.data, new_qimage_width, new_qimage_height, (4 * new_qimage_width),
                                       QImage.Format_RGBA8888)

        return new_qimage_from_array.copy()
