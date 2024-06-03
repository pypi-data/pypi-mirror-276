import os
import threading

import cv2
from fz_logger import fz_logger

script_name = os.path.basename(__file__).split(".")[0]

# INIT fz_logger get instance
log = fz_logger.Logger(className=script_name, lvl="INFO", filePath="./log")
logger = log.initLogger()


def add_camera_args(parser):
    """Add parser augument for camera options."""
    parser.add_argument("--width", type=int, default=640, help="image width [640]")
    parser.add_argument("--height", type=int, default=480, help="image height [480]")
    parser.add_argument("--threaded", action="store_false", help="using thread capture-reader")
    parser.add_argument("--usegst", action="store_false", help="using capture-reader gstreamer")
    return parser


class CaptureWriter:
    def __init__(self, file, fps=30, enabled=True):
        self.file = file
        self.fps = fps
        self.enabled = enabled
        self.writer = None

    def write(self, frame):
        if self.enabled:
            if self.writer is None:
                fourcc = cv2.VideoWriter_fourcc(*"XVID")
                self.writer = cv2.VideoWriter(self.file, fourcc, self.fps, (frame.shape[1], frame.shape[0]))

            self.writer.write(frame)

    def close(self):
        if self.enabled:
            if self.writer is not None:
                self.writer.release()


class CaptureReader:
    def __init__(self, id, width=640, height=480, threaded=False, use_gst=None):
        cmd = id
        cam_switch = False
        if cmd.startswith("rtsp://"):
            cam_switch = False
        elif cmd.endswith(".avi") or cmd.endswith(".mp4"):
            cam_switch = False
        else:
            cam_switch = True
        build_info = cv2.getBuildInformation().split("\n")
        for i in build_info:
            if "GStreamer" in i and "YES" in i:
                pass
            else:
                use_gst = False
                logger.error("Gstreamer is not init please check")

        if use_gst:
            self.cap = cv2.VideoCapture(cmd, cv2.CAP_GSTREAMER)
        else:
            if cam_switch:
                cmd = int(cmd)
                self.cap = cv2.VideoCapture(cmd)
            else:
                self.cap = cv2.VideoCapture(cmd)

        self.input_size = width, height
        self.threaded = threaded
        self.read_thread = None

        self.current_frame = None
        opt = [cmd, self.input_size, self.threaded, self.read_thread, self.is_open()]
        logger.info(opt)

    def _read_thread(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                if frame.shape[1] != self.input_size[0] or frame.shape[0] != self.input_size[1]:
                    self.current_frame = cv2.resize(frame, tuple(self.input_size))
                else:
                    self.current_frame = frame.copy()
            else:
                continue
            # time.sleep(0.001)

    def is_open(self):
        return self.cap.isOpened()

    def grab(self):
        self.cap.grab()

    def read(self):
        if not self.threaded:
            ret, frame = self.cap.read()

            if ret:
                if frame.shape[1] != self.input_size[0] or frame.shape[0] != self.input_size[1]:
                    frame = cv2.resize(frame, tuple(self.input_size))

                return frame
            else:
                return None
        else:
            if self.read_thread is None:
                self.read_thread = threading.Thread(target=self._read_thread)
                self.read_thread.daemon = True
                self.read_thread.start()

            return self.current_frame

    def get_fps(self):
        return self.cap.get(cv2.CAP_PROP_FPS)

    def get_size(self):
        return [self.cap.get(3), self.cap.get(4)]

    def set_frame_pos_sec(self, t):
        self.cap.set(cv2.CAP_PROP_POS_MSEC, round(t * 1000))

    def show_image(self, f, title):
        cv2.imshow(title, f)

    def key(self, t):
        return cv2.waitKey(t)

    def exit(self):
        self.cap.release()
        if self.threaded:
            self.read_thread.join()
