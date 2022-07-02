#---------------------------------------------------------------------------
# PlugInTemplate - Does nothing, example plugin
#---------------------------------------------------------------------------

class PlugInTemplate:
    def __init__(self,
                poller ,
                poll_seconds = 5) :
        print (__class__, "init")
        self.poller = poller
        self.active_interval_ms = poller.seconds_to_ms (poll_seconds)
        self.active_next_ms = self.poller.active_next_ms (1500) # start after 1500ms

    def poll_it (self) :
        #print (__class__, "poll_it")
        if not self.poller.active_now (self.active_next_ms) :
            return
        self.active_next_ms \
            = self.poller.active_next_ms (self.active_interval_ms)
        #print (__class__, "active")
        #---- Poll code goes here

    def shutdown (self) :
        print (__class__, "shutdown")
        #---- Shutdown code goes here

# end PlugInTemplate #