import weechat as wc

wc.register(
    'alpolice',
    'Al-Caveman <toraboracaveman [at] gmail [dot] com>',
    '0.0.0',
    'GPL3',
    'A bot to police offenders',
    '',
    ''
)

i = 0
halal_topic = [
    "a halal penis might be small, but is -nonetheless- ripe",
    "allah trumps all, but none trump allah (subhanallah)",
    "plz book ur halal-n-ripe penis right now: www.muslimdating.com",
    "friendly sites: https://www.cair.com/ http://www.uscmo.org/ http://smallbutripepenis.com",
    "welp. 1-800-ISLAM",
    "welcome to ##halal2. for ##halal plz /join ##halal",
    "welcome to ##CC66MOMVAG",
    "welcome to ##Americanistan",
    "welcome to ##DisputedLandsOfNorthernMexico",
    "the little halal penis trumps the giant haram dick",
    "no. subhanallah (s.a.) plz",
    "nope. s.a.",
    "kosher + halal = best.",
    "CC66's sister",
    "CC66's mom",
    "CC66 is a pigfucker",
    "CC66 is homo",
    "CC66's father inseminated CC66's mom via his crusty nail shit",
]

def topic_cb(data, signal, signal_data):
    global i
    (host, command, channel) = signal_data.split()[0:3]

    # ban cc66 from changing topic anywhere possible
    if (
        host.lower().find('unaffiliated/cc66') != -1 or
        host.lower().find('gateway/web') != -1
    ):
        
        wc.hook_signal_send (
            'irc_input_send',
            wc.WEECHAT_HOOK_SIGNAL_STRING,
            'freenode;{};priority_low;;/topic {}'.format(
                channel,
                halal_topic[i % len(halal_topic)]
            )
        )
        i += 1

    return wc.WEECHAT_RC_OK

wc.hook_signal('*,irc_in2_topic', 'topic_cb', '')
