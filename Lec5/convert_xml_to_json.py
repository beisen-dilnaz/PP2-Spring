import re
import json

def xml_to_json(xml_string):
    xml_string = re.sub(r'<\?xml.*?\?>', '', xml_string, flags=re.DOTALL).strip()

    xml_string = re.sub(r'<(\w+)([^>]*)/>', r'<\1\2></\1>', xml_string)

    def tag_to_json(match):
        tag, content = match.groups()
        content = content.strip()

        content = content.replace('"', "'")

        if content == "":
            return f'"{tag}": null'

        if re.match(r'^-?\d+(\.\d+)?$', content):
            return f'"{tag}": {content}'

        return f'"{tag}": "{content}"'

    xml_string = re.sub(r'<(\w+)>(.*?)</\1>', tag_to_json, xml_string, flags=re.DOTALL)

    courses = re.findall(r'{(.*?)}', xml_string, flags=re.DOTALL)
    courses_json = "[" + ", ".join("{" + course + "}" for course in courses) + "]"

    json_string = '{ "courses": ' + courses_json + ' }'

    print("DEBUG: Generated JSON string before loading:\n", json_string)  

    try:
        json_data = json.loads(json_string)  
        return json.dumps(json_data, indent=4)
    except json.JSONDecodeError as e:
        print(" JSON Error:", e)
        return None  

with open("reed.xml", "r", encoding="utf-8") as file:
    xml_data = file.read()

json_output = xml_to_json(xml_data)

if json_output:
    with open("output.json", "w") as file:
        file.write(json_output)

    print(" Conversion complete! JSON saved as output.json")
else:
    print(" JSON conversion failed due to invalid structure.")