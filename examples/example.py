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
#print (sys.implementation.name)

#---- Example module:
from poll_looper import PollLooper

#---- Example plugins:
from pi_shutdown_timer import ShutdownTimer
from pi_ledblink import LEDBlink
from pi_template import PlugInTemplate
from pi_garbage_collect import GarbageCollect
if MICRO_PYTHON :               # micropython only
    from pi_watchdog import Watchdog

POLL_INTERVAL = 100             # milliseconds

#-------------------------------------------------------------------------------
# main
#-------------------------------------------------------------------------------

poller = PollLooper (POLL_INTERVAL)

poller.poll_add (ShutdownTimer (poller ,
                                minutes = 0 ,
                                seconds = 30))
poller.poll_add (LEDBlink (poller))
poller.poll_add (PlugInTemplate (poller ,
                                poll_seconds = 5))
poller.poll_add (GarbageCollect (poller))
                                 
if MICRO_PYTHON :               # micropython only
    poller.poll_add (Watchdog (poller))

poller.poll_start ()
