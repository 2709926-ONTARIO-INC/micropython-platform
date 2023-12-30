import ujson
import uasyncio as asyncio
from machine import UART
import umodbus.serial as modbus_serial
from umodbus.tcp import TCP as ModbusTCPMaster
import socket
import struct
import errno
import queue

#MQTT imports
from mqtt_as import MQTTClient
from mqtt_as import config

#web UI imports
from web_srv import web_ui

mqtt_pub_queue = queue.Queue()

#MQTT callbacks
# Subscription callback
def sub_cb(topic, msg, retained):
    print(f'Topic: "{topic.decode()}" Message: "{msg.decode()}" Retained: {retained}')
    
async def mqtt_operations(client):
    try:
        await client.connect()
    except OSError:
        print('Connection failed.')
        return
    while True:
        # If WiFi is down the following will pause for the duration.
        await client.publish('data/modbus', await mqtt_pub_queue.get(), qos = 1)
        
# If you connect with clean_session True, must re-subscribe (MQTT spec 3.1.2.4)
async def conn_han(client):
    await client.subscribe('foo_topic', 1)

# Function to read configuration
def read_config(filename):
    with open(filename, 'r') as f:
        return ujson.load(f)

# Async function to poll a single Modbus server
async def poll_modbus_server(client, server_config):
    while True:
        try:
            #create new dict for MQTT payload
            mqtt_data = dict()
            for reg in server_config['registers']:
                if reg['register_type'] == 'holding_registers':
                    if reg['data_type'] is 'float':
                        result = client.read_holding_registers(slave_addr=server_config['modbus_id'],starting_addr=reg['register_start'],register_qty=2,signed=False)
                        result = struct.unpack('!f', bytes.fromhex('{0:04x}'.format(result[0]) + '{0:04x}'.format(result[1])))
                    elif reg['data_type'] is 'float_cdab':
                        result = client.read_holding_registers(slave_addr=server_config['modbus_id'],starting_addr=reg['register_start'],register_qty=2,signed=False)
                        result = struct.unpack('!f', bytes.fromhex('{0:04x}'.format(result[1]) + '{0:04x}'.format(result[0])))
                    elif reg['data_type'] is 'int16':
                        result = client.read_holding_registers(slave_addr=server_config['modbus_id'],starting_addr=reg['register_start'],register_qty=1,signed=False)
                        result = struct.unpack('!h', bytes.fromhex('{0:04x}'.format(result[0])))
                    elif reg['data_type'] is 'uint16':
                        result = client.read_holding_registers(slave_addr=server_config['modbus_id'],starting_addr=reg['register_start'],register_qty=1,signed=False)
                        result = struct.unpack('!H', bytes.fromhex('{0:04x}'.format(result[0])))
                    elif reg['data_type'] is 'int32':
                        result = client.read_holding_registers(slave_addr=server_config['modbus_id'],starting_addr=reg['register_start'],register_qty=2,signed=False)
                        result = struct.unpack('!i', bytes.fromhex('{0:04x}'.format(result[0]) + '{0:04x}'.format(result[1])))
                    elif reg['data_type'] is 'uint32':
                        result = client.read_holding_registers(slave_addr=server_config['modbus_id'],starting_addr=reg['register_start'],register_qty=2,signed=False)
                        result = struct.unpack('!I', bytes.fromhex('{0:04x}'.format(result[0]) + '{0:04x}'.format(result[1])))
                    elif reg['data_type'] is 'int64':
                        result = client.read_holding_registers(slave_addr=server_config['modbus_id'],starting_addr=reg['register_start'],register_qty=4,signed=False)
                        result = struct.unpack('!q', bytes.fromhex('{0:04x}'.format(result[0]) + '{0:04x}'.format(result[1]) + '{0:04x}'.format(result[2]) + '{0:04x}'.format(result[3])))
                    elif reg['data_type'] is 'uint64':
                        result = client.read_holding_registers(slave_addr=server_config['modbus_id'],starting_addr=reg['register_start'],register_qty=4,signed=False)
                        result = struct.unpack('!q', bytes.fromhex('{0:04x}'.format(result[0]) + '{0:04x}'.format(result[1]) + '{0:04x}'.format(result[2]) + '{0:04x}'.format(result[3])))
                elif reg['register_type'] == 'input_registers':
                    if reg['data_type'] is 'float':
                        result = client.read_input_registers(slave_addr=server_config['modbus_id'],starting_addr=reg['register_start'],register_qty=2,signed=False)
                        result = struct.unpack('!f', bytes.fromhex('{0:04x}'.format(result[0]) + '{0:04x}'.format(result[1])))
                    elif reg['data_type'] is 'float_cdab':
                        result = client.read_input_registers(slave_addr=server_config['modbus_id'],starting_addr=reg['register_start'],register_qty=2,signed=False)
                        result = struct.unpack('!f', bytes.fromhex('{0:04x}'.format(result[1]) + '{0:04x}'.format(result[2])))   
                    elif reg['data_type'] is 'int16':
                        result = client.read_input_registers(slave_addr=server_config['modbus_id'],starting_addr=reg['register_start'],register_qty=1,signed=False)
                        result = struct.unpack('!h', bytes.fromhex('{0:04x}'.format(result[0])))
                    elif reg['data_type'] is 'uint16':
                        result = client.read_input_registers(slave_addr=server_config['modbus_id'],starting_addr=reg['register_start'],register_qty=1,signed=False)
                        result = struct.unpack('!H', bytes.fromhex('{0:04x}'.format(result[0])))
                    elif reg['data_type'] is 'int32':
                        result = client.read_input_registers(slave_addr=server_config['modbus_id'],starting_addr=reg['register_start'],register_qty=2,signed=False)
                        result = struct.unpack('!i', bytes.fromhex('{0:04x}'.format(result[0]) + '{0:04x}'.format(result[1])))
                    elif reg['data_type'] is 'uint32':
                        result = client.read_input_registers(slave_addr=server_config['modbus_id'],starting_addr=reg['register_start'],register_qty=2,signed=False)
                        result = struct.unpack('!I', bytes.fromhex('{0:04x}'.format(result[0]) + '{0:04x}'.format(result[1])))
                    elif reg['data_type'] is 'int64':
                        result = client.read_input_registers(slave_addr=server_config['modbus_id'],starting_addr=reg['register_start'],register_qty=4,signed=False)
                        result = struct.unpack('!q', bytes.fromhex('{0:04x}'.format(result[0]) + '{0:04x}'.format(result[1]) + '{0:04x}'.format(result[2]) + '{0:04x}'.format(result[3])))
                    elif reg['data_type'] is 'uint64':
                        result = client.read_input_registers(slave_addr=server_config['modbus_id'],starting_addr=reg['register_start'],register_qty=4,signed=False)
                        result = struct.unpack('!q', bytes.fromhex('{0:04x}'.format(result[0]) + '{0:04x}'.format(result[1]) + '{0:04x}'.format(result[2]) + '{0:04x}'.format(result[3])))
                elif reg['register_type'] == 'coil':
                    result = client.read_coils(slave_addr=server_config['modbus_id'],starting_addr=reg['register_start'],coil_qty=1)
                elif reg['register_type'] == 'discrete_input':
                    result = client.read_discrete_inputs(slave_addr=server_config['modbus_id'],starting_addr=reg['register_start'],coil_qty=1)
                    
                if server_config['interface'] == 'RTU':
                    print(f"Server ID {server_config['modbus_id']} - {reg['name']} = {result[0]}")
                else:
                    print(f"Server ID {server_config['ip']} - {reg['name']} = {result[0]}")
                #Add to the MQTT payload
                mqtt_data[reg['name']] = result[0]
            #Generate the MQTT payload and queue for transmission
            mqtt_pub_queue.put_nowait(ujson.dumps(mqtt_data))
        except Exception as e:
            print(f"Error reading Modbus Server ID {server_config['modbus_id']}: {str(e)}")
            if (e.errno == errno.ENOTCONN) or (e.errno == errno.ETIMEDOUT):                
                #Try to reconnect the socket
                try:
                    if 'error_cnt' in server_config:
                        server_config['error_cnt'] = server_config['error_cnt'] + 1
                    else:
                        server_config['error_cnt'] = 1
                    if server_config['error_cnt'] > 3:
                        server_config['error_cnt'] = 0
                        print(f"Trying to restart socket for {server_config['ip']}")
                        client = ModbusTCPMaster(slave_ip=server_config['ip'], slave_port=server_config['port'])
                except Exception as e:
                    print(f"Connection error Modbus Server ID {server_config['modbus_id']}: {str(e)}")

        await asyncio.sleep(server_config['poll_interval'])

