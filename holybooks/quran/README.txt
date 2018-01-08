english-translated quran verses are structured as follows X/Y.txt, where X is
the sorah identifier, and Y is the verse identifier. e.g. 1/3.txt is the 3rd
verse in the 1st sorah.

to fetch sorah, say 5, from quran.com:
    python fetch_quran.com.py 5

to fetch all sorahs (from 1 to 114), with 30 concurrent jobs:
    parallel -j30 python fetch_quran.com.py ::: (seq 1 114)

todo: currently fetch_quran.com.py only fetches the default translation. i
personally think the translation by dr. ghali (iirc) is the one that i tend to
find closest to the arabic text. but i think quran.com sets translator via
cookies (not sure; i just didn't see it in url), and hence i gave up and
collected default one.
