import difflib
import unicodedata

from fugashi import Tagger
from jaconv import jaconv


def _is_kanji(ch):
    return 'CJK UNIFIED IDEOGRAPH' in unicodedata.name(ch)


def _get_pairs(origin: str, kana: str) -> list[tuple]:
    ret = list()
    if any(_is_kanji(_) for _ in origin):
        hiragana = jaconv.kata2hira(kana)
        for p in _generate_furigana_pairs(origin, hiragana):
            ret.append(p)
    else:
        ret.append((origin,))
    return ret


def _get_pair_list(text: str) -> list[tuple]:
    tagger = Tagger()
    ret = list()
    for word in tagger(text):
        origin = word.feature.orth
        kana = word.feature.kana
        if origin is None and kana is None:
            ret.append((word.surface,))
            continue
        pairs = _get_pairs(origin, kana)
        ret.extend(pairs)
    return ret

def _get_furigana_html(tuple_list: list[tuple]) -> str:
    str_list = list()
    for pair in tuple_list:
        if len(pair) == 2:
            kanji, hira = pair
            str_list.append("<ruby>{0}<rt>{1}</rt></ruby>".format(kanji, hira))
        else:
            str_list.append(pair[0])
            # return (pair[0], end='')
    return ''.join(str_list)
def _generate_furigana_pairs(str1, str2) -> list[tuple]:
    s = difflib.SequenceMatcher(None, str1, str2)
    result = []
    temp1 = ""
    temp2 = ""

    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if tag == 'equal':
            # Append previous differing segments if exist
            if temp1 or temp2:
                result.append((temp1, temp2))
                temp1 = ""
                temp2 = ""
            # Add the matching segment
            result.append((str1[i1:i2], str2[j1:j2]))
        elif tag == 'replace' or tag == 'delete' or tag == 'insert':
            # Collect differing segments
            temp1 += str1[i1:i2]
            temp2 += str2[j1:j2]

    # Append any remaining differing segments
    if temp1 or temp2:
        result.append((temp1, temp2))
    another_result = list()

    # remove duplicate hiragana
    for r in result:
        if r[0] == r[1]:
            another_result.append((r[1],))
        else:
            another_result.append(r)

    return another_result
