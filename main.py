# pico-pomodoro
#
# uses: 
#     Pico Inky 296x128 eink display from Pimono
#     Buzzer
#
# installed:
#    https://github.com/pimoroni/pimoroni-pico/releases
#    

import time
from machine import Pin
from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_INKY_PACK

display = PicoGraphics(display=DISPLAY_INKY_PACK)

display.set_update_speed(1)
display.update()
display.set_update_speed(3)

button_a = Button(12)
button_b = Button(13)
button_c = Button(14)

buzz = Pin(28, Pin.OUT)
buzz.value(0)

work_cycles = 16     # shows how many work cycles are left
cycle_tally = 0      # keeps a tally of how many pomodoro cycles you've done total
focus_mode = 1       # when 1 timer is active
work_mode = 0        # when active, workcycles count down
pause_mode = 0       # pauses timer

# works the buttons
switch_hold = 0
work_hold = 0
pause_hold = 0
no_butt = 0
tigger = 0

refresh_counter = 0

f_secs = 25.00 * 60.00
b_secs = 5.00 * 60.00
mins, secs = divmod(int(f_secs), 60)

timer = '{:02d}:{:02d}'.format(25, 0)

def clear():
    display.set_pen(15)
    display.clear()

    


def refresh_dsp():
    clear()
    display.set_font("bitmap6")
    display.set_pen(0)
    display.rectangle(15,15,258,18)
    display.text("workcycles left", 16, 34, 258, 2)
    display.text("total", 16, 65, 2, 2)
    if focus_mode == 1:
        display.text("focus", 100, 58, 2, 2)
    else:
        display.text("rest", 100, 58, 2, 2)
    if work_mode == 1:
        display.text("workmode: on", 16, 96, 256, 2)
    else:
        display.text("workmode:off", 16, 96, 256, 2)
    i = cycle_tally
    while i > 0:
        if i % 5 != 0:
            display.line(16 + (i * 3),49,16 + (i * 3),64)
        else:
            display.line(16 + ((i-5) * 3), 49, 16 + ((i-1) * 3), 64)
        i=i-1
    display.set_font("bitmap14_outline")
    display.text(timer, 168, 72, 130, 3)
    display.set_pen(15)
    i = 17-(work_cycles+1)
    while i>0:
       display.rectangle(272-(16 * i),16,15,16)
       i=i-1
    if pause_mode == 1:
        display.rectangle(127,43,12,42)
        display.rectangle(157,43,12,42)
        display.set_pen(0)
        display.rectangle(128,44,10,40)
        display.rectangle(158,44,10,40)
    display.set_update_speed(2)
    display.update()
    display.set_update_speed(3)
        
#setup
refresh_dsp()


#loop
while cycle_tally <=24:
    if button_a.read():
        pause_hold += 1
        no_butt = 0
        if pause_hold <= 2:
            if pause_mode == 0:
                pause_mode = 1
            else:
                pause_mode = 0
            refresh_dsp()
        if pause_hold>=15 and tigger == 0:
            f_secs = 25 * 60
            b_secs = 5 * 60
            no_butt = 0
            tigger = 1
            if focus_mode == 1:
                mins, secs = divmod(int(f_secs), 60)
            else:
                mins, secs = divmod(int(b_secs), 60)
            refresh_dsp()
        timer = '{:02d}:{:02d}'.format(int(mins), int(secs))
        
    elif button_b.read():
        switch_hold += 1
        no_butt = 0
        if switch_hold>=13 and tigger == 0:
            f_secs = 25 * 60
            b_secs = 5 * 60
            tigger = 1
            if focus_mode == 1:
                focus_mode = 0
                mins, secs = divmod(int(b_secs), 60)
            else:
                focus_mode = 1
                mins, secs = divmod(int(f_secs), 60)
            switch_hold = 0
            timer = '{:02d}:{:02d}'.format(int(mins), int(secs))
            refresh_dsp()
    elif button_c.read():
        work_hold += 1
        no_butt = 0
        buzz.value(0)
        if work_hold >= 13 and tigger == 0:
            tigger = 1
            if work_mode == 1:
                work_mode = 0
                refresh_dsp()
            else:
                work_mode = 1
                refresh_dsp()
            work_hold = 0
    else:
        no_butt += 1
        if no_butt >= 10:
            work_hold = 0
            pause_hold = 0
            switch_hold = 0
            no_butt = 0
            tigger = 0
    if pause_mode == 1:
        pause_mode = 1
    elif focus_mode == 1 and f_secs <= 0.00:
        focus_mode = 0
        f_secs = 25 * 60
        b_secs = 5 * 60
        if work_mode == 1:
            buzz.value(1)
        cycle_tally += 1
        if work_mode == 1:
            work_cycles -= 1
        refresh_dsp()
    elif focus_mode == 1:
        f_secs -= .011
    elif focus_mode == 0 and b_secs <= 0.00:
        focus_mode = 1
        f_secs = 25 * 60
        b_secs = 5 * 60
        if work_mode == 1:
            buzz.value(1)
        refresh_dsp()
    elif focus_mode==0:
        b_secs-= .011
    if f_secs <= 24 * 60 or b_secs <= 4 * 60:
        buzz.value(0)
    if refresh_counter >= 495:
        if focus_mode == 1:
            mins, secs = divmod(int(f_secs), 60)
        else:
            mins, secs = divmod(int(b_secs), 60)
        timer = '{:02d}:{:02d}'.format(int(mins), int(secs))
        display.set_pen(15)
        display.rectangle(168, 72, 150, 60)
        display.set_pen(0)
        display.set_font("bitmap14_outline")
        display.text(timer, 168, 72, 130, 3)
        display.update()
        refresh_counter = 0
    else:
        refresh_counter += 1
        #nl = time.ticks_ms()
        #print(nl)
    time.sleep(.01)
