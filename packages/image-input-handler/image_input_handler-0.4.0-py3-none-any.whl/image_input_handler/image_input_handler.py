import numpy as np
import cv2
import base64
import urllib3
import re
from PIL import Image, UnidentifiedImageError
import io
import logging

logging.basicConfig(level=logging.WARNING)  # Set global logging level
logging.getLogger("urllib3").setLevel(logging.WARNING)

class UniversalImageInputHandler:
    def __init__(self, img_input, img_is_a_mask=False, debug=False):
        self.img_input = img_input
        self.img_is_a_mask = img_is_a_mask
        self.img = None
        self.COMPATIBLE = False
        self.debug=debug

        if self.debug:
            print("debug On")

        self.read_image()

    def adjust_image_channels(self, img):
        if img.ndim == 3 and img.shape[2] == 4:
            img = img[:, :, :3]  # Remove the alpha channel if present
        if self.img_is_a_mask and img.ndim == 3:
            img = img[:, :, 0]  # Use the first channel for masks
        return img

    def read_image(self):

        if self.debug:
            print("checking image input type")
            print(self.img_input)

        if isinstance(self.img_input, np.ndarray):

            if self.debug :
                print("input is ndarray")
            self.process_image(self.img_input)
        elif isinstance(self.img_input, str):
            if self.debug:
                print("input is string")
            if self.is_url(self.img_input):
                if self.debug:
                    print("input is url")
                self.handle_url_image(self.img_input)
            elif self.is_path(self.img_input):
                if self.debug:
                    print("input is path")
                self.handle_path_image(self.img_input)
            elif self.is_base64(self.img_input):
                if self.debug:
                    print("input is base64 image")
                self.handle_base64_image(self.img_input)

    # def handle_url_image(self, url):
    #     try:
    #         user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) ..'}
    #         http = urllib3.PoolManager(10, headers=user_agent)
    #         response = http.urlopen('GET', url)
    #         image = Image.open(io.BytesIO(response.data))
    #         img_arr = np.array(image)
    #         self.process_image(img_arr)
    #     except (UnidentifiedImageError, urllib3.exceptions.HTTPError) as e:
    #         print(f"Failed to load image from URL: {e}")

    def handle_url_image(self, url):
        try:
            user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) ..'}
            http = urllib3.PoolManager(10, headers=user_agent, cert_reqs='CERT_NONE')  # Disable SSL verification
            response = http.urlopen('GET', url)
            image = Image.open(io.BytesIO(response.data))
            img_arr = np.array(image)
            self.process_image(img_arr)
        except (UnidentifiedImageError, urllib3.exceptions.HTTPError) as e:
            print(f"Failed to load image from URL: {e}")

    def handle_path_image(self, path):
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        if img is not None:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.process_image(img)
        else:
            print("Failed to load image from path.")

    def handle_base64_image(self, encoded_img):
        try:
            decoded_img = base64.b64decode(encoded_img)
            img_np_arr = np.frombuffer(decoded_img, np.uint8)
            img = cv2.imdecode(img_np_arr, cv2.IMREAD_UNCHANGED)
            self.process_image(img)
        except ValueError:
            print("Invalid Base64 encoding.")

    def process_image(self, img):
        img = self.adjust_image_channels(img)
        self.img = img
        self.COMPATIBLE = True

    # def is_path(self, s):
    #     path_regex = re.compile(
    #         r'^(/|\\|[a-zA-Z]:\\|\.\\|..\\|./|../)'
    #         r'(?:(?:[^\\/:*?"<>|\r\n]+\\|[^\\/:*?"<>|\r\n]+/)*'
    #         r'[^\\/:*?"<>|\r\n]*)$',
    #         re.IGNORECASE)
    #     return re.match(path_regex, s) is not None

    def is_path(self, s):
        path_regex = re.compile(
            r'^(/|\\|[a-zA-Z]:\\|\.\\|..\\|./|../)?'  # Optional start with /, \, C:\, .\, ..\, ./, or ../
            r'(?:(?:[^\\/:*?"<>|\r\n]+\\|[^\\/:*?"<>|\r\n]+/)*'  # Directory names
            r'[^\\/:*?"<>|\r\n]*)$',  # Last part of the path which can be a file
            re.IGNORECASE)
        return re.match(path_regex, s) is not None

    def is_url(self, s):
        url_regex = re.compile(
            r'^(https?://|ftp://)'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(url_regex, s) is not None

    def is_base64(self, s):
        try:
            s = s.strip()
            if len(s) % 4 != 0:
                return False
            base64.b64decode(s, validate=True)
            return True
        except ValueError:
            return False

