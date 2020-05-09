import upower

BATTERY_MODEL_NAME = "SDI ICR18650"
DEBUG_OUTPUT = True
IS_DEVICE_ALREADY_FOUND = False

obj = upower.UPowerManager()


def debug_out(*args):
    if not DEBUG_OUTPUT:
        return
    for i in range(len(args)):

        print(args[i], " ", end='', sep='')
    print('\n')


def print_all_info(info_table):
    for i, j in info_table.items():
        print(i, ":", j,)


def print_device_info(device):
    info = obj.get_full_device_information(device)
    print_all_info(info)


def print_all_icon_names(info_table):
    print(info_table['IconName'])


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
    if asus_lap_battery is -1:
        print("Error: Could not obtain device.")
        return
    else:
        # print_device_info(asus_lap_battery)
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
