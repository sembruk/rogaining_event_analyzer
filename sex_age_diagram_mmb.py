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

title = data["Raids"][0]["raid_name"]
event_date = datetime.strptime(title.split()[0], "%Y").date()
print(title, event_date)

# Extract age and sex data from JSON
birth_dates = [person["user_birthyear"] for person in data["Users"]]
ages = [(event_date - datetime.strptime(birth_date if birth_date is not None else str(event_date), "%Y").date()).days//365 for birth_date in birth_dates]
sexes = [int(person["user_sex"]) for person in data["Users"]]

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
male_counts = [count_dict[(age_group, 2)] if (age_group, 2) in count_dict else 0 for age_group in age_groups]
female_counts = [count_dict[(age_group, 1)] if (age_group, 1) in count_dict else 0 for age_group in age_groups]

persons_count = sum(male_counts) + sum(female_counts)

# Calculate percentages
male_percentages = [(count/persons_count)*100 for count in male_counts]
female_percentages = [(count/persons_count)*100 for count in female_counts]

# Plotting the diagram
plt.figure(figsize=(10, 6))
bar_width = 2
plt.bar([age_group - bar_width/2 for age_group in age_groups], male_percentages, bar_width,
        label='Male', color='blue', alpha=0.7)
plt.bar([age_group + bar_width/2 for age_group in age_groups], female_percentages, bar_width,
        label='Female', color='purple', alpha=0.7)
plt.xlabel("Age Group")
plt.ylabel("%")
plt.title(f"Sex/Age Diagram (ММБ {title} {event_date})\nPersons: {persons_count}")
plt.xticks(age_groups)
plt.legend()
plt.grid(True)
plt.show()

