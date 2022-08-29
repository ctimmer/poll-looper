#
################################################################################
# The MIT License (MIT)
#
# Copyright (c) 2022 Curt Timmerman
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
################################################################################
#

try:
    from machine import Pin, freq
except:
    def freq (f="default") :
        return f

import sys
MICRO_PYTHON = sys.implementation.name == "micropython"

MACHINE_FREQ = 240000000         # Ignored if <= 0

CROSSWALK_PIN = None
#CROSSWALK_PIN = 35               # Button pin

POLL_INTERVAL_MS = 100            # milliseconds
USE_ASYNCIO = False

#---- Example module:
from poll_looper import PollLooper

#---- Example plugins:
#-------------------------------------------------------------------------------
# TL_Controller
#   o Controls red/green/yellow and walk/dontwalk states
#   o Crossing request ony affects the green light state
#     If the second_counter > dont_walk_start_seconds
#       set the second_counter to dont_walk_start_seconds
#-------------------------------------------------------------------------------

class TL_Controller :

    def __init__ (self ,
                poller ,
                red_on_seconds = 10 ,
                green_on_seconds = 15 ,
                yellow_on_seconds = 4 ,
                dont_walk_start_seconds = 8
                ) :
        self.poller = poller
        self.active_interval_ms = poller.seconds_to_ms (1)
        self.active_next_ms = self.poller.active_next_ms (0)
        self.red_on_seconds = red_on_seconds
        self.green_on_seconds = green_on_seconds
        self.yellow_on_seconds = yellow_on_seconds
        self.dont_walk_start_seconds = dont_walk_start_seconds
        self.second_counter = 0
        self.display = poller.message_set ("display" ,
                                            {"red" : "RED" ,
                                             "green" : "GRN" ,
                                             "yellow" : "YEL" ,
                                             "walk" : "WK" ,
                                             "dontwalk" : "DW"
                                             })
        poller.message_set ("state" ,
                            {"light_on" : self.display ["red"] ,
                            "walk_display" : self.display ["dontwalk"] ,
                            "crossing_request" : False})
        self.state = poller.message_get ("state")
        self.next_light_on = self.display ["red"]

    def poll_it (self) :
        #print (__class__, "poll_it")
        if not self.poller.active_now (self.active_next_ms) :
            return
        self.active_next_ms \
            = self.poller.active_next_ms (self.active_interval_ms)
        #print (__class__, "poll_it: active")           # every second
        self.state ["light_on"] = self.next_light_on
        if self.state ["light_on"] == self.display["red"] : # "red" state
            if self.second_counter <= 0 :               # First cycle
                self.second_counter = self.red_on_seconds
                self.state ["walk_display"] = self.display["dontwalk"]
            else :
                self.second_counter -= 1
                if self.second_counter < 1 :
                    self.next_light_on = self.display["green"] # switch
        elif self.state ["light_on"] == self.display["green"] : # "green" state
            if self.second_counter <= 0 :               # First cycle
                self.second_counter = self.green_on_seconds
                self.state ["walk_display"] = self.display["walk"]
                self.state ["crossing_request"] = False
            else :
                self.second_counter -= 1
                if self.second_counter < 1 :
                    self.next_light_on = self.display["yellow"] # switch
                elif self.state ["crossing_request"] :
                    if self.second_counter > self.dont_walk_start_seconds :
                        self.second_counter = self.dont_walk_start_seconds
                if self.second_counter <= self.dont_walk_start_seconds :
                    #self.state ["walk_display"] = self.display["dontwalk"]
                    self.state ["walk_display"] \
                        = "{wk} {secs:02}".format (wk=self.display["dontwalk"],
                                                    secs=self.second_counter)
        elif self.state ["light_on"] == self.display["yellow"] : # "yellow" state
            if self.second_counter <= 0 :               # First cycle
                self.second_counter = self.yellow_on_seconds
                self.state ["walk_display"] = self.display["dontwalk"]
            else :
                self.second_counter -= 1
                if self.second_counter < 1 :
                    self.next_light_on = self.display["red"]  # switch
        else :
            print ("light_on:", self.state ["light_on"])

    def crossing_request (self) :           # Called by interrupt handler
        self.state ["crossing_request"] = True

    def shutdown (self) :
        pass

# end TL_Controller

#-------------------------------------------------------------------------------
# TL_CrossingRequest - Handle request to cross traffic
#   o In a "real world" implementation this class would test if an
#     input PIN is pressed
#-------------------------------------------------------------------------------
class TL_CrossingRequest :

    def __init__ (self ,
                poller ,
                button_pin = None) :
        self.poller = poller
        self.button_pin = button_pin
        self.button_pushed = False          # crossing request
        self.state = poller.message_get ("state")

    def poll_it (self) :
        #print (__class__, "poll_it")
        if self.button_pushed :
            self.state ["crossing_request"] = True
            self.button_pushed = False
        #---- This would normally be used to test an input pin

    def crossing_request (self ,
                          pin = None) :     # Called by interrupt handler
        #print (__class__, "crossing_request")
        self.button_pushed = True

    def shutdown (self) :
        pass

# end TL_CrossingRequest

#-------------------------------------------------------------------------------
# TL_View - Displays current stop light and walk/dontwalk state
#   o Only shows display when it changes
#   o In a "real world" implementation this class would turn on/off LEDs
#-------------------------------------------------------------------------------
class TL_View :

    def __init__ (self ,
                poller
                ) :
        self.poller = poller
        self.state = poller.message_get ("state")
        self.display = poller.message_get ("display")
        self.previous_display = ""
        self.current_display = ""

    def poll_it (self) :
        #print (__class__, "poll_it")
        self.current_display = self.state["light_on"] \
                        + " " + self.state["walk_display"]
        if self.current_display != self.previous_display :
            print (self.current_display)
            self.previous_display = self.current_display

    def shutdown (self) :
        self.state["light_on"] = self.display["red"]
        self.state["walk_display"] = "shutdown"
        self.poll_it ()

# end TL_View

#-------------------------------------------------------------------------------
# main
#-------------------------------------------------------------------------------

if MACHINE_FREQ > 0 :
    freq (MACHINE_FREQ)
    print ("machine.freq:", freq())

poller = PollLooper (POLL_INTERVAL_MS,
                     use_asyncio = USE_ASYNCIO)

crossing_request = TL_CrossingRequest (poller)

poller.poll_add (TL_Controller (poller))
poller.poll_add (crossing_request)
poller.poll_add (TL_View (poller))

if CROSSWALK_PIN != None :
    crosswalk_ir = Pin (CROSSWALK_PIN, Pin.IN)
    crosswalk_ir.irq (trigger = Pin.IRQ_RISING ,
                      handler = crossing_request.crossing_request)
        
if USE_ASYNCIO :
    import uasyncio as asyncio
    async def poll_plugins () :
        while True :
            #print ("poll_plugins: entry:")
            sleep_ms = poller.poll_wait ()
            #---- poll_wait returns ms to wait for next poll cycle
            await asyncio.sleep_ms (sleep_ms)
            #---- polls plugins added to poll-looper
            poller.poll_plugins ()
    async def main() :
        asyncio.create_task (poll_plugins())
        #---- Create additional tasks here
        while True:
            await asyncio.sleep(1)
    asyncio.run (main ())           # start the traffic lights
else :
    poller.poll_start ()            # normal startup
