# Trigger Data in Templates

Ever wondered what trigger data is available for you when writing automations? Just copy the mqtt.publish service below 
and put it in **any** of your automation action section, and <b>it will dump all the attributes and information related to trigger, and state into your mqtt with a topic name "/dump/platform" </b>.

Pre-requisite is to have MQTT configured in your Home Assistant. Use tools like `mqttfx` to browse mqtt data.

Hope you find it useful!

```
  - alias: Test Kitchen Light
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
                {{- statePrefix ~ ".attributes." ~ attrib ~ ": " -}} {{- stateObj.attributes[attrib] -}}
                {{- "\n" -}}
                {%- endif -%}
              {%- endfor -%}
            {%- endmacro -%}
            
            {% set p = trigger.platform %}
            {{"trigger.platform: "}} {{ p }}{{- "\n" -}}
            
            {%- if p == "mqtt" -%}
            {{"trigger.topic: "}} {{ trigger.topic }}{{- "\n" -}}
            {{"trigger.payload: "}} {{ trigger.payload }}{{- "\n" -}}
            {{"trigger.payload_json: "}} {{ trigger.payload_json }}{{- "\n" -}}
            {{"trigger.qos: "}} {{ trigger.qos }}{{- "\n" -}}
            {%- endif -%}
            
            {%- if p == "event" or p == "sun" or p == "zone" -%}
            {{"trigger.event: "}} {{ trigger.event }}{{- "\n" -}}
            {%- endif -%}
            
            {%- if p == "numeric_state" -%}
            {{"trigger.above: "}} {{ trigger.above }}{{- "\n" -}}
            {{"trigger.below: "}} {{trigger.below }}{{- "\n" -}}
            {%- endif -%}
            
            {%- if p == "state" -%}
            {{"trigger.for: "}} {{ trigger.for }}{{- "\n" -}}
            {%- endif -%}
            
            {%- if p == "time" -%}
            {{"trigger.now: "}} {{ trigger.now }}{{- "\n" -}}
            {%- endif -%}
            
            {%- if p == "zone" -%}
            {{"trigger.zone: "}} {{ trigger.zone }}{{- "\n" -}}
            {%- endif -%}
            
            {%- if p == "state" or p == "numeric_state" or p == "template" or p == "zone" -%}
            {{"trigger.entity_id: "}} {{ trigger.entity_id }}{{- "\n" -}}{{- "\n" -}}
            {{"trigger.from_state: "}} {{- "\n" -}}
            -------------------{{- "\n" -}}
            {{ dumpState("trigger.from_state", trigger.from_state) }} {{- "\n" -}}
            trigger.to_state:{{- "\n" -}}
            -----------------{{- "\n" -}}
            {{ dumpState("trigger.to_state", trigger.to_state) }}            
            {%- endif -%}
```

To add the same to logbook instead of MQTT, use the following code:

```


1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66

- alias: Test Kitchen Light
    trigger:
      platform: state
      entity_id: light.dinette
    action:
    - service: logbook.log
      data_template:
        name: "Dump of {{ trigger.platform }}"	
          message: >-
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
                {{- statePrefix ~ ".attributes." ~ attrib ~ ": " -}} {{- stateObj.attributes[attrib] -}}
                {{- "\n" -}}
                {%- endif -%}
              {%- endfor -%}
            {%- endmacro -%}
            
            {% set p = trigger.platform %}
            {{"trigger.platform: "}} {{ p }}{{- "\n" -}}
            
            {%- if p == "mqtt" -%}
            {{"trigger.topic: "}} {{ trigger.topic }}{{- "\n" -}}
            {{"trigger.payload: "}} {{ trigger.payload }}{{- "\n" -}}
            {{"trigger.payload_json: "}} {{ trigger.payload_json }}{{- "\n" -}}
            {{"trigger.qos: "}} {{ trigger.qos }}{{- "\n" -}}
            {%- endif -%}
            
            {%- if p == "event" or p == "sun" or p == "zone" -%}
            {{"trigger.event: "}} {{ trigger.event }}{{- "\n" -}}
            {%- endif -%}
            
            {%- if p == "numeric_state" -%}
            {{"trigger.above: "}} {{ trigger.above }}{{- "\n" -}}
            {{"trigger.below: "}} {{trigger.below }}{{- "\n" -}}
            {%- endif -%}
            
            {%- if p == "state" -%}
            {{"trigger.for: "}} {{ trigger.for }}{{- "\n" -}}
            {%- endif -%}
            
            {%- if p == "time" -%}
            {{"trigger.now: "}} {{ trigger.now }}{{- "\n" -}}
            {%- endif -%}
            
            {%- if p == "zone" -%}
            {{"trigger.zone: "}} {{ trigger.zone }}{{- "\n" -}}
            {%- endif -%}
            
            {%- if p == "state" or p == "numeric_state" or p == "template" or p == "zone" -%}
            {{"trigger.entity_id: "}} {{ trigger.entity_id }}{{- "\n" -}}{{- "\n" -}}
            {{"trigger.from_state: "}} {{- "\n" -}}
            -------------------{{- "\n" -}}
            {{ dumpState("trigger.from_state", trigger.from_state) }} {{- "\n" -}}
            trigger.to_state:{{- "\n" -}}
            -----------------{{- "\n" -}}
            {{ dumpState("trigger.to_state", trigger.to_state) }}            
            {%- endif -%%
```
