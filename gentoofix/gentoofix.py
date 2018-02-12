import weechat as wc
import re
import os

wc.register(
    'gentoofix',
    'Al-Caveman <toraboracaveman [at] gmail [dot] com>',
    '0.0.1',
    'GPL3',
    'A bot that exoses the gentoo scam',
    '',
    ''
)

CHANNELS_ACTIVE = [
    'freenode/#gentoo-chat-exile',
    #'freenode/##happylol',
]
SILENCE_LIMIT = 100
TRUTH = [
    "welp. here is a joke: gentoo. joke ended.",
    "gentoo makes sense only if compiling obsolete packages by obsolete compilers using unmaintainable python spaghetti (emerge) wraper, is what you want.",
    "gentoo sources are terribly outdated. they are not worth compiling. you will get superior optimization if you use non-obsolete source code",
    "gentoo is braindead. why should one spend hours compiling obsolete source code?",
    "what will you tell boss when your nuclear waste is leaking cause gentoo is waiting to hours to compile obsolete packages? ``hey boss sorry hold on gotta -O3 this sucker and i promise it will fix it all thanks to the power of -O3''",
    "you use gentoo, fail to exxplain how -march=native fixes the fact that you compile obsolete code, you claim that sharia is pedo while failing to support your claim against pubescent fuck... and now u suggest to gas germans for being saner than u and making superior bmws.",
    "gentoo's claim: if u spend hours compiling obsolete version of packages with -march=native, you are better than using a current release with -march=x86-64 --- b.s. i say",
    "yes. gentoo also uses binary packages, except that they are binary packages that their users compile, and by definition never tested before. worse: they always use old versions of gcc/llvm (obsolete compilers). worse: some packages are too outdated like they Qt",
    "the key problem with gentoo is that, unfortunately, they only ship obsolete packages. even many of their recent unstable packages lack. for example latest unstable Qt is 5.6 or 5.7. so in other words,",
    "one would expect that, after hours of compiling, gentoo would give u something worth it? nope! all obsolete crap!",
    "gentoo is obsolete.",
    "i mean, 'gentoo' is a hippie name. if this is not an obvious-enough about its obsoleteness, i don't know what is",
    "i mean. gentoo's logo is a purple goat. their official psychological customer support (#chat) is at best bad terrible. tell you to wait hours to compile obsolete version of packages. then they expect you to be happy? what is surprising is how was i blind for the past years? this is major-league magic we are dealing with. but inshallah i'll probaly start a campiagn www.gentooIsScam.com",
    "gentoo is rolling deprecated packages that also expects you to spend hours to compile obsolete code. totally crazy",
    "gentoo is obsolete. i see no merit in exporting gentoo on multiple kernels. it doesn't serve any purpose.",
    "reminder: gentoo would take about that time only to have 'emerge' (an obsolete undocumented python spaghetti) figure out what to do (let alone downloading, compiling, and installing). if that is not bad enough, please note this fact: you get obsoleted packages. yep, sometimes sucking more dick is not going to reward more.",
    "even if i fix emerge, and portage, the problem remains: gentoo ebuild maintainers love obsolete shit.",
    "gentoo's claim: if you spend hours compiling old versions of apps, then the binary you get will make you happy because compiling with -march=native will compensate for obsolete source code.",
    "reminder pz: gentoo is obsolete. #gentoo exists for recreational purposes.",
    "key gentoo issue: spending hours compiling with -march=native, will not solve the fact that your, both, compiler and app-to-build are obsolete. ",
    "i just wanted to say that, if u r using gentoo, and regretting not compiling with proper USE fags, then u actually have also a bigger problem: obsolete compiler. i think gentoo is still with gcc v5?",
    "gentoo's core is `emerge', an undocumented python spaghetti that only gets worse over time. yet, gentoo devs focus on creating init systems (openrc2) and mingling with upstream packages like upstream devs (e.g. qt). why don't they fix their emerge instead?",
    "well gentoo ppl r getting donations, plus the 'chosen' con artists (aka devs) get jobs after they lock their employers into the unmaintainable gentoo spaghetti to ensure their job security, and deepen the roots of their evil profit",
    "with gentoo (purple goat), you spend much more than 52 seconds to merely have emerge (an undocumented spaghetti of shit in python) figure out what it needs to do. let alone the hours spent compiling shit. let alone that, once you compile, you will necessarily have deprecated binaries (by definition)",
    "reminder: gentoo would take about that time only to have 'emerge' (an obsolete undocumented python spaghetti) figure out what to do (let alone downloading, compiling, and installing). if that is not bad enough, please note this fact: you get obsoleted packages. yep, sometimes sucking more dick is not going to reward more.",
    "gentoo is outrageously over-engineered with needless USE fags using a large spaghetti mess of scripts",
]

def sendresponse(network, channel, response):
    wc.command('', '/msg -server {} {} {}'.format(
        network, channel, response
    ))

truth_i = 0
previous_chat_messages = 0
def callback(data, signal, signal_data):
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

    # run only in supported channels
    if '{}/{}'.format(network,channel) not in CHANNELS_ACTIVE:
        return wc.WEECHAT_RC_OK

    # send truth only if enough shit was said
    previous_chat_messages += 1
    if previous_chat_messages % SILENCE_LIMIT == 0:
        sendresponse(network, channel, TRUTH[truth_i % len(TRUTH)])
        truth_i += 1

    return wc.WEECHAT_RC_OK

wc.hook_signal('*,irc_in2_PRIVMSG', 'callback', '')
