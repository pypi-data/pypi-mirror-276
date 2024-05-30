import bql
import threading
import logging
import time
from typing import Optional

logger = logging.getLogger(__name__)

_bqService: Optional[bql.Service] = None

_bpsession = None
bqllock = threading.Lock()  # Prevent concurrent

BQSERVICE_TIMEOUT = 120
BQSERVICE_NEEDED_RETRY = False


def get_bqapi_session():
    global _bpsession
    if _bpsession is not None:
        return _bpsession
    with bqllock:
        # make sure we didn't create it after acquiring lock
        if _bpsession is not None:
            return _bpsession
        import bqapi as bp  # pyright: ignore

        _bpsession = bp.get_session_singleton()
        return _bpsession


class BqServiceRetriever(threading.Thread):
    service = None

    def run(self):
        self.service = bql.Service()


def get_bqservice(retries: int = 3) -> bql.Service:
    global _bqService
    global BQSERVICE_NEEDED_RETRY

    try:
        if _bqService is None:  # type: ignore
            logger.debug("Creating new bqService")

            start_time = time.time()

            retrieverThread = BqServiceRetriever()
            retrieverThread.start()
            retrieverThread.join(timeout=BQSERVICE_TIMEOUT)
            if retrieverThread.is_alive():
                raise TimeoutError(f"Unable to get bqservice in {BQSERVICE_TIMEOUT}")
            _bqService = retrieverThread.service

            end_time = time.time()
            duration = end_time - start_time
            logger.debug("Creating new bqService took %s seconds", round(duration))

    except Exception as e:
        logger.exception("Unable to create bq service")
        if retries <= 0:
            raise e

    if _bqService is None:
        if retries > 0:
            BQSERVICE_NEEDED_RETRY = True
            logger.warning("Retry get bqservice (retries left %s)", retries)
            return get_bqservice(retries - 1)
        raise ValueError("Unable to obtain bql.Service()")
    return _bqService


def close_bqservice():
    """Closing the session is not normally needed, but there is a limit on the number of concurrent connections.
    BQL uses (as far as we can tell) a Singleton so multiple bql sessions requests will not consume more connections.
    """
    try:
        global _bqService
        if _bqService is None or _bqService._Service__bqapi_session is None:  # type: ignore
            logger.debug("_Service__bqapi_session already closed or None")
            return
        else:
            logger.debug("Closing _Service__bqapi_session session")
            _bqService._Service__bqapi_session.close()  # type: ignore
            _bqService = None
    except Exception:
        logger.exception("Error closing bqapi session")
