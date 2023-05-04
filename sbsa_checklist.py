import yaml

with open("sbsa_checklist.yml", encoding="utf-8") as yml:
    sbsa_level_checklist = yaml.safe_load(yml)
