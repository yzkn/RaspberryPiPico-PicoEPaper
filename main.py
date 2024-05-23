#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2024 YA-androidapp(https://github.com/yzkn) All rights reserved.


import epaper_utility
import network_utility


import machine
import urequests
from microdot_asyncio import Microdot
import uasyncio



async def switch_loop():
    """
    Switch listener loop
    Pin 14 is used for switch input.
    When press switch, send request to http web server.
    """
    print('start switch_loop')
    switch_pin = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)

    while True:
        current_state = switch_pin.value()
        if current_state:
            # Change the URL to your own server, IFTTT, Slack, etc.
            response = urequests.get('https://example.com/')
            print(response.content)
            response.close()
            await uasyncio.sleep(2)
        else:
            await uasyncio.sleep(0.1)

async def run_web_server():
    """
    Start microdot web server
    https://microdot.readthedocs.io/en/latest/index.html
    """
    app = Microdot()
    led_pin = machine.Pin('LED', machine.Pin.OUT)

    @app.get('/')
    async def _index(request):
        return 'Microdot on Raspberry Pi Pico W'

    @app.get('/led/<status>')
    async def _led(request, status):
        """
        /led/on : LED ON
        /led/off : LED OFF
        """
        if status == 'on':
            led_pin.on()
            return 'LED turned on'
        elif status == 'off':
            led_pin.off()
            return 'LED turned off'
        return 'Invalid status.'

    print('microdot run')
    app.run(port=80)


def update_epaper():
    epd = epaper_utils.EPD_2in13_V4_Landscape()
    epd.Clear()

    epd.fill(0xff)
    epd.text("Waveshare", 0, 10, 0x00)
    # epd.text("ePaper-2.13_V4", 0, 20, 0x00)
    # epd.text("Raspberry Pico", 0, 30, 0x00)
    # epd.text("Hello World", 0, 40, 0x00)
    epd.display(epd.buffer)
    epd.delay_ms(2000)

    print("sleep")
    epd.init()
    epd.Clear()
    epd.delay_ms(2000)
    epd.sleep()


async def main():
    wlan = await network_utils.prepare_wifi()
    print('LED ON: http://{}/led/on'.format(wlan.ifconfig()[0]))

    uasyncio.create_task(switch_loop())
    await run_web_server()


if __name__ == '__main__':
    uasyncio.run(main())

