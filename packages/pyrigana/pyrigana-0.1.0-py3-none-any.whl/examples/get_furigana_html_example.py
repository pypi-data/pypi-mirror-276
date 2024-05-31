import pyrigana

text = "ホテルによると、ムササビの巣は細かい木などでできていて、親が2匹の子どもを育てています。"
result = pyrigana.get_furigana_html(text)
print(result)
# ホテルによると、ムササビの<ruby>巣<rt>す</rt></ruby>は<ruby>細<rt>こま</rt></ruby>かい<ruby>木<rt>き</rt></ruby>などでできていて、<ruby>親<rt>おや</rt></ruby>が2<ruby>匹<rt>ひき</rt></ruby>の<ruby>子<rt>こ</rt></ruby>どもを<ruby>育<rt>そだ</rt></ruby>てています。
