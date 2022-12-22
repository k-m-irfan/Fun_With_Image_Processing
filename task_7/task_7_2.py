# import required libraries here
import cv2
import mediapipe as mp
import face_recognition as fr

# video capture object where 0 is the camera number for a usb camera (or webcam)
# cam = cv2.VideoCapture(0)

# for video file, use:
cam = cv2.VideoCapture("./task_7/mrBean2.mp4")
width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
faces = mp.solutions.face_detection.FaceDetection()

face = fr.load_image_file("./task_7/mrBean.png") # load a face
faceEncoding = fr.face_encodings(face)[0]
print(face)

while True:
    _ , frame = cam.read() # reading one frame from the camera object
    if _:
        frameRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)#convert to RGB for encoding
        faceResults = faces.process(frameRGB)
        if faceResults.detections != None:
            for face in faceResults.detections:
                bBox = face.location_data.relative_bounding_box
                x,y,w,h = int(bBox.xmin*width),int(bBox.ymin*height),int(bBox.width*width),int(bBox.height*height)
                face = frameRGB[y:y+h,x:x+w]
                if (face.shape[0]*face.shape[1]) > 0: #to filter out false detection and empty dimentioned crops  
                    encoding = fr.face_encodings(face)
                    match = fr.compare_faces(encoding,faceEncoding)
                    if True in match:
                        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                        cv2.putText(frame,'Mr. Bean',(x,y),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
        cv2.imshow('Webcam', frame)        

    # Waits for 1ms and check for the pressed key
    if cv2.waitKey(1) & 0xff == ord('q'): # press q to quit the camera (get out of loop)
        break
cam.release() # close the camera
cv2.destroyAllWindows() # Close all the active windows