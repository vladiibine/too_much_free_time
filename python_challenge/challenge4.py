import requests

num = '63579'  # First one was 12345, then i had to divide this one by 2: 16044

for counter in range(410):
    resp = requests.get(
        'http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing=%s' %
        num)
    num = resp.content.split()[-1]
    print counter, resp.content