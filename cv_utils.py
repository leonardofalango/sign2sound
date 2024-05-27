import cv2
import time


font = cv2.FONT_HERSHEY_SIMPLEX
fps = 0
start = time.time()


def print(frame, text: str, x: int, y: int) -> None:
    cv2.putText(
        frame,
        text,
        (x, y),
        font,
        1,
        (255, 0, 0),
        2,
        cv2.LINE_AA,
    )


def print(frame, text: str, position: tuple[int, int]) -> None:
    cv2.putText(
        frame,
        text,
        position,
        font,
        1,
        (255, 0, 0),
        2,
        cv2.LINE_AA,
    )


def show_fps(frame, current):
    global start, fps
    if current - start > 1:
        fps = 60 / (current - start)
        start = time.time()
    print(frame, f"FPS: {fps:.2f}", (10, 30))
    return fps
