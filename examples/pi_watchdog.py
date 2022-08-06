#---------------------------------------------------------------------------
# Watchdog
#---------------------------------------------------------------------------

import machine

WATCHDOG_TIMEOUT_MS = 2000              # 2 seconds

class Watchdog:

    def __init__(self ,
                 poller ,
                 wd_timeout_ms = WATCHDOG_TIMEOUT_MS) :
        #print ("Watchdog: init")
        self.poller = poller            # not used, could be omitted
        try :
            self.wdt = machine.WDT (timeout=wd_timeout_ms)
        except :
            self.wdt = machine.WDT ()   # esp8266?

    def poll_it (self) :
        #print ("Watchdog: poll_it")
        self.wdt.feed ()                # Still going

    def shutdown (self) :
        pass

# end Watchdog #

