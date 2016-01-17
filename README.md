# piContoller
Remote relay controller using a raspberry pi. 

There is two diferent modules in this project:

a) GPIO Manager: Python module to controll leds, buttons and GPIO in order to control the relay, sensors and stuff. 

b) Web side: This module consists on a pretty simple LAMP solution involving a PHP module to the IPC comunication with the GPIO Manager, and an AngularJS based website.

# GPIO Manager

This module has a basic logger, and two different threats:

a) Server Manager Thread: inits the IPC with PHP. This threat waits for server queries: "ON" (Turn on the relay),
"OFF" (Turn off the relay), "STATUS" (Returns the GPIO status).

b) GPIO Manager Thread: This threat waits for direct GPIO actions such as button pressing to turn off or on the relay.

Can be found at: python/daemon_2.py

# Website

This module has been developed using AngularJS, and PHP:

a) AngularJS: simple web GUI where is displayed the relay status and allows to turn it off/on.

b) PHP: ajax request handler to communicate with the GPIO daemon.

Can be found at: branch root.





