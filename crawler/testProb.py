#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 00:29:05 2017

@author: raymondmg
"""
import os
from gensim import corpora
import gensim
import jieba
import jieba.posseg as pseg

def splitResultFromLDAModel(data):
    freq  =[]
    words =[]
    if '*' not in data or '+' not in data:
        return freq,words
    firArray=data.split('+')
    
    for d in firArray:
        secArray=d.split('*')
        freq.append(secArray[0])
        words.append(secArray[1])
    return freq,words
    

def creadstoplist(stopwordspath):
    stwlist = [line.strip()
               for line in open(stopwordspath, 'r', encoding='utf-8').readlines()]
    return stwlist

stwlist = creadstoplist('stopwords.txt')
jieba.load_userdict("userdict.txt") 

def dealWithCutWord(data,filterOrNot,flag):
    curtexts = []
    words=pseg.cut(data.strip())  
    for w in words:
     #remove stopwords
     if w.word not in stwlist:
      if len(w.word) > 1:
        if filterOrNot:
         flagStrArray=flag.split(',')
         if w.flag in flagStrArray:
            curtexts.append(w.word)
        else:
          curtexts.append(w.word)
    return curtexts


doc_a="文化大革命、无产阶级文化大革命（全称）[2][3]或文革（简称），因其时间长达十年之久，被人们称为“十年动乱”[4][5]、“十年浩劫”[6][7]，是一场于1966年5月至1976年10月间在中华人民共和国境内所发生的政治运动。[8]由时任中国共产党中央委员会主席的毛泽东与中央文化革命小组，自上而下动员成千上万红卫兵在中国大陆进行全方位发动的阶级斗争。[9]在此期间以四大指导原则为借口，普及的批斗、抄家、告密等行为文化，使中国传统文化与道德沦亡[10]，整体经济受严重影响[11]，受害人数以千万计[12]，亦有数不清文物在1966年6月1日的破四旧中[13]惨遭红卫兵的蹂躏[14]。时任国家主席刘少奇、十大元帅的彭德怀和贺龙等领导人[15][16][17]被迫害致死，邓小平、陈云等党内高层亦在此期间被下放。[18][19]1976年10月，这场运动以遭到中共官方公开全盘否定而告终，整场运动历时共计长达十年之久，因此通常被人们称为“十年动乱”、“十年浩劫”，此外这场运动同时也影响了阿尔巴尼亚、北朝鲜、法国、埃塞俄比亚和智利等一系列左翼势力强大的地区。[20]广义上，一般认为文革[21]正式开始于1966年5月16日“五一六通知”出台[22][23]，是毛泽东在1958年前后的三面红旗的挫败[24]后、以及在反苏修、反美帝等口号的情况下，以革命名义攻击温和派（当时蔑称走资派）并重回党核心的尝试，并在日后一两年达到高潮，右派人物的影响力则多遭到剥夺，而当权派亦有内斗，并导致了原定接班人林彪的死亡。[25]1978年12月中共十一届三中全会，在文革结束及经过一连串政治斗争后[26][27]，中共中央形成了以邓小平为首的第二代领导核心人物，[28][29]并推动了拨乱反正、平反冤假错案和改革开放，逐渐消减毛泽东时代的极左派色彩，也由于藉毛泽东权势推动文革的极左派多被整肃，使中国社会经济复苏并顺利地由计划经济走向市场经济。不过为了确保共产党治理的一致性，文革平反后中共认为所谓的改革开放是完成对社会主义生产资料所有制的改造，并宣称改开后中国直接步入长期地社会主义初级阶段，籍中国特色的社会主义市场经济一词来挡驾路线变动，但包装之下本质上已是往回走的政策，不过允许资本再度开始活跃的做法，也令中国经济回到了轨道上，让人类历史上前所未有的经济增长成为可能[30]。1981年6月27日，中华人民共和国政府当局针对1966年至1976年执政阶段（文革阶段）给予立场和态度是[31]，将其定性为“由领导者错误发动、被反革命集团利用，给党、国家和人民带来严重灾难的内乱，造成全面而严重的危害”。[32]至今，文化大革命在中国大陆地区仍然具有极大的争议性[33]，中国官方和自由派人士[34][35]认为文化大革命是错误的，自由派人士甚至认为毛泽东要对此负主要责任。[36][37][38]但极左派仍支持文化大革命的“正当性”，认为邓小平等“走资派”成功篡夺了党和国家，建立起了修正主义国家。"
doc_b="经济学是一门对产品和服务的生产、分配以及消费进行研究的社会科学。西方语言中的“经济学”一词源于古希腊的οἰκονομία[1]。起初这一领域被称为政治经济学，但19世纪经济学家采用简短的“经济学”一词来代表“经济科学”，这也是为避免被误解为政治学、数学和伦理学等领域[2]。经济学注重的是研究经济行为者在一个经济体系下的行为，以及他们彼此之间的互动。在现代，经济学的教材通常将这门领域的研究分为宏观经济学和微观经济学。微观经济学检视一个社会里基本层次的行为，包括个体的行为者（例如个人、公司、买家或卖家）以及与市场的互动。而宏观经济学则分析整个经济体和其议题，包括失业、通货膨胀、经济成长、财政和货币政策等。其他的对照还包括了实证经济学（研究“是什么”）以及规范经济学（研究“应该是什么”）、经济理论与实用经济学、行为经济学与理性选择经济学、主流经济学（研究理性-个体-均衡等）与非主流经济学（研究体制-历史-社会结构等）[3][4]。[5]经济学的分析也被用在其他各种领域上，主要领域包括了商业、金融、和政府等，但同时也包括了如健康、犯罪[6]、教育[7]、法律、政治、社会架构、宗教[8]、战争[9]、和科学[10]等等。到了21世纪初，经济学在社会科学领域各方面不断扩张影响力，使得有些学者讽刺地称其为“经济学帝国主义”[11]。"
doc_c="管理学（又称管理科学，英语：Management Science）是一门研究人类管理活动规律及其应用的科学。它偏重于用一些工具和方法来解决管理上的问题，如用运筹学、统计学等来定量定性分析。管理的定义为管理者和他人及透过他人有效率且有效能地完成活动的程序。[1]以前管理科学主要用运筹学来解决管理中碰到的问题。近十几年管理科学发展很快，它已经不单单是用运筹学来分析一些具体问题，而是用自然科学与社会科学两大领域的综合性交叉科学来分析如运作管理、人力资源管理、风险管理与不确定性决策，复杂系统的演化、涌现、自适应、自组织、自相似的机理等。已经不是一个运筹学所能涵盖的。由于所有组织都可以被视为一定的系统，管理也可以被视为一种人类行为现象，包括设计、促进系统更好地生产。这种观点为“管理”自身创造了发展机会，是管理他人之前，先管好自己的先决条件。一些人认为管理学应该归入自然科学，而另外一些人则认为应该归入社会科学。"

doc_d="会计是以货币为主要的计量单位，以凭证为主要的依据，借助于专门的技术方法，对一定单位的资金运动进行全面、综合、连续、系统的核算与监督，向有关方面提供会计信息、参与经营管理、旨在提高经济效益的一种经济管理活动。古义是集会议事。我国从周代就有了专设的会计官职，掌管赋税收入、钱银支出等财务工作，进行月计、岁会。亦即，每月零星盘算为“计”，一年总盘算为“会”，两者合在一起即成“会计”。"
doc_set = [doc_a,doc_b,doc_c]

topicNum=4
wordNum=5

texts = []
for i in doc_set:
    
    curdoc=dealWithCutWord(i,False,"pos")
    curtexts=[]
    curtexts.append(curdoc)
    texts.append(curdoc)    

# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(texts)
    
# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]


ldamodel = gensim.models.ldamodel.LdaModel(corpus,num_topics=topicNum,id2word=dictionary,passes=20)  

kkd=dealWithCutWord(doc_d,False,"pos")
print(ldamodel.print_topics(topicNum,wordNum))
print(list(ldamodel[corpus[0]]))




