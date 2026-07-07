from PySide6.QtWidgets import QApplication

from app.showroom.showroom_runtime import ShowroomRuntime

app = QApplication([])

runtime = ShowroomRuntime()

runtime.start()

print("Runtime Started")

print(runtime.state)

runtime.stop()

print("Runtime Stopped")