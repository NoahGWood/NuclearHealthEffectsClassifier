#!/usr/bin/python3

""" main.py

	COPYRIGHT NOTICE:
    This classifier is based heavily on the breast cancer classifier described in Chapter 10 of
    'The Practice of Computing in Using Python, 3rd Edition' by William Punch & Richard Enbody.

    The creation of this software falls under 'Fair Use' for educational purposes. 
    
    The classifier source code was adapted by: Noah G. Wood
    At: College of Computer Science, Baker College
    For: COM1020: Composition & Critical Thinking II
    Instructor: Dr. Joseph Walker
    Date: August 3rd, 2022
    Contact: nwood10@baker.edu

    MODIFICATIONS COPYRIGHT NOTICE:
        (C) 2022 NOAH G. WOOD
        All modifications contributed to this source code, and any ideas expressed or implied
        are the property of Noah G. Wood who has granted a worldwide, non-revocable, non-exclusive
        license to freely use, remix, modify, distribute, sell, and enjoy this product to all
        persons in the hopes that it will be useful.

        This license is provided without any warranty express or implied as to the merchantability
        or fitness of this program for any particular purpose. DO NOT rely upon this software for
        determining the safety of ANY radiological or other hazard. This software is supplied for
        informational and theoretical purposes ONLY, it CAN NOT be relied upon for ANY safety critical
        applications.

        By using this software, YOU are agreeing to assume all risks and responsibilities associated
        with this software.

    Data Usage Acknowledgement:

    This report makes use of data obtained from the Radiation Effects Research Foundation (RERF),
    Hiroshima and Nagasaki, Japan. RERF is a private, non-profit foundation funded by the
    Japanese Ministry of Health, Labour and Welfare and the U.S. Department of Energy,
    the latter through the National Academy of Sciences.
    The conclusions in this report are those of the authors and do not necessarily reflect the
    scientific judgment of RERF or its funding agencies.
"""
import csv
import random


def sum_lists(list1, list2):
    """Element by element sums of two lists"""
    sums_list = []
    for i in range(len(list1)):
        sums_list.append(list1[i]+list2[i])
    return sums_list


def make_averages(sums_list, total_int):
    """Converts each list into an average by dividing the total."""
    averages_list = []
    for value in sums_list:
        if total_int == 0:
            total_int = 1
        averages_list.append(value/total_int)
    return averages_list


def make_triple_averages(list1, list2, list3):
    sums_list = []
    averages_list = []
    for i in range(list1):
        sums_list.append(list1[i]+list2[i]+list3[i])
    for value in sums_list:
        averages_list.append(value/3)


def Randomizer(filename):
    """Randomizer pulls a random number of lines randomly from a file and returns them."""
    lines = open(filename).read().splitlines()
    out_lines = []
    for i in range(random.randint(100, len(lines))):
        out_lines.append(random.choice(lines))
    if '/' in filename:
        filename = filename.split('/')[-1]
    with open('/tmp/' + filename, 'w+') as f:
        for line in out_lines:
            f.write(line)
            f.write('\n')
    return '/tmp/' + filename


def validate(row):
    if 'sex' not in row[1]:  # Exclude header row
        if float(row[20]) < 8000:  # Exclude long distances
            if float(row[21]) > 0.25:  # Exclude known safe doses of radiation
                return True
    return False


def make_training_set(file_name):
    # Initialize training_set_list
    set_list = []

    # open file
    lines = []
# Uncomment next line and comment following line to run with randomization
    with open(Randomizer(file_name), 'r') as f:
#    with open(file_name, 'r') as f:
        # Get the training data
        reader = csv.reader(f)
        # Collect everything,  but we will only use some of the values
        #   0 city,  1 sex, 2 un4gy, 3 nfact, 4 gdcat, 5 agxcat, 6 agecat, 7 dcat, 8 has86, 9 time, 10 PYR, 11 subjects,
        #   12  agex, 13 age, 14 year, 15 death, 16 cancer, 17 solid, 18 liquid, 19 leuk, 20 gdist, 21 skrt02t, 22 skrt02g,\
        #   23 skrt02n, 24 skrt86t, 25 skrt86g, 26 skrt86n, 27 cola02w10, 28 cola02g, 29 cola02n, 30 cola86w10,\
        #   31 cola86g, 32 cola86n,  33 mara02w10, 34 mara02g, 35 mara02n, 36 mara86w10, mara86g, mara86n,\
        #    36 trunc02, 37 trunc86, 38 adjust02, 39 adjust86
        for row in reader:
            if validate(row):
                # sex, deaths, cancer, solid, hema,  leukemia,  agex, age, gdist, skr02t, skrt02g, skrt02n, cola02w10, cola02g, cola02n, mara02w10, mara02g, mara02n
                a = bool(int(row[1])), float(row[15]), float(row[16]), float(row[17]), float(row[18]), float(row[19]), float(row[12]), float(row[13]), float(
                    row[21]), float(row[22]), float(row[23]), float(row[27]), float(row[28]), float(row[29]), float(row[33]), float(row[34]), float(row[35])
                set_list.append(a)
    return set_list


