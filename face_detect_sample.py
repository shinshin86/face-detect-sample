import cv2
from os import path
from datetime import datetime
import json


# read config
with open("setting.json") as f:
  settings = json.load(f)
  SAVE_FULL_IMAGE_DIR = settings["saveFullImageDir"]
  SAVE_FACE_IMAGE_DIR = settings["saveFaceImageDir"]
  FACE_CASCADE_PATH = settings["faceCascadePath"]
  W = int(settings["w"])
  H = int(settings["h"])
  POSITION_X = int(settings["positionX"])
  POSITION_Y = int(settings["positionY"])
  FACE_MIN_W = int(settings["faceMinW"])
  FACE_MIN_H = int(settings["faceMinH"])
  THRESH_HOLD = int(settings["threshHold"])

def main(video_file=None):
  if video_file is None:
    cam = cv2.VideoCapture(0)
  else:
    cam = cv2.VideoCapture(video_file)
  
  # frame initialize
  img1 = img2 = img3 = get_image(cam)
  num = 1

  while True:
    # Enter key is finish
    if cv2.waitKey(1) == 13: break
    diff = check_image(img1, img2, img3)
    count = cv2.countNonZero(diff)

    if count > THRESH_HOLD:
      cv2.imshow('push enter key', img3)
      save_face_image(num, img3)
      num += 1
    else:
      cv2.imshow('push enter key', diff)
      cv2.moveWindow('push enter key', POSITION_X, POSITION_Y)

    img2, img2, img3 = (img2, img3, get_image(cam))

  cam.release()
  cv2.destroyAllWindows()


def detectFace(img):
  img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
  img_gray = cv2.equalizeHist(img_gray)

  cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)
  facerect = cascade.detectMultiScale(img_gray, scaleFactor=1.1, minNeighbors=3, minSize=(FACE_MIN_W, FACE_MIN_H))

  return facerect


def save_face_image(count, img):
  facerect = detectFace(img)
  print(facerect)

  if len(facerect) != 0:
    save_file_name = datetime.now().strftime("%Y%m%d%H%M%S") + '-' + str(count) + '.jpg'
    save_full_image_file(count, img, save_file_name)
    for rect in facerect:
      croped = img[rect[1]:rect[1]+rect[3],rect[0]:rect[0]+rect[2]]
      save_face_image_file(count, croped, save_file_name)


def save_full_image_file(count, img, filename):
  cv2.imwrite(path.join(SAVE_FULL_IMAGE_DIR,  filename), img)


def save_face_image_file(count, img, filename):
  cv2.imwrite(path.join(SAVE_FACE_IMAGE_DIR,  filename), img)


def check_image(img1, img2, img3):
  gray1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
  gray2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
  gray3 = cv2.cvtColor(img3, cv2.COLOR_RGB2GRAY)

  diff1 = cv2.absdiff(gray1, gray2)
  diff2 = cv2.absdiff(gray2, gray3)

  diff_and = cv2.bitwise_and(diff1, diff2)

  _, diff_wb = cv2.threshold(diff_and, 30, 255, cv2.THRESH_BINARY)
  diff = cv2.medianBlur(diff_wb, 5)
  return diff


def get_image(cam):
  img = cam.read()[1]
  img = cv2.resize(img, (W, H))
  return img


if __name__ == "__main__":
  main() # if not have video file, using Your pc camera
  # main(<video file path>)
