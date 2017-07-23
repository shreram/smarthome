## Ever wondered how to get all the Entity IDs and attributes of all those entities in one place? 
You've come to the right place!

Just copy and paste the following in the templates page of your HA to see all the entities and their attributes in one place in a well formatted way. To maintain the formatting to copy the output to a text file, please use Mozilla Firefox browser. 

The information is formatted in such a way, that it can be used to customize, create groups and views to manage your entities.

```
The following are the entities that are recognized by the Home Assistant:
Just add components in the components list below for additional entities.

{{ "_".ljust(90, "_") }}
{{ "Entity ID".ljust(50) }}{{ "Entity Name" }}
  {{ "Attribute Name".ljust(50) }}{{ "Attribute Value" }}

{% for item in states %}
{{ "_".ljust(90, "_") }}
{{ item.entity_id.ljust(50) }}
  {{ "State".ljust(50) }}: {{ item.state}}
  {{ "Domain".ljust(50) }}: {{ item.domain}}
  {{ "Object ID".ljust(50) }}: {{ item.object_id}}
  {{ "Last Updated".ljust(50) }}: {{ item.last_updated}}
  {{ "Last Changed".ljust(50) }}: {{ item.last_changed}}
{%- for attrib in item.attributes|sort() %}
{%- if attrib is defined %} 
  {{attrib.ljust(50)}}: {{ item.attributes[attrib] }} 
{%- endif %}
{%- endfor %}
{%- endfor %}
```
### If you just want to see the entities, and not the attributes, run the following script:

```
{{ "Entity ID".ljust(49) }}  {{ "Entity Name" }}
{{ "---------------------------------------------------------------"}}
{%- for item in states %}
{{ item.entity_id.ljust(50) }} {{ item.name }}
{%- endfor %}

```
