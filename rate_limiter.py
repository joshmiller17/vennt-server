from collections import defaultdict
import threading, time

MAX_REQUESTS_PER_MINUTE = 60
REQUESTS = defaultdict(int)

def clear_rate_limits():
	while True:
		REQUESTS = defaultdict(int)
		time.sleep(60)
		
def is_rate_limited(client):
	REQUESTS[client] += 1
	return REQUESTS[client] > MAX_REQUESTS_PER_MINUTE
	
request_sched_thread = threading.Thread(target=clear_rate_limits, daemon=True)
request_sched_thread.start()