# base url for api
# BASE_URL = "https://ef5a-171-253-8-36.ngrok-free.app"
BASE_URL = "https://irrigationapi.onrender.com"

DEVIVE_ID = "BCM2708"
# state relay
ON = 1
OFF = 0

# Relay ID
RELAY_1 = 1
RELAY_2 = 2
RELAY_3 = 3
RELAY_4 = 4
RELAY_5 = 5
RELAY_6 = 6
PUMP_1 = 7
PUMP_2 = 8

# status of irrigation activity
IN_QUEUE=0
READY=1
DONE=2

# state fsm
IDLE=0 # no action required, everything is ok and the system can be used.
WAITING=1 # waiting for user input to start a new task or stop an existing one (or cancel)
RUNNING=2 # running a task
PAUSED=3 # paused by user request
ERROR=-1 # error occurred in any step

# sensor soil
TEMP = 0
HUMI = 1
PH =  2
EC = 3
N = 4
P = 5
K = 6

# state app
