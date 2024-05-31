import pyrigana


def test_furigana_html1():
    text = "ホテルによると、ムササビの巣は細かい木などでできていて、親が2匹の子どもを育てています。"
    result = pyrigana.get_furigana_html(text)
    assert result == "ホテルによると、ムササビの<ruby>巣<rt>す</rt></ruby>は<ruby>細<rt>こま</rt></ruby>かい<ruby>木<rt>き</rt></ruby>などでできていて、<ruby>親<rt>おや</rt></ruby>が2<ruby>匹<rt>ひき</rt></ruby>の<ruby>子<rt>こ</rt></ruby>どもを<ruby>育<rt>そだ</rt></ruby>てています。"
    print(result)


def test_furigana_html2():
    text = "友達は新しい下宿に引っ越しました。"
    result = pyrigana.get_furigana_html(text)
    assert result == '<ruby>友達<rt>ともだち</rt></ruby>は<ruby>新<rt>あたら</rt></ruby>しい<ruby>下宿<rt>げしゅく</rt></ruby>に<ruby>引<rt>ひ</rt></ruby>っ<ruby>越<rt>こ</rt></ruby>しました。'
    print(result)
