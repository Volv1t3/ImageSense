#!-------------------------------------------
# * Descripcion del Contenido
# * @authors: Maria Granda Anazco, Santiago Arellano
# * @date: 13-Apr-2025
# * @description: El presente archivo implementa el main como una entrada principal para la aplicacion
# * de escritorio visual.
#!-------------------------------------------
import sys
from PyQt5.QtWidgets import QApplication
from Views.UIPanels.ImageSenseMainUI import ImageSenseMainUIApplication


def main()-> None:
    application: QApplication = QApplication([])
    window: ImageSenseMainUIApplication = ImageSenseMainUIApplication()
    window.show()
    sys.exit(application.exec())

if __name__ == '__main__':
    main();
