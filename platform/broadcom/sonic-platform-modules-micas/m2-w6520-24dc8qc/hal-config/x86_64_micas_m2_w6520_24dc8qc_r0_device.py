#!/usr/bin/python3

psu_fan_airflow = {
    "intake": ['DPS-1300AB-6 S', 'GW-CRPS1300D'],
    "exhaust": []
}

fanairflow = {
    "intake": ['M1HFAN II-F'],
    "exhaust": [],
}

psu_display_name = {
    "PA1300I-F": ['GW-CRPS1300D', 'DPS-1300AB-6 S'],
}

psutypedecode = {
    0x00: 'N/A',
    0x01: 'AC',
    0x02: 'DC',
}

class Unit:
    Temperature = "C"
    Voltage = "V"
    Current = "A"
    Power = "W"
    Speed = "RPM"

class threshold:
    PSU_TEMP_MIN = -10 * 1000
    PSU_TEMP_MAX = 60 * 1000

    PSU_FAN_SPEED_MIN = 2000
    PSU_FAN_SPEED_MAX = 28000

    PSU_OUTPUT_VOLTAGE_MIN = 11 * 1000
    PSU_OUTPUT_VOLTAGE_MAX = 14 * 1000

    PSU_AC_INPUT_VOLTAGE_MIN = 200 * 1000
    PSU_AC_INPUT_VOLTAGE_MAX = 240 * 1000

    PSU_DC_INPUT_VOLTAGE_MIN = 190 * 1000
    PSU_DC_INPUT_VOLTAGE_MAX = 290 * 1000

    ERR_VALUE = -9999999

    PSU_OUTPUT_POWER_MIN = 10 * 1000 * 1000
    PSU_OUTPUT_POWER_MAX = 1300 * 1000 * 1000

    PSU_INPUT_POWER_MIN = 10 * 1000 * 1000
    PSU_INPUT_POWER_MAX = 1444 * 1000 * 1000

    PSU_OUTPUT_CURRENT_MIN = 2 * 1000
    PSU_OUTPUT_CURRENT_MAX = 107 * 1000

    PSU_INPUT_CURRENT_MIN = 0.2 * 1000
    PSU_INPUT_CURRENT_MAX = 7 * 1000

    FRONT_FAN_SPEED_MAX = 25000
    REAR_FAN_SPEED_MAX = 22000
    FAN_SPEED_MIN = 2000

