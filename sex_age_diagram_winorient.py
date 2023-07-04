#!/bin/env python3

import sys
import matplotlib.pyplot as plt
import math
from datetime import datetime
import re
from bs4 import BeautifulSoup



# Check if filename is provided as argument
if len(sys.argv) < 4:
    print("Please provide the filename as an argument.")
    sys.exit(1)

# Get filename from command-line argument
filename = sys.argv[1]
title = sys.argv[2]
event_year = int(sys.argv[3])

# Read HTML content from file
try:
    with open(filename, 'r', encoding='cp1251') as file:
        html_content = file.read()
except FileNotFoundError:
    print("File not found.")
    sys.exit(1)

# Create a BeautifulSoup object to parse the HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Find all <h2> tags
h2_tags = soup.find_all('h2')

# Find all <pre> tags
pre_tags = soup.find_all('pre')

ages = []
sexes = []

# Iterate over the <h2> and <pre> tags together
for h2_tag, pre_tag in zip(h2_tags, pre_tags):
    # Extract sex from the <h2> tag
    sex = h2_tag.text[0]
    
    # Find all lines within the <pre> tag
    lines = pre_tag.text.strip().split('\n')
    
    # Iterate over the lines
    for line in lines[1:]:
        # Split the line into fields
        fields = line.split()
        
        # Extract the year of birth for each person
        year_of_birth = fields[-6]
        print(year_of_birth)
        if not year_of_birth.isdigit():
            year_of_birth = fields[-7]
            print(year_of_birth)
            if not year_of_birth.isdigit():
                year_of_birth = fields[-4]
                print(year_of_birth)
        year_of_birth = int(year_of_birth)
        if year_of_birth < 1900 or year_of_birth > event_year:
            continue
        age = event_year - year_of_birth
        ages.append(age)
        sexes.append(sex)
        
        # Print the sex and year of birth for each person
        print(f"Sex: {sex}, Year of Birth: {year_of_birth}")

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
plt.title(f"Sex/Age Diagram ({title} {event_year})\nPersons: {persons_count}")
plt.xticks(age_groups)
plt.legend()
plt.grid(True)
plt.show()



