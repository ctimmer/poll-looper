#---------------------------------------------------------------------------
# ShutdownTimer - Shut down after predetermined time interval
#---------------------------------------------------------------------------

try :
    import utime as time
except :
    from types import MethodType
    import time as time
    def ticks_ms(self):
        return int (round (time.time () * 1000))
    def ticks_add(self, ms_1, ms_2):
        return ms_1 + ms_2
    def ticks_diff(self, ms_1, ms_2):
        return ms_1 - ms_2
    def sleep_ms (self, ms_1) :
        return time.sleep (ms_1 / 1000)
    time.ticks_ms = MethodType (ticks_ms, time)
    time.ticks_add = MethodType (ticks_add, time)
    time.ticks_diff = MethodType (ticks_diff, time)
    time.sleep_ms = MethodType (sleep_ms, time)

SHUTDOWN_HOURS = 0          # defaults - no shutdown
SHUTDOWN_MINUTES = 0
SHUTDOWN_SECONDS = 0

class ShutdownTimer :

    def __init__(self,
                 poller ,
                 hours = SHUTDOWN_HOURS ,
                 minutes = SHUTDOWN_MINUTES ,
                 seconds = SHUTDOWN_SECONDS) :
        self.poller = poller
        self.run_ms = poller.hours_to_ms (hours) \
                           + poller.minutes_to_ms (minutes) \
                           + poller.seconds_to_ms (seconds)
        self.start_time_ms = poller.get_current_time_ms ()
        self.run_time_ms = self.start_time_ms
        self.last_time_ms = self.start_time_ms
        self.stop_time_ms = self.start_time_ms + self.run_ms

    def poll_it (self) :
        if self.run_ms <= 0 :
            return                   # Not set - exit
        current_time_ms = self.poller.get_current_time_ms ()
        self.run_time_ms += time.ticks_diff (current_time_ms, self.last_time_ms)
        self.last_time_ms = current_time_ms
        if self.run_time_ms >= self.stop_time_ms :
            self.poller.shutdown ()

    def shutdown (self) :
        pass

# end ShutdownTimer #

