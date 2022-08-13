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
    - `__init__` initializes WDT
    - `poll_it` feeds WDT
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
  - `TL_Controller`
    - Sets light sequence: RED->GRN->YEL
    - Sets WALK
      - "RED"/"YEL": "DW"
      - "GRN":
        - "WK" until \<= 8 seconds, then adds countdown
        - If crossing_request is True and countdown > 8, set countdown to 8
  - `crossing_request`
    - Sets crossing_request boolean
  - `TL_View`
    - Displays lights/walk state when there is a change
- Sample output:

```
$ python3 trafficlights.py
RED DW
GRN WK
GRN DW 08
GRN DW 07
GRN DW 06
GRN DW 05
GRN DW 04
GRN DW 03
GRN DW 02
GRN DW 01
GRN DW 00
YEL DW
RED DW
GRN WK
GRN DW 08
GRN DW 07
GRN DW 06
GRN DW 05
```