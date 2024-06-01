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


def test_compare_list_6():
    str1 = '忙しい'
    str2 = 'いそがい'
    result = _generate_furigana_pairs(str1, str2)
    print(result)
    assert result == [('忙し', 'いそが'), ('い',)]


def test_compare_list_7():
    str1 = 'お茶'
    str2 = 'おちゃ'
    result = _generate_furigana_pairs(str1, str2)
    print(result)
    assert result == [('お',), ('茶', 'ちゃ')]


def test_compare_list_8():
    str1 = 'ご無沙汰'
    str2 = 'ごぶさた'
    result = _generate_furigana_pairs(str1, str2)
    print(result)
    assert result == [('ご',), ('無沙汰', 'ぶさた')]


def test_compare_list_9():
    str1 = 'お子さん'
    str2 = 'おこさん'
    result = _generate_furigana_pairs(str1, str2)
    print(result)
    assert result == [('お',), ('子', 'こ'), ('さん',)]


def test_compare_list_pair():
    paris = [('出会う', ' であう'),
             ('明るい', 'あかるい'),
             ('駆け抜け', 'かけぬけ'),
             ]
    results = []
    for p in paris:
        results.append(_generate_furigana_pairs(p[0], p[1]))
    assert results[0] == [('出会', ' であ'), ('う',)]
    assert results[1] == [('明', 'あか'), ('るい',)]
    assert results[2] == [('駆', 'か'), ('け',), ('抜', 'ぬ'), ('け',)]
