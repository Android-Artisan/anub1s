from PyQt6.QtCore import QPropertyAnimation, QEasingCurve

def fade_in(widget, duration=500):
    widget.setWindowOpacity(0)
    widget.show()
    anim = QPropertyAnimation(widget, b"windowOpacity")
    anim.setDuration(duration)
    anim.setStartValue(0)
    anim.setEndValue(1)
    anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
    anim.start()
    widget._animation = anim  # keep reference alive

def fade_out(widget, duration=500):
    anim = QPropertyAnimation(widget, b"windowOpacity")
    anim.setDuration(duration)
    anim.setStartValue(1)
    anim.setEndValue(0)
    anim.setEasingCurve(QEasingCurve.Type.InOutQuad)

    def on_finished():
        widget.hide()
        anim.deleteLater()

    anim.finished.connect(on_finished)
    anim.start()
    widget._animation = anim

