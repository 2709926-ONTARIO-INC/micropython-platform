import uasyncio as asyncio
from umqtt.robust import MQTTClient

c = MQTTClient("umqtt_client", "localhost")
# Print diagnostic messages when retries/reconnects happens
c.DEBUG = True
# Information whether we store unsent messages with the flag QoS==0 in the queue.
c.KEEP_QOS0 = False
# Option, limits the possibility of only one unique message being queued.
c.NO_QUEUE_DUPS = True
# Limit the number of unsent messages in the queue.
c.MSG_QUEUE_MAX = 2

last_will_topic = '/lw/topic'

def sub_cb(topic, msg, retained, duplicate):
    print((topic, msg, retained, duplicate))
    
def pub_data(topic, data):
    c.publish(topic, data)

async def mqtt_mgr():
    c.set_last_will(last_will_topic, 'Disconnected', retain=True)

    c.set_callback(sub_cb)
    if not c.connect(clean_session=False):
    print("New session being set up")
    c.subscribe(b"foo_topic")

while 1:
    await asyncio.sleep(1)

    # At this point in the code you must consider how to handle
    # connection errors.  And how often to resume the connection.
    if c.is_conn_issue():
        while c.is_conn_issue():
            # If the connection is successful, the is_conn_issue
            # method will not return a connection error.
            c.reconnect()
            await asyncio.sleep(2)
            #c.publish(last_will_topic, 'Connected', retain=True)
        else:
            c.resubscribe()


    # WARNING!!!
    # The below functions should be run as often as possible.
    # There may be a problem with the connection. (MQTTException(7,), 9)
    # In the following way, we clear the queue.
    for _ in range(500):
        c.check_msg()  # needed when publish(qos=1), ping(), subscribe()
        c.send_queue()  # needed when using the caching capabilities for unsent messages
        if not c.things_to_do():
            break
        await asyncio.sleep(2)