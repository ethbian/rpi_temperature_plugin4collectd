"""
This is a collectd plugin reporting Raspbeery Pi temperature (in Celsius or Fahrenheit).
Tested on RPi3 and RPi4 with Raspbian.
For more details see https://github.com/ethbian/rpi_temperature_plugin4collectd
version 0.1
"""
try:
    import collectd
except ImportError:
    raise ImportError('\n\n cannot find Python module: ' +
                      'collectd\n try executing: pip install collectd')

SENSOR = '/sys/class/thermal/thermal_zone0/temp'
CELSIUS = True

def conf(config):
    """
    This method has been registered as the config callback and is used to parse options from
    given config.
    """
    for kv in config.children:
        key = kv.key.lower()
        val = kv.values[0]

        if key == 'celsius':
            global CELSIUS
            CELSIUS = bool(val)
        elif key == 'sensor':
            global SENSOR
            SENSOR = val
        else:
            collectd.info('rpi_temperature: Ignoring unknown config key: {}'.format(key))

    if CELSIUS:
        collectd.info('rpi_temperature: reporting temperature in Celsius')
    else:
        collectd.info('rpi_temperature: reporting temperature in Fahrenheit')

def read_temperature():
    """
    This method has been registered as the read callback and will be called every polling interval
    to dispatch metrics.
    """
    try:
        with open(SENSOR, 'rb') as sensor_file:
            temperature = sensor_file.read()
    except Exception as exception:
        collectd.warning('Error reading temperature: check config Sensor option: {}'.format(exception))
        temperature = 0
    else:
        if CELSIUS:
            temperature = int(int(temperature)/1000)
        else:
            temperature = int(int(temperature)/1000*1.8+32)

    collectd.Values(plugin='rpi_temperature',
                    type='gauge',
                    values=[temperature]).dispatch()

if __name__ != '__main__':
    collectd.register_config(conf)
    collectd.register_read(read_temperature)
else:
    raise SystemExit('Nope - it is a plugin reporting to collected.')
