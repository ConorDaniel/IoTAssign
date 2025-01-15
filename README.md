# IoT Assignment December 2024

**Recap**

The original idea was to enhance patient safety by preventing falls.  This would be done by measuring the relative strength of RSSI value received from a bluettooth sensor by two R-Pi's. 
This was to be a means of identifying when a patient is actually leaving their bed area, rather than just shifting position in their bed/chair, so providing care staff
with a reliable alert as to when a patient is on the move. 

It was further proposed to have the two Pi's send signals to each other, as a back-up safety measure, so that an alert could be issued if either one were unplugged.

Two bluetooth sensors were purchased, each having built in electronics that measure acceleration and angular change in the X,Y and Z planes. 

**Challenges**

The sensors only provide an RSSI reading on connection - and not as part of the routine data packages which give angular/acceleration movement
The movement readings are quite complicated - they give relative movement to the last position, rather than distance moved from a fixed point
This means they can be used to measure movement upwards or sideways, but not movement in terms of distance travelled from an area
The sensors can only couple with one programme on one receiver at a time - meaning it is not possible measure the RSSI strenght on two receivers from the one device
Work arounds were required

**What was achieved**

1) R-Pi 'Heart-Beat Signal' and failure alert based on MQTT and Email. 

   Two programmes were written using MQTT and a public broker
   The first programme sends out a 'heartbeat' (I'm here!) MQTT signal to the broker every 10 seconds.
   The second programme subscribes to that, and attempts to send an email if it stops receiving the message.
   Each programme could be run on both Pi's so that if one is unplugged, it alerts the other - but I'm just running it on one, as a 'proof of concept
   (I couldn't crack the email 2FA/App password requirements in the time available - but you can see that it tries to send an email if it stops getting the heartbeat)

    See programmes:

2) RSSI Signal Strength & Blynk Diplay

   Again, two programmes were involved
   I got the MAC address for each sensor from the Android app provided by the vendor (WIT Motion) 
   Through a bit (a lot) of trial and error, I found that by using the bluetooth controls built into the R-PI, I could scan for the target MAC and connect (not couple), and then get an RSSI reading
   By disconnecting and reconnecting every few seconds, I could then get a series of RSSI values over time
   With the help of ChatGBT v4.0, I automated this process, writing the RSSI values to a text log file

   The second programme takes the last RSSI value from the log and transmits this to Blynk
   I did try to combine the two programmes, but when I did, the disconnect/reconnect and subsequent transmission to Blynk became really slow. Use of the log eliminates that
   Blynk then gives a visual representation of the RSSI value, to which i have added an alert if the value becomes too low ( its minus 30 when beside the Pi and decreases to -90 when moved away)

4) Angular Movement and Blynk

   The vendor provided python code which, when connected to a target MAC, provides a data package of the sensor angular movements every few milliseconds
   I was able to connect to a sensor and filter out the data on movement in the X (forward) and Z (vertical) planes
   By simple observation of the values on the vendor app, I made a stab at guesssing levels at which the patient is 'at rest' or moving in the X and Z planes
   A display on Blynk shows the text 'at rest' when the default value of 0 is sent
   If the X value AND the Z Value is exceeded, a value of 1 is sent to Blynk
   This changes the mssage to 'movement detected'
   The change is momentary - I need to refine that.

   Programmes: test.py and device_model.py (running test calls device_model)

**Next Steps**

Ideally I would combine the RSSI values and the angular movement values together- but that defeated me in the time available.
Ideally I would also get a bluetooth sensor which could connect to two receivers (or which has a dual mac addresss)
Ideally I would calibrate the RSSI values and the angular ones more precisely in terms of what is the impact of standing up and moving forward - again, time did not allow. 
I would like to build in battery strength as well - its shown on the proprietary app, but not as part of the data package. 


   



