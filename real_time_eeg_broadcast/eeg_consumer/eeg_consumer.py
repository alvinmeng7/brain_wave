import time
import sys
import stomp
# Create a Listener class inheriting the stomp.ConnectionListener class
# stomp.ConnectionListener class definition can be found here:
# https://github.com/jasonrbriggs/stomp.py/blob/2435108cfc3eb4bd6477653b071e85acd6a2f211/stomp/listener.py
class Listener(stomp.ConnectionListener):
# Override the methods on_error and on_message provides by the
# parent class
    def on_error(self, headers, message):
        print('received an error "%s"' % message)
# Print out the message received
    def on_message(self, headers, message):
        print('received a message "%s"' % message)
# Decare hosts as an array of tuples containing the ActiveMQ server # IP address or hostname and the port number
hosts = [('localhost', 61616)]
# Create a connection object by passing the hosts as an argument
conn = stomp.Connection(host_and_ports=hosts)
# Tell the connection object to listen for messages using the
# Listener class we created above
conn.set_listener('', Listener())
# Initiate the connection with the credentials of the ActiveMQ server
conn.start()
conn.connect('admin', 'admin', wait=True)
# Register a consumer with ActiveMQ. This tells ActiveMQ to send all # messages received on the queue 'queue-1' to this listener
conn.subscribe(destination='/topic/topic-1', ack='auto')
# Act as a message producer and send a message the queue queue-1
# The actual message to be sent is picked up from the command line arguments
# Say, if you want to send the message "Hello Queue", you will run
# the code aspython queue.py "Hello Queue"
conn.send(body=' '.join(sys.argv[1:]), destination='/topic/topic-1')
# When this message is received by the listener, it will be handled
# by the on_message method we defined above.
# Wait for things to clean up and close the connection
time.sleep(2)
conn.disconnect()