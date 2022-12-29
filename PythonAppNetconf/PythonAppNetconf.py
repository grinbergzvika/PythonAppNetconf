import sys
from time import sleep
from netconf_notification import NotificationThread
from netconf_functions import NetconfClient


def notification_callback(notification):
    # Process the notification here
    print(notification)



########################################################################
# Create an instance of the NetconfClient class
########################################################################
client = NetconfClient(hostname="10.0.1.200", port=830, username="admin", password="admin")
########################################################################


########################################################################
# Create an instance of the NotificationThread class and start the thread
########################################################################
notification_thread = NotificationThread(client)
notification_thread.start()
########################################################################

########################################################################
# Call the read_hostname method
########################################################################
client.read_hostname()
client.read_sys_state()
client.set_hostname("PL4000T")
sleep(3)
########################################################################


########################################################################
client.close()
notification_thread.stop()
sleep(3)
########################################################################




