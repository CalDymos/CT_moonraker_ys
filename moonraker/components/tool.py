import json
import logging
import os
import re, threading
from subprocess import call
import time
import random


def send(msg, data={}):
    pipeFilePath = "/mnt/UDISK/pipe"
    try:
        if not os.path.exists(pipeFilePath):
            call("touch %s" % pipeFilePath, shell=True)
            os.chmod(pipeFilePath, 0o700)
        net_state = call("ping -c 2 -w 2 api.crealitycloud.com > /dev/null 2>&1", shell=True)
        if net_state:
            return
        ret = re.findall('key.*?,', msg)
        if ret:
            msg = ret[0].strip('"').strip(",").replace('"', '')
            if os.path.getsize(pipeFilePath) > 0:
                random_float = random.uniform(0.1, 1)
                time.sleep(random_float)

            if os.path.getsize(pipeFilePath) == 0:
                send_data = {"reqId": str(int(time.time()*1000)), "dn": "00000000000000", "code": msg, "data": data}
                with open(pipeFilePath, "w") as f:
                    f.write(json.dumps(send_data))
                    f.flush()
    except Exception as err:
        logging.error("reportInformation err:%s" % err)

def reportInformation(msg, data={}):
    t = threading.Thread(target=send, args=(msg, data))
    t.start()
