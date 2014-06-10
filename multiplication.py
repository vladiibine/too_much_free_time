import sys
import os
import random
from datetime import datetime    

def multiplication(input_stream=sys.stdin, output_stream=sys.stdout, stats_log=sys.stdout, turn_size=20):
    counter = 1
    t0 = datetime.now()
    while True:
        num1 = random.randint(11, 99)
        num2 = random.randint(11, 99)
        result = ''
        while not result == num1*num2:
            result = get_user_result(input_stream, output_stream, "%s x %s = "% (num1, num2))
            if is_num(result):
                if int(result) == num1 * num2:
                    output_stream.write('yaaay!!'+os.linesep)
                    counter += 1
                    break
                else:
                    output_stream.write("sorry... try again!!"+os.linesep)
        if counter % turn_size == 0:
            tnow = datetime.now()
            stats_log.write(str(tnow - t0)+os.linesep)
            t0 = tnow

def is_num(string):
    return string.isalnum() and not string.isalpha()

def get_user_result(input_stream, output_stream, msg):
    output_stream.write(msg)
    output_stream.write(os.linesep)
    output_stream.flush()
    result = input_stream.readline().split(os.linesep)[0]
    return result
