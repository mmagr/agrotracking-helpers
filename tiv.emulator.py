#!/usr/bin/python

import os
import random
import json
import time
import paho.mqtt.client as mqtt
import numpy as np

known_locs = [
    "-21.2074587,-47.8344727",
    "-22.9179229,-46.9995117",
    "-20.4887733,-54.5581055",
    "-16.7203851,-49.2407227",
    "-25.562265,-49.21875",
    "-26.3328069,-48.7573242",
    "-7.1008927,-35.0244141",
    "-7.9286748,-35.15625",
    "-5.2222465,-35.4748535",
    "-4.5654736,-37.7929687",
    "-3.9300202,-38.3752441",
    "-3.4695573,-39.5617676",
    "-2.9869274,-40.8911133",
    "-11.0490383,-37.2216797",
    "-1.4061088,-48.515625",
    "0.175781,-51.3720703",
    "-20.0559313,-43.8574219",
    "-30.069094,-51.2841797",
    "-27.6056708,-48.8671875",
    "-15.0721235,-55.6347656",
    "2.591889,-60.7763672",
    "-3.1624555,-59.9853516",
    "-9.9688506,-67.8515625",
    "-10.2284373,-48.8452148",
    "-12.1897038,-45.1318359",
    "-12.6617775,-38.3422852",
    "-16.4044705,-39.1552734",
    "-20.3652275,-40.4296875",
    "-18.9582465,-48.2958984",
    "-22.6951202,-43.1982422",
    "-9.644077,-35.7275391",
    "-2.5479879,-44.2089844",
    "-2.8991527,-41.7919922",
    "-9.5140793,-40.4516602",
    "-7.2752923,-39.309082",
    "-14.8386116,-40.8691406",
    "-10.4229884,-40.1000977",
    "-7.0354757,-41.484375",
    "-17.8951143,-41.0009766",
    "-2.5040853,-54.6240234",
    "-3.9957805,-63.2592773",
    "-21.8003081,-52.1630859",
    "-20.3034175,-51.3061523",
    "-31.8215645,-52.5146484",
    "-14.8598504,-39.2211914",
    "-5.0909442,-36.9580078",
    "-7.5149809,-36.5844727",
    "-8.863362,-37.4194336",
    "-4.1272853,-39.8583984",
    "-8.2767271,-36.3647461"
]

