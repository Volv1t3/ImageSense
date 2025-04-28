#!-------------------------------------------
# * Descripcion del Contenido
# * @authors: Maria Granda Anazco, Santiago Arellano
# * @date: 17-Apr-2025
# * @description: El presente archivo incluye algunos de los estilos compartidos de la Main UI como constantes para
# * en diversos sectores de la UI principal de la aplicacion.
# !-------------------------------------------
class Styles:


    FlOATING_TOOLBAR: str = \
    """
    #CustomToolbar, CustomToolbar
 {
            background-color: #273B65 !important;
            margin-top: 20px;
            margin-left: 10px;
            margin-right: 10px;
            border: none;
            border-radius: 16px;
            vertical-align: center;
            align-items: start;
        }

    """

    LABEL_TOOLBAR_TEXT: str = \
    """
    QLabel {
         background-color: #273B65;
         color: #BED6DF;
         font-family: sans-serif, 'Microsoft JhengHei UI';
         font-size: 16px;
         font-weight: bold;
         text-align: center;
          border-radius: 16px;
        padding: 10px 20px;
    }
    """


    BUTTON_PRIMARY_NOT_PRESSED: str = \
        """
        QPushButton {
            background-color: #273B65;
            color: #BED6DF;
            border: none;
            border-radius: 16px;
            padding: 10px 20px;
            font-size: 14px;
            font-weight: bold;
            font-family: 'Microsoft JhengHei UI', sans-serif;
        }
        
        QPushButton:hover {
            background-color: #17223b;
            color: #BED6DF;
            
        }
        
        QPushButton:pressed {
             background-color: #283c66;
            color: #BED6DF;
            padding-top: 12px;
            padding-bottom: 8px;
        }
        """

    Q_MENU_FOR_ITEMS: str = \
        """
                QMenu {
                    background-color: #273B65;
                    color: #BED6DF;
                    border: none;
                    border-radius: 16px;
                    padding: 5px;
                    font-family: 'Microsoft JhengHei UI', sans-serif;
                    
                }
    
                QMenu::item {
                    background-color: #273B65;
                    color: #BED6DF;
                    padding: 8px 20px;
                    margin: 2px;
                    border-radius: 6px;
                    font-family: 'Microsoft JhengHei UI', sans-serif;
                    
                }
    
                QMenu::item:selected {
                    background-color: #17223b;
                }
    
                QMenu::item:pressed {
                    background-color: #283c66;
                }
    
                QMenu::separator {
                    height: 1px;
                    background-color: #BED6DF;
                    margin: 5px 10px;
                }
                """
