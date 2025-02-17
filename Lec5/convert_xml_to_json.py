import re
import json

def xml_to_json(xml_string):
    xml_string = re.sub(r'<\?xml.*?\?>', '', xml_string, flags=re.DOTALL).strip()
    xml_string = re.sub(r'<(\w+)([^>]*)/>', r'<\1\2></\1>', xml_string)

    course_blocks = re.findall(r'<course>(.*?)</course>', xml_string, flags=re.DOTALL)
    courses = []

    for course in course_blocks:
        course_dict = {}
        tags = re.findall(r'<(\w+)>(.*?)</\1>', course, flags=re.DOTALL)

        for tag, value in tags:
            value = value.strip().replace('"', "'")

            if tag == "time":
                time_tags = re.findall(r'<(\w+)>(.*?)</\1>', value, flags=re.DOTALL)
                value = {t[0]: t[1].strip() for t in time_tags}
            elif tag == "place":
                place_tags = re.findall(r'<(\w+)>(.*?)</\1>', value, flags=re.DOTALL)
                value = {p[0]: p[1].strip() for p in place_tags}
            elif value == "":
                value = None
            elif re.match(r'^-?\d+(\.\d+)?$', value):
                value = float(value) if '.' in value else int(value)

            course_dict[tag] = value

        courses.append(course_dict)

    json_data = {"courses": courses}

    return json.dumps(json_data, indent=4)

with open("reed.xml", "r", encoding="utf-8") as file:
    xml_data = file.read()

json_output = xml_to_json(xml_data)

if json_output:
    with open("output.json", "w") as file:
        file.write(json_output)
    print("Conversion complete! JSON saved as output.json")
else:
    print("JSON conversion failed due to invalid structure.")