import os
import pathlib
from typing import List

import numpy as np
from PIL.Image import Image
from ultralytics import YOLO
from ultralytics.engine.results import Results

from ocr.word_representations import ImageSegment, Segment

model = YOLO(
    os.path.join(
        pathlib.Path(__file__).parent.resolve(),
        "..",
        "machine_learning_models",
        "text_detection",
        "onnx",
        "v2.onnx"
    ), task="detect")


def get_word_segments(img: Image) -> List[ImageSegment]:
    img = img.convert("RGB")
    results: List[Results] = model(img, conf=0.5)  # results list

    word_box_list: List[ImageSegment] = []
    for r in results:
        for box in r.boxes:
            coordinates = box.xyxy.tolist()[0]
            word_box_list.append(
                ImageSegment(
                    x1=coordinates[0],
                    y1=coordinates[1],
                    x2=coordinates[2],
                    y2=coordinates[3],
                    image=img))

    return word_box_list


def _get_words_in_area(area: Segment, words: List[ImageSegment]) -> List[ImageSegment]:
    return [w for w in words if area.x1 <= w.x1 <= area.x2 and area.y1 <= w.y1 <= area.y2]


def _get_average_segment_height(words: List[ImageSegment]) -> int:
    heights = [abs(w.y2 - w.y1) for w in words]
    return int(sum(heights) / len(heights))


def get_line_segments(img: Image, words: List[ImageSegment]) -> List[ImageSegment]:
    scan_height = _get_average_segment_height(words)
    all_words = words.copy()
    prev_words_in_scan_area: List[ImageSegment] = []
    line_segments: List[ImageSegment] = []
    for i in range(img.height - scan_height):
        words_in_scan_area = _get_words_in_area(
            Segment(x1=0, y1=i, x2=img.width, y2=i + scan_height),
            all_words
        )
        if len(words_in_scan_area) > len(prev_words_in_scan_area):
            prev_words_in_scan_area = words_in_scan_area
        elif len(words_in_scan_area) < len(prev_words_in_scan_area):
            avg_y2 = (int(sum(w.y2 for w in prev_words_in_scan_area)) / len(prev_words_in_scan_area))
            line_segments.append(ImageSegment(
                x1=(min(w.x1 for w in prev_words_in_scan_area)),
                y1=(min(w.y1 for w in prev_words_in_scan_area)),
                x2=(max(w.x2 for w in prev_words_in_scan_area)),
                y2=(int(avg_y2)),
                image=img))
            all_words = [w for w in all_words if w not in prev_words_in_scan_area]
            prev_words_in_scan_area = []

    return line_segments


def get_line_separated_word_segments(img: Image, words: List[ImageSegment]) -> List[List[ImageSegment]]:
    scan_height = _get_average_segment_height(words)
    all_words = words.copy()
    prev_words_in_scan_area: List[ImageSegment] = []
    line_segments: List[List[ImageSegment]] = []
    for i in range(img.height - scan_height):
        words_in_scan_area = _get_words_in_area(
            Segment(x1=0, y1=i, x2=img.width, y2=i + scan_height),
            all_words
        )
        if len(words_in_scan_area) > len(prev_words_in_scan_area):
            prev_words_in_scan_area = words_in_scan_area
        elif len(words_in_scan_area) < len(prev_words_in_scan_area):
            line_segments.append(prev_words_in_scan_area)
            all_words = [w for w in all_words if w not in prev_words_in_scan_area]
            prev_words_in_scan_area = []

    return line_segments