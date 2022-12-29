from asyncio.windows_events import NULL
from gc import callbacks
import ncclient
from ncclient import manager as Manager
from lxml import etree


class NetconfClient:
    def __init__(self, hostname, port, username, password):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password  

        print("NetconfClient connect...")
        self.conn = ncclient.manager.connect(
            host=self.hostname,
            port=self.port,
            username=self.username,
            password=self.password,
            hostkey_verify=False,
            timeout=120
        )
        self.conn.create_subscription()


    def close(self):        
        self.conn.close_session()
        print("NetconfClient close")

    def read_hostname(self):

        # Retrieve the ietf-system hostname
        result = self.conn.get(
            filter=('subtree',
                    f"""
                    <system xmlns="urn:ietf:params:xml:ns:yang:ietf-system">
                        <hostname />
                    </system>
                    """
                   )
        )

        # Parse the result.data element and extract the hostname       
        root = etree.fromstring(result.data_xml.replace(' encoding="UTF-8"', ''))
        hostname = root.find(".//{urn:ietf:params:xml:ns:yang:ietf-system}hostname")

        try:
            print(hostname.text)
        except AttributeError:
            print("hostname is None")


    def set_hostname(self, new_hostname):

        # Define the configuration data
        config_data = """
        <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
          <system xmlns="urn:ietf:params:xml:ns:yang:ietf-system">
            <hostname>""" + new_hostname+ """</hostname>
          </system>
        </config>
        """
        print(config_data)
        # Apply the configuration data using the edit-config operation
        result = self.conn.edit_config(
            config=config_data,
            target="running",
            default_operation="replace"
        )

    def read_sys_state(self):
       # Retrieve the ietf-system hostname
        result = self.conn.get(
            filter=('subtree',
                    f"""
                    <system-state xmlns="urn:ietf:params:xml:ns:yang:ietf-system">                       
                    </system-state>
                    """
                   )
        )

        # Parse the result.data element and extract the hostname
        xml_str = result.data_xml
        xml_bytes = xml_str.encode('utf-8')
        root = etree.fromstring(xml_bytes)
        string_value = etree.tostring(root, pretty_print=True)
        print(string_value.decode())        

    def get_latest_notification(self):
        # "take_notification" blocking function read from another thread
        n = self.conn.take_notification()
        return(n.notification_xml)    






