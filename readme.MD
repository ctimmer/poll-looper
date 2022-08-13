# poll-looper
## micropython module for managing multiple I/O plugins

### __About__

After developing a couple of micropython applications utilizing convoluted IO loops with complicated sleep logic I thought there must be a more organized and modular way to handle this. PollLooper allows you to modularize IO interfaces with plugins that are polled at a specified interval.

### __Components__

#### PollLooper Module

```
from poll_looper import PollLooper

class InputPlugin :
    def __init__ (poller) :
        pass
    def poll_it (self) :
        pass
    def shutdown (self) :
        pass
class OutputPlugin :
    def __init__ (poller) :
        pass
    def poll_it (self) :
        pass
    def shutdown (self) :
        pass

POLL_INTERVAL = 200

my_poller = PollLooper (POLL_INTERVAL)

my_input_plugin = InputPlugin (my_poller)

my_poller.poll_add (my_input_plugin)
my_poller.poll_add (OutputPlugin (my_poller))
my_poller.start ()
```

##### __Description__

- If the POLL_INTERVAL parameter is omitted the default value is 100ms
  - The sleep time between polls is determined by the amount of time is used by the previous poll (poll_interval - poll_time).
  - If the poll time is greater than the poll interval the next poll loop is initiated immediately.
- Plugins will be polled in the same order they are entered
  - Usually plugins that read input would be added first
  - Plugins that react to input changes would be added next
  - Plugins that operate independently can be added anywhere
- The 'start' method initiates the polling loop
  - Polling can be interrupted by the operator
  - Polling can be terminated by calling PollLooper 'shutdown' method

##### __Class Variables__

- current_time_ms = time.ticks_ms ()
- poll_interval_ms = poll_ms
  - milliseconds for each poll cycle, default: 100
- poll_time_ms = time.ticks_ms ()
  - Current poll counter ms
- poll_time_next_ms = 0
- plugin_array = []
  - Array of plugin objects to be polled
- message_data = {}
  - Global dictionary for passing data between plugins. Each entry will be an ID:dict.
- states = {'running' : True}
  - `shutdown` method sets 'running' to False
- show_timeout = True
  - Displays error if poll interval ms is exceeded by plugin activity

##### __Methods__

- `__init__ (poll_interval=100)`
  - poll_interval defaults to 100 ms.
  - If the poll_interval is <= zero there will be no wait time between poll cycles. This allows plugin(s) to control the wait time.
- Poll handling
  - `poll_add (PluginObject)` - Adds plugin to poll loop
  - `poll_start ()` Start polling loop
  - `poll_wait ()` Sleep between poll loops
    - Normally only called internally
  - `running ()` Returns True if poll is running
  - `shutdown ()` Sets running status to False
- Poll timer handling
  - `seconds_to_ms (seconds)` Returns milliseconds
  - `minutes_to_ms (minutes)` Returns milliseconds
  - `hours_to_ms (hours)` Returns milliseconds
  - `get_current_time_ms ()` Returns current millisecond counter set at the beginning of the poll cycle.
  - `allow_timeout ()` Ignore (no error) poll timeout
  - `active_next_ms (ms)` Returns the poll counter ms of the next active milliseconds (current + ms).
  - `active_now (next_ms)` Returns True if the current poll ms > next_ms. next_ms is set by `active_next_ms`
  - Notes
    - `*_to_ms ()` methods can be passed decimal numbers. Example: `seconds_to_ms (1.5)` would return 1500.
    - Because ticks_ms used by poll cycle timing wraps after a maximum time, the poll intervals are limited to slightly less than a week.
- Plugin to plugin communication handling
  - `message_set(DictID, {ValuePairs})` Sets global data
  - `message_get(DictID)` Get global data
  - `message_set_entry(DictID, EntID, Value)` Set global dictionary entry
  - `message_get_entry(DictID, EntID)` Get global dictionary entry value

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
- `__init__ ()`
  - There are no required parameters for plugins
  - The PollLooper object is usually passed to take advantage of it's utility methods
- `poll_it ()`
  - The only required plugin method
  - Called on every poll cycle
  - Calls `active_now` and `active_next_ms` to determine if this plugin is active and set the next active ms
  - This method should never block unless it is used for the poll interval
- `shutdown ()` called when the polling has been stopped. This could be used by an oven controller to set the power level to zero.

### __References:__
- [ticks_ms functions](https://docs.micropython.org/en/latest/library/time.html)