def train_classifier(training_set_list):
    survive_list = [0]*11
    survive_count = 0
    benign_list = [0]*11
    benign_count = 0
    death_list = [0]*11
    death_count = 0
    cancer_list = [0]*11
    cancer_count = 0
    solid_cancer_list = [0]*11  # Tumors
    solid_cancer_count = 0
    hema_cancer_list = [0]*11  # hematopoietic/liquid
    hema_cancer_count = 0
    leukemia_list = [0]*11
    leukemia_cancer_count = 0
    for patient_tuple in training_set_list:
        # Skip first entry [0] (boolean gender)
        if patient_tuple[1] < 1:
            # patient is not dead
            # Add to survive list
            survive_list = sum_lists(survive_list, patient_tuple[6:])
            survive_count += 1
            if patient_tuple[2] < 1:
                # Patient does not have cancer
                benign_list = sum_lists(benign_list, patient_tuple[6:])
                benign_count += 1
            else:
                # Add to cancer list
                cancer_list = sum_lists(cancer_list, patient_tuple[6:])
                cancer_count += 1
                if patient_tuple[3] > 1:
                    # Add to solid list
                    solid_cancer_list = sum_lists(
                        solid_cancer_list, patient_tuple[6:])
                    solid_cancer_count += 1
                if patient_tuple[4] > 1:
                    # Add to hema list
                    hema_cancer_list = sum_lists(
                        hema_cancer_list, patient_tuple[6:])
                    hema_cancer_count += 1
                if patient_tuple[5] > 1:
                    # Add to leukemia list
                    leukemia_list = sum_lists(
                        leukemia_list, patient_tuple[6:])
                    leukemia_cancer_count += 1
        else:
            # Add to death list
            death_list = sum_lists(death_list, patient_tuple[6:])
            death_count += 1
            if patient_tuple[2] > 1:
                # Patient has cancer
                # Add to cancer list
                cancer_list = sum_lists(cancer_list, patient_tuple[6:])
                cancer_count += 1
                if patient_tuple[3] > 1:
                    # Add to solid list
                    solid_cancer_list = sum_lists(
                        solid_cancer_list, patient_tuple[6:])
                    solid_cancer_count += 1
                if patient_tuple[4] > 1:
                    # Add to hematic list
                    hema_cancer_list = sum_lists(
                        hema_cancer_list, patient_tuple[6:])
                    hema_cancer_count += 1
                if patient_tuple[5] > 1:
                    # Add to leukemia list
                    leukemia_list = sum_lists(
                        leukemia_list, patient_tuple[6:])
                    leukemia_cancer_count += 1

    # Generate averages
    survive_averages = make_averages(survive_list, survive_count)
    death_averages = make_averages(death_list, death_count)
    cancer_averages = make_averages(cancer_list, cancer_count)
    benign_averages = make_averages(benign_list, benign_count)
    solid_cancer_average = make_averages(solid_cancer_list, solid_cancer_count)
    hema_cancer_average = make_averages(hema_cancer_list, hema_cancer_count)
    leukemia_cancer_average = make_averages(
        leukemia_list, leukemia_cancer_count)

    # Separator values for each attribute averages survival/death
    survival_classifier = make_averages(
        sum_lists(survive_averages, death_averages), 2)
    # Separator values for each attribute averages cancer/benign
    cancer_classifier = make_averages(sum_lists(benign_list, cancer_list), 2)
    # Separator values for each attribute averages solid/hema
    solid_cancer_classifier = make_averages(
        sum_lists(solid_cancer_list, benign_list), 2)
    # Separator values for each attribute averages hema/leukemia
    hema_cancer_classifier = make_averages(
        sum_lists(hema_cancer_list, benign_list), 2)
    # Separator values for each attribute averages solid/hema classifiers
    leukemia_cancer_classifier = make_averages(
        sum_lists(leukemia_list, benign_list), 2)
    return [survival_classifier, cancer_classifier, solid_cancer_classifier, hema_cancer_classifier, leukemia_cancer_classifier]


def classify_test_set_list(test_set_list, classifier_lists):
    """Given a test set list and a list of classifiers, classify each patient.
        Return with a list of classifiers."""
    result_list = []
    # For each patient in the set
    for patient_tuple in test_set_list:
        # print(patient_tuple)
        # For each attribute
        survive_count = 0
        death_count = 0
        cancer_count = 0
        benign_count = 0
        solid_cancer_count = 0
        hema_cancer_count = 0
        leukemia_cancer_count = 0
        # [survival_classifier, cancer_classifier, solid_cancer_classifier, hema_cancer_classifier, leukemia_cancer_classifier]
        for i in range(len(patient_tuple[6:])):
            # Check if survive
            if patient_tuple[i] > classifier_lists[0][i]:
                death_count += 1
            else:
                survive_count += 1
            # Check cancer
            if patient_tuple[i] > classifier_lists[1][i]:
                cancer_count += 1
                # Check cancer type
                if patient_tuple[i] > classifier_lists[2][i]:
                    solid_cancer_count += 1
                if patient_tuple[i] > classifier_lists[3][i]:
                    hema_cancer_count += 1
                if patient_tuple[i] > classifier_lists[4][i]:
                    leukemia_cancer_count += 1
            else:
                benign_count += 1
        # Create results tuple
        results_tuple = [patient_tuple[1:6], survive_count, death_count, cancer_count, benign_count, solid_cancer_count,
                         hema_cancer_count, leukemia_cancer_count]
        # append results tuple to results list
        result_list.append(results_tuple)
    # Return the list of results tuple
    return result_list


