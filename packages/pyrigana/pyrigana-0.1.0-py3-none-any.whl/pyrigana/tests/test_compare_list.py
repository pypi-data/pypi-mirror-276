from pyrigana._internal.utils import _generate_furigana_pairs


def test_compare_list():
    str1 = '間違っ'
    str2 = 'まちがっ'
    result = _generate_furigana_pairs(str1, str2)
    print(result)
    assert result == [('間違', 'まちが'), ('っ',)]


def test_compare_list_2():
    str1 = '壊'
    str2 = 'こわ'
    result = _generate_furigana_pairs(str1, str2)
    print(result)
    assert result == [('壊', 'こわ')]


def test_compare_list_3():
    str1 = '速やか'
    str2 = 'すみやか'
    result = _generate_furigana_pairs(str1, str2)
    print(result)
    assert result == [('速', 'すみ'), ('やか',)]


def test_compare_list_4():
    str1 = 'お日様'
    str2 = 'おひさま'
    result = _generate_furigana_pairs(str1, str2)
    print(result)
    assert result == [('お',), ('日様', 'ひさま')]


def test_compare_list_5():
    str1 = '思い出'
    str2 = 'おもいで'
    result = _generate_furigana_pairs(str1, str2)
    print(result)
    assert result == [('思', 'おも'), ('い',), ('出', 'で')]
