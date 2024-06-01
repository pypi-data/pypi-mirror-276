from pyrigana._internal.utils import _get_pair_list, _get_furigana_html


def get_furigana_html(text) -> str:
    ret = _get_pair_list(text)
    return _get_furigana_html(ret)
