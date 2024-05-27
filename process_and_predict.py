import logging
import pandas as pd
import mediapipe as mp
import sklearn.preprocessing

mp_hands = mp.solutions.hands.Hands(
    max_num_hands=2,
)
mp_drawing = mp.solutions.drawing_utils
hands = mp.solutions.hands
x = [0 for init in range(21 * 3)]


def process_frame_and_predict(
    frame, model, normlizer: sklearn.preprocessing.StandardScaler = None
):
    predictions = []
    img = mp_hands.process(frame)
    if img.multi_hand_landmarks:
        logging.debug(img.multi_hand_landmarks)
        for hand_landmarks in img.multi_hand_landmarks:
            for lm_index in range(21):
                x[lm_index] = hand_landmarks.landmark[lm_index].x
                x[lm_index + 21] = hand_landmarks.landmark[lm_index].y
                x[lm_index + 21 * 2] = hand_landmarks.landmark[lm_index].z
            mp_drawing.draw_landmarks(frame, hand_landmarks, hands.HAND_CONNECTIONS)

            df = pd.DataFrame(x).T

            if normlizer is not None:
                df = normlizer.transform(df)

            predictions.append(model.predict(df)[0])
        return predictions
