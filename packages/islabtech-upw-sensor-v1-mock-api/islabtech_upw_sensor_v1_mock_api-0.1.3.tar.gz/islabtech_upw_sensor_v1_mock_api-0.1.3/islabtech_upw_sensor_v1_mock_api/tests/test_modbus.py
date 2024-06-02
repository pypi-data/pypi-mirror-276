"""
tests the Modbus/TCP API
"""

# pylint: disable=logging-fstring-interpolation

# imports
from __future__ import annotations
from typing import Optional
import time
import threading
import logging
import pytest
import pymodbus.pdu
import pymodbus.client
from islabtech_upw_sensor_v1_mock_api import run_mock_api

# state
SERVER_THREAD: Optional[threading.Thread] = None
CLIENT: pymodbus.client.ModbusTcpClient
HOST = "localhost"
PORT = 1502

# logging
logging.basicConfig(level=logging.DEBUG)
logging.info("running Modbus/TCP tests...")


def pytest_generate_tests(metafunc):
    """required to process parameters from pytest_addoption (v.s.)"""
    global HOST  # pylint: disable=global-statement
    host = None
    try:
        host = metafunc.config.getoption("host")
    except ValueError:
        pass
    if host is not None:
        HOST = str(host)

    global PORT  # pylint: disable=global-statement
    port = None
    try:
        port = metafunc.config.getoption("port")
    except ValueError:
        pass
    if port is not None:
        PORT = int(port)


def test_start_mock_api():
    """starts a local mock API server – this gets skipped if a remote host+port are specified"""
    if HOST != "localhost" or PORT != 1502:
        pytest.skip(reason="specified custom server, not connecting to local mock API")
    global SERVER_THREAD  # pylint: disable=global-statement
    SERVER_THREAD = threading.Thread(target=run_mock_api, daemon=True)
    SERVER_THREAD.start()
    time.sleep(1.0)
    assert SERVER_THREAD.is_alive(), "can not start mock Modbus/TCP server"


def test_connect_to_mock_api():
    """checks TCP connection to the Modbus/TCP server"""
    global CLIENT  # pylint: disable=global-statement
    CLIENT = pymodbus.client.ModbusTcpClient(host=HOST, port=PORT)
    CLIENT.connect()
    assert CLIENT.connected, f"can not connect to mock api on {HOST}:{PORT}"


def test_coil_connect_to_wifi():
    """checks coil 100: connect to WiFi AP"""
    response: pymodbus.pdu.ModbusResponse = CLIENT.read_coils(100, 1)
    assert response.isError() is False, "can not fetch coil 100: connect to WiFi AP"
    value: bool = response.bits[0]

    response = CLIENT.write_coil(100, not value)
    assert response.isError() is False, "can not write to coil 100: connect to WiFi AP"

    response = CLIENT.read_coils(100, 1)
    assert (
        response.isError() is False
    ), "can fetch coil 100 (connect to WiFi API) once but not again after writing to it"
    assert (
        response.bits[0] is not value
    ), "can write to coil 100 (connect to WiFi AP), but its value has not changed"


def test_read_conductivity():
    """reads conductivity and checks for plausibility"""
    response = CLIENT.read_input_registers(10, 1)
    assert response.isError() is False
    print(f"response: {response.registers}")
    value = response.registers[0]
    assert value > 10 and value < 10e3, "implausible conductivity"

    response = CLIENT.read_discrete_inputs(10, 1)
    assert response.isError() is False
    binary_value = response.bits[0]
    assert (  # add some fuzziness because the value might have changed since the above reading
        value < 1200 and binary_value is True
    ) or (
        value >= 1000 and binary_value is False
    )


def test_read_temperature():
    """reads temperature and checks for plausibility"""
    response = CLIENT.read_input_registers(20, 1)
    assert response.isError() is False
    value = response.registers[0]
    assert value > 0 and value < 110e2, "implausible temperature"

    response = CLIENT.read_discrete_inputs(20, 1)
    assert response.isError() is False
    binary_value = response.bits[0]
    assert (  # add some fuzziness because the value might have changed since the above reading
        value < 26e2 and binary_value is True
    ) or (
        value >= 24e2 and binary_value is False
    )


def test_firmware_version():
    """
    reads firmware version and checks for plausibility; also makes sure that it is not writable
    """
    response = CLIENT.read_input_registers(310, 3)
    assert response.isError() is False, "can not read firmware version"
    assert response.registers[0] == 0, "implausible firmware version"

    response = CLIENT.write_register(310, 5)
    assert response.isError(), "should not be able to change firmware version"

    response = CLIENT.read_input_registers(310, 2)
    assert response.isError() is False
    assert response.registers[0] == 0, "should not be able to change firmware version"


def test_close_connection():
    """closes the previously opened TCP connection to the Modbus/TCP server"""
    CLIENT.close()
    assert CLIENT.connected is False, "can not close TCP connection"


# def test_stop_mock_api():
#     # TODO
#     pass
