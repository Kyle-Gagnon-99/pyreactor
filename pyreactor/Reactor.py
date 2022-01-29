import logging
import zmq
import threading
from pyreactor import ReactorId

class Reactor:
    """
    A class that can send messages and react to incoming ones. The logic on what to do with a message
    must be implemented along with implementing what happens on a failed to deliver message.
    """
    
    # Private Variables
    __socketType = zmq.DEALER
    __socketAddress = "tcp://127.0.0.1:5555"
    __context = zmq.Context()
    __dealerSocket = __context.socket(__socketType)
    __threadObject = threading.Thread()
    __running = True
    
    def __init__(self, reactorId, p_socketAddress = __socketAddress):
        """
        Sets up the reactor class by setting the socket's id, type, and address.
        After setting up the socket it then connects it to the address.
    
        Uses the default address of tcp://127.0.0.1:5555

        Args:
            reactorId (int): The way the reactor identifies itself to the outside world
        """
        reactorIdObj = ReactorId.ReactorId()
        reactorIdObj.rid = reactorId
        reactorIdObjStr = reactorIdObj.SerializeToString()
        
        self.__dealerSocket.setsockopt(zmq.ROUTING_ID, reactorIdObjStr)
        
        self.__dealerSocket.connect(p_socketAddress)
        
    def __run(self):
        """
        Starts the Reactor class
        """
        
        message = zmq.Frame()
        destMsg = zmq.Frame()
        
        while (self.__running):
            
            try:
                message = self.__dealerSocket.recv_string(flags=zmq.DONTWAIT)
            except zmq.ZMQError as error:
                if (error.errno == zmq.EAGAIN):
                    continue
                else:
                    logging.error("ZMQ Error: %s", error.strerror)
            
            if (message == "FAIL_TO_DELIVER"):
                destMsg = self.__dealerSocket.recv_string()
                reactorIdObj = ReactorId.ReactorId()
                reactorIdObj.ParseFromString(destMsg)
                self.processFailMsg(message, reactorIdObj.rid)
            else:
                self.consumeMessage(message)    
        
    def start(self):
        """
        Start the Reactor thread and connect to the address
        """
        self.__threadObject = threading.Thread(target=self.__run)
        self.__threadObject.start()
        
    def sendMessage(self, destRid, message):
        """
        Sends a message to the specified reactor

        Args:
            destRid (int): Where the message will send to
            message (string): The message to send
        """
        reactorIdObj = ReactorId.ReactorId()
        reactorIdObj.rid = destRid
        reactorIdObjStr = reactorIdObj.SerializeToString()
        
        self.__dealerSocket.send(reactorIdObjStr, zmq.SNDMORE)
        self.__dealerSocket.send_string(message)
        
    def shutdown(self):
        """
        Shuts down the class by disconnecting from the address, closing the socket,
        and then stopping the thread.
        """
        self.__running = False
        self.__dealerSocket.disconnect(self.__socketAddress)
        self.__dealerSocket.close()
        try:
            self.__threadObject.join()
        except:
            pass
        
    def consumeMessage(self, message):
        """
        An abstract method that gets called to get the contents of messages received

        Args:
            message (string): The message that was received
        """
        raise NotImplementedError
        
    def processFailMsg(self, failMsgStr, destRid):
        """
        Called when a FAIL_TO_DELIVER message is received by the reactor

        Args:
            failMsgStr (string): The FAIL_TO_DELIVER message
            destRid (int): Where it was suppose to go
        """
        raise NotImplementedError
        

        