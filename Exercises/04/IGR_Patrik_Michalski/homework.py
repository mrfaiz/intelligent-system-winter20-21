import csv
from copy import copy

with open("homework.csv", "r") as table1, \
     open("binned_homework.csv", "w", newline = '') as binned, \
     open("ir.txt", "w") as result:
    table_reader = csv.DictReader(table1)
    
    bin_data = []
    for row in table_reader:
        bin_data.append(row)

    temperatures = list(map(lambda x: int(x["temperature"]), bin_data))
 
    # Task A:

    # Discretize value range into 3 ordinal ranges.
    min_t = min(temperatures)
    max_t = max(temperatures)
    interval_size = (max_t - min_t) / 3

    # Assign binned ordinal values. Since the temperature values are
    # integers, border values are never directly reached, however, for proper
    # distinction, we make our bin value ranges open at the lower bound and
    # closed at the upper bound.
    for item in bin_data:
        section = (int(item["temperature"]) - min_t) / interval_size
        if section > 2:
            item["temperature"] = "high"
        elif section > 1:
            item["temperature"] = "medium"
        else:
            item["temperature"] = "low"

    # Store result in file.
    bin_write = csv.DictWriter(binned, ["outlook", "temperature", "humidity", "windy", "play"])
    bin_write.writeheader()

    for item in bin_data:
        bin_write.writerow(item)

    # Task B:
    # Use set to ignore duplicates.
    samples = set()

    # Create lookup dictionary for class count for sample.
    class_dict = {}

    # Hard coded number of possible values for class (2), for generalization,
    # the number of different values of the class field ought to be examined.
    for item in bin_data:
        sample = (item["outlook"], item["temperature"], item["humidity"], item["windy"])
        class_dict[sample] = [0, 0]
        
    # Count different occurences.
    for item in bin_data:
        if item["play"] == "yes":
            class_dict[(item["outlook"], item["temperature"], item["humidity"], item["windy"])][0] += 1
        else:
            class_dict[(item["outlook"], item["temperature"], item["humidity"], item["windy"])][1] += 1

    # Vector containing computed IZs for IR computation.
    izs = []

    # Write to text file for when $USER presents this, as helper notes.
    for sample in class_dict:
        iz = class_dict[sample][0] + class_dict[sample][1] - max(class_dict[sample])
        result.write("For sample " + str(sample) + " IZ is given by " + str(class_dict[sample][0] + class_dict[sample][1]) + " - " + \
             str(max(class_dict[sample])) + " = " + str(iz) + " with most frequent classification " + \
                  ("yes" if class_dict[sample][0] > class_dict[sample][1] else "no") + ".\n")
        izs.append(iz)

    # Additional IR result.
    result.write("Resulting in an IR value of " +  str(float(sum(izs)) / len(bin_data)) + ".")
