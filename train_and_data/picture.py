import depthai as dai
import cv2

pipeline = dai.Pipeline()

cam_rgb = pipeline.create(dai.node.ColorCamera)
cam_rgb.setVideoSize(640,640)
cam_rgb.setBoardSocket(dai.CameraBoardSocket.RGB)
cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)

xout_video = pipeline.create(dai.node.XLinkOut)
xout_video.setStreamName("video")

cam_rgb.video.link(xout_video.input)

with dai.Device(pipeline) as device:
    # Output queue will be used to get the frames from the output defined above
    q_video = device.getOutputQueue(name="video", maxSize=4, blocking=False)

    frame_count = 24

    while True:
        in_video = q_video.get()  # Get frame

        # Convert to OpenCV format and show frame
        frame = in_video.getCvFrame()
        cv2.imshow("video", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):  # Press 'c' to capture image
            frame_count += 1
            cv2.imwrite(f'captured_frame{frame_count}.jpg', frame)
            print(f"Captured frame{frame_count}.jpg")

    cv2.destroyAllWindows()