import sys
from PyQt5.Qt import *

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("第一个py程序")
window.resize(500, 500)
window.move(400, 250)

lable = QLabel(window)
lable.setText("Hello world")
lable.move(200, 240)
window.show()
sys.exit(app.exec_())
