# pypower
A small but effective py3status module for displaying power details on py3status bar.

![screenshot](https://i.imgur.com/oJzzN4a.png)
## Motivation
The default battery module for py3status ( [battery_level](https://py3status.readthedocs.io/en/latest/modules.html#battery-level) ) does not work on some devices.
This is an alternative module that can be used in such cases. 

**Note: This was made as a quick fix and contains pretty bad code. There is a lot of room for improvement.**


## Prerequisites
- Font Awesome
- [Python Dbus Module](https://pypi.org/project/dbus-python/)

## How to use
Add the following line to your pystatus config file:
```
order += "pypower"
```
Make sure you pass location of this module in your i3config.
It should look like this:
```
bar {
      ...
      
      status_command py3status -i /path/to/this/pypower-module/
      
      ...
}

```

## Acknowledgement
[wogscpar](https://github.com/wogscpar/upower-python) for his UPower wrapper.
