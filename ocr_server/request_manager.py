import threading
import queue
import time

from model import Model
from utils import sysconfig
from utils.logger import logger


class RequestManager(threading.Thread):

    def __init__(self):
        self._input_queue = queue.Queue()
        self._output_dict = dict()
        self._model = Model()
        threading.Thread.__init__(self)

    def add_request(self, request):
        self._input_queue.put(request)

    def wait_for_output(self, request_id):
        start_time = time.time()
        while True:
            if request_id in self._output_dict:
                return self._output_dict[request_id]
            current_time = time.time()
            if current_time - start_time > sysconfig.request_timeout:
                return None
            time.sleep(0.1)

    def run(self):
        while True:
            try:
                request = self._input_queue.get(True, 0.01)
                request_id, images = request
                logger.info("Processing request {}, with {im}".format(request_id,im=images))
                score = self._model.predict(images)
                self._output_dict[request_id] = score
            except queue.Empty:
                pass
            except KeyboardInterrupt:
                return
            except Exception as e:
                logger.error(str(e))

