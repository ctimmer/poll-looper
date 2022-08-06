# poll-looper example applications

### __example.py__
- Plugins
  - LEDBlink (pi_ledblink.py)
    - Turns LED on (500ms) and off (1500ms)
    - Example of multiple active intervals.
      This produces a lighthouse effect.
  - PlugInTemplate (pi_template.py)
    - Minimal plugin example
  - GarbageCollect (pi_garbage_collect.py)
    - Runs garbage collection (gc) at a regular interval (5 seconds)
  - ShutdownTimer (pi_shutdown_timer.py)
    - Shuts down PollLooper after set time
  - Watchdog (pi_watchdog.py)
    - \_\_init\_\_ initializes WDT
    - poll_it feeds WDT
- Sample output:
```
$ python3 example.py
<class 'pi_ledblink.LEDBlink'> init
<class 'pi_template.PlugInTemplate'> init
<class 'pi_garbage_collect.GarbageCollect'> init
<class 'pi_ledblink.LEDBlink'> LED is ON
<class 'pi_ledblink.LEDBlink'> LED is OFF
<class 'pi_ledblink.LEDBlink'> LED is ON
<class 'pi_ledblink.LEDBlink'> LED is OFF
<class 'pi_ledblink.LEDBlink'> LED is ON
<class 'pi_ledblink.LEDBlink'> LED is OFF
<class 'pi_garbage_collect.GarbageCollect'> active
<class 'pi_ledblink.LEDBlink'> LED is ON
<class 'pi_ledblink.LEDBlink'> LED is OFF
<class 'pi_ledblink.LEDBlink'> LED is ON
<class 'pi_ledblink.LEDBlink'> LED is OFF
<class 'pi_ledblink.LEDBlink'> LED is ON
<class 'pi_garbage_collect.GarbageCollect'> active
<class 'pi_ledblink.LEDBlink'> LED is OFF
<class 'pi_ledblink.LEDBlink'> LED is ON
<class 'pi_ledblink.LEDBlink'> LED is OFF
<class 'pi_ledblink.LEDBlink'> LED is ON
<class 'pi_ledblink.LEDBlink'> LED is OFF
<class 'pi_garbage_collect.GarbageCollect'> active
<class 'pi_ledblink.LEDBlink'> LED is ON
<class 'pi_ledblink.LEDBlink'> LED is OFF
<class 'pi_ledblink.LEDBlink'> LED is ON
<class 'pi_ledblink.LEDBlink'> LED is OFF
<class 'pi_ledblink.LEDBlink'> LED is ON
<class 'pi_garbage_collect.GarbageCollect'> active
<class 'pi_ledblink.LEDBlink'> LED is OFF
<class 'pi_ledblink.LEDBlink'> LED is ON
<class 'pi_ledblink.LEDBlink'> LED is OFF
<class 'pi_ledblink.LEDBlink'> LED is ON
<class 'pi_ledblink.LEDBlink'> LED is OFF
<class 'pi_garbage_collect.GarbageCollect'> active
<class 'pi_ledblink.LEDBlink'> LED is ON
<class 'pi_ledblink.LEDBlink'> LED is OFF
<class 'pi_ledblink.LEDBlink'> LED is ON
<class 'pi_ledblink.LEDBlink'> LED is OFF
<class 'pi_ledblink.LEDBlink'> LED is ON
<class 'pi_garbage_collect.GarbageCollect'> active
Shutdown requested
Poll completed
<class 'pi_ledblink.LEDBlink'> shutdown
<class 'pi_ledblink.LEDBlink'> LED is OFF
<class 'pi_template.PlugInTemplate'> shutdown
<class 'pi_garbage_collect.GarbageCollect'> shutdown
That's all folks
```

### __trafficlights.py__
- Controls RED/GREEN/YELLOW traffic lights and walk/dontwalk display
- Plugins
  - TL_Controller
    - Sets light sequence: RED->GREEN->YELLOW
    - Sets WALK
      - RED/YELLOW: "Dont Walk"
      - GREEN:
        - Walk until \<= 8 seconds, then countdown
        - If crossing_request is True and countdown > 8, set countdown to 8
  - crossing_request
    - Sets crossing_request boolean
  - TL_View
    - Displays lights/walk state when there is a change
- Sample output:
```
$ python3 trafficlights.py
red Dont Walk
green      Walk
green 8
green 7
green 6
green 5
green 4
green 3
green 2
green 1
green 0
yellow Dont Walk
red Dont Walk
green      Walk
green 8
green 7
green 6
```