# middleware.py
import logging

logger = logging.getLogger(__name__)

class LogRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log request details
        logger.info(f"Request method: {request.method}")
        logger.info(f"Request path: {request.path}")
        logger.info(f"Request headers: {request.headers}")

        response = self.get_response(request)
        response.headers = {
            'Content-Type': 'application/json', 'Vary': 'Accept', 'Allow': 'GET, POST, HEAD, OPTIONS',
            'Access-Control-Allow-Origin': 'https://d4-medicals.vercel.app',
                               
                            }

        logger.info(f"Response headers: {response.headers}")

        return response
   