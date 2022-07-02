#---------------------------------------------------------------------------
# LEDBlink -
#---------------------------------------------------------------------------

PIN_DEFAULT = 99

class LEDBlink:
    def __init__(self,
                poller ,
                led_pin = PIN_DEFAULT) :
        print (__class__, "init")
        self.poller = poller
        self.led_pin = led_pin
        self.on_ms = 500
        self.off_ms = 1500
        self.led_on = False
        self.active_next_ms = self.poller.active_next_ms (0)
        #---- Initialize LED output pin here

    def poll_it (self) :
        #print ("PlugInLEDBlink: poll_it")
        if not self.poller.active_now (self.active_next_ms) :
            return
        #print ("PlugInLEDBlink: active")
        if self.led_on :
            self.led_on = False
            #---- Turn off LED here
            print (__class__, "LED is OFF")
            self.active_next_ms \
                = self.poller.active_next_ms (self.off_ms)
        else :
            self.led_on = True
            #---- Turn on LED here
            print (__class__, "LED is ON")
            self.active_next_ms \
                = self.poller.active_next_ms (self.on_ms)
        #---- Poll code goes here

    def shutdown (self) :
        print (__class__, "shutdown")
        #---- Shutdown code goes here
        self.led_on = False
        #---- Turn off LED here
        print (__class__, "LED is OFF")

# end PlugInTemplate #