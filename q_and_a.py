#!/usr/bin/env python
# -*- coding: cp1252 -*-
"""This module is used for saving questions (together with 3 answers)
to a dummy db (namely a json file "questions.json") and then answering 
those questions.

It's a prime example of how to hard-code stuff.

Everything here is in romanian, and spelt wrong, so good luck! :)
"""
from __future__ import print_function
from __future__ import unicode_literals
import json
import os
import sys

if sys.version_info.major == 2:
    from Queue import Queue
else:
    from queue import Queue
    raw_input = input

QFILE = './questions.json'


def save(questions):
    with open(QFILE, 'wb') as f:
        f.write(json.dumps(questions).encode(sys.getfilesystemencoding()))


def supply_questions():
    exists = os.path.exists(QFILE)
    questions = {}
    if exists:
        with open(QFILE, 'rb') as thefile:
            questions = json.loads(thefile.read().decode(sys.getfilesystemencoding()))

    last_question_num = 1
    if questions:
        last_question_num = max((int(key) for key in questions.keys()))

    print(
        "Introdu intrebarea, da-i Enter, dupa care da-i A (mare sau mic)"
        "daca urmatorul raspuns e adevarat sau f mare sau mic daca e fals si "
        "ENTER, dupa care raspunsul, dupa care iar a/f, iar enter, iar "
        "raspunsul, si cand se termina raspunsurile la o intrebare dai n "
        "(mare sau mic), de la next. Cand vrei sa termini de introdus, dai "
        "q/Q (si daca n-ai introdus 3 raspunsuri, intrebarea nu se salveaza)")

    while True:
        answer = raw_input('\nquestion: ')
        questions[last_question_num + 1] = {'question': answer}
        truth, text = get_answer()
        questions[last_question_num + 1][1] = {'truth': truth, 'text': text}
        truth, text = get_answer()
        questions[last_question_num + 1][2] = {'truth': truth, 'text': text}
        truth, text = get_answer()
        questions[last_question_num + 1][3] = {'truth': truth, 'text': text}
        answer = ''
        while answer.lower() not in ['q', 'n']:
            answer = raw_input('q/n?')

        last_question_num += 1

        if answer == 'q':
            save(questions)
            break


def get_answer():
    answer = ''
    while answer.lower() not in ['a', 'f']:
        answer = raw_input('adevarat/fals? ')
    truth_value = answer.lower() == 'a'
    answer = raw_input('text: ')
    return truth_value, answer


def answer_questions():
    with open(QFILE, 'rb') as f:
        questions = json.loads(f.read().decode(sys.getfilesystemencoding()))

    q = Queue()

    questions_left = [(k, questions[str(k)]) for k in sorted([int(k_) for k_ in questions.keys()])]

    for question in questions_left:
        q.put(question)

    while not q.empty():
        question_tuple = q.get()
        question_num = question_tuple[0]
        print('\n\nIntrebarea {}. Mai ai {}'.format(question_num, q.qsize()))
        print(question_tuple[1]['question'])
        for answer_num in range(1, 4):
            print(answer_num, ' : ',
                  question_tuple[1][str(answer_num)]['text'])

        answer = ''
        while len(answer) != 3 or answer.lower().strip('af'):
            answer = raw_input('answer? ').strip()

        first_letter = 'a' if question_tuple[1]['1']['truth'] else 'f'
        second_letter = 'a' if question_tuple[1]['2']['truth'] else 'f'
        third_letter = 'a' if question_tuple[1]['3']['truth'] else 'f'

        actual_answer = ''.join((first_letter, second_letter, third_letter))

        if actual_answer != answer:
            print("GRESIIIIIT!!!! era {}".format(actual_answer))
            q.put(question_tuple)


MENU = {
    1: ("Introduceti intrebari/ raspunsuri", supply_questions),
    2: ("Raspundeti la intrebari", answer_questions),
    3: ("Inchideti", quit)
}


def main():
    while True:
        print('\n\n')
        for k, v in MENU.items():
            print(k, ':', v[0])

        answer = ''
        while answer.lower() not in [str(key) for key in MENU.keys()]:
            answer = raw_input('option: ')

        MENU[int(answer)][1]()


if __name__ == '__main__':
    main()

