# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 19:32:07 2017

@author: raymo
"""
import gensim
from scipy.misc import imread
import matplotlib.pyplot as plt

from wordcloud import WordCloud, ImageColorGenerator


d = "./image/"

ldamodel=gensim.models.LdaModel.load('lda.model')

source=str(ldamodel.show_topics(num_topics=28,num_words=15))


back_coloring = imread(d+"wordclouddemo.png")

wc = WordCloud( font_path='./image/font.ttf',
                background_color="black",
                mask=back_coloring,
                random_state=42,
                )
# 生成词云, 可以用generate输入全部文本(中文不好分词),也可以我们计算好词频后使用generate_from_frequencies函数
wc.generate(source)
# wc.generate_from_frequencies(txt_freq)
# txt_freq例子为[('词a', 100),('词b', 90),('词c', 80)]
# 从背景图片生成颜色值
image_colors = ImageColorGenerator(back_coloring)

plt.figure()
# 以下代码显示图片
plt.imshow(wc)
plt.axis("off")
plt.show()

# 保存图片
wc.to_file(d+"res.jpg")

