import sys
from PyQt6.QtWidgets import QApplication
from src.gui.main_window import VentanaPrincipal

def main():
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 