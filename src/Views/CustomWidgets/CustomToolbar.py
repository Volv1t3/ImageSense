#!-------------------------------------------
# * Descripcion del Contenido
# * @authors: Maria Granda Anazco, Santiago Arellano
# * @date: 13-Apr-2025
# * @description: El presente archivo implementa la base del layout entero de la toolbar creada para la aplicacion, dado
# * que no es un diseno convencional, no podemos usar la toolbar creada por la ventana de PyQt, sino que vamos a usar una
# * propia
# !-------------------------------------------
import os

from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5.QtWidgets import QWidget, QSizePolicy, QHBoxLayout, QPushButton, QLabel, QMenu, QAction, QFileDialog

from Models.styles import Styles


class CustomToolbar(QWidget):
    """
    A custom toolbar widget that provides file and preview control functionality.
    
    This class implements a custom toolbar with buttons for file operations and image preview controls.
    It emits signals for image operations that can be intercepted by the main UI.
    
    Signals:
        image_opened_signal (str): Emitted when an image is opened, contains the file path
        image_saved_signal (str): Emitted when an image is saved, contains the file path
        reset_preview_image_signal: Emitted when the preview image needs to be reset
    """
    image_opened_signal: pyqtSignal = pyqtSignal(str)
    image_saved_signal: pyqtSignal = pyqtSignal(str)
    reset_preview_image_signal: pyqtSignal = pyqtSignal()

    def __init__(self):
        """
        Initialize the CustomToolbar widget.
        
        Calls the parent class constructor and initializes the UI components.
        """
        super().__init__()
        self.__init_UI__()

    def __init_UI__(self):
        """
        Initialize the user interface components of the toolbar.
    
        This method sets up the main UI components including:
        - Setting size policy and styles
        - Creating and configuring file control buttons and menus
        - Creating and configuring preview control buttons and menus
        - Setting up the layout and adding the application title
    
        The toolbar layout consists of two main buttons (File Controls and Preview Controls)
        aligned to the left, and the application name "ImageSense" aligned to the right.
        """
        #? 1. Inicializamos la UI de la toolbar definiendo las caracteristicas principales de la vista
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.setStyleSheet(Styles.FlOATING_TOOLBAR)
        #? 2. Inicializamos los botones y un layout para el manejo de los botones
        widgetForButtons: QWidget = QWidget()
        layoutForButtonsAndText: QHBoxLayout = QHBoxLayout(widgetForButtons)
        layoutForButtonsAndText.setContentsMargins(10, 20, 10, 20)
        layoutForButtonsAndText.setObjectName("CustomToolbar")

        self.buttonForFileControl: QPushButton = QPushButton("File Controls")
        self.buttonForFileControl.setStyleSheet(Styles.BUTTON_PRIMARY_NOT_PRESSED)

        #? 2.1 Le creamos un menu con opciones para cargar y guardar una imagen al boton principal de file controls
        self.menuForFileControl: QMenu = QMenu(self)
        self.menuForFileControl.setStyleSheet(Styles.Q_MENU_FOR_ITEMS)

        self.open_image_action: QAction = QAction("Open Image From Disk", self)
        self.save_image_action: QAction = QAction("Save Image To Disk", self)
        self.menuForFileControl.addAction(self.open_image_action)
        self.menuForFileControl.addSeparator()
        self.menuForFileControl.addAction(self.save_image_action)
        #? 2.1.1 Conectamos un listener para mostrar el menu
        self.buttonForFileControl.clicked.connect(self.mostrarMenuAlUsuario)
        #? 2.1.2 Conectamos liteners para cada accion para manejar la opcion del usuasrio
        self.open_image_action.triggered.connect(self.abrirImagenDelUsuario)
        self.save_image_action.triggered.connect(self.guardarImagenDelUsuario)

        #? 2.2.Le creamos un menu de opciones a la preview de la imagen
        self.buttonForPreviewControl: QPushButton = QPushButton("Preview Controls")
        self.buttonForPreviewControl.setStyleSheet(Styles.BUTTON_PRIMARY_NOT_PRESSED)
        self.menuForPreviewControl: QMenu = QMenu(self)
        self.menuForPreviewControl.setStyleSheet(Styles.Q_MENU_FOR_ITEMS)
        self.reset_preview_image_action: QAction = QAction("Reset Preview Image", self)
        self.reset_preview_image_action.triggered.connect(self.buttonForPreviewControlHandler)
        self.buttonForPreviewControl.clicked.connect(self.mostrarPreviewMenuAlUsuario)
        self.menuForPreviewControl.addAction(self.reset_preview_image_action)
        layoutForButtonsAndText.addWidget(self.buttonForFileControl)
        layoutForButtonsAndText.addWidget(self.buttonForPreviewControl)

        layoutForButtonsAndText.addStretch(1)

        self.rightTextLabel: QLabel = QLabel("ImageSense")
        self.rightTextLabel.setStyleSheet(Styles.LABEL_TOOLBAR_TEXT)

        layoutForButtonsAndText.addWidget(self.rightTextLabel)

        self.setLayout(layoutForButtonsAndText)

    def mostrarPreviewMenuAlUsuario(self) -> None:
        """
        Display the preview control menu to the user.
        
        Shows a popup menu below the preview control button with options for managing the preview image.
        The menu appears at the bottom-left corner of the preview control button.
    
        Returns:
            None
        """
        position = self.buttonForPreviewControl.mapToGlobal(self.buttonForPreviewControl.rect().bottomLeft())
        self.menuForPreviewControl.popup(position)
    def mostrarMenuAlUsuario(self) -> None:
        """
        Display the file control menu to the user.
        
        Shows a popup menu below the file control button with options for opening and saving images.
        The menu appears at the bottom-left corner of the file control button.
    
        Returns:
            None
        """
        position = self.buttonForFileControl.mapToGlobal(self.buttonForFileControl.rect().bottomLeft())
        self.menuForFileControl.popup(position)


    def guardarImagenDelUsuario(self) -> None:
        """
        Save the current image to disk.
        
        Opens a file dialog allowing the user to select a location and filename to save the image.
        Supports PNG, JPG, and JPEG formats. If no extension is provided, defaults to PNG.
        
        The method will emit image_saved_signal with the selected file path when a file is successfully selected.
    
        Returns:
            None
    
        Signals:
            image_saved_signal (str): Emitted with the selected save file path
        """
        fileDialogForSavingImage = QFileDialog(self,
                                               "Guardar la imagen modificada como...",
                                               os.path.expanduser('~'))

        fileDialogForSavingImage.setFileMode(QFileDialog.FileMode.AnyFile)
        fileDialogForSavingImage.setNameFilter("Image Files (*.png *.jpg *.jpeg)")
        fileDialogForSavingImage.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)

        fileDialogForSavingImage.setDefaultSuffix("png")

        if fileDialogForSavingImage.exec() == QFileDialog.DialogCode.Accepted:
            selectedFileNames = fileDialogForSavingImage.selectedFiles()
            selectedFilePath = selectedFileNames[0]

            if len(selectedFilePath) > 0:
                _, extension = os.path.splitext(selectedFilePath)
                if not extension:
                    selectedFilePath += '.png'
                print(selectedFilePath)
                self.image_saved_signal.emit(selectedFilePath)

    def abrirImagenDelUsuario(self) -> None:
        """
        Open an image file from disk.
        
        Opens a file dialog allowing the user to select an image file to open.
        Supports PNG, JPG, and JPEG formats. The dialog starts in the user's home directory.
        
        The method will emit image_opened_signal with the selected file path when a file is successfully selected.
    
        Returns:
            None
    
        Signals:
            image_opened_signal (str): Emitted with the selected image file path
        """
        fileDialogToOpenImage = QFileDialog(self,
                                               "Guardar la imagen modificada como...",
                                               os.path.expanduser('~'))

        fileDialogToOpenImage.setFileMode(QFileDialog.FileMode.ExistingFile)
        fileDialogToOpenImage.setNameFilter("Image Files (*.png *.jpg *.jpeg)")
        fileDialogToOpenImage.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)

        fileDialogToOpenImage.setDefaultSuffix("png")

        if fileDialogToOpenImage.exec() == QFileDialog.DialogCode.Accepted:
            selectedFileNames = fileDialogToOpenImage.selectedFiles()
            selectedFilePath = selectedFileNames[0]

            if len(selectedFilePath) > 0:
                _, extension = os.path.splitext(selectedFilePath)
                if not extension:
                    selectedFilePath += '.png'
                print(selectedFilePath)
                self.image_opened_signal.emit(selectedFilePath)
    def buttonForPreviewControlHandler(self) -> None:
        """
        Handle the preview control button action.
        
        This method is called when the reset preview option is selected from the preview control menu.
        Emits the reset_preview_image_signal to reset the preview image to its original state.
    
        Returns:
            None
    
        Signals:
            reset_preview_image_signal: Emitted to trigger preview image reset
        """
        self.reset_preview_image_signal.emit()