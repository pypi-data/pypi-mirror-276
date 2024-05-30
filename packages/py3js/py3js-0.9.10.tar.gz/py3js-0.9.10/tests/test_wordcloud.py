from py3js.wordcloud import WordCloud

save_path = "c:\\tmp\\1.html"


def test_default():
    wc = WordCloud([("one", 1), ("two", 2)])
    wc.save(save_path)
