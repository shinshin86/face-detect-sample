# face-detect-sample
Face detect sample. Using opencv

## Setup

Install opencv(cv2)

```sh
pip install opencv-python
```

Specify the path to the Haar-Cascade file.  
Files can be found [here(OpenCV - GitHub)](https://github.com/opencv/opencv/tree/master/data/haarcascades).

```diff
--- a/setting.json
+++ b/setting.json
@@ -1,7 +1,7 @@
 {
     "saveFullImageDir": "full",
     "saveFaceImageDir": "faces",
-    "faceCascadePath": "<cascade file path>",
+    "faceCascadePath": "./haarcascade_file_path",
     "w": "960",
     "h": "540",
     "positionX": "10",
```

## Usage

```
python3 face_detect_sample.py
```



## Capture condition

* When the camera image and video has changed
* When a face is detected



## Utils

```
# remove images ---> './full/*.jpg' and './faces/*.jpg'
./image_remove.sh
```

