import cv2
import numpy as np

class DetectaMovCamara:
    def __init__(self):
        self.prevFrame = None
        self.prevCenter = None

    def detectarMovimiento(self):
        # Abrir la cámara
        capture = cv2.VideoCapture(0)
        if not capture.isOpened():
            print("No se pudo abrir la cámara")
            return

        while True:
            ret, frame = capture.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            if self.prevFrame is None:
                self.prevFrame = gray
                continue

            frameDelta = cv2.absdiff(self.prevFrame, gray)
            thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

            contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                if cv2.contourArea(contour) < 500:
                    continue
                (x, y, w, h) = cv2.boundingRect(contour)
                center = (x + w / 2, y + h / 2)

                if self.prevCenter is None:
                    self.prevCenter = center
                    continue

                dx = center[0] - self.prevCenter[0]
                dy = center[1] - self.prevCenter[1]

                if abs(dx) > 2 and abs(dy) > 2:
                    direction = "movimiento en diagonal hacia " + ("abajo y a la derecha" if dx > 0 and dy > 0 else "arriba y a la derecha" if dx > 0 else "abajo y a la izquierda" if dy > 0 else "arriba y a la izquierda")
                elif abs(dx) > 2:
                    direction = "movimiento hacia la " + ("derecha" if dx > 0 else "izquierda")
                elif abs(dy) > 2:
                    direction = "movimiento hacia " + ("abajo" if dy > 0 else "arriba")

                print(direction)
                self.prevCenter = center

            self.prevFrame = gray
        capture.release()
        return direction
    
    
    def mostrarCamara(self):
        print ("Mostrando camara")
        #cv2.destroyAllWindows()