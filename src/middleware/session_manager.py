import logging 

class SessionManager:
    def __init__(self, session_maker):
        self.db_session_maker = session_maker
        self.logger = logging.getLogger(__name__)

    def process_request(self, req, resp):
        self.logger.info('Processing resource on SessionManager')
        if req.method == 'OPTIONS':
            req.context.db_session = None
            return
        self.logger.info('Creating db_session on context')
        req.context.db_session = self.db_session_maker()

    def process_response(self, req, resp, resource, req_succeeded):
        self.logger.info('Disposing context')
        if req.method == 'OPTIONS':
            return
        if hasattr(req.context, 'db_session') and req.context.db_session is not None:
            if not req_succeeded:
                self.logger.info('Rolling back')
                req.context.db_session.rollback()
            self.logger.info('Closing')
            req.context.db_session.close()
