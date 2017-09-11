chimera-autopierchange plugin
=============================

Automatically flip pier side for German Equatorial mounts in the chimera observatory control system
https://github.com/astroufsc/chimera.

Usage
-----

Install and configure `chimera-autopierchange` plugin as example below.

Installation
------------

::

   pip install -U https://github.com/astroufsc/chimera-autopierchange/archive/master.zip


Configuration Example
---------------------

::

   - type: AutoPierChange
     name: pier_change
     telescope: /FakeTelescope/fake
     dome: None  # If dome is set, controller calls syncWithTel() dome method after pierside flip
     ha_flip: 0  # Flip hour angle
     check_interval: 2 # Check telescope position every check_interval seconds
     chimera_config: SYSTEM_CONFIG_DEFAULT_FILENAME # Path to chimera.config file

Contact
-------

For more information, contact us on chimera's discussion list:
https://groups.google.com/forum/#!forum/chimera-discuss

Bug reports and patches are welcome and can be sent over our GitHub page:
https://github.com/astroufsc/chimera-autopierchange/
