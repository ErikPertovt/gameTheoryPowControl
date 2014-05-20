## Introduction
This package provides Python *.py files for conductiong a simple power allocation game between two players (four nodes) located in a VESNA-based wireless sensor network that uses ALH protocol in order to communicate. (link to LOG-a-TEC portal can be found [here](http://www.log-a-tec.eu/) - you need a username and password in order to have access to the testbed).

Before using this package, please install VESNA ALH Tools and Python bindings for VESNA spectrum sensor application. In order to do this, please follow the steps described here:

* 1) **Installation of VESNA ALH Tools**
(see its own README file for installation instructions - _Tomaz Solc_ )
* https://github.com/avian2/vesna-alh-tools
* 2) **Installation of Python bindings for VESNA spectrum application** 
(see its own README file for installation instructions - _Tomaz Solc_ )
* https://github.com/sensorlab/vesna-spectrum-sensor

**This package contains the following Python classes:**
* **Node** - used for setting the nodes as transmitters or receivers
* **gainCalculations** - used for performing channel gain measurements.
* **Noise** - used for measuring the noise power.
* **MyQueue** - use as a queue of channel gains and best responses.

------------------------------------------------------------------

* **gameSINRControlExample** - used as an example on how to run the game.