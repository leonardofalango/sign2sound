import cv2
import pickle
import logging
import warnings
import cv_utils
import process_and_predict
from fastapi.responses import StreamingResponse
from fastapi import FastAPI, Response

app = FastAPI()

warnings.filterwarnings("ignore")
logging.basicConfig(
    filename="var/logs/hand_detector.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("normalizer.pkl", "rb") as f:
    norm = pickle.load(f)


def process_frame(frame, width=640, height=480):
    pred = process_and_predict.process_frame_and_predict(frame, model, norm)
    cv_utils.print(frame, f"Prediction: {pred}", (width - 300, 30))

    return frame


# Rota para streaming de vídeo
@app.get("/video_feed")
def video_feed():
    cap = cv2.VideoCapture(0)  # Use 0 para a câmera padrão

    def video_generator():
        try:
            while cap.isOpened():
                ret, frame = cap.read()  # Lê um frame do vídeo

                if not ret:
                    break

                processed_frame = process_frame(frame)  # Processa o frame

                # Converte o frame processado para bytes
                ret, buffer = cv2.imencode(".jpg", processed_frame)
                frame_bytes = buffer.tobytes()

                # Envia o frame
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
                )

        finally:
            # Libera o objeto de captura
            cap.release()

    return StreamingResponse(
        video_generator(), media_type="multipart/x-mixed-replace; boundary=frame"
    )


@app.get("/")
async def main():
    content = """
<html>
    <head>
        <title>Amigo do Surdo</title>
    </head>
    
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
    </style>
        
    <body>
        <img src="/video_feed" style="width:100vw;height:100vh">
    </body>
</html>
    """
    try:
        return Response(content=content)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8080)
