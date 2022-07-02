#---------------------------------------------------------------------------
# Watchdog
#---------------------------------------------------------------------------

import machine

WATCHDOG_TIMEOUT_MS = 2000

class Watchdog:

    def __init__(self ,
                 poller ,
                 wd_timeout_ms = WATCHDOG_TIMEOUT_MS) :
        #print ("Watchdog: init")
        self.poller = poller
        self.wdt = machine.WDT (timeout=wd_timeout_ms)

    def poll_it (self) :
        #print ("Watchdog: poll_it")
        self.wdt.feed ()           # Still going

    def shutdown (self) :
        pass

# end Watchdog #

