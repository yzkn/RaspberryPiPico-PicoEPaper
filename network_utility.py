#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2024 YA-androidapp(https://github.com/yzkn) All rights reserved.

import rp2
import network
import uasyncio
import WIFI_CONFIG


async def connect_wifi():
    rp2.country(secrets.COUNTRY)

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_CONFIG.SSID, WIFI_CONFIG.PSK)

    for i in range(10):
        status = wlan.status()
        if wlan.status() < 0 or wlan.status() >= network.STAT_GOT_IP:
            break
        print(f'status={status}')
        uasyncio.sleep(1)
    else:
        raise RuntimeError("network connection failed")

    # CYW43_LINK_DOWN (0)
    # CYW43_LINK_JOIN (1)
    # CYW43_LINK_NOIP (2)
    # CYW43_LINK_UP (3)
    # CYW43_LINK_FAIL (-1)
    # CYW43_LINK_NONET (-2)
    # CYW43_LINK_BADAUTH (-3)

    wlan_status = wlan.status()

    if wlan_status != network.STAT_GOT_IP:
        raise RuntimeError(
            'network connection failed status={}'.format(wlan_status))

    print('network connected ifconfig:', wlan.ifconfig())
    return wlan
