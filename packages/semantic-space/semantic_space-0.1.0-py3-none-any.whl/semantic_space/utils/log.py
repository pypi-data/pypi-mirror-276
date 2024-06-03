"""
    A general purpose logger for the library. Copied the code
    from Vectorgebra...
"""

import logging

logger = logging.getLogger("root log")
handler = logging.StreamHandler()
format = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

handler.setFormatter(format)
logger.addHandler(handler)
logger.setLevel(logging.INFO)