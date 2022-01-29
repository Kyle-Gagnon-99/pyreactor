from errno import EAGAIN
import logging
import threading
import zmq

class EventService:
    """
    The Event Service class is used as a way to pass messages (events) from
    one endpoint (a dealer/reactor) to another endpoint.
    """

    # Private variables
    __socketType = zmq.ROUTER
    __socketAddress = "tcp://127.0.0.1:5555"
    __context = zmq.Context()
    __routerSocket = __context.socket(__socketType)
    __threadObject = threading.Thread()
    __running = True
    
    def __init__(self, p_socketAddress = __socketAddress):
        """
        Constructs the EventService object.
        
        Upon construction of the object, the socket will be created
        with the type and it's address and binds the address. Does not
        start the thread.
        
        Uses the default address of tcp://127.0.0.1:5555
        
        Args: 
            p_socketAddress ([String]): The address to bind to. If not supplied
                                        then it defaults to the default address
        """
        self.__routerSocket.setsockopt(zmq.ROUTER_MANDATORY, 1)
        self.__routerSocket.bind(p_socketAddress)
      
    def __run(self):
        """ 
        Starts the Event Service by listening on the specified address
        """
        
        while(self.__running):
            
            sourceMsg = zmq.Frame()
            destMsg = zmq.Frame()
            message = zmq.Frame()
            
            try:
                sourceMsg = self.__routerSocket.recv(zmq.DONTWAIT)
            except zmq.ZMQError as error:
                if (error.errno == zmq.EAGAIN):
                    continue
                else:
                    logging.error("ZMQ Error: %s", error.strerror)                    
            
            destMsg = self.__routerSocket.recv()
            message = self.__routerSocket.recv()
            
            try:
                self.__passMessage(destMsg, message)
            except zmq.ZMQError as error:
                logging.error("ZMQ Error %s", error.strerror)
                self.__failMessage(sourceMsg, destMsg)
              
    def start(self):
        """ 
        Starts the Event Service thread and start listening on the address
        """
        self.__threadObject = threading.Thread(target=self.__run)
        self.__threadObject.start()
        
    def __passMessage(self, destMsg, message):
        """
        Passes along the message that was received to the destination

        Args:
            destMsg (Frame): The destination on where the message needs to go
            message (Frame): The actual message to send
        """
        self.__routerSocket.send(destMsg, zmq.SNDMORE)
        self.__routerSocket.send(message)
        
    def __failMessage(self, sourceMsg, destMsg):
        """
        Sends a FAIL_TO_DELIVER message when the router could not find the client

        Args:
            sourceMsg (Frame): Where the message came from
            destMsg (Frame): Where the message was supposed to go
        """
        failToDeliver = "FAIL_TO_DELIVER"
        
        self.__routerSocket.send(sourceMsg, zmq.SNDMORE)
        self.__routerSocket.send_string(failToDeliver, flags=zmq.SNDMORE)
        self.__routerSocket.send(destMsg)
        
    def shutdown(self):
        """
        Shuts down the class by disconnecting from the address, closing the socket,
        and then stopping the thread.
        """
        self.__running = False
        self.__routerSocket.disconnect(self.__socketAddress)
        self.__routerSocket.close()
        try:
            self.__threadObject.join()
        except:
            pass
        
    