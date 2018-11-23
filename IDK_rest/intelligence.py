import sys
import os
from IDK_rest.ML_Models.nlpSimilarity.wup_sim import wup_sim
from IDK_rest.ML_Models.collapseChecker.src.models.predict_model import predictCollapse
from IDK_rest.ML_Models.tagExtractor.preprocess import normalize_and_clean

def collapseCheck(text):
    return predictCollapse(text)

def extractTags(text):
    predictedTags = normalize_and_clean(text)
    if len(predictedTags) == 0:
        print("no predictions so spliiting..")
        return text.split()
    return predictedTags

def getSimilarityScore(question1,question2):
    t = wup_sim(question1,question2)
    return t.sim_wup()

def testCollapse():
    print("testing collapse..")
    s1 = input("enter text = >")
    print("isCollapsed is",collapseCheck(s1))

def testExtractTags():
    print("testing extract tags..")
    s1 = input("enter text = >")
    print("tags is",extractTags(s1))

def testSimilarity():
    print("testing similarity..")
    s1 = input("enter text = >")
    s2 = input("enter text = >")
    print("similiarity is",getSimilarityScore(s1,s2))

if __name__ == '__main__':
    while True:
        testCollapse()
        testSimilarity()
        testExtractTags()