from pyreactor import EventService
import logging

from tests.FullReactor import FullReactor

#********************************************************************************************
# NOTE
# 
# This class was mainly used for testing during development. This can be used as an example
# but better examples are planned for the future.
#********************************************************************************************

# Formatting logs
logging.addLevelName( logging.DEBUG, "\033[1;36m%s\033[1;0m" % logging.getLevelName(logging.DEBUG))
logging.addLevelName( logging.WARNING, "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
logging.addLevelName( logging.ERROR, "\033[1;41m%s\033[1;0m" % logging.getLevelName(logging.ERROR))
logging.addLevelName( logging.CRITICAL, "\033[1;91m%s\033[1;0m" % logging.getLevelName(logging.CRITICAL))

format = "[%(levelname)1s] %(asctime)s: %(message)s (%(module)s.py:%(lineno)d)"
logging.basicConfig(format=format, level=logging.DEBUG, datefmt='%m/%d/%Y %I:%M:%S %p')

evService = EventService.EventService()
evService.start()

fullReactor = FullReactor(10)
fullReactor.start()

fullReactor.sendMessage(5, "Hello Reactor 10!")