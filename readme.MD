# poll-looper
## micropython module for managing multiple I/O plugins

### __Components__
#### PollLooper Module
```
from poll_looper import PollLooper
# def's for InputPlugin and OutputPlugin (see Plugins)

POLL_INTERVAL = 200

my_poller = PollLooper (POLL_INTERVAL)

my_input_plugin InputPlugin (my_poller)
my_output_plugin OutputPlugin (my_poller)

my_poller.poll_add (my_input_plugin)
my_poller.poll_add (my_output_plugin)
my_poller.start ()
```
##### __Description__
- If the optional POLL_INTERVAL parameter the default value is 100ms
- Plugins will be polled in the same order they are entered
  - Usually plugins that read input would be added first
  - Plugins that react to input changes would be added next
  - Plugins that operate independently can be added anywhere
- The 'start' method initiates the polling loop
  - Polling can be interrupted by the operator
  - Polling can be terminated with the PollLooper 'shutdown' method
##### __Methods__
- \_\_init\_\_
  - saves poll_interval
- Poll handling
  - poll_add (\<Plugin Object\>) - Add plugin to poll loop
  - poll_start () - Start polling loop
  - poll_wait () - Sleep between poll loops
    - Normally only called internally
  - running () - Returns True if poll is running
  - shutdown () - Sets running status to False
- Poll timer handling
  - seconds_to_ms(\<seconds\>) - Computes seconds to milliseconds
  - minutes_to_ms(\<minutes\>) - Computes minutes to milliseconds
  - hours_to_ms(\<hours\>) - Computes hours to milliseconds
  - get_current_time_ms() - Returns current millisecond counter
  - allow_timeout() - Ignore (no error) poll timeout
- Plugin to plugin communication handling
  - message_set(\<dict ID\>, {\<dict values\>}) - Set global data
  - message_get(\<dict ID\>) - Get global data
  - message_set_entry(\<dict ID\>, \<ent ID\>, \<val\>) - Set global dictionary entry
  - message_get_entry(\<dict ID\>) - Get global dictionary entry
##### __Notes:__
- This module was written for micropython, it will run with python3

#### PollLooper Plugins
```
class PlugInTemplate:
    def __init__(self,
                poller ,
                poll_seconds = 5) :
        #print (__class__, "init")
        self.poller = poller
        self.active_interval_ms = poller.seconds_to_ms (poll_seconds)
        self.active_next_ms = self.poller.active_next_ms (0)

    def poll_it (self) :
        #print (__class__, "poll_it")
        if not self.poller.active_now (self.active_next_ms) :
            return
        self.active_next_ms \
            = self.poller.active_next_ms (self.active_interval_ms)
        #print (__class__, "active")
        #---- Poll code goes here

    def shutdown (self) :
        #print (__class__, "shutdown")
        #---- Shutdown code goes here
        pass

# end PlugInTemplate #
```
##### __Description__
- Do whatever action is required when active
  - Read/write GPIO pins
  - Test for network input
  - Shut down PollLooper
##### __Methods__
- \_\_init\_\_
  - There are no required parameters for plugins
  - The PollLooper instance is passed in to take advantage of it's utility methods
- poll_it, the only required plugin method
  - This method is called on every poll loop
  - 'active_now' returns True if enough ms have passed since the last time the plugin was active
  - 'active_next_ms' sets the time when the plugin will next be active
- shutdown, called when the polling has been stopped
##### __Notes__
- A plugin should never block unless it sets the poll interval