devices = {
    "onie_e2": [
        {
            "name": "ONIE_E2",
            "e2loc": {"loc": "/sys/bus/i2c/devices/1-0056/eeprom", "way": "sysfs"},
            "airflow": "intake"
        },
    ],
    "psus": [
        {
            "e2loc": {"loc": "/sys/bus/i2c/devices/41-0050/eeprom", "way": "sysfs"},
            "pmbusloc": {"bus": 41, "addr": 0x58, "way": "i2c"},
            "present": {"loc": "/sys/wb_plat/psu/psu1/present", "way": "sysfs", "mask": 0x01, "okval": 1},
            "name": "PSU1",
            "psu_display_name": psu_display_name,
            "airflow": psu_fan_airflow,
            "TempStatus": {"bus": 41, "addr": 0x58, "offset": 0x79, "way": "i2cword", "mask": 0x0004},
            "Temperature": {
                "value": {"loc": "/sys/bus/i2c/devices/i2c-41/41-0058/hwmon/hwmon*/temp1_input", "way": "sysfs"},
                "Min": threshold.PSU_TEMP_MIN,
                "Max": threshold.PSU_TEMP_MAX,
                "Unit": Unit.Temperature,
                "format": "float(float(%s)/1000)"
            },
            "FanStatus": {"bus": 41, "addr": 0x58, "offset": 0x79, "way": "i2cword", "mask": 0x0400},
            "FanSpeed": {
                "value": {"loc": "/sys/bus/i2c/devices/i2c-41/41-0058/hwmon/hwmon*/fan1_input", "way": "sysfs"},
                "Min": threshold.PSU_FAN_SPEED_MIN,
                "Max": threshold.PSU_FAN_SPEED_MAX,
                "Unit": Unit.Speed
            },
            "psu_fan_tolerance": 40,
            "InputsStatus": {"bus":41, "addr": 0x58, "offset": 0x79, "way": "i2cword", "mask": 0x2000},
            "InputsType": {"bus": 41, "addr": 0x58, "offset": 0x80, "way": "i2c", 'psutypedecode': psutypedecode},
            "InputsVoltage": {
                'AC': {
                    "value": {"loc": "/sys/bus/i2c/devices/i2c-41/41-0058/hwmon/hwmon*/in1_input", "way": "sysfs"},
                    "Min": threshold.PSU_AC_INPUT_VOLTAGE_MIN,
                    "Max": threshold.PSU_AC_INPUT_VOLTAGE_MAX,
                    "Unit": Unit.Voltage,
                    "format": "float(float(%s)/1000)"

                },
                'DC': {
                    "value": {"loc": "/sys/bus/i2c/devices/i2c-41/41-0058/hwmon/hwmon*/in1_input", "way": "sysfs"},
                    "Min": threshold.PSU_DC_INPUT_VOLTAGE_MIN,
                    "Max": threshold.PSU_DC_INPUT_VOLTAGE_MAX,
                    "Unit": Unit.Voltage,
                    "format": "float(float(%s)/1000)"
                },
                'other': {
                    "value": {"loc": "/sys/bus/i2c/devices/i2c-41/41-0058/hwmon/hwmon*/in1_input", "way": "sysfs"},
                    "Min": threshold.ERR_VALUE,
                    "Max": threshold.ERR_VALUE,
                    "Unit": Unit.Voltage,
                    "format": "float(float(%s)/1000)"
                }
            },
            "InputsCurrent": {
                "value": {"loc": "/sys/bus/i2c/devices/i2c-41/41-0058/hwmon/hwmon*/curr1_input", "way": "sysfs"},
                "Min": threshold.PSU_INPUT_CURRENT_MIN,
                "Max": threshold.PSU_INPUT_CURRENT_MAX,
                "Unit": Unit.Current,
                "format": "float(float(%s)/1000)"
            },
            "InputsPower": {
                "value": {"loc": "/sys/bus/i2c/devices/i2c-41/41-0058/hwmon/hwmon*/power1_input", "way": "sysfs"},
                "Min": threshold.PSU_INPUT_POWER_MIN,
                "Max": threshold.PSU_INPUT_POWER_MAX,
                "Unit": Unit.Power,
                "format": "float(float(%s)/1000000)"
            },
            "OutputsStatus": {"bus": 41, "addr": 0x58, "offset": 0x79, "way": "i2cword", "mask": 0x8800},
            "OutputsVoltage": {
                "value": {"loc": "/sys/bus/i2c/devices/i2c-41/41-0058/hwmon/hwmon*/in2_input", "way": "sysfs"},
                "Min": threshold.PSU_OUTPUT_VOLTAGE_MIN,
                "Max": threshold.PSU_OUTPUT_VOLTAGE_MAX,
                "Unit": Unit.Voltage,
                "format": "float(float(%s)/1000)"
            },
            "OutputsCurrent": {
                "value": {"loc": "/sys/bus/i2c/devices/i2c-41/41-0058/hwmon/hwmon*/curr2_input", "way": "sysfs"},
                "Min": threshold.PSU_OUTPUT_CURRENT_MIN,
                "Max": threshold.PSU_OUTPUT_CURRENT_MAX,
                "Unit": Unit.Current,
                "format": "float(float(%s)/1000)"
            },
            "OutputsPower": {
                "value": {"loc": "/sys/bus/i2c/devices/i2c-41/41-0058/hwmon/hwmon*/power2_input", "way": "sysfs"},
                "Min": threshold.PSU_OUTPUT_POWER_MIN,
                "Max": threshold.PSU_OUTPUT_POWER_MAX,
                "Unit": Unit.Power,
                "format": "float(float(%s)/1000000)"
            },
        },
        {
            "e2loc": {"loc": "/sys/bus/i2c/devices/42-0050/eeprom", "way": "sysfs"},
            "pmbusloc": {"bus": 42, "addr": 0x58, "way": "i2c"},
            "present": {"loc": "/sys/wb_plat/psu/psu2/present", "way": "sysfs", "mask": 0x01, "okval": 1},
            "name": "PSU2",
            "psu_display_name": psu_display_name,
            "airflow": psu_fan_airflow,
            "TempStatus": {"bus": 42, "addr": 0x58, "offset": 0x79, "way": "i2cword", "mask": 0x0004},
            "Temperature": {
                "value": {"loc": "/sys/bus/i2c/devices/i2c-42/42-0058/hwmon/hwmon*/temp1_input", "way": "sysfs"},
                "Min": threshold.PSU_TEMP_MIN,
                "Max": threshold.PSU_TEMP_MAX,
                "Unit": Unit.Temperature,
                "format": "float(float(%s)/1000)"
            },
            "FanStatus": {"bus": 42, "addr": 0x58, "offset": 0x79, "way": "i2cword", "mask": 0x0400},
            "FanSpeed": {
                "value": {"loc": "/sys/bus/i2c/devices/i2c-42/42-0058/hwmon/hwmon*/fan1_input", "way": "sysfs"},
                "Min": threshold.PSU_FAN_SPEED_MIN,
                "Max": threshold.PSU_FAN_SPEED_MAX,
                "Unit": Unit.Speed
            },
            "psu_fan_tolerance": 40,
            "InputsStatus": {"bus": 42, "addr": 0x58, "offset": 0x79, "way": "i2cword", "mask": 0x2000},
            "InputsType": {"bus": 42, "addr": 0x58, "offset": 0x80, "way": "i2c", 'psutypedecode': psutypedecode},
            "InputsVoltage": {
                'AC': {
                    "value": {"loc": "/sys/bus/i2c/devices/i2c-42/42-0058/hwmon/hwmon*/in1_input", "way": "sysfs"},
                    "Min": threshold.PSU_AC_INPUT_VOLTAGE_MIN,
                    "Max": threshold.PSU_AC_INPUT_VOLTAGE_MAX,
                    "Unit": Unit.Voltage,
                    "format": "float(float(%s)/1000)"

                },
                'DC': {
                    "value": {"loc": "/sys/bus/i2c/devices/i2c-42/42-0058/hwmon/hwmon*/in1_input", "way": "sysfs"},
                    "Min": threshold.PSU_DC_INPUT_VOLTAGE_MIN,
                    "Max": threshold.PSU_DC_INPUT_VOLTAGE_MAX,
                    "Unit": Unit.Voltage,
                    "format": "float(float(%s)/1000)"
                },
                'other': {
                    "value": {"loc": "/sys/bus/i2c/devices/i2c-42/42-0058/hwmon/hwmon*/in1_input", "way": "sysfs"},
                    "Min": threshold.ERR_VALUE,
                    "Max": threshold.ERR_VALUE,
                    "Unit": Unit.Voltage,
                    "format": "float(float(%s)/1000)"
                }
            },
            "InputsCurrent": {
                "value": {"loc": "/sys/bus/i2c/devices/i2c-42/42-0058/hwmon/hwmon*/curr1_input", "way": "sysfs"},
                "Min": threshold.PSU_INPUT_CURRENT_MIN,
                "Max": threshold.PSU_INPUT_CURRENT_MAX,
                "Unit": Unit.Current,
                "format": "float(float(%s)/1000)"
            },
            "InputsPower": {
                "value": {"loc": "/sys/bus/i2c/devices/i2c-42/42-0058/hwmon/hwmon*/power1_input", "way": "sysfs"},
                "Min": threshold.PSU_INPUT_POWER_MIN,
                "Max": threshold.PSU_INPUT_POWER_MAX,
                "Unit": Unit.Power,
                "format": "float(float(%s)/1000000)"
            },
            "OutputsStatus": {"bus": 42, "addr": 0x58, "offset": 0x79, "way": "i2cword", "mask": 0x8800},
            "OutputsVoltage": {
                "value": {"loc": "/sys/bus/i2c/devices/i2c-42/42-0058/hwmon/hwmon*/in2_input", "way": "sysfs"},
                "Min": threshold.PSU_OUTPUT_VOLTAGE_MIN,
                "Max": threshold.PSU_OUTPUT_VOLTAGE_MAX,
                "Unit": Unit.Voltage,
                "format": "float(float(%s)/1000)"
            },
            "OutputsCurrent": {
                "value": {"loc": "/sys/bus/i2c/devices/i2c-42/42-0058/hwmon/hwmon*/curr2_input", "way": "sysfs"},
                "Min": threshold.PSU_OUTPUT_CURRENT_MIN,
                "Max": threshold.PSU_OUTPUT_CURRENT_MAX,
                "Unit": Unit.Current,
                "format": "float(float(%s)/1000)"
            },
            "OutputsPower": {
                "value": {"loc": "/sys/bus/i2c/devices/i2c-42/42-0058/hwmon/hwmon*/power2_input", "way": "sysfs"},
                "Min": threshold.PSU_OUTPUT_POWER_MIN,
                "Max": threshold.PSU_OUTPUT_POWER_MAX,
                "Unit": Unit.Power,
                "format": "float(float(%s)/1000000)"
            },
        }
    ],
    "temps": [
        {
            "name": "BOARD_TEMP",
            "temp_id": "TEMP1",
            "api_name": "Board",
            "Temperature": {
                "value": {"loc": "/sys/bus/i2c/devices/40-004e/hwmon/hwmon*/temp1_input", "way": "sysfs"},
                "Min": -10000,
                "Low": 0,
                "High": 70000,
                "Max": 80000,
                "Unit": Unit.Temperature,
                "format": "float(float(%s)/1000)"
            }
        },
        {
            "name": "CPU_TEMP",
            "temp_id": "TEMP2",
            "api_name": "CPU",
            "Temperature": {
                "value": {"loc": "/sys/bus/platform/devices/coretemp.0/hwmon/hwmon*/temp1_input", "way": "sysfs"},
                "Min": 2000,
                "Low": 10000,
                "High": 100000,
                "Max": 104000,
                "Unit": Unit.Temperature,
                "format": "float(float(%s)/1000)"
            }
        },
        {
            "name": "INLET_TEMP",
            "temp_id": "TEMP3",
            "api_name": "Inlet",
            "Temperature": {
                "value": {"loc": "/sys/bus/i2c/devices/40-004f/hwmon/hwmon*/temp1_input", "way": "sysfs"},
                "Min": -10000,
                "Low": 0,
                "High": 40000,
                "Max": 50000,
                "Unit": Unit.Temperature,
                "format": "float(float(%s)/1000)"
            }
        },
        {
            "name": "OUTLET_TEMP",
            "temp_id": "TEMP4",
            "api_name": "Outlet",
            "Temperature": {
                "value": {"loc": "/sys/bus/i2c/devices/36-0048/hwmon/hwmon*/temp1_input", "way": "sysfs"},
                "Min": -10000,
                "Low": 0,
                "High": 70000,
                "Max": 80000,
                "Unit": Unit.Temperature,
                "format": "float(float(%s)/1000)"
            }
        },
        {
            "name": "SWITCH_TEMP",
            "temp_id": "TEMP5",
            "api_name": "ASIC_TEMP",
            "Temperature": {
                "value": {"loc": "/sys/bus/i2c/devices/44-0044/hwmon/hwmon*/temp99_input", "way": "sysfs"},
                "Min": 2000,
                "Low": 10000,
                "High": 100000,
                "Max": 105000,
                "Unit": Unit.Temperature,
                "format": "float(float(%s)/1000)"
            }
        },
        {
            "name": "PSU1_TEMP",
            "temp_id": "TEMP6",
            "Temperature": {
                "value": {"loc": "/sys/bus/i2c/devices/i2c-41/41-0058/hwmon/hwmon*/temp1_input", "way": "sysfs"},
                "Min": -10000,
                "Low": 0,
                "High": 55000,
                "Max": 60000,
                "Unit": Unit.Temperature,
                "format": "float(float(%s)/1000)"
            }
        },
        {
            "name": "PSU2_TEMP",
            "temp_id": "TEMP7",
            "Temperature": {
                "value": {"loc": "/sys/bus/i2c/devices/i2c-42/42-0058/hwmon/hwmon*/temp1_input", "way": "sysfs"},
                "Min": -10000,
                "Low": 0,
                "High": 55000,
                "Max": 60000,
                "Unit": Unit.Temperature,
                "format": "float(float(%s)/1000)"
            }
        },
        {
            "name": "SFF_TEMP",
            "Temperature": {
                "value": {"loc": "/tmp/highest_sff_temp", "way": "sysfs", "flock_path": "/tmp/highest_sff_temp"},
                "Min": -15000,
                "Low": 0,
                "High": 80000,
                "Max": 100000,
                "Unit": Unit.Temperature,
                "format": "float(float(%s)/1000)"
            },
            "invalid": -10000,
            "error": -9999,
        }
    ],
    "leds": [
        {
            "name": "FRONT_SYS_LED",
            "led_type": "SYS_LED",
            "led": {"bus": 2, "addr": 0x2d,  "offset":0x40, "way":"i2c"},
            "led_attrs": {
                "off": 0x0, "green": 0x01, "red": 0x02,"default":0x01,
                "amber": 0x03, "green_flash": 0x41, "red_flash": 0x42,
                "amber_flash": 0x43, "mask": 0xff
            },
        },
        {
            "name": "FRONT_PSU_LED",
            "led_type": "PSU_LED",
            "led": {"bus": 2, "addr": 0x2d,  "offset":0x43, "way":"i2c"},
            "led_attrs": {
                "green":0x04, "red":0x02, "amber":0x06, "default":0x04,
                "flash":0xff, "light":0xff, "off": 0, "mask":0x07
            },
        },
        {
            "name": "FRONT_FAN_LED",
            "led_type": "FAN_LED",
            "led": {"bus": 2, "addr": 0x2d,  "offset":0x42, "way":"i2c"},
            "led_attrs": {
                "green":0x04, "red":0x02, "amber":0x06, "default":0x04,
                "flash":0xff, "light":0xff, "off": 0, "mask":0x07
            },
        },
    ],
    "fans": [
        {
            "name": "FAN1",
            "airflow": fanairflow,
            "e2loc": {'loc': '/sys/bus/i2c/devices/i2c-35/35-0050/eeprom', 'way': 'sysfs'},
            "present": {"loc": "/sys/wb_plat/fan/fan1/present", "way": "sysfs", "mask": 0x01, "okval": 1},
            "SpeedMin": threshold.FAN_SPEED_MIN,
            "SpeedMax": threshold.FRONT_FAN_SPEED_MAX,
            "led": {"bus": 4, "addr": 0x3d, "offset": 0x41, "way": "i2c"},
            "led_attrs": {
                "off": 0x0, "red_flash": 0x01, "red": 0x02,
                "green_flash": 0x03, "green": 0x04, "amber_flash": 0x05,
                "amber": 0x06, "mask": 0x07
            },
            "PowerMax": 38.16,
            "Rotor": {
                "Rotor1_config": {
                    "name": "Rotor1",
                    "Set_speed": {"bus": 4, "addr": 0x3d, "offset": 0x65, "way": "i2c"},
                    "Running": {"loc": "/sys/wb_plat/fan/fan1/motor0/status", "way": "sysfs", "mask": 0x01, "is_runing": 1},
                    "HwAlarm": {"loc": "/sys/wb_plat/fan/fan1/motor0/status", "way": "sysfs", "mask": 0x01, "no_alarm": 1},
                    "SpeedMin": threshold.FAN_SPEED_MIN,
                    "SpeedMax": threshold.FRONT_FAN_SPEED_MAX,
                    "Speed": {
                        "value": {"loc": "/sys/wb_plat/fan/fan1/motor0/speed", "way": "sysfs"},
                        "Min": threshold.FAN_SPEED_MIN,
                        "Max": threshold.FRONT_FAN_SPEED_MAX,
                        "Unit": Unit.Speed,
                    },
                },
                "Rotor2_config": {
                    "name": "Rotor2",
                    "Set_speed": {"bus": 4, "addr": 0x3d, "offset": 0x65, "way": "i2c"},
                    "Running": {"loc": "/sys/wb_plat/fan/fan1/motor1/status", "way": "sysfs", "mask": 0x01, "is_runing": 1},
                    "HwAlarm": {"loc": "/sys/wb_plat/fan/fan1/motor1/status", "way": "sysfs", "mask": 0x01, "no_alarm": 1},
                    "SpeedMin": threshold.FAN_SPEED_MIN,
                    "SpeedMax": threshold.REAR_FAN_SPEED_MAX,
                    "Speed": {
                        "value": {"loc": "/sys/wb_plat/fan/fan1/motor1/speed", "way": "sysfs"},
                        "Min": threshold.FAN_SPEED_MIN,
                        "Max": threshold.REAR_FAN_SPEED_MAX,
                        "Unit": Unit.Speed,
                    },
                },
            },
        },
        {
            "name": "FAN2",
            "airflow": fanairflow,
            "e2loc": {'loc': '/sys/bus/i2c/devices/i2c-34/34-0050/eeprom', 'way': 'sysfs'},
            "present": {"loc": "/sys/wb_plat/fan/fan2/present", "way": "sysfs", "mask": 0x01, "okval": 1},
            "SpeedMin": threshold.FAN_SPEED_MIN,
            "SpeedMax": threshold.FRONT_FAN_SPEED_MAX,
            "led": {"bus": 4, "addr": 0x3d, "offset": 0x40, "way": "i2c"},
            "led_attrs": {
                "off": 0x0, "red_flash": 0x01, "red": 0x02,
                "green_flash": 0x03, "green": 0x04, "amber_flash": 0x05,
                "amber": 0x06, "mask": 0x07
            },
            "PowerMax": 38.16,
            "Rotor": {
                "Rotor1_config": {
                    "name": "Rotor1",
                    "Set_speed": {"bus": 4, "addr": 0x3d, "offset": 0x64, "way": "i2c"},
                    "Running": {"loc": "/sys/wb_plat/fan/fan2/motor0/status", "way": "sysfs", "mask": 0x01, "is_runing": 1},
                    "HwAlarm": {"loc": "/sys/wb_plat/fan/fan2/motor0/status", "way": "sysfs", "mask": 0x01, "no_alarm": 1},
                    "SpeedMin": threshold.FAN_SPEED_MIN,
                    "SpeedMax": threshold.FRONT_FAN_SPEED_MAX,
                    "Speed": {
                        "value": {"loc": "/sys/wb_plat/fan/fan2/motor0/speed", "way": "sysfs"},
                        "Min": threshold.FAN_SPEED_MIN,
                        "Max": threshold.FRONT_FAN_SPEED_MAX,
                        "Unit": Unit.Speed,
                    },
                },
                "Rotor2_config": {
                    "name": "Rotor2",
                    "Set_speed": {"bus": 4, "addr": 0x3d, "offset": 0x64, "way": "i2c"},
                    "Running": {"loc": "/sys/wb_plat/fan/fan2/motor1/status", "way": "sysfs", "mask": 0x01, "is_runing": 1},
                    "HwAlarm": {"loc": "/sys/wb_plat/fan/fan2/motor1/status", "way": "sysfs", "mask": 0x01, "no_alarm": 1},
                    "SpeedMin": threshold.FAN_SPEED_MIN,
                    "SpeedMax": threshold.REAR_FAN_SPEED_MAX,
                    "Speed": {
                        "value": {"loc": "/sys/wb_plat/fan/fan2/motor1/speed", "way": "sysfs"},
                        "Min": threshold.FAN_SPEED_MIN,
                        "Max": threshold.REAR_FAN_SPEED_MAX,
                        "Unit": Unit.Speed,
                    },
                },
            },
        },
        {
            "name": "FAN3",
            "airflow": fanairflow,
            "e2loc": {'loc': '/sys/bus/i2c/devices/i2c-33/33-0050/eeprom', 'way': 'sysfs'},
            "present": {"loc": "/sys/wb_plat/fan/fan3/present", "way": "sysfs", "mask": 0x01, "okval": 1},
            "SpeedMin": threshold.FAN_SPEED_MIN,
            "SpeedMax": threshold.FRONT_FAN_SPEED_MAX,
            "led": {"bus": 4, "addr": 0x3d, "offset": 0x3f, "way": "i2c"},
            "led_attrs": {
                "off": 0x0, "red_flash": 0x01, "red": 0x02,
                "green_flash": 0x03, "green": 0x04, "amber_flash": 0x05,
                "amber": 0x06, "mask": 0x07
            },
            "PowerMax": 38.16,
            "Rotor": {
                "Rotor1_config": {
                    "name": "Rotor1",
                    "Set_speed": {"bus": 4, "addr": 0x3d, "offset": 0x63, "way": "i2c"},
                    "Running": {"loc": "/sys/wb_plat/fan/fan3/motor0/status", "way": "sysfs", "mask": 0x01, "is_runing": 1},
                    "HwAlarm": {"loc": "/sys/wb_plat/fan/fan3/motor0/status", "way": "sysfs", "mask": 0x01, "no_alarm": 1},
                    "SpeedMin": threshold.FAN_SPEED_MIN,
                    "SpeedMax": threshold.FRONT_FAN_SPEED_MAX,
                    "Speed": {
                        "value": {"loc": "/sys/wb_plat/fan/fan3/motor0/speed", "way": "sysfs"},
                        "Min": threshold.FAN_SPEED_MIN,
                        "Max": threshold.FRONT_FAN_SPEED_MAX,
                        "Unit": Unit.Speed,
                    },
                },
                "Rotor2_config": {
                    "name": "Rotor2",
                    "Set_speed": {"bus": 4, "addr": 0x3d, "offset": 0x63, "way": "i2c"},
                    "Running": {"loc": "/sys/wb_plat/fan/fan3/motor1/status", "way": "sysfs", "mask": 0x01, "is_runing": 1},
                    "HwAlarm": {"loc": "/sys/wb_plat/fan/fan3/motor1/status", "way": "sysfs", "mask": 0x01, "no_alarm": 1},
                    "SpeedMin": threshold.FAN_SPEED_MIN,
                    "SpeedMax": threshold.REAR_FAN_SPEED_MAX,
                    "Speed": {
                        "value": {"loc": "/sys/wb_plat/fan/fan3/motor1/speed", "way": "sysfs"},
                        "Min": threshold.FAN_SPEED_MIN,
                        "Max": threshold.REAR_FAN_SPEED_MAX,
                        "Unit": Unit.Speed,
                    },
                },
            },
        },
        {
            "name": "FAN4",
            "airflow": fanairflow,
            "e2loc": {'loc': '/sys/bus/i2c/devices/i2c-32/32-0050/eeprom', 'way': 'sysfs'},
            "present": {"loc": "/sys/wb_plat/fan/fan4/present", "way": "sysfs", "mask": 0x01, "okval": 1},
            "SpeedMin": threshold.FAN_SPEED_MIN,
            "SpeedMax": threshold.FRONT_FAN_SPEED_MAX,
            "led": {"bus": 4, "addr": 0x3d, "offset": 0x3e, "way": "i2c"},
            "led_attrs": {
                "off": 0x0, "red_flash": 0x01, "red": 0x02,
                "green_flash": 0x03, "green": 0x04, "amber_flash": 0x05,
                "amber": 0x06, "mask": 0x07
            },
            "PowerMax": 38.16,
            "Rotor": {
                "Rotor1_config": {
                    "name": "Rotor1",
                    "Set_speed": {"bus": 4, "addr": 0x3d, "offset": 0x62, "way": "i2c"},
                    "Running": {"loc": "/sys/wb_plat/fan/fan4/motor0/status", "way": "sysfs", "mask": 0x01, "is_runing": 1},
                    "HwAlarm": {"loc": "/sys/wb_plat/fan/fan4/motor0/status", "way": "sysfs", "mask": 0x01, "no_alarm": 1},
                    "SpeedMin": threshold.FAN_SPEED_MIN,
                    "SpeedMax": threshold.FRONT_FAN_SPEED_MAX,
                    "Speed": {
                        "value": {"loc": "/sys/wb_plat/fan/fan4/motor0/speed", "way": "sysfs"},
                        "Min": threshold.FAN_SPEED_MIN,
                        "Max": threshold.FRONT_FAN_SPEED_MAX,
                        "Unit": Unit.Speed,
                    },
                },
                "Rotor2_config": {
                    "name": "Rotor2",
                    "Set_speed": {"bus": 4, "addr": 0x3d, "offset": 0x62, "way": "i2c"},
                    "Running": {"loc": "/sys/wb_plat/fan/fan4/motor1/status", "way": "sysfs", "mask": 0x01, "is_runing": 1},
                    "HwAlarm": {"loc": "/sys/wb_plat/fan/fan4/motor1/status", "way": "sysfs", "mask": 0x01, "no_alarm": 1},
                    "SpeedMin": threshold.FAN_SPEED_MIN,
                    "SpeedMax": threshold.REAR_FAN_SPEED_MAX,
                    "Speed": {
                        "value": {"loc": "/sys/wb_plat/fan/fan4/motor1/speed", "way": "sysfs"},
                        "Min": threshold.FAN_SPEED_MIN,
                        "Max": threshold.REAR_FAN_SPEED_MAX,
                        "Unit": Unit.Speed,
                    },
                },
            },
        },
        {
            "name": "FAN5",
            "airflow": fanairflow,
            "e2loc": {'loc': '/sys/bus/i2c/devices/i2c-31/31-0050/eeprom', 'way': 'sysfs'},
            "present": {"loc": "/sys/wb_plat/fan/fan5/present", "way": "sysfs", "mask": 0x01, "okval": 1},
            "SpeedMin": threshold.FAN_SPEED_MIN,
            "SpeedMax": threshold.FRONT_FAN_SPEED_MAX,
            "led": {"bus": 4, "addr": 0x3d, "offset": 0x3d, "way": "i2c"},
            "led_attrs": {
                "off": 0x0, "red_flash": 0x01, "red": 0x02,
                "green_flash": 0x03, "green": 0x04, "amber_flash": 0x05,
                "amber": 0x06, "mask": 0x07
            },
            "PowerMax": 38.16,
            "Rotor": {
                "Rotor1_config": {
                    "name": "Rotor1",
                    "Set_speed": {"bus": 4, "addr": 0x3d, "offset": 0x61, "way": "i2c"},
                    "Running": {"loc": "/sys/wb_plat/fan/fan5/motor0/status", "way": "sysfs", "mask": 0x01, "is_runing": 1},
                    "HwAlarm": {"loc": "/sys/wb_plat/fan/fan5/motor0/status", "way": "sysfs", "mask": 0x01, "no_alarm": 1},
                    "SpeedMin": threshold.FAN_SPEED_MIN,
                    "SpeedMax": threshold.FRONT_FAN_SPEED_MAX,
                    "Speed": {
                        "value": {"loc": "/sys/wb_plat/fan/fan5/motor0/speed", "way": "sysfs"},
                        "Min": threshold.FAN_SPEED_MIN,
                        "Max": threshold.FRONT_FAN_SPEED_MAX,
                        "Unit": Unit.Speed,
                    },
                },
                "Rotor2_config": {
                    "name": "Rotor2",
                    "Set_speed": {"bus": 4, "addr": 0x3d, "offset": 0x61, "way": "i2c"},
                    "Running": {"loc": "/sys/wb_plat/fan/fan5/motor1/status", "way": "sysfs", "mask": 0x01, "is_runing": 1},
                    "HwAlarm": {"loc": "/sys/wb_plat/fan/fan5/motor1/status", "way": "sysfs", "mask": 0x01, "no_alarm": 1},
                    "SpeedMin": threshold.FAN_SPEED_MIN,
                    "SpeedMax": threshold.REAR_FAN_SPEED_MAX,
                    "Speed": {
                        "value": {"loc": "/sys/wb_plat/fan/fan5/motor1/speed", "way": "sysfs"},
                        "Min": threshold.FAN_SPEED_MIN,
                        "Max": threshold.REAR_FAN_SPEED_MAX,
                        "Unit": Unit.Speed,
                    },
                },
            },
        },
        {
            "name": "FAN6",
            "airflow": fanairflow,
            "e2loc": {'loc': '/sys/bus/i2c/devices/i2c-30/30-0050/eeprom', 'way': 'sysfs'},
            "present": {"loc": "/sys/wb_plat/fan/fan6/present", "way": "sysfs", "mask": 0x01, "okval": 1},
            "SpeedMin": threshold.FAN_SPEED_MIN,
            "SpeedMax": threshold.FRONT_FAN_SPEED_MAX,
            "led": {"bus": 4, "addr": 0x3d, "offset": 0x3c, "way": "i2c"},
            "led_attrs": {
                "off": 0x0, "red_flash": 0x01, "red": 0x02,
                "green_flash": 0x03, "green": 0x04, "amber_flash": 0x05,
                "amber": 0x06, "mask": 0x07
            },
            "PowerMax": 38.16,
            "Rotor": {
                "Rotor1_config": {
                    "name": "Rotor1",
                    "Set_speed": {"bus": 4, "addr": 0x3d, "offset": 0x60, "way": "i2c"},
                    "Running": {"loc": "/sys/wb_plat/fan/fan6/motor0/status", "way": "sysfs", "mask": 0x01, "is_runing": 1},
                    "HwAlarm": {"loc": "/sys/wb_plat/fan/fan6/motor0/status", "way": "sysfs", "mask": 0x01, "no_alarm": 1},
                    "SpeedMin": threshold.FAN_SPEED_MIN,
                    "SpeedMax": threshold.FRONT_FAN_SPEED_MAX,
                    "Speed": {
                        "value": {"loc": "/sys/wb_plat/fan/fan6/motor0/speed", "way": "sysfs"},
                        "Min": threshold.FAN_SPEED_MIN,
                        "Max": threshold.FRONT_FAN_SPEED_MAX,
                        "Unit": Unit.Speed,
                    },
                },
                "Rotor2_config": {
                    "name": "Rotor2",
                    "Set_speed": {"bus": 4, "addr": 0x3d, "offset": 0x60, "way": "i2c"},
                    "Running": {"loc": "/sys/wb_plat/fan/fan6/motor1/status", "way": "sysfs", "mask": 0x01, "is_runing": 1},
                    "HwAlarm": {"loc": "/sys/wb_plat/fan/fan6/motor1/status", "way": "sysfs", "mask": 0x01, "no_alarm": 1},
                    "SpeedMin": threshold.FAN_SPEED_MIN,
                    "SpeedMax": threshold.REAR_FAN_SPEED_MAX,
                    "Speed": {
                        "value": {"loc": "/sys/wb_plat/fan/fan6/motor1/speed", "way": "sysfs"},
                        "Min": threshold.FAN_SPEED_MIN,
                        "Max": threshold.REAR_FAN_SPEED_MAX,
                        "Unit": Unit.Speed,
                    },
                },
            },
        },
    ],
    "cplds": [
        {
            "name": "CPU_CPLD",
            "cpld_id": "CPLD1",
            "VersionFile": {"loc": "/dev/cpld0", "offset": 0, "len": 4, "way": "devfile_ascii"},
            "desc": "Used for system power",
            "slot": 0,
            "warm": 1,
        },
        {
            "name": "CONNECT_CPLD",
            "cpld_id": "CPLD2",
            "VersionFile": {"loc": "/dev/cpld1", "offset": 0, "len": 4, "way": "devfile_ascii"},
            "desc": "Used for base functions",
            "slot": 0,
            "warm": 1,
        },
        {
            "name": "MAC_CPLDA",
            "cpld_id": "CPLD3",
            "VersionFile": {"loc": "/dev/cpld4", "offset": 0, "len": 4, "way": "devfile_ascii"},
            "desc": "Used for sff modules",
            "slot": 0,
            "warm": 1,
        },
        {
            "name": "MAC_CPLDB",
            "cpld_id": "CPLD4",
            "VersionFile": {"loc": "/dev/cpld5", "offset": 0, "len": 4, "way": "devfile_ascii"},
            "desc": "Used for sff modules",
            "slot": 0,
            "warm": 1,
        },
        {
            "name": "FAN_CPLD",
            "cpld_id": "CPLD5",
            "VersionFile": {"loc": "/dev/cpld6", "offset": 0, "len": 4, "way": "devfile_ascii"},
            "desc": "Used for fan modules",
            "slot": 0,
            "warm": 1,
        },
        {
            "name": "FPGA",
            "cpld_id": "CPLD6",
            "VersionFile": {"loc": "/dev/fpga0", "offset": 0, "len": 4, "way": "devfile_ascii"},
            "desc": "Used for base functions",
            "slot": 0,
            "format": "little_endian",
            "warm": 1,
        },
        {
            "name": "BIOS",
            "cpld_id": "CPLD7",
            "VersionFile": {"cmd": "dmidecode -s bios-version", "way": "cmd"},
            "desc": "Performs initialization of hardware components during booting",
            "slot": 0,
            "type": "str",
            "warm": 0,
        },
    ],
    "dcdc": [
        {
            "name": "VDD5V_CLK_MCU",
            "dcdc_id": "DCDC1",
            "value": {
                "loc": "/sys/bus/i2c/devices/45-005b/hwmon/hwmon*/in1_input",
                "way": "sysfs",
            },
            "read_times": 1,
            "Min": 4250,
            "Max": 5750,
            "Unit": "V",
            "format": "float(float(%s)/1000)",
        },

        {
            "name": "VDD3.3_CLK",
            "dcdc_id": "DCDC2",
            "value": {
                "loc": "/sys/bus/i2c/devices/45-005b/hwmon/hwmon*/in2_input",
                "way": "sysfs",
            },
            "read_times": 1,
            "Min": 2805,
            "Max": 3795,
            "Unit": "V",
            "format": "float(float(%s)/1000)",
        },

        {
            "name": "VDD1.0V",
            "dcdc_id": "DCDC3",
            "value": {
                "loc": "/sys/bus/i2c/devices/45-005b/hwmon/hwmon*/in3_input",
                "way": "sysfs",
            },
            "read_times": 1,
            "Min": 850,
            "Max": 1150,
            "Unit": "V",
            "format": "float(float(%s)/1000)",
        },

        {
            "name": "VDD1.8V",
            "dcdc_id": "DCDC4",
            "value": {
                "loc": "/sys/bus/i2c/devices/45-005b/hwmon/hwmon*/in4_input",
                "way": "sysfs",
            },
            "read_times": 1,
            "Min": 1530,
            "Max": 2070,
            "Unit": "V",
            "format": "float(float(%s)/1000)",
        },

        {
            "name": "MAC_BOARD_VDD3.3V",
            "dcdc_id": "DCDC5",
            "value": {
                "loc": "/sys/bus/i2c/devices/45-005b/hwmon/hwmon*/in5_input",
                "way": "sysfs",
            },
            "read_times": 1,
            "Min": 2805,
            "Max": 3795,
            "Unit": "V",
            "format": "float(float(%s)/1000)",
        },

        {
            "name": "VDD1.2V",
            "dcdc_id": "DCDC6",
            "value": {
                "loc": "/sys/bus/i2c/devices/45-005b/hwmon/hwmon*/in6_input",
                "way": "sysfs",
            },
            "read_times": 1,
            "Min": 1020,
            "Max": 1380,
            "Unit": "V",
            "format": "float(float(%s)/1000)",
        },

        {
            "name": "VDD_CORE",
            "dcdc_id": "DCDC7",
            "value": {
                "loc": "/sys/bus/i2c/devices/45-005b/hwmon/hwmon*/in7_input",
                "way": "sysfs",
            },
            "read_times": 1,
            "Min": 600,
            "Max": 1100,
            "Unit": "V",
            "format": "float(float(%s)/1000)",
        },

        {
            "name": "ANALOG0.75V",
            "dcdc_id": "DCDC8",
            "value": {
                "loc": "/sys/bus/i2c/devices/45-005b/hwmon/hwmon*/in8_input",
                "way": "sysfs",
            },
            "read_times": 1,
            "Min": 615,
            "Max": 1000,
            "Unit": "V",
            "format": "float(float(%s)/1000)",
        },

        {
            "name": "MAC_VDD1.2V",
            "dcdc_id": "DCDC9",
            "value": {
                "loc": "/sys/bus/i2c/devices/45-005b/hwmon/hwmon*/in9_input",
                "way": "sysfs",
            },
            "read_times": 1,
            "Min": 1020,
            "Max": 1380,
            "Unit": "V",
            "format": "float(float(%s)/1000)",
        },

        {
            "name": "VDDO1.8V",
            "dcdc_id": "DCDC10",
            "value": {
                "loc": "/sys/bus/i2c/devices/45-005b/hwmon/hwmon*/in10_input",
                "way": "sysfs",
            },
            "read_times": 1,
            "Min": 1530,
            "Max": 2070,
            "Unit": "V",
            "format": "float(float(%s)/1000)",
        },

        {
            "name": "MAC_ANA1.2V",
            "dcdc_id": "DCDC11",
            "value": {
                "loc": "/sys/bus/i2c/devices/45-005b/hwmon/hwmon*/in11_input",
                "way": "sysfs",
            },
            "read_times": 1,
            "Min": 1020,
            "Max": 1380,
            "Unit": "V",
            "format": "float(float(%s)/1000)",
        },

        {
            "name": "MAC_ANA1.8V",
            "dcdc_id": "DCDC12",
            "value": {
                "loc": "/sys/bus/i2c/devices/45-005b/hwmon/hwmon*/in12_input",
                "way": "sysfs",
            },
            "read_times": 1,
            "Min": 1530,
            "Max": 2070,
            "Unit": "V",
            "format": "float(float(%s)/1000)",
        },

        {
            "name": "QSFP56_VDD3.3V_A",
            "dcdc_id": "DCDC13",
            "value": {
                "loc": "/sys/bus/i2c/devices/45-005b/hwmon/hwmon*/in13_input",
                "way": "sysfs",
            },
            "read_times": 1,
            "Min": 2805,
            "Max": 3795,
            "Unit": "V",
            "format": "float(float(%s)/1000)",
        },

        {
            "name": "QSFP56_VDD3.3V_B",
            "dcdc_id": "DCDC14",
            "value": {
                "loc": "/sys/bus/i2c/devices/45-005b/hwmon/hwmon*/in14_input",
                "way": "sysfs",
            },
            "read_times": 1,
            "Min": 2805,
            "Max": 3795,
            "Unit": "V",
            "format": "float(float(%s)/1000)",
        },

        {
            "name": "QSFPDD_VDD3.3V_A",
            "dcdc_id": "DCDC15",
            "value": {
                "loc": "/sys/bus/i2c/devices/45-005b/hwmon/hwmon*/in15_input",
                "way": "sysfs",
            },
            "read_times": 1,
            "Min": 2805,
            "Max": 3795,
            "Unit": "V",
            "format": "float(float(%s)/1000)",
        },

        {
            "name": "QSFPDD_VDD3.3V_B",
            "dcdc_id": "DCDC16",
            "value": {
                "loc": "/sys/bus/i2c/devices/45-005b/hwmon/hwmon*/in16_input",
                "way": "sysfs",
            },
            "read_times": 1,
            "Min": 2805,
            "Max": 3795,
            "Unit": "V",
            "format": "float(float(%s)/1000)",
        },

        {
            "name": "VDD5.0V",
            "dcdc_id": "DCDC17",
            "value": {
                "loc": "/sys/bus/i2c/devices/24-005b/hwmon/hwmon*/in1_input",
                "way": "sysfs",
            },
            "read_times": 1,
            "Min": 4250,
            "Max": 5750,
            "Unit": "V",
            "format": "float(float(%s)/1000)",
        },

        {
            "name": "SW_VDD1.2V",
            "dcdc_id": "DCDC18",
            "value": {
                "loc": "/sys/bus/i2c/devices/24-005b/hwmon/hwmon*/in2_input",
                "way": "sysfs",
            },
            "read_times": 1,
            "Min": 1020,
            "Max": 1380,
            "Unit": "V",
            "format": "float(float(%s)/1000)",
        },

        {
            "name": "VDD2.5V",
            "dcdc_id": "DCDC19",
            "value": {
                "loc": "/sys/bus/i2c/devices/24-005b/hwmon/hwmon*/in3_input",
                "way": "sysfs",
            },
            "read_times": 1,
            "Min": 2125,
            "Max": 2875,
            "Unit": "V",
            "format": "float(float(%s)/1000)",
        },

        {
            "name": "CONNECT_BOARD_VDD3.3V",
            "dcdc_id": "DCDC20",
            "value": {
                "loc": "/sys/bus/i2c/devices/24-005b/hwmon/hwmon*/in4_input",
                "way": "sysfs",
            },
            "read_times": 1,
            "Min": 2805,
            "Max": 3795,
            "Unit": "V",
            "format": "float(float(%s)/1000)",
        },

        {
            "name": "VDD12V",
            "dcdc_id": "DCDC21",
            "value": {
                "loc": "/sys/bus/i2c/devices/24-005b/hwmon/hwmon*/in6_input",
                "way": "sysfs",
            },
            "read_times": 1,
            "Min": 10200,
            "Max": 13800,
            "Unit": "V",
            "format": "float(float(%s)/1000)",
        },

        {
            "name": "VDD3.3_STBY",
            "dcdc_id": "DCDC22",
            "value": {
                "loc": "/sys/bus/i2c/devices/24-005b/hwmon/hwmon*/in7_input",
                "way": "sysfs",
            },
            "read_times": 1,
            "Min": 2805,
            "Max": 3795,
            "Unit": "V",
            "format": "float(float(%s)/1000)",
        },

        {
            "name": "SSD_VDD3.3V",
            "dcdc_id": "DCDC23",
            "value": {
                "loc": "/sys/bus/i2c/devices/24-005b/hwmon/hwmon*/in8_input",
                "way": "sysfs",
            },
            "read_times": 1,
            "Min": 2805,
            "Max": 3795,
            "Unit": "V",
            "format": "float(float(%s)/1000)",
        },

        {
            "name": "VCCIN",
            "dcdc_id": "DCDC24",
            "value": {
                "loc": "/sys/bus/i2c/devices/25-0067/hwmon/hwmon*/in2_input",
                "way": "sysfs",
            },
            "read_times": 1,
            "Min": 1368,
            "Max": 2244,
            "Unit": "V",
            "format": "float(float(%s)/1000)",
        },

        {
            "name": "P1V05",
            "dcdc_id": "DCDC25",
            "value": {
                "loc": "/sys/bus/i2c/devices/25-0067/hwmon/hwmon*/in3_input",
                "way": "sysfs",
            },
            "read_times": 1,
            "Min": 882,
            "Max": 1232,
            "Unit": "V",
            "format": "float(float(%s)/1000)",
        },

        {
            "name": "VCCD_V",
            "dcdc_id": "DCDC26",
            "value": {
                "loc": "/sys/bus/i2c/devices/25-006c/hwmon/hwmon*/in2_input",
                "way": "sysfs",
            },
            "read_times": 1,
            "Min": 990,
            "Max": 1452,
            "Unit": "V",
            "format": "float(float(%s)/1000)",
        },

        {
            "name": "VCCSCSUS_V",
            "dcdc_id": "DCDC27",
            "value": {
                "loc": "/sys/bus/i2c/devices/25-006c/hwmon/hwmon*/in3_input",
                "way": "sysfs",
            },
            "read_times": 1,
            "Min": 855,
            "Max": 1265,
            "Unit": "V",
            "format": "float(float(%s)/1000)",
        },

        {
            "name": "P3V3_STBY_V",
            "dcdc_id": "DCDC28",
            "value": {
                "loc": "/sys/bus/i2c/devices/25-0043/hwmon/hwmon*/in2_input",
                "way": "sysfs",
            },
            "read_times": 1,
            "Min": 2682,
            "Max": 4004,
            "Unit": "V",
            "format": "float(float(%s)/1000)",
        },

        {
            "name": "P5V_AUX_IN",
            "dcdc_id": "DCDC29",
            "value": {
                "loc": "/sys/bus/i2c/devices/25-0043/hwmon/hwmon*/in1_input",
                "way": "sysfs",
            },
            "read_times": 1,
            "Min": 3852,
            "Max": 6347,
            "Unit": "V",
            "format": "float(float(%s)/1000)",
        },

        {
            "name": "P1V7_VCCSCFUSESUS_IN",
            "dcdc_id": "DCDC30",
            "value": {
                "loc": "/sys/bus/i2c/devices/25-0043/hwmon/hwmon*/in3_input",
                "way": "sysfs",
            },
            "read_times": 1,
            "Min": 1377,
            "Max": 2057,
            "Unit": "V",
            "format": "float(float(%s)/1000)",
        },
    ],
    "cpu": [
        {
            "name": "cpu",
            "CpuResetCntReg": {"loc": "/dev/cpld1", "offset": 0x88, "len": 1, "way": "devfile_ascii"},
            "reboot_cause_path": "/etc/sonic/.reboot/.previous-reboot-cause.txt"
        }
    ],
    "sfps": {
        "ver": '1.0',
        "port_index_start": 0,
        "port_num": 32,
        "log_level": 2,
        "eeprom_retry_times": 5,
        "eeprom_retry_break_sec": 0.2,
        "presence_cpld": {
            "dev_id": {
                4: {
                    "offset": {
                        0x30: "1-8",
                        0x31: "9-16",
                        0x32: "17-24",
                        0x33: "25-32"
                    },
                },
            },
        },
        "presence_val_is_present": 0,
        "eeprom_path": "/sys/bus/i2c/devices/i2c-%d/%d-0050/eeprom",
        "eeprom_path_key": list(range(46, 78)),
        "optoe_driver_path": "/sys/bus/i2c/devices/i2c-%d/%d-0050/dev_class",
        "optoe_driver_key": list(range(46, 78)),
        "reset_cpld": {
            "dev_id": {
                5: {
                    "offset": {
                        0x22: "1-8",
                        0x23: "9-16"
                    },
                },
                4: {
                    "offset": {
                        0x21: "17-24",
                        0x22: "25-32"
                    },
                },
            },
        },
        "reset_val_is_reset": 0,
    }
}