from pyrigana._internal.utils import _get_pair_list


def test_getting_pair():
    text = "友達は新しい下宿に引っ越しました。"
    print("the result", _get_pair_list(text))
    assert _get_pair_list(text) == [('友達', 'ともだち'), ('は',), ('新', 'あたら'), ('しい',), ('下宿', 'げしゅく'), ('に',), ('引', 'ひ'), ('っ',), ('越', 'こ'), ('し',), ('まし',), ('た',),
                                    ('。',)]
