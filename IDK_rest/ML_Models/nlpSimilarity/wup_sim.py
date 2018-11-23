import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from numpy import dot
from numpy.linalg import norm

import pandas as pd

class wup_sim:

    def __init__(self, s1, s2):

        self.s1 = s1
        self.s2 = s2
    
    def sim_wup(self):

        if self.s1 == self.s2:
            return 1.0
        stop_words = set(stopwords.words('english'))

        tokens1 = nltk.word_tokenize(self.s1)
        tokens2 = nltk.word_tokenize(self.s2)
        cw1 = []
        cw2 = []

        for t in tokens1:
            if t.isalpha() and t.lower() not in stop_words:
                cw1.append(t)

        for t in tokens2:
            if t.isalpha() and t.lower() not in stop_words:
                cw2.append(t)

        content = cw1 + cw2
        entities = []

        for word in content:
            entities.append(wn.synsets(word)[0])

        entity_names = [entity.split('.')[0] for entity in content]
        similarities = []

        for entity in entities:
            
            l = []

            for compared_entity in entities:
                
                j = entity.wup_similarity(compared_entity)

                if(isinstance(j,float)):
                    l.append(round(j,2))

                else:
                    l.append(0.0)

            similarities.append(l)

        # build pairwise similarity matrix

        similarity_frame = pd.DataFrame(similarities,index=entity_names,columns=entity_names)

        jointwordset = list(set(cw1)|set(cw2))
        sm1 = [0 for x in range(len(jointwordset))]
        sm2 = [0 for x in range(len(jointwordset))]

        for i in range(len(jointwordset)):
            
            similarity_frame2 = similarity_frame.copy()
            similarity_frame2.drop(jointwordset[i],axis=1,inplace=True)

            if(jointwordset[i] in cw1):
                sm1[i] = 1

            else:
                sm1[i] = max(similarity_frame2.loc[jointwordset[i]]) if max(similarity_frame2.loc[jointwordset[i]])>0.06 else 0

            if(jointwordset[i] in cw2):
                sm2[i] = 1

            else:
                sm2[i] = max(similarity_frame2.loc[jointwordset[i]]) if max(similarity_frame2.loc[jointwordset[i]])>0.06 else 0

        return dot(sm1,sm2)/(norm(sm1)*norm(sm2))