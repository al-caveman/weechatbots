import requests
import os
import sys

try:
    sorah = int(sys.argv[1])
    verses = range(1,1000)
except:
    sys.stderr.write('syntax error: {} <SORAH_ID>\n')
    sys.exit(1)

sys.stderr.write('fetching sorah {}:'.format(sorah))
sys.stderr.flush()
os.mkdir('{}'.format(sorah))
for v in verses:
    sys.stderr.write(' {}'.format(v))
    sys.stderr.flush()
    r = requests.get('https://quran.com/{}/{}'.format(sorah,v))
    if r.text.find('Ayah is out of range.') == -1:
        lol = r.text.split('</small></h2></div')
        lmfao = lol[0].split('">')
        ok = lmfao[-1]
    else:
        break

    with open('{}/{}.txt'.format(sorah,v), 'w') as f:
        f.write(ok)
sys.stderr.write('\n')
sys.stderr.flush()