attrs = [
    { "name": "ts",                      "object_id": "19208.30203",   "type": "string" },
    { "name": "imsi",                    "object_id": "26135.23029",   "type": "string" },
    { "name": "ue_status",               "object_id": "23459.3772",    "type": "string" },
    { "name": "rssi",                    "object_id": "14028.28181",   "type": "integer" },
    { "name": "cell_id",                 "object_id": "24382.13155",   "type": "integer" },
    { "name": "sinr",                    "object_id": "20705.9477",    "type": "integer" },
    { "name": "temperature",             "object_id": "19666.10357",   "type": "float" },
    { "name": "track",                   "object_id": "2004.3919",     "type": "float" },
    { "name": "speed",                   "object_id": "16984.20704",   "type": "float" },
    { "name": "sattelites",              "object_id": "27692.6258",    "type": "integer" },
    { "name": "quality",                 "object_id": "19788.4444",    "type": "integer" },
    { "name": "fix",                     "object_id": "18242.6734",    "type": "integer" },
    { "name": "lat",                     "object_id": "19305.15017",   "type": "float" },
    { "name": "lng",                     "object_id": "30620.1459",    "type": "float" },
    { "name": "coordinates",             "object_id": "25480.8783",    "type": "geo:point" },
    { "name": "alt",                     "object_id": "9229.26992",    "type": "float" },
    { "name": "number_of_tests",         "object_id": "9094.25165",    "type": "integer" },
    { "name": "number_of_ok",            "object_id": "17264.20025",   "type": "integer" },
    { "name": "number_of_failed",        "object_id": "32202.30604",   "type": "integer" },
    { "name": "average_latency_msec",    "object_id": "29.27437",      "type": "float" },
    { "name": "maximum_latency_msec",    "object_id": "19478.31319",   "type": "float" },
    { "name": "minimum_latency_msec",    "object_id": "786.25714",     "type": "float" },
    { "name": "latency_std_deviation",   "object_id": "22379.25760",   "type": "float" },
    { "name": "latency_variance",        "object_id": "31044.26866",   "type": "float" },
    { "name": "test_time_elapsed",       "object_id": "29172.7228",    "type": "integer" },
    { "name": "rpm",                     "object_id": "16796.22941",   "type": "integer" },
    { "name": "fuelRate",                "object_id": "16787.5841",    "type": "float" },
    { "name": "engineUpTime",            "object_id": "1886.31141",    "type": "integer" },
    { "name": "coolantTemp",             "object_id": "24028.2594",    "type": "integer" },
    { "name": "boostPressure",           "object_id": "20748.20858",   "type": "float" },
    { "name": "oilPressure",             "object_id": "5666.16377",    "type": "float" },
    { "name": "oilTemperature",          "object_id": "1989.1479",     "type": "integer" },
    { "name": "engineLoad",              "object_id": "11328.11777",   "type": "integer" },
    { "name": "manifoldTemperature",     "object_id": "15323.31846",   "type": "integer" },
    { "name": "fuelLevel",               "object_id": "7797.24149",    "type": "float" },
    { "name": "hidrOilTemperature",      "object_id": "22845.15173",   "type": "integer" },
    { "name": "cutterPressure",          "object_id": "3252.13401",    "type": "float" },
    { "name": "cutterHeight",            "object_id": "4202.22362",    "type": "integer" },
    { "name": "cutterStatus",            "object_id": "9666.29518",    "type": "integer" },
    { "name": "elevatorUpTime",          "object_id": "17203.6712",    "type": "integer" },
    { "name": "elevatorStatus",          "object_id": "18156.22777",   "type": "integer" },
    { "name": "extractorRpm",            "object_id": "1508.17298",    "type": "integer" },
    { "name": "workCondition",           "object_id": "18687.20544",   "type": "integer" },
    { "name": "fieldMode",               "object_id": "15743.27810",   "type": "integer" },
    { "name": "groundSpeed",             "object_id": "28185.28857",   "type": "float" },
    { "name": "workStatus",              "object_id": "4824.3187",     "type": "integer" },
    { "name": "fuelRateAverage",         "object_id": "11005.24990",   "type": "float" },
    { "name": "fuelAreaAverage",         "object_id": "3324.21652",    "type": "float" },
    { "name": "fuelUsedField",           "object_id": "15088.8036",    "type": "float" },
    { "name": "fuelUsedRoad",            "object_id": "25344.22012",   "type": "float" },
    { "name": "farmingAreaRemain",       "object_id": "29339.20240",   "type": "integer" },
    { "name": "area",                    "object_id": "16737.21810",   "type": "integer" },
    { "name": "yieldWet",                "object_id": "9172.28627",    "type": "float" },
    { "name": "yieldWetAverage",         "object_id": "7455.25670",    "type": "float" },
    { "name": "flowWet",                 "object_id": "23407.24925",   "type": "float" },
    { "name": "flowWetAverage",          "object_id": "25804.22591",   "type": "float" },
    { "name": "weightWet",               "object_id": "24561.26076",   "type": "integer" },
    { "name": "idleReason",              "object_id": "25663.29661",   "type": "integer" },
    { "name": "idleDuration",            "object_id": "3148.29762",    "type": "integer" },
    { "name": "operator",                "object_id": "16997.10852",   "type": "string" },
    { "name": "crop",                    "object_id": "27146.14221",   "type": "integer" },
    { "name": "grower",                  "object_id": "26285.22678",   "type": "string" },
    { "name": "farm",                    "object_id": "6643.18310",    "type": "string" },
    { "name": "field",                   "object_id": "14752.10571",   "type": "string" },
    { "name": "task",                    "object_id": "17097.7162",    "type": "string" },
    { "name": "taskSUID",                "object_id": "26898.13243",   "type": "string" },
    { "name": "tags",                    "object_id": "12604.3405",    "type": "string" },
    { "name": "vehicleID",               "object_id": "8759.7916",     "type": "string" },
    { "name": "fuelTheft",               "object_id": "9974.24527",    "type": "integer" },
    { "name": "displayAlarmStatus",      "object_id": "18141.25758",   "type": "integer" },
    { "name": "displayAlarmCode",        "object_id": "20508.23702",   "type": "string" },
    { "name": "tiv_id",                  "object_id": "13828.6321",    "type": "string" },
    { "name": "rfid_tag_id",             "object_id": "23800.8101",    "type": "string" },
    { "name": "rfid_antenna",            "object_id": "16387.19878",   "type": "integer" },
    { "name": "rfid_rssi",               "object_id": "10343.27297",   "type": "integer" },
    { "name": "rfid_read_count",         "object_id": "26167.22719",   "type": "integer" },
    { "name": "rfid_read_elapsed_time",  "object_id": "25928.4757",    "type": "integer "}
]

devices = [
    "0b06",
    "cbf7",
    "b3b5",
    "846f",
    "0b6b",
    "1362",
    "9de0",
    "442f",
    "374c",
    "98f4",
    "138e",
    "c686",
    "9822",
    "02f7",
    "c981",
    "250f",
    "438c",
    "42e9",
    "6e0c"
]

def generateValue(value, payload):
    def generateInt():
        return int(np.random.normal(-36.0, 1.5))
    def generateString():
        return known_locs[random.randrange(len(known_locs))]
    def generateFloat():
        return round(np.random.normal(-36.0, 1.5), 2)
    def generateGeo():
        return known_locs[random.randrange(len(known_locs))]


    if value['type'] == 'integer':
        payload[value['name']] = generateInt()
    elif value['type'] == 'float':
        payload[value['name']] = generateFloat()
    elif value['type'] == 'string':
        payload[value['name']] = generateString()
    elif value['type'] == 'geo':
        payload[value['name']] = generateGeo()
    elif value['type'] == 'geo:point':
        payload[value['name']] = generateGeo()


# mqtt init
client = mqtt.Client()
client.connect('iotmid-docker49.cpqd.com.br', 1883, 60)
client.loop_start()

for device in devices:
    payload = {}
    for k in attrs:
        generateValue(k, payload)
    client.publish("/admin/%s/attrs" % device, json.dumps(payload))
    #time.sleep(0.5)

client.loop_stop()
