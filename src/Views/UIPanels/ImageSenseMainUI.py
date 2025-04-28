#!-------------------------------------------
# * Descripcion del Contenido
# * @authors: Maria Granda Anazco, Santiago Arellano
# * @date: 13-Apr-2025
# * @description: El presente archivo implementa la interface visual principal, de la aplicacion, la idea de este archivo es
# * incluir un layout en el que se pueda enchufar las instancias de los diversos paneles directamente al programa principal
# * aqui.
# !-------------------------------------------
from PyQt5.QtWidgets import (QMainWindow, QToolBar, QPushButton, QLabel,
                             QVBoxLayout, QWidget, QSplitter,
                             QSizePolicy, QHBoxLayout)
from PyQt5.QtCore import Qt, QSize

import Views.UIPanels.ImagePreviewCenterPane as centerPane
import Views.UIPanels.ImageAnalysisRightPane as rightPane
import Views.UIPanels.ImageModificationLeftPane as leftPane
from Models.ImageManager import ImageManager
from Models.styles import Styles
from Views.CustomWidgets.CustomToolbar import CustomToolbar
from Views.UIPanels.ImageModificationLeftPane import LeftSideImageModificationPane
from Views.UIPanels.ImagePreviewCenterPane import CenterSidePreview


class ImageSenseMainUIApplication(QMainWindow):

    def __init__(self):
        super().__init__()
        self.imageManager: ImageManager = ImageManager()
        self.centralWidgetForLayouts: QWidget = QWidget()
        self.centralWidgetForLayouts.setStyleSheet("background-color: #BED6DF;")
        self.setCentralWidget(self.centralWidgetForLayouts)
        self.__init_UI__()
        self.__connect_signals_from_toolbar__()

    def __init_UI__(self):
        #? 1. En primera instancia, definimos el tamano de la UI en general, definiendo titulos.
        self.setWindowTitle("ImageSense ― Analyze and Modify your Images")
        self.setBaseSize(1024,768); self.setMinimumSize(1024,768)
        self.setObjectName("ImageSenseMainUIApplication")

        #? Definimos un widget para manejar el layout general de la aplicacion.
        vBoxForGeneralLayout: QVBoxLayout = QVBoxLayout(self)
        vBoxForGeneralLayout.setSpacing(20)
        vBoxForGeneralLayout.setContentsMargins(10, 10, 10, 10)
        vBoxForGeneralLayout.setAlignment(self, Qt.AlignVCenter)
        vBoxForGeneralLayout.setDirection(QVBoxLayout.Direction.TopToBottom)
        toolbarForApplication: CustomToolbar = CustomToolbar()
        vBoxForGeneralLayout.addWidget(toolbarForApplication)

        #? Definimos un widget de tipo HBOX para definir los paneles internos de la aplicacion
        panelsWidget: QWidget = QWidget()
        hBoxForPanelSection: QHBoxLayout = QHBoxLayout(panelsWidget)
        hBoxForPanelSection.setSpacing(20)

        #? 2. Definimos internamente en el widget tres widgets distintos para manejar cada uno de las layouts
        self.leftPanel: QWidget = LeftSideImageModificationPane()
        self.leftPanel.setStyleSheet("background-color: #2C3E50;")  # Dark blue
        self.leftPanel.setMinimumWidth(325)
        self.leftPanel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        self.middlePanel = CenterSidePreview()
        self.middlePanel.setStyleSheet("background-color: #34495E;")  # Slightly lighter blue
        self.middlePanel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)


        self.rightPanel = rightPane.RightSideImageAnalysisPane()
        self.rightPanel.setStyleSheet("background-color: #1A2530;")  # Darker blue
        self.rightPanel.setMinimumWidth(325)
        self.rightPanel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)


        hBoxForPanelSection.addWidget(self.leftPanel)
        hBoxForPanelSection.addWidget(self.middlePanel)
        hBoxForPanelSection.addWidget(self.rightPanel)

        hBoxForPanelSection.setStretchFactor(self.leftPanel, 3)
        hBoxForPanelSection.setStretchFactor(self.middlePanel, 4)
        hBoxForPanelSection.setStretchFactor(self.rightPanel, 3)

        vBoxForGeneralLayout.addWidget(panelsWidget)

        self.centralWidget().setLayout(vBoxForGeneralLayout)

    def __connect_signals_from_toolbar__(self) -> None:
        #? 1. Nos Conectamos al toolbar para manejar sus eventos
        toolbarInApplication = self.findChild(CustomToolbar)
        if toolbarInApplication:
            #? 1.1 Conectamos el listener del imageManager para cargar la imagen del sistema del usuario.
            toolbarInApplication.image_opened_signal.connect(self.imageManager.connect_to_toolbar_image_url_communication)

            #? 1.2 Conectamos el ResetActualImageAndPrevi method del middle pane para restablecer las vistas de la app
            toolbarInApplication.reset_preview_image_signal.connect(self.middlePanel.resetActualImageAndPreview)
            toolbarInApplication.reset_preview_image_signal.connect(self.imageManager.connect_to_toolbar_clear_image_register)
            #? 1.3 Conectamos el listener para el ImageManager para guardar la imagen de la preview
            toolbarInApplication.image_saved_signal.connect(self.imageManager.connect_to_toolbar_save_image_information)
        #? 2. Conectamos los listeners del imageManager para que este tambien pueda comunicarse con el sistema externo
        #? especificamente para mandar senales cuando imagen se carga
        if self.imageManager:
            #? 2.1 Conectamos un listener en el caso de tener una imagen cargada en el sistema para actualizacion de graficos
            (self.imageManager.image_manager_dictates_preview_image_update \
             .connect(self.middlePanel.updatePreviewImage))
            (self.imageManager.image_manager_orders_image_and_preview_update_after_clearing_signal
             .connect(self.middlePanel.resetActualImageAndPreview))
            (self.imageManager.image_manager_dictates_actual_image_update.connect(self.middlePanel.updateDisplay))
        #? 3. Nos conectamos al Layout izquierdo, es decir, tenemos que conectar listeners para manejar los cambios de la UI
        leftSidePanelInApplication = self.findChild(leftPane.LeftSideImageModificationPane)
        if leftSidePanelInApplication:
            leftSidePanelInApplication.preview_image_needs_to_be_updated.connect(self.middlePanel.updatePreviewImage)
            leftSidePanelInApplication.preview_image_needs_to_be_updated.connect(self.imageManager.connect_to_left_pane_modification_image_storage)

        #? 4. Nos conectamos con el right side para receptar el cambio
        rightSidePanelInApplication = self.findChild(rightPane.RightSideImageAnalysisPane)
        if rightSidePanelInApplication:
            rightSidePanelInApplication.preview_image_needs_to_be_updated.connect(self.imageManager.connect_to_left_pane_modification_image_storage)
            rightSidePanelInApplication.preview_image_needs_to_be_updated.connect(self.middlePanel.updatePreviewImage)
