import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon

class MainWindow(QMainWindow):
    """
    Main window class for the application.
    This class handles the creation of the main window and provides functionality to minimize it to the system tray.
    """

    def __init__(self):
        super().__init__()
        
        # Set up the main window
        self.setWindowTitle("System Tray Example")
        self.setGeometry(100, 100, 400, 300)
        
        # Create a system tray icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(os.path.join(os.path.dirname(__file__), 'icon.png')))
        
        # Ensure the application has a native icon for the system tray
        if not QSystemTrayIcon.isSystemTrayAvailable():
            print("No system tray available.")
            sys.exit(1)
        
        self.tray_icon.show()
        
        # Create actions for the system tray menu
        show_action = QAction("Show", self)
        quit_action = QAction("Quit", self)
        
        show_action.triggered.connect(self.show_normal)
        quit_action.triggered.connect(QApplication.quit)
        
        # Set up the context menu for the system tray icon
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        
        # Connect the window's close event to minimize to tray
        self.closeEvent = self.minimize_to_tray

    def minimize_to_tray(self, event):
        """
        Event handler for minimizing the application to the system tray.
        :param event: QCloseEvent object representing the window close event.
        """
        if self.tray_icon.isVisible():
            self.hide()
            event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Ensure the application has a native icon for the system tray
    if not QSystemTrayIcon.isSystemTrayAvailable():
        print("No system tray available.")
        sys.exit(1)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())
