# 2013-01-22 Rennaissance IO Conference

### 2013-01-22 Renaissance IO Bluegiga Presentation.key

Presentation slides in Keynote format.

### 2013-01-22 Renaissance IO Bluegiga Presentation.pptx

Presentation slides in Microsoft Powerpoint 2010 format.

### BLE_Stack_API_Reference_v2.2.pdf

Full BGAPI reference manual. Heavy on technical details, light on example code.

### BLE112_Datasheet.pdf

Official datasheet for the BLE112 module.

### DKBLE112_Schematic.pdf

Complete schematic for the DKBLE112 development kit board, including details
about the SPI display and accelerometer on board. Excellent reference for your
own projects.

### BLEMailbox_Xcode.zip

Xcode project to go along with the light-sensitive mail delivery sensor demo
given during the demo party. This is a very simple single-view iOS application
built for the iPhone 5 which searches for a Bluetooth Smart sensor that
includes the custom service UUID found in the "mailbox_sensor_bgscript" demo
project created for the BLE112 Bluegiga module. This compiles without error
on the latest version of Xcode and the latest release version of iOS (6.0.2)
as of January 14, 2013.

### glucose_demo_bgscript.zip

Glucose sensor demo project, as shown towards the end of my presentation. This
implements a fairly complete glucose sensor profile using only the features of
our BLE112, and a few of the peripherals included on our DKBLE112 development
kit board. All of the heavy lifting is done by the module itself; peripherals
are only used because they can be. The GATT database structure and non-volatile
flash PS key memory storage is self-contained, and the project requries no
external microcontrollers as written. However, the actual glucose concentration
value is emulated by a potentiometer on the DKBLE112, as there is obviously no
real glucose sensor on the dev kit to use.

### gpio_demo_bgscript.zip

An extra sample project demostrating some GPIO usage with interrupts. This is
not part of the presentation or demo party, but still a useful reference.

### mailbox_sensor_bgscript.zip

Mailbox sensor BGScript project, as shown during the demo party. This project
requires only the BLE112 and a light sensor connected to P0_0 (power) and P0_1
(analog output). I use an Ambilight logarithmic sensor, but a CdS cell or a few
other options would work as will with the right calibration. This is the project
which goes on the hardware that is meant to communicate with the BLEMailbox
Xcode project.