# Function to create and run Modbus clients
async def run_modbus_clients(servers_config):
    tasks = []
    for server_config in servers_config:
        if server_config['interface'] == 'RTU':
            uart = UART(2, baudrate=9600, bits=8, parity=None, stop=2)  # Adjust UART settings as needed
            client = modbus_serial.ModbusSerial(uart, mode=modbus_serial.MODE_RTU, unit_addr=server_config['modbus_id'])
        elif server_config['interface'] == 'TCP':
            client = ModbusTCPMaster(slave_ip=server_config['ip'], slave_port=server_config['port'])

        task = asyncio.create_task(poll_modbus_server(client, server_config))
        tasks.append(task)
    #Add the mqtt coro
    task = asyncio.create_task(mqtt_operations(mqtt_client))
    tasks.append(task)
    #Now add the web server coro
    task = asyncio.create_task(web_ui.app.serve())
    tasks.append(task)
    await asyncio.gather(*tasks)

# Main Execution
# Set up the MQTT and wifi config
wifi_config = read_config('wifi.json')
config['ssid'] = wifi_config['ssid']
config['wifi_pw'] = wifi_config['password']

# Define configuration
mqtt_config = read_config('mqtt.json')
config['subs_cb'] = sub_cb
#config['connect_coro'] = conn_han
config['clean'] = True
config['server'] = mqtt_config['server']
config['port'] = mqtt_config['port']

MQTTClient.DEBUG = True  # Optional
mqtt_client = MQTTClient(config)

servers_config = read_config('config.json')
print(servers_config)
asyncio.run(run_modbus_clients(servers_config))