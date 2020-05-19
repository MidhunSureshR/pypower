import dbus

class UPowerManager():

    def __init__(self):
        self.UPOWER_NAME = "org.freedesktop.UPower"
        self.UPOWER_PATH = "/org/freedesktop/UPower"

        self.DBUS_PROPERTIES = "org.freedesktop.DBus.Properties"
        self.bus = dbus.SystemBus()

    def detect_devices(self):
        upower_proxy = self.bus.get_object(self.UPOWER_NAME, self.UPOWER_PATH) 
        upower_interface = dbus.Interface(upower_proxy, self.UPOWER_NAME)
        devices = upower_interface.EnumerateDevices()

        return devices

    def get_device_percentage(self, battery):
        battery_proxy = self.bus.get_object(self.UPOWER_NAME, battery)
        battery_proxy_interface = dbus.Interface(battery_proxy, self.DBUS_PROPERTIES)

        return battery_proxy_interface.Get(self.UPOWER_NAME + ".Device", "Percentage")
   
    def get_full_device_information(self, battery):
        battery_proxy = self.bus.get_object(self.UPOWER_NAME, battery)
        battery_proxy_interface = dbus.Interface(battery_proxy, self.DBUS_PROPERTIES)

        hasHistory = battery_proxy_interface.Get(self.UPOWER_NAME + ".Device", "HasHistory")
        hasStatistics = battery_proxy_interface.Get(self.UPOWER_NAME + ".Device", "HasStatistics")
        isPresent = battery_proxy_interface.Get(self.UPOWER_NAME + ".Device", "IsPresent")
        isRechargable = battery_proxy_interface.Get(self.UPOWER_NAME + ".Device", "IsRechargeable")
        online = battery_proxy_interface.Get(self.UPOWER_NAME + ".Device", "Online")
        powersupply = battery_proxy_interface.Get(self.UPOWER_NAME + ".Device", "PowerSupply")
        capacity = battery_proxy_interface.Get(self.UPOWER_NAME + ".Device", "Capacity")
        energy = battery_proxy_interface.Get(self.UPOWER_NAME + ".Device", "Energy")
        energyempty = battery_proxy_interface.Get(self.UPOWER_NAME + ".Device", "EnergyEmpty")
        energyfull = battery_proxy_interface.Get(self.UPOWER_NAME + ".Device", "EnergyFull")
        energyfulldesign = battery_proxy_interface.Get(self.UPOWER_NAME + ".Device", "EnergyFullDesign")
        energyrate = battery_proxy_interface.Get(self.UPOWER_NAME + ".Device", "EnergyRate")
        luminosity = battery_proxy_interface.Get(self.UPOWER_NAME + ".Device", "Luminosity")
        percentage = battery_proxy_interface.Get(self.UPOWER_NAME + ".Device", "Percentage")
        temperature = battery_proxy_interface.Get(self.UPOWER_NAME + ".Device", "Temperature")
        voltage = battery_proxy_interface.Get(self.UPOWER_NAME + ".Device", "Voltage")
        timetoempty = battery_proxy_interface.Get(self.UPOWER_NAME + ".Device", "TimeToEmpty")
        timetofull = battery_proxy_interface.Get(self.UPOWER_NAME + ".Device", "TimeToFull")
        iconname = battery_proxy_interface.Get(self.UPOWER_NAME + ".Device", "IconName")
        model = battery_proxy_interface.Get(self.UPOWER_NAME + ".Device", "Model")
        nativepath = battery_proxy_interface.Get(self.UPOWER_NAME + ".Device", "NativePath")
        serial = battery_proxy_interface.Get(self.UPOWER_NAME + ".Device", "Serial")
        vendor = battery_proxy_interface.Get(self.UPOWER_NAME + ".Device", "Vendor")
        state = battery_proxy_interface.Get(self.UPOWER_NAME + ".Device", "State")
        technology = battery_proxy_interface.Get(self.UPOWER_NAME + ".Device", "Technology")
        battype = battery_proxy_interface.Get(self.UPOWER_NAME + ".Device", "Type")
        warninglevel = battery_proxy_interface.Get(self.UPOWER_NAME + ".Device", "WarningLevel")
        updatetime = battery_proxy_interface.Get(self.UPOWER_NAME + ".Device", "UpdateTime")


        information_table = {
                'HasHistory': hasHistory,
                'HasStatistics': hasStatistics,
                'IsPresent': isPresent,
                'IsRechargeable': isRechargable,
                'Online': online,
                'PowerSupply': powersupply,
                'Capacity': capacity,
                'Energy': energy,
                'EnergyEmpty': energyempty,
                'EnergyFull': energyfull,
                'EnergyFullDesign': energyfulldesign,
                'EnergyRate': energyrate,
                'Luminosity': luminosity,
                'Percentage': percentage,
                'Temperature': temperature,
                'Voltage': voltage,
                'TimeToEmpty': timetoempty,
                'TimeToFull': timetofull,
                'IconName': iconname,
                'Model': model,
                'NativePath': nativepath,
                'Serial': serial,
                'Vendor': vendor,
                'State': state,
                'Technology': technology,
                'Type': battype,
                'WarningLevel': warninglevel,
                'UpdateTime': updatetime
                }

        return information_table

    def get_percent_icon(self, percent):
        print(type(percent))
        if (percent <= 23):
            return ""
        elif (percent <= 50):
            return ""
        elif (percent <= 90):
            return ""
        elif (percent <= 100):
            return ""

    def get_state(self, battery):
        battery_proxy = self.bus.get_object(self.UPOWER_NAME, battery)
        battery_proxy_interface = dbus.Interface(battery_proxy, self.DBUS_PROPERTIES)       
        state = int(battery_proxy_interface.Get(self.UPOWER_NAME + ".Device", "State"))

        if (state == 0):
            return ""  # unknown
        elif (state == 1):
            return "{  } "  # Charging
        elif (state == 2):
            p = self.get_device_percentage(battery)
            return self.get_percent_icon(p)  # discharging
        elif (state == 3):
            return ""  # empty
        elif (state == 4):
            return "{  } | "  # fully charged
        elif (state == 5):
            return "Pending charge"
        elif (state == 6):
            return "Pending discharge"


BATTERY_MODEL_NAME = "SDI ICR18650"
obj = UPowerManager()


def get_info_of_all_devices():
    """
    Use this function to get detailed view of all devices.
    :return:
    A list of dictionary with each dictionary describing a unique device.
    """
    device_list = obj.detect_devices()
    num_devices = len(device_list)
    device_info_table = list()
    for i in range(num_devices):
        info_table = obj.get_full_device_information(device_list[i])
        device_info_table.append(info_table)
    return device_info_table, device_list


def get_laptop_battery():
    dev_table, dev_list = get_info_of_all_devices()
    for i in range(len(dev_table)):
        device_dict = dev_table[i]
        if device_dict['Model'] == BATTERY_MODEL_NAME:
            return dev_list[i]
    return -1


def get_data():
    asus_lap_battery = get_laptop_battery()
    if asus_lap_battery == -1:
        print("Error: Could not obtain device.")
        return
    else:
        state = obj.get_state(asus_lap_battery)
        percentage_charge = obj.get_device_percentage(asus_lap_battery)
    return state, percentage_charge


class Py3status:

    def send_data_to_py3status(self):
        s, p = get_data()
        s_data = s + '  ' + str(p) + '%'
        return {
            'full_text': s_data,
            'cached_until': self.py3.time_in(2)
        }


if __name__ == "__main__":
    print("Please don't run this script.")
