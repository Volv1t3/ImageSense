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
    """Initializes and launches the ImageSense desktop application.
    
    This function serves as the entry point for the ImageSense application. It performs
    the following operations:
    1. Creates a QApplication instance for managing the application lifecycle
    2. Instantiates the main application window
    3. Displays the window
    4. Enters the application's main event loop
    
    The function will block until the application is terminated, at which point it ensures
    a clean shutdown through sys.exit().
    
    Returns:
        None: This function doesn't return explicitly, it exits the program through sys.exit()
    """
    application: QApplication = QApplication([])
    window: ImageSenseMainUIApplication = ImageSenseMainUIApplication()
    window.show()
    sys.exit(application.exec())

if __name__ == '__main__':
    main();
