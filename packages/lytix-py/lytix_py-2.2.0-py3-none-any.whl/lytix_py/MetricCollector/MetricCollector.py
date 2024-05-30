from typing import Callable
import uuid
import requests
from urllib.parse import urljoin
import os.path
import time

from lytix_py.LAsyncStore.LAsyncStore import LAsyncStoreClass
from lytix_py.LLogger.LLogger import LLogger
from lytix_py.envVars import LytixCreds

"""
 Main class to collect and report metrics
 back to HQ
"""
class _MetricCollector:
    _baseURL: str = None
    processing_metric_mutex: int = 0

    def __init__(self):
        self._baseURL = urljoin(LytixCreds.LX_BASE_URL, "/v1/metrics")
        self.processing_metric_mutex = 0
        pass


    """
    Interal wrapper to send a post request
    """
    def _sendPostRequest(self, endpoint: str, body: dict):
        url = os.path.join(self._baseURL, endpoint)
        headers = {
            "Content-Type": "application/json",
            "lx-api-key": LytixCreds.LX_API_KEY,
        }
        response = requests.post(url, headers=headers, json=body)
        if (response.status_code != 200):
            print(f"Failed to send post request to {url} with status code {response.status_code} and response {response.text}")

    """
    Increment a given metric
    """
    def increment(self, metricName: str, metricValue: int = 1, metricMetadata: dict = None):
        if LytixCreds.LX_API_KEY is None: 
            return 

        if metricMetadata is None:
            metricMetadata = {}
        body = {
            "metricName": metricName,
            "metricValue": metricValue,
            "metadata": metricMetadata
        }
        self._sendPostRequest("increment", body)

    """
    Capture a model input/output
    """
    def captureModelIO(self, modelName: str, modelInput: str, modelOutput: str, metricMetadata: dict = None, userIdentifier = None, sessionId = None, logs: list[str] =None):
        if LytixCreds.LX_API_KEY is None: 
            return 

        if metricMetadata is None:
            metricMetadata = {}
        body = {
            "modelName": modelName,
            "modelInput": modelInput,
            "modelOutput": modelOutput,
            "metricMetadata": metricMetadata,
            "userIdentifier": userIdentifier,
            "sessionId": sessionId,
            "logs": logs
        }
        self._sendPostRequest("modelIO", body)

    """
    Capture a model io event while also capturing the time to respond
    """
    async def captureModelTrace(self, modelName: str, modelInput: str, callback : Callable[[LLogger], str], metricMetadata: dict = {}, userIdentifier = None, sessionId = None):
        asyncStore = LAsyncStoreClass()
        logger = LLogger(f'lytix-{modelName}-trace-{uuid.uuid4()}', asyncStore=asyncStore)
        if LytixCreds.LX_API_KEY is None: 
            print("No Lytix API key found, skipping metric collection")
            return await callback(logger)

        startTime = time.time()
        modelOutput = await callback(logger)
        try:
            responseTime = int((time.time() - startTime) * 1000)  # Convert to milliseconds
            # Capture modelIO event along with the response time and any logs
            logs = logger.asyncStore.getLogs()
            self.captureModelIO(modelName, modelInput, modelOutput, metricMetadata, userIdentifier, sessionId, logs)
            self.increment("model.responseTime", responseTime, {"modelName": modelName}.update(metricMetadata))
        except Exception as err:
            self.logger.error(f"Failed to capture model trace: {err}", err, modelName, modelInput)
        finally:
            return modelOutput

    """
    Capture a metric trace event
    @note You likeley never need to call this directly
    """
    def _captureMetricTrace(self, metricName: str, metricValue: int, metricMetadata: dict = {}, logs: list = []):
        self.processing_metric_mutex += 1

        body = {
            "metricName": metricName,
            "metricValue": metricValue,
            "metricMetadata": metricMetadata,
            "logs": logs
        }

        self._sendPostRequest("increment", body)

        self.processing_metric_mutex -= 1

MetricCollector = _MetricCollector()

