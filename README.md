# rpi_temperature_plugin4collectd
A collectd plugin reporting Raspberry Pi temperature.  
Tested on RPi 3 and RPi 4 with Raspbian.

## quick start
- install collectd  
*raspbian: apt-get install collectd*
- clone the repository  
*git clone https://github.com/ethbian/rpi_temperature_plugin4collectd.git*
- create directory for the plugin  
*mkdir /usr/local/lib/collectd*
- copy the rpi_temperature.py file to the plugin directory  
*cp rpi_temperature.py /usr/local/lib/collectd/*
- update the collectd config file (raspbian: **/etc/collectd/collectd.conf**) by adding to the end of the file:

```
LoadPlugin python
<Plugin python>
    ModulePath "/usr/local/lib/collectd"
    Import "rpi_temperature"
    <Module rpi_temperature>
#        Sensor "/sys/class/thermal/thermal_zone0/temp"
#        Celsius true
    </Module>
</Plugin>
```

- restart collectd  
*raspbian: service collectd restart*
- check logfile for possible errors  
*raspbian: service collectd status*  
*raspbian: tail /var/log/syslog*

- uncomment and change the **Celsius** option to **false** to report temperature in Fahrenheit
- pull requests are more than welcome if you're fixing something
