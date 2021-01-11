from collections import defaultdict
import threading, time

MAX_REQUESTS_PER_MINUTE = 60
REQUESTS = defaultdict(int)

def clear_rate_limits():
	while True:
		REQUESTS = defaultdict(int)
		print("tick")
		time.sleep(60)
		
def is_rate_limited(client):
	REQUESTS[client] += 1
	if 0 == REQUESTS[client] % 10:
		print(client + " has made " + str(REQUESTS[client]) + " requests.")
	return REQUESTS[client] > MAX_REQUESTS_PER_MINUTE
	
request_sched_thread = threading.Thread(target=clear_rate_limits, daemon=True)
request_sched_thread.start()