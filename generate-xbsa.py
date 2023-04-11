#!/usr/bin/python3

from datetime import datetime
from jinja2 import Environment, FileSystemLoader

import yaml

with open("xbsa-checklist.yml", encoding="utf-8") as yml:
    xbsa_checklist = yaml.safe_load(yml)

with open("status-bsa.yml", encoding="utf-8") as yml:
    status_bsa = yaml.safe_load(yml)

with open("status-sbsa.yml", encoding="utf-8") as yml:
    status_sbsa = yaml.safe_load(yml)


def handle_checklist():

    checklist = []

    for category in xbsa_checklist:
        category_name = category.split('-')[1]
        for group in xbsa_checklist[category]["groups"]:
            group_name = group.split('-')[1]
            for rule in xbsa_checklist[category]["groups"][group]["rules"]:
                checklist.append({
                    'category': category_name,
                    'group': group_name,
                    'tag': rule["tag"],
                    'bsa': rule["required"]["bsa"],
                    'sbsa': rule["required"]["sbsa"],
                    'tests': rule["tests"]
                })

    return checklist

def generate_html_file(checklist):

    file_loader = FileSystemLoader("templates")
    env = Environment(loader=file_loader,
                      trim_blocks=True,
                      lstrip_blocks=True)

    template = env.get_template("bsa-sbsa.html.j2")

    output = template.render(
        generate_time=datetime.strftime(datetime.utcnow(), "%d %B %Y %H:%M"),
        checklist=checklist,
        status_bsa=status_bsa,
        status_sbsa=status_sbsa,
    )
    print(output)


if __name__ == "__main__":
    checklist = handle_checklist()
    generate_html_file(checklist)
