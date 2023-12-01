#!/bin/env python3

import sys
import json
import matplotlib.pyplot as plt
import math
from datetime import datetime

# Check if filename is provided as argument
if len(sys.argv) < 2:
    print("Please provide the filename as an argument.")
    sys.exit(1)

# Get filename from command-line argument
filename = sys.argv[1]

# Read JSON data from file
try:
    with open(filename) as file:
        data = json.load(file)
except FileNotFoundError:
    print("File not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print("Invalid JSON format in the file.")
    sys.exit(1)

title = data["races"][0]["data"]["title"]
event_date = datetime.strptime(data["races"][0]["data"]["start_datetime"], "%Y-%m-%d %H:%M:%S").date()
print(title, event_date)

# Extract age and sex data from JSON
#ages = [person["age"] for race in data["races"] for person in race["persons"]]
birth_dates = [person["birth_date"] for race in data["races"] for person in race["persons"]]
ages = [(event_date - datetime.strptime(birth_date if birth_date is not None else str(event_date), "%Y-%m-%d").date()).days // 365 for birth_date in birth_dates]

def predict_sex(name):
    # Convert the name to lowercase for case-insensitivity
    name_lower = name.lower()

    # Check for common female name endings
    if name_lower.endswith('а') or name_lower.endswith('я'):
        return 2
    else:
        return 1

sexes = []
for race in data["races"]:
    for person in race["persons"]:
        sex = person["sex"] 
        if sex == 0:
            sex = predict_sex(person["name"])
        sexes.append(sex)

# Count the number of occurrences for each age and sex combination
count_dict = {}
for age, sex in zip(ages, sexes):
    if age < 0:
        continue
    age_group = math.floor(age/5)*5  # Group ages by 5-year intervals
    if (age_group, sex) in count_dict:
        count_dict[(age_group, sex)] += 1
    else:
        count_dict[(age_group, sex)] = 1

# Separate the counts by sex and age group
age_groups = sorted(list(set(age_group for age_group, _ in count_dict)))
male_counts = [count_dict[(age_group, 1)] if (age_group, 1) in count_dict else 0 for age_group in age_groups]
female_counts = [count_dict[(age_group, 2)] if (age_group, 2) in count_dict else 0 for age_group in age_groups]
mf_counts = [count_dict[(age_group, 0)] if (age_group, 0) in count_dict else 0 for age_group in age_groups]

persons_count = sum(male_counts) + sum(female_counts)

# Calculate percentages
if persons_count > 0:
    male_percentages = [(count/persons_count)*100 for count in male_counts]
    female_percentages = [(count/persons_count)*100 for count in female_counts]
if sum(mf_counts) > 0:
    mf_percentages = [(count/sum(mf_counts))*100 for count in mf_counts]

# Plotting the diagram
plt.figure(figsize=(10, 6))
bar_width = 2
if persons_count > 0:
    plt.bar([age_group - bar_width/2 for age_group in age_groups], male_percentages, bar_width,
            label='Male', color='blue', alpha=0.7)
    plt.bar([age_group + bar_width/2 for age_group in age_groups], female_percentages, bar_width,
            label='Female', color='purple', alpha=0.7)
else:
    persons_count = sum(mf_counts)
    plt.bar([age_group for age_group in age_groups], mf_percentages, bar_width,
            color='green', alpha=0.7)
plt.xlabel("Age Group")
plt.ylabel("%")
plt.title(f"Sex/Age Diagram ({title} {event_date})\nPersons: {persons_count}")
plt.xticks(age_groups)
plt.legend()
plt.grid(True)
plt.show()

