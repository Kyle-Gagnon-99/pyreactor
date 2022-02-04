from pyreactor import Reactor
import logging

class FullReactor(Reactor.Reactor):
    
    def __init__(self, reactorId):
        super().__init__(reactorId)
    
    def consumeMessage(self, message):
        logging.debug("Message Received: %s", message)
        
    def processFailMsg(self, failMsgStr, destRid, numOfAttempts, message):
        logging.debug("Failed to deliver with a num of attempts %s", numOfAttempts)
        if(numOfAttempts <= 3):
            self.resendMessage(destRid, numOfAttempts, message)