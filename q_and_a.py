#!/usr/bin/env python
# -*- coding: mbcs -*-
"""This module is used for saving questions (together with 3 answers)
to a dummy db (namely a json file "questions.json") and then answering 
those questions.
It's a prime example of how to hard-code stuff.
Everything here is in romanian, and spelt wrong, so good luck! :)

Also, i tried to deal with an issue where windows CMD refuses to print 
special characters. Couldn't do it so i just replaced them with ? signs
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
        answer = raw_input('\nquestion: ').decode(sys.stdin.encoding)
        questions[last_question_num + 1] = {'question': answer}
        truth, text = get_answer()
        questions[last_question_num + 1][1] = {'truth': truth, 'text': text}
        truth, text = get_answer()
        questions[last_question_num + 1][2] = {'truth': truth, 'text': text}
        truth, text = get_answer()
        questions[last_question_num + 1][3] = {'truth': truth, 'text': text}
        answer = ''
        while answer.lower() not in ['q', 'n']:
            answer = raw_input('q/n?').decode(sys.stdin.encoding)

        last_question_num += 1

        if answer == 'q':
            save(questions)
            break


def get_answer():
    answer = ''
    while answer.lower() not in ['a', 'f']:
        answer = raw_input('adevarat/fals? ')
    truth_value = answer.lower() == 'a'
    answer = raw_input('text: ').decode(sys.stdin.encoding)
    return truth_value, answer


def answer_questions():
    if os.path.exists(QFILE):
        with open(QFILE, 'rb') as f:
            questions = json.loads(f.read().decode(sys.getfilesystemencoding()))
    else:
	    questions = {}

    q = Queue()

    questions_left = [(k, questions[str(k)]) for k in sorted([int(k_) for k_ in questions.keys()])]

    for question in questions_left:
        q.put(question)

    while not q.empty():
        question_tuple = q.get()
        question_num = question_tuple[0]
        print('\n\nIntrebarea {}. Mai ai {}'.format(question_num, q.qsize()))
        #print("Now we're going to crash, but really quick, we had a: {}".format(type(question_tuple[1]['question'])))
        #print("If we try to print this ourselves:")
        #print(question_tuple[1]['question'])
        #import pdb; pdb.set_trace()
        print(killgremlins(question_tuple[1]['question']))
        for answer_num in range(1, 4):
            print(answer_num, ' : ',
                  killgremlins(question_tuple[1][str(answer_num)]['text']))

        answer = ''
        while len(answer) != 3 or answer.lower().strip('af'):
            answer = raw_input('answer? ').decode(sys.stdin.encoding).strip()

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
            answer = raw_input('option: ').decode(sys.stdin.encoding)

        MENU[int(answer)][1]()

import re

## small collection:
#~ cp1252 = {
    #~ # from http://www.microsoft.com/typography/unicode/1252.htm
    #~ u"\x80": u"\u20AC", # EURO SIGN
    #~ u"\x82": u"\u201A", # SINGLE LOW-9 QUOTATION MARK
    #~ u"\x83": u"\u0192", # LATIN SMALL LETTER F WITH HOOK
    #~ u"\x84": u"\u201E", # DOUBLE LOW-9 QUOTATION MARK
    #~ u"\x85": u"\u2026", # HORIZONTAL ELLIPSIS
    #~ u"\x86": u"\u2020", # DAGGER
    #~ u"\x87": u"\u2021", # DOUBLE DAGGER
    #~ u"\x88": u"\u02C6", # MODIFIER LETTER CIRCUMFLEX ACCENT
    #~ u"\x89": u"\u2030", # PER MILLE SIGN
    #~ u"\x8A": u"\u0160", # LATIN CAPITAL LETTER S WITH CARON
    #~ u"\x8B": u"\u2039", # SINGLE LEFT-POINTING ANGLE QUOTATION MARK
    #~ u"\x8C": u"\u0152", # LATIN CAPITAL LIGATURE OE
    #~ u"\x8E": u"\u017D", # LATIN CAPITAL LETTER Z WITH CARON
    #~ u"\x91": u"\u2018", # LEFT SINGLE QUOTATION MARK
    #~ u"\x92": u"\u2019", # RIGHT SINGLE QUOTATION MARK
    #~ u"\x93": u"\u201C", # LEFT DOUBLE QUOTATION MARK
    #~ u"\x94": u"\u201D", # RIGHT DOUBLE QUOTATION MARK
    #~ u"\x95": u"\u2022", # BULLET
    #~ u"\x96": u"\u2013", # EN DASH
    #~ u"\x97": u"\u2014", # EM DASH
    #~ u"\x98": u"\u02DC", # SMALL TILDE
    #~ u"\x99": u"\u2122", # TRADE MARK SIGN
    #~ u"\x9A": u"\u0161", # LATIN SMALL LETTER S WITH CARON
    #~ u"\x9B": u"\u203A", # SINGLE RIGHT-POINTING ANGLE QUOTATION MARK
    #~ u"\x9C": u"\u0153", # LATIN SMALL LIGATURE OE
    #~ u"\x9E": u"\u017E", # LATIN SMALL LETTER Z WITH CARON
    #~ u"\x9F": u"\u0178", # LATIN CAPITAL LETTER Y WITH DIAERESIS
#~ }


## bigger collection:
cp1252 = {

    u"\x80": u"\u20AC",    #            e282ac
    u"\x81": u"\uFFFD",    #    `   ?    efbfbd
    u"\x82": u"\u201A",    #            e2809a
    u"\x83": u"\u0192",    #    à   à   c692
    u"\x84": u"\u201E",    #    G   G   e2809e
    u"\x85": u"\u2026",    #    Š   Š   e280a6
    u"\x86": u"\u2020",    #    O   O   e280a0
    u"\x87": u"\u2021",    #    ?   ?   e280a1
    u"\x88": u"\u02C6",    #    ?   ?   cb86
    u"\x89": u"\u2030",    #    ?   ?   e280b0
    u"\x8a": u"\u0160",    #    ?   ?   c5a0
    u"\x8b": u"\u2039",    #    ?   ?   e280b9
    u"\x8c": u"\u0152",    #    ?   ?   c592
    u"\x8d": u"\uFFFD",    #    ?   ?    efbfbd
    u"\x8e": u"\u017D",    #    ?   ?   c5bd
    u"\x8f": u"\uFFFD",    #    ?   ?    efbfbd
    u"\x90": u"\uFFFD",    #    ?   ?    efbfbd
    u"\x91": u"\u2018",    #    ?   ?   e28098
    u"\x92": u"\u2019",    #    ?   ?   e28099
    u"\x93": u"\u201C",    #    ?   ?   e2809c
    u"\x94": u"\u201D",    #    ?   ?   e2809d
    u"\x95": u"\u2022",    #    ?   ?   e280a2
    u"\x96": u"\u2013",    #    ?   ?   e28093
    u"\x97": u"\u2014",    #    ?   ?   e28094
    u"\x98": u"\u02DC",    #    ?   ?   cb9c
    u"\x99": u"\u2122",    #    ?   ?   e284a2
    u"\x9a": u"\u0161",    #    ?   ?   c5a1
    u"\x9b": u"\u203A",    #    ?   ?   e280ba
    u"\x9c": u"\u0153",    #    ?   ?   c593
    u"\x9d": u"\uFFFD",    #    ?   ?    efbfbd
    u"\x9e": u"\u017E",    #    ?   ?   c5be
    u"\x9f": u"\u0178",    #    ?   ?   c5b8
    u"\xa0": u"\u00A0",    #             c2a0
    u"\xa1": u"\u00A1",    #    `   `   c2a1
    u"\xa2": u"\u00A2",    #            c2a2
    u"\xa3": u"\u00A3",    #    à   à   c2a3
    u"\xa4": u"\u00A4",    #    G   G   c2a4
    u"\xa5": u"\u00A5",    #    Š   Š   c2a5
    u"\xa6": u"\u00A6",    #    O   O   c2a6
    u"\xa7": u"\u00A7",    #    ?   ?   c2a7
    u"\xa8": u"\u00A8",    #    ?   ?   c2a8
    u"\xa9": u"\u00A9",    #    ?   ?   c2a9
    u"\xaa": u"\u00AA",    #    ?   ?   c2aa
    u"\xab": u"\u00AB",    #    ?   ?   c2ab
    u"\xac": u"\u00AC",    #    ?   ?   c2ac
    u"\xad": u"\u00AD",    #    ?   ?   c2ad
    u"\xae": u"\u00AE",    #    ?   ?   c2ae
    u"\xaf": u"\u00AF",    #    ?   ?   c2af
    u"\xb0": u"\u00B0",    #    ?   ?   c2b0
    u"\xb1": u"\u00B1",    #    ?   ?   c2b1
    u"\xb2": u"\u00B2",    #    ?   ?   c2b2
    u"\xb3": u"\u00B3",    #    ?   ?   c2b3
    u"\xb4": u"\u00B4",    #    ?   ?   c2b4
    u"\xb5": u"\u00B5",    #    ?   ?   c2b5
    u"\xb6": u"\u00B6",    #    ?   ?   c2b6
    u"\xb7": u"\u00B7",    #    ?   ?   c2b7
    u"\xb8": u"\u00B8",    #    ?   ?   c2b8
    u"\xb9": u"\u00B9",    #    ?   ?   c2b9
    u"\xba": u"\u00BA",    #    ?   ?   c2ba
    u"\xbb": u"\u00BB",    #    ?   ?   c2bb
    u"\xbc": u"\u00BC",    #    ?   ?   c2bc
    u"\xbd": u"\u00BD",    #    ?   ?   c2bd
    u"\xbe": u"\u00BE",    #    ?   ?   c2be
    u"\xbf": u"\u00BF",    #    ?   ?   c2bf
    u"\xc0": u"\u00C0",    #            c380
    u"\xc1": u"\u00C1",    #    `   `   c381
    u"\xc2": u"\u00C2",    #            c382
    u"\xc3": u"\u00C3",    #    à   à   c383
    u"\xc4": u"\u00C4",    #    G   G   c384
    u"\xc5": u"\u00C5",    #    Š   Š   c385
    u"\xc6": u"\u00C6",    #    O   O   c386
    u"\xc7": u"\u00C7",    #    ?   ?   c387
    u"\xc8": u"\u00C8",    #    ?   ?   c388
    u"\xc9": u"\u00C9",    #    ?   ?   c389
    u"\xca": u"\u00CA",    #    ?   ?   c38a
    u"\xcb": u"\u00CB",    #    ?   ?   c38b
    u"\xcc": u"\u00CC",    #    ?   ?   c38c
    u"\xcd": u"\u00CD",    #    ?   ?   c38d
    u"\xce": u"\u00CE",    #    ?   ?   c38e
    u"\xcf": u"\u00CF",    #    ?   ?   c38f
    u"\xd0": u"\u00D0",    #    ?   ?   c390
    u"\xd1": u"\u00D1",    #    ?   ?   c391
    u"\xd2": u"\u00D2",    #    ?   ?   c392
    u"\xd3": u"\u00D3",    #    ?   ?   c393
    u"\xd4": u"\u00D4",    #    ?   ?   c394
    u"\xd5": u"\u00D5",    #    ?   ?   c395
    u"\xd6": u"\u00D6",    #    ?   ?   c396
    u"\xd7": u"\u00D7",    #    ?   ?   c397
    u"\xd8": u"\u00D8",    #    ?   ?   c398
    u"\xd9": u"\u00D9",    #    ?   ?   c399
    u"\xda": u"\u00DA",    #    ?   ?   c39a
    u"\xdb": u"\u00DB",    #    ?   ?   c39b
    u"\xdc": u"\u00DC",    #    ?   ?   c39c
    u"\xdd": u"\u00DD",    #    ?   ?   c39d
    u"\xde": u"\u00DE",    #    ?   ?   c39e
    u"\xdf": u"\u00DF",    #    ?   ?   c39f
    u"\xe0": u"\u00E0",    #    ?  ?  c3a0
    u"\xe1": u"\u00E1",    #    ?  ?  c3a1
    u"\xe2": u"\u00E2",    #    ?  ?  c3a2
    u"\xe3": u"\u00E3",    #    ?  ?  c3a3
    u"\xe4": u"\u00E4",    #    ?  ?  c3a4
    u"\xe5": u"\u00E5",    #    ?  ?  c3a5
    u"\xe6": u"\u00E6",    #    ?  ?  c3a6
    u"\xe7": u"\u00E7",    #    ?  ?  c3a7
    u"\xe8": u"\u00E8",    #    ?  ?  c3a8
    u"\xe9": u"\u00E9",    #    ?  ?  c3a9
    u"\xea": u"\u00EA",    #    ?  ?  c3aa
    u"\xeb": u"\u00EB",    #    ?  ?  c3ab
    u"\xec": u"\u00EC",    #    ?  ?  c3ac
    u"\xed": u"\u00ED",    #    ??  ??  c3ad
    u"\xee": u"\u00EE",    #    ?  ?  c3ae
    u"\xef": u"\u00EF",    #    ?  ?  c3af
    u"\xf0": u"\u00F0",    #    ?? ?? c3b0
    u"\xf1": u"\u00F1",    #    ?? ?? c3b1
    u"\xf2": u"\u00F2",    #    ?? ?? c3b2
    u"\xf3": u"\u00F3",    #    ?? ?? c3b3
    u"\xf4": u"\u00F4",    #    ???? ???? c3b4
    u"\xf5": u"\u00F5",    #    ???? ???? c3b5
    u"\xf6": u"\u00F6",    #    ???? ???? c3b6
    u"\xf7": u"\u00F7",    #    ???? ???? c3b7
    u"\xf8": u"\u00F8",    #    ?? ?? c3b8
    u"\xf9": u"\u00F9",    #    ?? ?? c3b9
    u"\xfa": u"\u00FA",    #    ?? ?? c3ba
    u"\xfb": u"\u00FB",    #    ?? ?? c3bb
    u"\xfc": u"\u00FC",    #    ???? ???? c3bc
    u"\xfd": u"\u00FD",    #    ???? ???? c3bd
    u"\xfe": u"\u00FE",    #    ???? ???? c3be
    u"\xff": u"\u00FF",    #    ???? ???? c3bf

}	
	
def killgremlins(text):
    new_text = ''
    for character in text:
        if character in cp1252:
            new_text += cp1252[character]
        else:
            new_text += character
    return text.encode(sys.stdout.encoding, errors='replace')

if __name__ == '__main__':
    main()
