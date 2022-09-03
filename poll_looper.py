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
# PollLooper.py - Poll multiple plugins
#
# class PollLooper
#   methods:
#     __init__
#     poll_init - Initialize poll timing
#     poll_add - Add plugin to poll loop
#     poll_start - Start polling loop
#     poll_wait - Sleep between poll loops
#     running - Returns True if poll is running
#     shutdown - Sets running status to False
#     seconds_to_ms - Computes seconds to milliseconds
#     minutes_to_ms - Computes minutes to milliseconds
#     hours_to_ms - Computes hours to milliseconds
#     get_current_time_ms - Returns current millisecond counter
#     allow_timeout - Ignore (no error) poll timeout
#     message_set - Set global data
#     message_get - Get global data
#     message_get_entry - Get global dictionary entry
#
################################################################################
#


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

try :
    import uasyncio as asyncio
except :
    pass

import gc

#---------------------------------------------------------------------------
# PollLooper
#---------------------------------------------------------------------------
class PollLooper :
    
    def __init__(self,
                 poll_ms = 100 ,         # default poll interval: 0.1 sec
                 use_asyncio = False) :
        #print ("Globals: init")
        self.current_time_ms = time.ticks_ms ()
        self.use_asyncio = use_asyncio
        self.poll_interval_ms = poll_ms
        self.poll_time_ms = 0
        self.poll_time_next_ms = 0      # Next poll time
        self.poll_init ()
        self.plugin_array = []          # PlugIn's to be polled
        self.message_data = {}
        self.states = {
            'running' : True
            }
        self.show_timeout = True

    def poll_init (self) :
        self.poll_time_ms = time.ticks_ms () # Current poll time
        if self.poll_interval_ms > 0 :
            self.poll_time_next_ms = time.ticks_add (self.poll_time_ms,
                                                    self.poll_interval_ms)

    def poll_add (self, plugin) :
        self.plugin_array.append (plugin)

    def poll_start (self) :
        gc.collect ()
        try :
        #if True :
            while self.states['running'] :
                self.poll_plugins ()
                self.poll_wait ()       # wait for next poll cycle
        except Exception as e :
            print ("poll_it: exception")
            print (e)
        finally :
            print ("Poll completed")
            for plugin in self.plugin_array :
                try :
                    plugin.shutdown ()
                except :
                    print ("plugin shutdown", plugin.__class__, "exception")
            print ("That's all folks")

    def poll_wait (self) :
        #print ("Globals: ======> poll_wait:", time.time())
        sleep_time_ms = 0
        if not self.states['running'] :
            return                  # shutting down
        self.current_time_ms = time.ticks_ms ()
        if self.poll_interval_ms <= 0 :
            self.poll_time_ms = self.current_time_ms
            return sleep_time_ms    # poll delay controlled externally
        #---- Set poll delay
        if time.ticks_diff (self.poll_time_next_ms, self.current_time_ms) <= 0 :
            if self.show_timeout :
                print ("poll_wait: too much time: Next" ,
                        self.poll_time_next_ms ,
                        "Curr:", self.current_time_ms)
            else :
                self.show_timeout = True
            self.poll_time_ms = self.current_time_ms
        else :
            #print ("Poll loop OK")
            sleep_time_ms = time.ticks_diff (self.poll_time_next_ms,
                                            self.current_time_ms)
            if sleep_time_ms < 0 :
                sleep_time_ms = 0
            if not self.use_asyncio :
                time.sleep_ms (sleep_time_ms)
            self.poll_time_ms = self.poll_time_next_ms
        self.poll_time_next_ms = time.ticks_add (self.poll_time_ms,
                                                self.poll_interval_ms)
        #print ("ptn:",self.poll_time_next_ms,"pt:",self.poll_time_ms)
        #print ("sleep_ms:", sleep_time_ms)
        return sleep_time_ms
    def poll_plugins (self) :
        #print (__class__)
        for plugin in self.plugin_array :     # poll each plugin
            plugin.poll_it ()

    def running (self) :
        return self.states['running']
    def shutdown (self) :
        print ("Shutdown requested")
        self.states['running'] = False

    def seconds_to_ms (self, interval_seconds) :
        return round (interval_seconds * 1000)
    def minutes_to_ms (self, interval_minutes) :
        return self.seconds_to_ms (interval_minutes) * 60
    def hours_to_ms (self, interval_hours) :
        return self.minutes_to_ms (interval_hours) * 60
    def get_current_time_ms (self) :
        return self.current_time_ms
    def allow_timeout (self) :
        self.show_timeout = False

    def active_next_ms (self, interval_ms) :
        return time.ticks_add (self.poll_time_ms, interval_ms)
    def active_now (self, next_active_ms) :
        return time.ticks_diff (self.poll_time_ms, next_active_ms) >= 0

    def message_set (self, mess_id, mess_dict) :
        if not mess_id in self.message_data :        # New
            self.message_data[mess_id] = mess_dict
        else :                                       # Update
            for mess_key in mess_dict :
                self.message_data[mess_id][mess_key] = mess_dict[mess_key]
        self.message_data[mess_id]["last_update_ms"] = self.current_time_ms
        return self.message_data[mess_id]
    def message_get (self, mess_id) :
        if not mess_id in self.message_data :
            self.message_data[mess_id] = {}
        return self.message_data[mess_id]
    def message_set_entry (self, mess_id, entry_id, entry_value) :
        if not mess_id in self.message_data :       # new
            self.message_data[mess_id] = {}
        self.message_data[mess_id][entry_id] = entry_value
        self.message_data[mess_id]["last_update_ms"] = self.current_time_ms
    def message_get_entry (self, mess_id, entry_id) :
        if not mess_id in self.message_data :
            return None
        if not entry_id in self.message_data[mess_id] :
            return None
        return self.message_data[mess_id][entry_id]

# end PollLooper
