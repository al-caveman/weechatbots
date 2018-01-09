import weechat as wc
import re
import os

wc.register(
    'holybooks',
    'Al-Caveman <toraboracaveman [at] gmail [dot] com>',
    '0.0.0',
    'GPL3',
    'A bot that does holy things',
    '',
    ''
)

QURAN = os.path.expanduser('~/.weechat/python/quran/{}/{}.txt')
MAX_LEN = 200

def callback(data, signal, signal_data):
    wc.prnt('', signal)
    wc.prnt('', signal_data)

    network = signal.split(',')[0]
    channel = signal_data.split(' ')[2]
    nickname = signal_data[1:signal_data.find('!')]
    msg = ' '.join(signal_data.split(':')[2:])

    if re.match(r'^!quran[^\d]+\d+[^\d]+\d+$', msg) != None:
        sid, vid = re.split(r'[^\d]', msg)[-2:]
        wc.prnt('', str([sid, vid]))

        # load verse and send it
        with open(QURAN.format(sid, vid), 'r') as f:
            verse = f.read()

        if len(verse) > MAX_LEN:
            verse = verse[0:MAX_LEN].strip() + '... (cont)'

        response = 'quran {}:{}: {} https://quran.com/{}/{}'.format(
            sid, vid,
            verse, sid, vid
        )

        wc.hook_signal_send (
            'irc_input_send',
            wc.WEECHAT_HOOK_SIGNAL_STRING,
            '{};{};priority_low;;{}'.format(
                network,
                channel,
                response
            )
        )

    return wc.WEECHAT_RC_OK

wc.hook_signal('*,irc_in2_PRIVMSG', 'callback', '')
