#!/usr/bin/env python3

import sys
from random import randint

dictionary = []
limit = (-1, -1)

file_name = ""
report_file_name = ""

random_config = False
reverse_config = False
infinite_config = False

def shuffle_dictionary():
    for i in range(len(dictionary)):
        rand = randint(0, len(dictionary)-1)
        p = dictionary[i]
        dictionary[i] = dictionary[rand]
        dictionary[rand] = p


def read_words():
    f = open(file_name, "r")
    i = 0
    for worlds in read_lines(f):
        addw = worlds.split(",")
        w2 = []
        for w in addw:
            w2.append(w.strip())
        if limit[0] <= i + 1 and ( limit[1] == -1 or limit[1] >= i + 1):
            dictionary.append(w2)
        i += 1
    if random_config:
        shuffle_dictionary()

def read_lines(f):
    line = f.readline()
    while line:
        yield line
        line = f.readline()

def read_limit_from_string(limit):
    l = limit.split(":")
    return (int(l[0]) if l[0] else 0, int(l[1]) if l[1] else -1)

def read_options(argv):
    global random_config
    global reverse_config
    global file_name
    global limit
    global infinite_config
    global report_file_name
    n = len(argv)
    i = 0
    while i < n:
        if argv[i] == "--random" or argv[i] == "-s":
            random_config = True
        elif argv[i] == "--reverse" or argv[i] == "-r":
            reverse_config = True
        elif argv[i] == "--infinite" or argv[i] == "-i":
            infinite_config = True
        elif argv[i] == "--file" or argv[i] == "-f":
            file_name = argv[i + 1]
            i += 1
        elif argv[i] == "--limit" or argv[i] == "-l":
            limit = read_limit_from_string(argv[i+1])
            i += 1
        elif argv[i] == "--report-file" or argv[i] == "-rf":
            report_file_name = argv[i + 1]
            i += 1
        i += 1

def validate_options():
    if not file_name:
        raise Exception("Invalida file path")

def start_questions():
    wi = (0, 1) if not reverse_config else (1, 0)

    for line in get_dictionary():
        while True:
            translate = input(line[wi[0]] + " > ")
            if translate.strip() == "!":
                print("SKIP")
                report_message(line[wi[0]] + "," + line[wi[1]] + ",SKIP")
                break
            if translate.strip() == line[wi[1]].strip():
                print("OK")
                report_message(line[wi[0]] + "," + line[wi[1]] + ",OK")
                break
            else:
                report_message(line[wi[0]] + "," + line[wi[1]] + ",NOPE-" + translate.strip())
                print("NOPE")

def infinite_dictionary():
    while True:
        for line in dictionary:
            yield line
        if random_config:
            shuffle_dictionary()

def get_dictionary():
    return dictionary if not infinite_config else infinite_dictionary()

def report_message(message):
    if report_file_name:
        f = open(report_file_name, "a")
        f.write(message + "\n")
        f.close()

read_options(sys.argv)
validate_options()
read_words()
start_questions()
