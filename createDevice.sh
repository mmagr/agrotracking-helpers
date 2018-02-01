#!/bin/bash

[ -f /etc/config/id_tiv ] && exit 0

username=${username-"tiv"}
password=${password-"tiv"}
target=${target-"cpqd036890.aquarius.cpqd.com.br:8000"}

getToken () {
  echo "authorization: Bearer $(curl -sS $target/auth -H 'content-type: application/json' -d "{\"username\":\"$username\", \"passwd\":\"$password\"}" | grep jwt | grep -oE [a-zA-Z0-9_-]+.[a-zA-Z0-9_-]+.[a-zA-Z0-9_-]+ )"
}

getId () {
  echo "$(echo $RANDOM).$(echo $RANDOM)"
}

deviceData=$(cat <<PAYLOAD
{
  "attrs": [
      {"name": "epc", "object_id": "$(getId)", "type": "string" },
      {"name": "antenna", "object_id": "$(getId)", "type": "string" },
      {"name": "rssi", "object_id": "$(getId)", "type": "float" },
      {"name": "canRpm",                 "object_id": "$(getId)", "type": "string" },
      {"name": "canFuelRate",            "object_id": "$(getId)", "type": "string" },
      {"name": "canEngineUpTime",        "object_id": "$(getId)", "type": "string" },
      {"name": "canCoolantTemp",         "object_id": "$(getId)", "type": "string" },
      {"name": "canBoostPressure",       "object_id": "$(getId)", "type": "string" },
      {"name": "canOilPressure",         "object_id": "$(getId)", "type": "string" },
      {"name": "canOilTemperature",      "object_id": "$(getId)", "type": "string" },
      {"name": "canEngineLoad",          "object_id": "$(getId)", "type": "string" },
      {"name": "canManifoldTemperature", "object_id": "$(getId)", "type": "string" },
      {"name": "canFuelLevel",           "object_id": "$(getId)", "type": "string" },
      {"name": "canBatteryVoltage",      "object_id": "$(getId)", "type": "string" },
      {"name": "canHidrOilTemperature",  "object_id": "$(getId)", "type": "string" },
      {"name": "canCutterPressure",      "object_id": "$(getId)", "type": "string" },
      {"name": "canCutterHeight",        "object_id": "$(getId)", "type": "string" },
      {"name": "canCutterStatus",        "object_id": "$(getId)", "type": "string" },
      {"name": "canElevatorUpTime",      "object_id": "$(getId)", "type": "string" },
      {"name": "canElevatorStatus",      "object_id": "$(getId)", "type": "string" },
      {"name": "canExtractorRpm",        "object_id": "$(getId)", "type": "string" },
      {"name": "canWorkCondition",       "object_id": "$(getId)", "type": "string" },
      {"name": "canFieldMode",           "object_id": "$(getId)", "type": "string" }
  ],
  "label": "tiv-$(getId)",
  "protocol": "MQTT",
  "static_attrs": [],
  "tags": [],
  "templates": []
}
PAYLOAD
)

deviceId=$(curl -sS $target/device -X POST -H "$(getToken)" -H 'content-type: application/json' -d "$deviceData" | grep -oE '"id": "[a-fA-F0-9]{4}"' | grep -oE '[a-fA-F0-9]{4}')

echo "got deviceId: $deviceId"
sed -e "s/___id___/$deviceId/g" -i /etc/config/metrics/config.json
sed -e "s/___id___/$deviceId/g" -i /etc/config/rfid_mqtt/config.json
echo $deviceId > /etc/config/id_tiv
