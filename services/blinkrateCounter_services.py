from fastapi import Depends, File, UploadFile
from fastapi.responses import JSONResponse
from app.schemas import BlinkDetectionResponse
from app.models.blinkmodel import BlinkDetection
from sqlalchemy.orm import Session
from app.database import SessionLocal

import cv2
import cvzone
import tempfile
import shutil
import os
from cvzone.FaceMeshModule import FaceMeshDetector



detector = FaceMeshDetector(maxFaces=1)
idList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]
ratioList = []
blinkCounter = 0
counter = 0
color = (255, 0, 255)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def create_blink_detection(db: Session, data: BlinkDetectionResponse.BlinkDetectionCreate):
    blink = BlinkDetection(
        filename=data.filename,
        blink_count=data.blink_count,
        blink_rate_per_minute=data.blink_rate_per_minute,
        video_duration_seconds=data.video_duration_seconds
    )
    blink.set_timestamps(data.blink_timestamps)
    db.add(blink)
    db.commit()
    db.refresh(blink)
    return blink



def detect_blinks(file: UploadFile = File(...), db: Session = Depends(get_db)):
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, file.filename)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    cap = cv2.VideoCapture(file_path)

    ratioList = []
    blinkCounter = 0
    counter = 0
    timestamps = []

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    duration_seconds = frame_count / fps if fps else 1
    duration_minutes = duration_seconds / 60

    while True:
        success, img = cap.read()
        if not success:
            break

        img, faces = detector.findFaceMesh(img, draw=False)

        if faces:
            face = faces[0]
            leftUp = face[159]
            leftDown = face[23]
            leftLeft = face[130]
            leftRight = face[243]
            lengthVer, _ = detector.findDistance(leftUp, leftDown)
            lengthHor, _ = detector.findDistance(leftLeft, leftRight)

            ratio = int((lengthVer / lengthHor) * 100)
            ratioList.append(ratio)
            if len(ratioList) > 3:
                ratioList.pop(0)
            ratioAvg = sum(ratioList) / len(ratioList)

            if ratioAvg < 37 and counter == 0:
                blinkCounter += 1
                counter = 1
                frame_number = cap.get(cv2.CAP_PROP_POS_FRAMES)
                timestamp = round(frame_number / fps, 2)
                timestamps.append(timestamp)

            if counter != 0:
                counter += 1
                if counter > 10:
                    counter = 0

    cap.release()
    os.remove(file_path)

    blink_rate_per_minute = round(blinkCounter / duration_minutes, 2) if duration_minutes > 0 else 0


    # Save to DB
    blink_data = BlinkDetectionResponse.BlinkDetectionCreate(
        filename=file.filename,
        blink_count=blinkCounter,
        blink_rate_per_minute=blink_rate_per_minute,
        video_duration_seconds=round(duration_seconds, 2),
        blink_timestamps=timestamps
    )

    db_blink = create_blink_detection(db, blink_data)
    return db_blink

    # return BlinkDetectionResponse(
    #     blink_count=blinkCounter,
    #     blink_timestamps=timestamps,
    #     video_duration_seconds=round(duration_seconds, 2),
    #     blink_rate_per_minute=blink_rate_per_minute
    # )
