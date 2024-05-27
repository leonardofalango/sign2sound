import cv2
import time
import pickle
import logging
import warnings
import cv_utils
import process_and_predict
from collections import Counter

warnings.filterwarnings("ignore")
running = True

TAM = 15
TOLERANCE = 5
LETTER_WIDTH = 20


word = ""
last_letters = ['' for x in range(TAM)]
index_letter = 0

most_common_letter = ''
logging.basicConfig(
    filename="var/logs/hand_detector.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)

try:
    cap = cv2.VideoCapture(0)
    _, frame = cap.read()
    logging.info("Camera is ready")

    camera_width = frame.shape[1]
    camera_height = frame.shape[0]
except Exception as e:
    logging.error(e)


with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("normalizer.pkl", "rb") as f:
    norm = pickle.load(f)


logging.info("Application is running")
while running:
    current = time.time()
    ret, frame = cap.read()
    if ret == False:
        break

    if index_letter == TAM:
        counter = Counter(last_letters)
        most_common_letter, count = counter.most_common()[0]
        index_letter = 0

        if most_common_letter is not None and count >= 10:
            if len(word) == 0:
                word += most_common_letter
            if most_common_letter != word[-1] and most_common_letter != word[-1]:
                word += most_common_letter

    pred = process_and_predict.process_frame_and_predict(frame, model, norm)
    last_letters[index_letter] = pred[0] if pred is not None else pred
    index_letter += 1

    padding_right = 120 + (len(word) * LETTER_WIDTH)
    cv_utils.print(frame, f"Word: {word}", (camera_width - padding_right, 30))
    cv_utils.print(frame, f"Letter: {last_letters[index_letter - 1]}", (camera_width - 175, 70))

    cv_utils.show_fps(frame, current)

    cv2.imshow("Sign2Sound", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        running = False

cap.release()
cv2.destroyAllWindows()
