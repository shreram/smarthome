# Template Fun

Ever wondered what trigger data is available for you when writing automations? Just copy the mqtt.publish service below 
and put it in any of your automation, and it will dump all the attributes and information into your mqtt.
Pre-requisite is to have MQTT configured. Use tools like `mqttfx` to browse mqtt data.

Enjoy!

```
  - alias: Test Kitchen Light
    initial_state: true
    hide_entity: false
    trigger:
      platform: state
      entity_id: light.dinette
    action:        
      - service: mqtt.publish
        data_template:
          topic: '/dump/{{ trigger.platform }}'
          retain: false
          payload: >-
            {%- macro dumpState(statePrefix, stateObj) -%}
              {{statePrefix ~ ": "}} {{- stateObj.state }}{{- "\n" -}}
              {{statePrefix ~ ".entity_id: "}} {{- stateObj.entity_id }}{{- "\n" -}}
              {{statePrefix ~ ".domain: "}} {{- stateObj.domain }}{{- "\n" -}}
              {{statePrefix ~ ".object_id: "}} {{- stateObj.object_id }}{{- "\n" -}}
              {{statePrefix ~ ".name: "}} {{- stateObj.name }}{{- "\n" -}}
              {{statePrefix ~ ".last_updated: "}} {{- stateObj.last_updated }}{{- "\n" -}}
              {{statePrefix ~ ".last_changed: "}} {{- stateObj.last_changed }}{{- "\n" -}}
              {%- for attrib in stateObj.attributes | sort() %}
                {%- if attrib is defined -%} 
                {{- statePrefix ~ ".attributes." ~ attrib ~ ": " -}} {{- stateObj.attributes[attrib] -}}{{- "\n" -}}
                {%- endif -%}
              {%- endfor -%}
            {%- endmacro -%}
            
            {{"trigger.platform: "}} {{ trigger.platform }}{{- "\n" -}}
            
            {%- if trigger.platform == "mqtt" -%}
            {{"trigger.topic: "}} {{ trigger.topic }}{{- "\n" -}}
            {{"trigger.payload: "}} {{ trigger.payload }}{{- "\n" -}}
            {{"trigger.payload_json: "}} {{ trigger.payload_json }}{{- "\n" -}}
            {{"trigger.qos: "}} {{ trigger.qos }}{{- "\n" -}}
            {%- endif -%}
            
            {%- if trigger.platform == "event" or trigger.platform == "sun" or trigger.platform == "zone" -%}
            {{"trigger.event: "}} {{ trigger.event }}{{- "\n" -}}
            {%- endif -%}
            
            {%- if trigger.platform == "numeric_state" -%}
            {{"trigger.above: "}} {{ trigger.above }}{{- "\n" -}}
            {{"trigger.below: "}} {{trigger.below }}{{- "\n" -}}
            {%- endif -%}
            
            {%- if trigger.platform == "state" -%}
            {{"trigger.for: "}} {{ trigger.for }}{{- "\n" -}}
            {%- endif -%}
            
            {%- if trigger.platform == "time" -%}
            {{"trigger.now: "}} {{ trigger.now }}{{- "\n" -}}
            {%- endif -%}
            
            {%- if trigger.platform == "zone" -%}
            {{"trigger.zone: "}} {{ trigger.zone }}{{- "\n" -}}
            {%- endif -%}
            
            {%- if trigger.platform == "state" or trigger.platform == "numeric_state" or trigger.platform == "template" or trigger.platform == "zone" -%}
            {{"trigger.entity_id: "}} {{ trigger.entity_id }}{{- "\n" -}}            
            {{"trigger.from_state: "}} {{- "\n" -}}
            -------------------{{- "\n" -}}
            {{ dumpState("trigger.from_state", trigger.from_state) }} {{- "\n" -}}
            trigger.to_state:{{- "\n" -}}
            -----------------{{- "\n" -}}
            {{ dumpState("trigger.to_state", trigger.to_state) }}            
            {%- endif -%}
```            
