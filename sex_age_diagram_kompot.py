#!/bin/env python3

import sys
import matplotlib.pyplot as plt
import math
from datetime import datetime
import re
from bs4 import BeautifulSoup

# Check if filename is provided as argument
if len(sys.argv) < 3:
    print("Please provide the filename as an argument.")
    sys.exit(1)

# Get filename from command-line argument
filename = sys.argv[1]
title = sys.argv[2]

# Read HTML content from file
try:
    with open(filename) as file:
        html_content = file.read()
except FileNotFoundError:
    print("File not found.")
    sys.exit(1)

# Create a BeautifulSoup object to parse the HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Find all <tr> elements with class "r0" or "r1"
tr_elements = soup.find_all('tr', class_=re.compile(r'r[01]'))

ages = []
sexes = []

# Iterate over the matching <tr> elements
for tr_element in tr_elements:
    # Find all <td> elements within the <tr> element
    td_elements = tr_element.find_all('td')

    # Extract the values from the <td> elements
    value_1 = td_elements[2].text.strip()  # Extract sex
    value_2 = td_elements[3].text.strip()  # Extract age

    sexes.append(value_1)
    ages.append(int(value_2))

# Count the number of occurrences for each age and sex combination
count_dict = {}
for age, sex in zip(ages, sexes):
    age_group = math.floor(age/5)*5  # Group ages by 5-year intervals
    if (age_group, sex) in count_dict:
        count_dict[(age_group, sex)] += 1
    else:
        count_dict[(age_group, sex)] = 1

# Separate the counts by sex and age group
age_groups = sorted(list(set(age_group for age_group, _ in count_dict)))
male_counts = [count_dict[(age_group, 'М')] if (age_group, 'М') in count_dict else 0 for age_group in age_groups]
female_counts = [count_dict[(age_group, 'Ж')] if (age_group, 'Ж') in count_dict else 0 for age_group in age_groups]

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
plt.title(f"Sex/Age Diagram ({title})\nPersons: {persons_count}")
plt.xticks(age_groups)
plt.legend()
plt.grid(True)
plt.show()

