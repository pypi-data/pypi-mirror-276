# ----------------------------
# Test dialler to show use of dc09_msg class
# (c 2018 van Ovost Automatisering b.v.
# Author : Jacq. van Ovost
# ----------------------------
import sys

sys.path.append('../')
from my_dc09_spt import dc09_spt

import logging
logging.basicConfig(format='%(module)-12s %(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger()
#handler = logging.StreamHandler()
#logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

ACCOUNT_ID = "ACCOUNT_ID"

spt1 = dc09_spt.dc09_spt(ACCOUNT_ID)
spt1.set_path('main', 'primary', "localhost", 10011, account=ACCOUNT_ID, type='TCP')
spt1.send_msg('ADM-CID', {
    'account':  '124',
    'code': 400,
    'q': 1,
    'zone': 14,
    'speed': 10,
    'event_ts': 1717055979010,
    'battery_level': 100,
    'lat': 6.84714,
    'lon': -30.24099,
    'alt': 0
})