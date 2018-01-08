import requests
import os
import sys

sorahs = range(1,114+1)
verses = range(1,1000)

for s in sorahs:
    sys.stderr.write('fetching sorah {}:'.format(s))
    sys.stderr.flush()
    os.mkdir('{}'.format(s))
    for v in verses:
        sys.stderr.write(' {}'.format(v))
        sys.stderr.flush()
        r = requests.get('https://quran.com/{}/{}'.format(s,v))
        if r.text.find('Ayah is out of range.') == -1:
            lol = r.text.split('</small></h2></div')
            lmfao = lol[0].split('">')
            ok = lmfao[-1]
        else:
            break

        with open('{}/{}.txt'.format(s,v), 'w') as f:
            f.write(ok)
    sys.stderr.write('\n')
    sys.stderr.flush()
