import logging
import falcon
from datetime import datetime

class Logger():
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def process_request(self, req, resp):
        req.context.timing = {}
        req.context.timing["request_start_time"] = datetime.utcnow()
        if req.content_type is not None and "json" in req.content_type :
            self.logger.info('{} {} headers:"{}" body:"{}"'.format(req.method,
                                                                req.relative_uri,
                                                                str(req.headers),
                                                                str(req.media)))
        else:
            self.logger.info('{} {} headers:"{}"'.format(req.method,
                                                                req.relative_uri,
                                                                str(req.headers)))

    def process_response(self, req, resp, resource, req_succeeded):
        req.context.timing["request_finish_time"] = datetime.utcnow()
        start_time = req.context.timing["request_start_time"]
        finish_time = req.context.timing["request_finish_time"]
        total_request_time = (finish_time - start_time).total_seconds() * 1000.0
        self.logger.info('{} {} {:.2f}ms {} Body: "{}"'.format(
            req.method, resp.status, total_request_time, req.relative_uri, resp.media))