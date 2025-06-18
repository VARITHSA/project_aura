import datetime
import json
import os
import time


class GeminiUsageLimiter:
    def __init__(self, daily_limit = 150, min_interval =5):
        """
        daily_limit: Maximum number of API calls allowed per day.
        min_interval: Minimum time interval between API calls in seconds.
        """
        self.daily_limit = daily_limit
        self.min_interval = min_interval
        self.log_file = "gemini_usage_log.json"
        self.load_usage()
        
    def load_usage(self):
        today = datetime.date.today().isoformat()
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as f:
                self.usage_log = json.load(f)
        else:
            self.usage_log = {}
        if today not in self.usage_log:
            self.usage_log[today] = {
                "count": 0,
                "last_call": 0
            }
    def save_usage(self):
        with open(self.log_file,"w") as f:
            json.dump(self.usage_log, f)
            
    def can_make_call(self):
        today = datetime.date.today().isoformat()
        current_time = time.time()
        day_usage = self.usage_log[today]
        
        if day_usage["count"] >= self.daily_limit:
            print(f" ⚠️ Daily limit of {self.daily_limit} API calls reached.")
            return False
        
        if current_time - day_usage["last_call"] < self.min_interval:
            print(f" ⚠️ Minimum interval of {self.min_interval} seconds not met since last call.")
            return False
        
        return True
    
    def record_call(self):
        today = datetime.date.today().isoformat()
        current_time = time.time()  
        self.usage_log[today]["count"] += 1
        self.usage_log[today]["last_call"] = current_time
        self.save_usage()
    
    
