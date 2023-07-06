#!/bin/env python3

import sys
import json
import matplotlib.pyplot as plt
import math
from datetime import datetime

limit = 50
total_jsons = 1000

title = "GRUT"
event_date = "2021"

ages = []
sexes = []

# Read JSON data from file
for i in range(0, total_jsons, limit):
    filename = f'json_{i}.json'
    try:
        with open(filename) as file:
            data = json.load(file)
    except FileNotFoundError:
        print("File not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Invalid JSON format in the file.")
        sys.exit(1)

    ages.extend([person["age"] for course in data for person in course["interval"]["intervalResults"]])
    sexes.extend([person["gender"] for course in data for person in course["interval"]["intervalResults"]])

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
male_counts = [count_dict[(age_group, 'M')] if (age_group, 'M') in count_dict else 0 for age_group in age_groups]
female_counts = [count_dict[(age_group, 'F')] if (age_group, 'F') in count_dict else 0 for age_group in age_groups]

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
plt.title(f"Sex/Age Diagram ({title} {event_date})\nPersons: {persons_count}")
plt.xticks(age_groups)
plt.legend()
plt.grid(True)
plt.show()

