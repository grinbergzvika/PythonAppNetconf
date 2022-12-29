import threading
import time

class NotificationThread(threading.Thread):
    def __init__(self, netconf_client):
        # Initialize the thread
        threading.Thread.__init__(self)
        self.netconf_client = netconf_client
        self.stop_event = threading.Event()
        self.notification = None
   
    def run(self):
        # Poll for notifications in a loop until the stop event is set
        while not self.stop_event.is_set():
            # Get the latest notification from the Netconf client
            self.notification = self.netconf_client.get_latest_notification()
            print(self.notification)
            # Sleep for a short period before checking again
            time.sleep(1)    

    def stop(self):
        # Set the stop event to signal the thread to stop
        self.stop_event.set()


