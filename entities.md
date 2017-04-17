## Ever wondered how to get all the Entity IDs and attributes of all those entities in one place? 
You've come to the right place!

Just copy and paste the following in the templates page of your HA to see all the entities and their attributes in one place in a well formatted way.

The information is formatted in such a way, that it can be used to customize, create groups and views to manage your entities.

```
The following are the entities that are recognized by the Home Assistant:
Just add components in the components list below for additional entities.

{{ "_".ljust(90, "_") }}
{%- set domains = [states.light, states.switch, states.automation, states.device_tracker, states.group, states.media_player, states.proximity, states.script, states.zone, states.zwave, states.binary_sensor, states.sensor, states.calendar ] %}
{{ "Entity ID".ljust(50) }}{{ "Entity Name" }}
  {{ "Attribute Name".ljust(50) }}{{ "Attribute Value" }}
{%- for domain in domains -%}
{% for item in domain %}
{{ "_".ljust(90, "_") }}
{{ item.entity_id.ljust(50) }}
  {{ "State".ljust(50) }}: {{ item.state}}
  {{ "Domain".ljust(50) }}: {{ item.domain}}
  {{ "Object ID".ljust(50) }}: {{ item.object_id}}
  {{ "Last Updated".ljust(50) }}: {{ item.last_updated}}
  {{ "Last Changed".ljust(50) }}: {{ item.last_changed}}
{%- for attrib in item.attributes|sort() %}
{%- if attrib is defined %} 
  {{attrib.ljust(50)|replace("_", " ") |title}}: {{ item.attributes[attrib] }} 
{%- endif %}
{%- endfor %}
{%- endfor %}
{%- endfor %}

```
### If you just want to see the entities, and not the attributes, run the following script:

```
{%- set domains = [states.light, states.switch, states.automation, states.device_tracker, states.group, states.media_player, states.proximity, states.script, states.zone, states.zwave, states.binary_sensor, states.sensor, states.calendar ] %}

{{ "Entity ID".ljust(50) }}  {{ "Entity Name" }}

{%- for domain in domains %}
{% for item in domain %}
{{ item.entity_id.ljust(50) }} {{ item.name }}
{%- endfor %}
{%- endfor %}
```
