import time

class common_utils:
    def __init__(self):
        self.start_time = time.time()
        self.request_count = 0

    def rate_limit(self):
        """
        A simple rate limiter that can be used to limit the number of requests made to an API.
        """
        # 1. Check if a full second has passed - then reset the counter and start time
        current_time = time.time()
        if current_time - self.start_time >= 1.0:
            self.start_time = current_time
            self.request_count = 0

        # 2. If we have made 10 requests in the current second, wait until the next second
        if self.request_count >= 10:
            print("Rate limit reached. Waiting for the next second...")
            time_to_wait = 1.0 - (current_time - self.start_time)
            if time_to_wait > 0:
                time.sleep(time_to_wait)
            self.start_time = time.time()
            self.request_count = 0
        
        # 3. Increment the request count for each request made
        self.request_count += 1