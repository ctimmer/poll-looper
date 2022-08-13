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

import sys
MICRO_PYTHON = sys.implementation.name == "micropython"

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
        poller.message_set ("state" ,
                            {"light_on" : "RED" ,
                            "walk_display" : "DW" ,
                            "crossing_request" : False})
        self.state = poller.message_get ("state")
        self.next_light_on = "RED"

    def poll_it (self) :
        #print (__class__, "poll_it")
        if not self.poller.active_now (self.active_next_ms) :
            return
        self.active_next_ms \
            = self.poller.active_next_ms (self.active_interval_ms)
        #print (__class__, "poll_it: active")           # every second
        self.state ["light_on"] = self.next_light_on
        if self.state ["light_on"] == "RED" :           # "red" state
            if self.second_counter <= 0 :               # First cycle
                self.second_counter = self.red_on_seconds
                self.state ["walk_display"] = "DW"
            else :
                self.second_counter -= 1
                if self.second_counter < 1 :
                    self.next_light_on = "GRN"          # switch
        elif self.state ["light_on"] == "GRN" :         # "green" state
            if self.second_counter <= 0 :               # First cycle
                self.second_counter = self.green_on_seconds
                self.state ["walk_display"] = "WK"
                self.state ["crossing_request"] = False
            else :
                self.second_counter -= 1
                if self.second_counter < 1 :
                    self.next_light_on = "YEL"          # switch
                elif self.state ["crossing_request"] :
                    if self.second_counter > self.dont_walk_start_seconds :
                        self.second_counter = self.dont_walk_start_seconds
                if self.second_counter <= self.dont_walk_start_seconds :
                    #self.state ["walk_display"] = "DW"
                    self.state ["walk_display"] = "DW {secs:02}".format (secs=self.second_counter)
        elif self.state ["light_on"] == "YEL" :         # "yellow" state
            if self.second_counter <= 0 :               # First cycle
                self.second_counter = self.yellow_on_seconds
                self.state ["walk_display"] = "DW"
            else :
                self.second_counter -= 1
                if self.second_counter < 1 :
                    self.next_light_on = "RED"          # switch
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

    def crossing_request (self) :           # Called by interrupt handler
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
        self.previous_display = ""
        self.display = ""

    def poll_it (self) :
        #print (__class__, "poll_it")
        self.display = self.state["light_on"] \
                        + " " + self.state["walk_display"]
        if self.display != self.previous_display :
            print (self.display)
            self.previous_display = self.display

    def shutdown (self) :
        self.state["light_on"] = "RED"
        self.state["walk_display"] = "shutdown"
        self.poll_it ()

# end TL_View

POLL_INTERVAL = 100            # milliseconds

#-------------------------------------------------------------------------------
# main
#-------------------------------------------------------------------------------

poller = PollLooper (POLL_INTERVAL)

crossing_request = TL_CrossingRequest (poller)

poller.poll_add (TL_Controller (poller))
poller.poll_add (crossing_request)
poller.poll_add (TL_View (poller))

poller.poll_start ()
