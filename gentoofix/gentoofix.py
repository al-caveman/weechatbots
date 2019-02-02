# coding=utf8
import weechat as wc
import re
import os
import random
import time


######################
#                    #
# constant wannabies #
#                    #
######################
BUFFERS_ACTIVE = [
    'irc.freenode.#gentoo-chat-exile',
]
SILENCE_LIMIT = 100
TRUTH = [
    "( ͡◉ ͜ʖ ͡◉)",
    "reminder: emerge is not good (╯°□°）╯︵ ┻━┻).",
    "reminder: pacman is good ┬─┬ノ(º _ ºノ).",
]
BYPASS_NICKS = [
#    'blop',
#    'blap',
#    'blop_',
#    'blap_',
]
BYPASS_PAUSE = 1
TOPIC_DELAY = 5 # seconds


########################
#                      #
# global var wannabies #
#                      #
########################
wc.register(
    'gentoofix',
    'Al-Caveman <toraboracaveman [at] protonmail [dot] com>',
    '0.0.1',
    'GPL3',
    'A bot that exposes the gentoo scam',
    '',
    ''
)
#random.seed(time.time())
#random.shuffle(TRUTH)
truth_i = 0
previous_chat_messages = {}
iscorvus = {
    'MrReader' : True,
    'Mr_Reader' : True,
    'Inst':True
}
last_approved_topic = ''
todos = {}


########################
#                      #
# func niggr wannabies #
#                      #
########################
def sendresponse(network, channel, response):
    wc.command('', '/msg -server {} {} {}'.format(
        network, channel, response
    ))

def settopic(buff_id, channel, topic):
    buff_ptr = wc.buffer_search('==', buff_id)
    if topic == '':
        topic = '-delete'
    wc.command(buff_ptr, '/topic {} {}'.format(
        channel, topic
    ))

def educate(data, signal, signal_data):
    global truth_i
    global previous_chat_messages
    global todos

    # parse input messages
    network, event = signal.split(',')
    m_signal_data = re.match(
        r'^:(?P<nickname>\S+)!\S+ PRIVMSG (?P<channel>\S+) :(?P<msg>.*)$',
        signal_data
    )
    nickname = m_signal_data.groupdict()['nickname']
    channel = m_signal_data.groupdict()['channel']
    msg = m_signal_data.groupdict()['msg']
    msg = msg.lower()

    # buffer i.d.
    buff_id = 'irc.{}.{}'.format(network,channel)

    # run only in supported buffers
    if buff_id in BUFFERS_ACTIVE:
        # send truth only if enough shit was said
        if buff_id in previous_chat_messages:
            previous_chat_messages[buff_id] += 1
        else:
            previous_chat_messages[buff_id] = 1

        # reset counter if some bypass dude talks
        if nickname in BYPASS_NICKS:
            if previous_chat_messages[buff_id] > BYPASS_PAUSE:
                previous_chat_messages[buff_id] -= BYPASS_PAUSE

        if previous_chat_messages[buff_id] % SILENCE_LIMIT == 0:
            todos['educate'] = (network, channel, TRUTH[truth_i % len(TRUTH)])
            truth_i += 1

    return wc.WEECHAT_RC_OK

def topic(data, signal, signal_data):
    global iscorvus
    global last_approved_topic
    global todos

    # parse input messages
    network, event = signal.split(',')
    m_signal_data = re.match(
        r'^:(?P<nickname>\S+)!(?P<username>\S+)@(?P<host>\S+) '
        r'\S+ (?P<channel>\S+) :(?P<topic>.*)$',
        signal_data
    )
    nickname = m_signal_data.groupdict()['nickname']
    username = m_signal_data.groupdict()['username']
    host     = m_signal_data.groupdict()['host']
    channel  = m_signal_data.groupdict()['channel']
    topic    = m_signal_data.groupdict()['topic']
    nickname = nickname.lower()
    username = username.lower()
    host     = host.lower()
    channel  = channel.lower()

    # buffer i.d.
    buff_id = 'irc.{}.{}'.format(network,channel)

    # act only in supported buffers
    if buff_id in BUFFERS_ACTIVE:
        # extend definitions of corvus
        if (
            nickname in iscorvus
            or username in iscorvus
            or host in iscorvus
        ):
            iscorvus[nickname] = True
            iscorvus[username] = True
            iscorvus[host]     = True

        # undo topic only if corvus changed it
        if nickname in iscorvus:
            todos['topic'] = (buff_id, channel, last_approved_topic)
        else:
            if topic.lower().find('caveman') == -1:
                last_approved_topic = topic
                todos['topic'] = None
            else:
                todos['topic'] = (buff_id, channel, last_approved_topic)
    return wc.WEECHAT_RC_OK

def think(data, signal, signal_data):
    global previous_chat_messages

    # parse input messages
    network, event = signal.split(',')
    m_signal_data = re.match(
        r'^PRIVMSG (?P<channel>\S+) :(?P<msg>.*)$',
        signal_data
    )
    channel = m_signal_data.groupdict()['channel']
    msg = m_signal_data.groupdict()['msg']
    msg = msg.lower()

    # buffer i.d.
    buff_id = 'irc.{}.{}'.format(network,channel)

    # run only in supported buffers
    if buff_id in BUFFERS_ACTIVE:
        previous_chat_messages[buff_id] = 0

    return wc.WEECHAT_RC_OK

def housekeeping(data, remaining_calls):
    global todos

    for job in todos:
        # process job
        if job == 'topic':
            if todos[job] is not None:
                buff_id, channel, topic_clean = todos[job]
                settopic(buff_id, channel, topic_clean)
        elif job == 'educate':
            if todos[job] is not None:
                network, channel, msg = todos[job]
                sendresponse(network, channel, msg)

        # mark job as done
        todos[job] = None

    return wc.WEECHAT_RC_OK


########################
#                      #
#       hookers        #
#                      #
########################
wc.hook_signal('*,irc_in2_PRIVMSG', 'educate', '')
#wc.hook_signal('*,irc_in_TOPIC', 'topic', '')
wc.hook_signal('*,irc_out_PRIVMSG', 'think', '')
wc.hook_timer(int(TOPIC_DELAY * 1000), 0, 0, "housekeeping", "")
