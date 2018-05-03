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
CHANNELS_ACTIVE = [
    'freenode/#gentoo-chat-exile',
    #'freenode/##happylol',
]
SILENCE_LIMIT = 50
TRUTH = [
    "( ͡◉ ͜ʖ ͡◉)",
    "(╯°□°）╯︵ ┻━┻)",
    "┬─┬ノ(º _ ºノ)",
    "r: g. s.",
    "welp.",
    "G-d bless catholic priests.",
    "pacman is fast.",
    "pacman is good.",
    "i like pacman.",
    "reminder: imo gentoo devs r schwul.",
    "reminder: imo systemd is nice.",
    "reminder: imo arch is nice.",
    "reminder: imo gentoo is not nice.",
    "reminder: imo gentoo devs charlatans.",
    "reminder: imo opal is not nice.",
    "reminder: imo some gentoo devs need to enter this list: https://en.wikipedia.org/wiki/Charlatan#Infamous_individuals",
    "reminder: Khabib Abdulmanapovich Nurmagomedov is the undefeated undisputed champion of the flagship weight division of u.f.c. - allahuackbar.",
    """reminder: ``[pepe the frog] became an Internet meme when its popularity steadily grew across Myspace, Gaia Online and 4chan in 2008.''.""",
    """reminder: ``That is Jesus, the son of Mary - the word of truth about which they are in dispute.'' -- https://quran.com/19/34.""",
    """reminder: ``Say, "If the sea were ink for [writing] the words of my Lord, the sea would be exhausted before the words of my Lord were exhausted, even if We brought the like of it as a supplement."''.""",
    """reminder: ``He is Allah, other than whom there is no deity, the Sovereign, the Pure, the Perfection, the Bestower of Faith, the Overseer, the Exalted in Might, the Compeller, the Superior. Exalted is Allah above whatever they associate with Him.''.""",
    """reminder: ``And your Lord has decreed that you not worship except Him, and to parents, good treatment. Whether one or both of them reach old age [while] with you, say not to them [so much as], "uff," and do not repel them but speak to them a noble word.''.""",
    """reminder: ``Satan only wants to cause between you animosity and hatred through intoxicants [sic. alcohol] and gambling and to avert you from the remembrance of Allah and from prayer. So will you not desist?''.""",
]
BYPASS_NICKS = [
#    'blop',
#    'blap',
#    'blop_',
#    'blap_',
]
BYPASS_PAUSE = 1


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
random.seed(time.time())
random.shuffle(TRUTH)
truth_i = 0
previous_chat_messages = {}


########################
#                      #
# func niggr wannabies #
#                      #
########################
def sendresponse(network, channel, response):
    wc.command('', '/msg -server {} {} {}'.format(
        network, channel, response
    ))

def educate(data, signal, signal_data):
    global truth_i
    global previous_chat_messages

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

    # channel i.d.
    chan_id = '{}/{}'.format(network,channel)

    # run only in supported channels
    if chan_id in CHANNELS_ACTIVE:
        # send truth only if enough shit was said
        if chan_id in previous_chat_messages:
            previous_chat_messages[chan_id] += 1
        else:
            previous_chat_messages[chan_id] = 1

        # reset counter if some bypass dude talks
        if nickname in BYPASS_NICKS:
            if previous_chat_messages[chan_id] > BYPASS_PAUSE:
                previous_chat_messages[chan_id] -= BYPASS_PAUSE

        if previous_chat_messages[chan_id] % SILENCE_LIMIT == 0:
            sendresponse(network, channel, TRUTH[truth_i % len(TRUTH)])
            truth_i += 1

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

    # channel i.d.
    chan_id = '{}/{}'.format(network,channel)

    # run only in supported channels
    if chan_id in CHANNELS_ACTIVE:
        previous_chat_messages[chan_id] = 0

    return wc.WEECHAT_RC_OK


########################
#                      #
#       hookers        #
#                      #
########################
wc.hook_signal('*,irc_in2_PRIVMSG', 'educate', '')
wc.hook_signal('*,irc_out_PRIVMSG', 'think', '')
