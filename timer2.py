import time

# Just 3 global variables
_timer_start_time = None
_timer_elapsed = 0
_timer_running = False

def timer_start():
    global _timer_start_time, _timer_running
    if not _timer_running:
        _timer_start_time = time.time()
        _timer_running = True

def timer_stop():
    global _timer_start_time, _timer_elapsed, _timer_running
    if _timer_running:
        _timer_elapsed += time.time() - _timer_start_time
        _timer_running = False

def timer_reset():
    global _timer_start_time, _timer_elapsed, _timer_running
    _timer_start_time = None
    _timer_elapsed = 0
    _timer_running = False

def timer_get():
    if _timer_running:
        return _timer_elapsed + (time.time() - _timer_start_time)
    return _timer_elapsed
