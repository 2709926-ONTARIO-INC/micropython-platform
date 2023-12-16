import ujson
import uasyncio as asyncio
from machine import UART
import umodbus.serial as modbus_serial
from umodbus.tcp import TCP as ModbusTCPMaster
import socket
import struct

# Function to read configuration
def read_config(filename):
    with open(filename, 'r') as f:
        return ujson.load(f)

# Async function to poll a single Modbus server
async def poll_modbus_server(client, server_config):
    while True:
        try:
            for reg in server_config['registers']:
                if reg['register_type'] == 'holding_registers':
                    if reg['data_type'] is 'float':
                        result = client.read_holding_registers(slave_addr=server_config['modbus_id'],starting_addr=reg['register_start'],register_qty=2,signed=False)
                        result = struct.unpack('!f', bytes.fromhex('{0:02x}'.format(result[0]) + '{0:02x}'.format(result[1])))
                elif reg['register_type'] == 'input_registers':
                    result = client.read_input_registers(server_config['register_start'], server_config['register_count'])
                # Add more data type conditions as necessary

                print(f"Server ID {server_config['modbus_id']} - Received data: {result}")
        except Exception as e:
            print(f"Error reading Modbus Server ID {server_config['modbus_id']}: {str(e)}")

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

    await asyncio.gather(*tasks)

# Main Execution
servers_config = read_config('config.json')
print(servers_config)
asyncio.run(run_modbus_clients(servers_config))