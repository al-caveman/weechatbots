import weechat as wc
import re
import os

wc.register(
    'holybooks',
    'Al-Caveman <toraboracaveman [at] gmail [dot] com>',
    '0.0.1',
    'GPL3',
    'A bot that does holy things',
    '',
    ''
)

MAX_LEN = 200
QURAN = os.path.expanduser('~/.weechat/python/quran')
BIBLE_KJV = os.path.expanduser('~/.weechat/python/bible/kjv')
BIBLE_KJV_BOOKS = sorted(os.listdir(BIBLE_KJV))
CHANNELS_ACTIVE = [
    'freenode/#gentoo-chat-exile',
    'freenode/##islam',
    'freesay/#freesay',
    'freenode/##happylol'
]
BOOK_FRIENDLY = {
    '1chron'   : '1-Chronicles',
    '1cor'     : '1-Corinthians',
    '1john'    : '1-John',
    '1kings'   : '1-Kings',
    '1peter'   : '1-Peter',
    '1sam'     : '1-Samuel',
    '1thes'    : '1-Thessalonians',
    '1tim'     : '1-Timothy',
    '2chron'   : '2-Chronicles',
    '2cor'     : '2-Corinthians',
    '2john'    : '2-John',
    '2kings'   : '2-Kings',
    '2peter'   : '2-Peter',
    '2sam'     : '2-Samuel',
    '2thes'    : '2-Thessalonians',
    '2tim'     : '2-Timothy',
    '3john'    : '3-John',
    'acts'     : 'Acts',
    'amos'     : 'Amos',
    'col'      : 'Colossians',
    'daniel'   : 'Daniel',
    'deut'     : 'Deuteronomy',
    'eccl'     : 'Ecclesiastes',
    'eph'      : 'Ephesians',
    'esther'   : 'Esther',
    'exodus'   : 'Exodus',
    'ezekiel'  : 'Ezekiel',
    'ezra'     : 'Ezra',
    'gal'      : 'Galatians',
    'genesis'  : 'Genesis',
    'habakkuk' : 'Habakkuk',
    'haggai'   : 'Haggai',
    'hebrews'  : 'Hebrews',
    'hosea'    : 'Hosea',
    'isaiah'   : 'Isaiah',
    'james'    : 'James',
    'jeremiah' : 'Jeremiah',
    'job'      : 'Job',
    'joel'     : 'Joel',
    'john'     : 'John',
    'jonah'    : 'Jonah',
    'joshua'   : 'Joshua',
    'jude'     : 'Jude',
    'judges'   : 'Judges',
    'lament'   : 'Lamentations',
    'lev'      : 'Leviticus',
    'luke'     : 'Luke',
    'malachi'  : 'Malachi',
    'mark'     : 'Mark',
    'matthew'  : 'Matthew',
    'micah'    : 'Micah',
    'nahum'    : 'Nahum',
    'nehemiah' : 'Nehemiah',
    'num'      : 'Numbers',
    'obadiah'  : 'Obadiah',
    'philemon' : 'Philemon',
    'philip'   : 'Philippians',
    'proverbs' : 'Proverbs',
    'psalms'   : 'Psalms',
    'rev'      : 'Revelation',
    'romans'   : 'Romans',
    'ruth'     : 'Ruth',
    'song'     : 'Song-of-Solomon',
    'titus'    : 'Titus',
    'zech'     : 'Zechariah',
    'zeph'     : 'Zephaniah'
}

def loadfile(p):
    with open(p, 'r') as f:
        verse = f.read()
    if len(verse) > MAX_LEN:
        verse = verse[0:MAX_LEN].strip() + '... (cont)'
    return verse

def sendresponse(network, channel, response):
    wc.command('', '/msg -server {} {} {}'.format(
        network, channel, response
    ))

def callback(data, signal, signal_data):
    # parse wtf
    network, event = signal.split(',')
    if event.find('in') >= 0:
        m_signal_data = re.match(
            #r'^:(?P<nickname>\S+).\S+ PRIVMSG (?P<channel>\S+) :(?P<msg>.*)$',
            r'^:(?P<nickname>\S+?)!\S+ PRIVMSG (?P<channel>\S+) :(?P<msg>.*)$',
            signal_data
        )
        nickname = m_signal_data.groupdict()['nickname']
    elif event.find('out') >= 0:
        m_signal_data = re.match(
            r'^PRIVMSG (?P<channel>\S+) :(?P<msg>.*)$',
            signal_data
        )
        nickname = wc.info_get('irc_nick', network)
    channel = m_signal_data.groupdict()['channel']
    msg = m_signal_data.groupdict()['msg']
    msg = msg.lower()

    # run only in supported channels
    if '{}/{}'.format(network,channel) not in CHANNELS_ACTIVE:
        return wc.WEECHAT_RC_OK

    # get book name
    m_book = re.match(r'^\.(?P<book>\w+)', msg)
    if m_book:
        book = m_book.groupdict()['book']
    else:
        book = None

    # handle the books
    if book == 'quran':
        m = re.match(
            r'^.\w+\W+(?P<sorah>\d+)\D+(?P<verse>\d+)',
            msg,
        )
        if m:
            sid = m.groupdict()['sorah']
            vid = m.groupdict()['verse']
            verse = loadfile('{}/{}/{}.txt'.format(QURAN, sid, vid))
            response = 'quran {}:{}: {} https://quran.com/{}/{}'.format(
                sid, vid,
                verse, sid, vid
            )
        else:
            response = (
                        '{}: syntax err. use .quran X:Y to pull the Yth '
                        'verse of the Xth sorah, where both X an Y are '
                        'natural numbers 1, 2, ....'.format(nickname)
                       )
        sendresponse(network, channel, response)

    elif book == 'bible':
        # make response
        response = (
            'use the syntax .BOOK CHAPTER:VERSE, where BOOK is one of '
            'the following: {}.'.format(' '.join(BIBLE_KJV_BOOKS))
        )

        # send help to pm
        sendresponse(network, nickname, response)

        # remind that pm is sent
        sendresponse(network, channel, '{}: help pmed to you.'.format(
            nickname
        ))

    elif book in BIBLE_KJV_BOOKS:
        m = re.match(
            r'^.\w+\W+(?P<chapter>\d+)\D+(?P<verse>\d+)',
            msg
        )
        if m:
            cid = m.groupdict()['chapter']
            vid = m.groupdict()['verse']
            verse = loadfile('{}/{}/{}/{}.txt'.format(
                BIBLE_KJV, book, cid, vid
            ))
            response = (
                '{} {}:{}: {} '
                'https://www.kingjamesbibleonline.org/{}-{}-{}/'.format(
                BOOK_FRIENDLY[book],
                cid, vid, verse,
                BOOK_FRIENDLY[book], cid, vid
            ))

        else:
            response = '{}: syntax err. .bible for help'.format(nickname)

        # send response
        sendresponse(network, channel, response)

    return wc.WEECHAT_RC_OK

wc.hook_signal('*,irc_in2_PRIVMSG', 'callback', '')
wc.hook_signal('*,irc_out_PRIVMSG', 'callback', '')