def report_results(result_list, pprint=True):
    total_count = 0
    inaccurate_count = 0
    inaccurate_cancer_count = 0
    inaccurate_hema_count = 0
    inaccurate_solid_count = 0
    inaccurate_leukemia_count = 0
    for result_tuple in result_list:
        survive_count, death_count, cancer_count, benign_count, solid_cancer_count,\
            hema_cancer_count, leukemia_cancer_count = result_tuple[1:]
        real_death, real_cancer, real_solid, real_hema, real_leukemia = result_tuple[0]
        if survive_count > death_count and real_death > 0:
            inaccurate_count += 1
        elif survive_count < death_count and real_death == 0:
            inaccurate_count += 1
        # Cancer Accuracy
        if cancer_count > benign_count and real_cancer == 0:
            inaccurate_cancer_count += 1
        elif cancer_count < benign_count and real_cancer > 0:
            inaccurate_cancer_count += 1
        # Solid cancer accuracy
        if solid_cancer_count > benign_count and real_solid == 0:
            inaccurate_solid_count += 1
        elif solid_cancer_count < benign_count and real_cancer > 0:
            inaccurate_solid_count += 1
        # Hematic cancer accuracy
        if hema_cancer_count > benign_count and real_hema == 0:
            inaccurate_hema_count += 1
        elif hema_cancer_count < benign_count and real_hema > 0:
            inaccurate_hema_count += 1
        # Leukemia cancer accuracy
        if leukemia_cancer_count > benign_count and real_leukemia == 0:
            inaccurate_leukemia_count += 1
        elif leukemia_cancer_count < benign_count and real_leukemia > 0:
            inaccurate_leukemia_count += 1
        total_count += 1
    survival_accuracy = (total_count - inaccurate_count)/total_count * 100
    cancer_accuracy = (total_count - inaccurate_cancer_count)/total_count * 100
    solid_accuracy = (total_count - inaccurate_solid_count)/total_count * 100
    hema_accuracy = (total_count - inaccurate_hema_count)/total_count * 100
    leuk_accuracy = (total_count - inaccurate_leukemia_count)/total_count * 100
    if pprint:
        print("Ionizing Radiation Survival Report: ")
        print("Of ", total_count, " patients, there were: ",
              inaccurate_count, " inaccuracies")
        print("Survival prediction accuracy: ", survival_accuracy, '%')
        print("Cancer prediction accuracy", cancer_accuracy, '%')
        print("Solid Cancer Prediction Accuracy: ", solid_accuracy, '%')
        print("Hematopoietic Cancer Prediction Accuracy", hema_accuracy, '%')
        print("Leukemia Cancer Prediction Accuracy", leuk_accuracy, '%')
        print("\nReported the results")
    else:
        out = [total_count, inaccurate_count, inaccurate_cancer_count,
               inaccurate_hema_count, inaccurate_solid_count, inaccurate_leukemia_count,
               survival_accuracy, cancer_accuracy, solid_accuracy, hema_accuracy, leuk_accuracy]
        with open('test_results.csv', 'a+') as f:
            f.write(",".join([str(x) for x in out]))
            f.write('\n')


def main():
    print("Reading in training data")
    training_file_name = 'data/DS02can.dat'
    training_set_list = make_training_set(training_file_name)
    print("Done reading training data in")

    print("Training classifier...")
    classifier_lists = train_classifier(training_set_list)
    print("Done training classifier")

    print("Writing weights to file")
    with open('weights', 'a+') as f:
        f.write(','.join([str(x) for x in classifier_lists]))
        f.write('\n')

    print("Reading in test data")
    test_file_name = 'data/DS02can.dat'
    test_set_list = make_training_set(test_file_name)
    print("Done reading test data")

    print("Classifying test data")
    result_list = classify_test_set_list(test_set_list, classifier_lists)
    print("Done classifying\n")

    report_results(result_list)

    print("Program finished")


def main_nop():
    training_file_name = 'data/DS02can.dat'
    training_set_list = make_training_set(training_file_name)
    classifier_lists = train_classifier(training_set_list)
    test_file_name = 'data/DS02can.dat'
    test_set_list = make_training_set(test_file_name)
    result_list = classify_test_set_list(test_set_list, classifier_lists)
    report_results(result_list, False)


if __name__ in '__main__':
    main()
    # Uncomment the following three lines to run testing.
#    trials = input("Number of trials to run: ")
#    for i in range(int(trials)):
#        main_nop()
