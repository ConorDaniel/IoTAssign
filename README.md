# IoT Assignment December 2024

**Recap**

The original idea was to enhance patient safety, by preventing falls through reliable detection of movement.  
This was to be done by measuring the relative strength of RSSI values received from a bluetooth sensor, by two R-Pi's. 
The idea was to create an alert when a patient moved away from their bed area, rather than just shifting position in their bed/chair, 
thereby providing care staff with a reliable alert as to when a patient is on the move. The RSSI signal in one Pi would decrease and the signal at a 2nd Pi would increase.

It was further proposed to have the two Pi's send MQTT signals to each other, as a back-up safety measure, so that an alert could be issued if either one were unplugged.

Two bluetooth sensors were purchased, each having built in electronics that measure acceleration and angular change in the X,Y and Z planes. 

**Challenges**

The sensors only provide an RSSI reading on connection - and not as part of the routine data packages which give angular/acceleration movement.
The accelerometer movements readings are quite complicated - they give relative movement to the last position, rather than distance moved from a fixed point.
This means they can be used to measure movement upwards or sideways, but not movement in terms of distance travelled from a bed or chair.
The sensors can only couple with one programme on one receiver at a time - meaning it is not possible measure the RSSI strength on two receivers from the one device at the same time.
Work arounds were required.

**What was achieved**

1) R-Pi 'Heart-Beat Signal' and failure alert based on MQTT and Email. 

   Two programmes were written using MQTT and the emqx public broker 
   The first programme sends out a 'heartbeat' (I'm here!) MQTT signal to the broker every 10 seconds.
   The second programme subscribes to that. The subscription programm also attempts to send an email if it stops receiving the message.
   Each programme could be run on 2 Pi's so that if one is unplugged, it alerts the other.  I'm demonstrating it on one, as a 'proof of concept'.
   I couldn't crack the email 2FA/App password requirements in the time available - but you can see that the subscription programme tries to send an email, if stops getting the heartbeat message

    See programmes: PiHere.py and SubAlertPi.py

3) RSSI Signal Strength, Blynk Display and Blynk App Alert

   Again, two python programmes were involved:
   
   I got the MAC address for each sensor from the Android app provided by the vendor (WIT Motion) 
   Through a bit (a lot) of trial and error, I found that by using the bluetooth controls built into the R-PI, I could scan for the target MAC and connect (not couple), and then get an RSSI reading
   By disconnecting and reconnecting every few seconds, I could then get a series of RSSI values over time, thereby tracking the signal strength as the sensor moves. 
   With the help of ChatGBT v4.0, I automated this process, writing the RSSI values to a text log file

   The second programme takes the last RSSI value from the log and transmits this to Blynk.  Blynk displays a gauge with the signal strenght. 

   Note that I did try to combine the two programmes, but when I did, the disconnect/reconnect and subsequent transmission to Blynk became really slow. Use of a separate blynk message programme from the log eliminated that lag.
   Blynk then gives a visual representation of the RSSI value.

   I then added a Blynk automation to give an 'in app' push notification when the value of RSSI went below -60


   See:  rssi.py, rssi_log.txt and upload_rssi_log.py

5) Angular Movement and Blynk

   The vendor provided python code which, when connected to a target MAC, provides a data package of the sensor angular movements every few milliseconds.
   I was able to connect to a sensor and filter out the data on movement in the X (forward) and Z (vertical) planes.
   By simple observation of the values on the vendor app, I made a stab at guesssing levels at which the patient is 'at rest' or moving in the X and Z planes.
   A display on Blynk shows the text 'at rest' when the default value of 0 is sent.
   If the X value AND the Z Value is exceeded, a value of 1 is sent to Blynk.
   This changes a texgt mssage display from 'at rest' to 'movement detected'.
   The change is momentary - I need to refine that.

   I also added in a separate 'Heart Beat' signal from the PI as part of this programme.  This sends an integer value to Blynk when the pi programme is connected.
   I added a visual signal to this, so that an led changes from blue to yellow every 10 seconds, to confirm the pi is connected.
   I then added a Blynk automation to this, again to give a push alert to the app if the signal stops. 


   Programmes: test.py and device_model.py (running 'test' calls 'device_model' NB both python programmes provided by sensor vendor, test.py modified by me to target key data) and to include a heartbeat signal. 

**Next Steps**
Ideally
I would combine the RSSI values and the angular movement values together for a really reliable detection of movemeent - but that defeated me in the time available.
I would also get a 'multipoint' bluetooth sensor which could connect to two receivers (or which has a dual mac addresss).
I would calibrate the RSSI values and the angular ones more precisely in terms of what is the impact of standing up and moving forward - again, time did not allow. 
I would like to build in battery strength as well - the battery strength shown on the proprietary app, but not as part of the data package. 

References:

Course materials, vendor software and ChatGPT (as a python reference and syntax guide) were used for this assignment 

   



