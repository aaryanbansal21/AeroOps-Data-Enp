import signal
import sys

def handler(signum, frame):
    print("Hung!")
    sys.exit(1)

signal.signal(signal.SIGALRM, handler)
signal.alarm(2)

print("Importing auth...")
import auth
print("Importing models...")
import models
print("Importing ingestion...")
import ingestion
print("Importing main...")
import main
print("All good!")
