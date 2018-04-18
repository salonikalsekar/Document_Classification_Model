import pandas as pd
import pprint
import numpy as np
from sklearn.model_selection import train_test_split

billLable = ""

def generate_dict(temp_dict, value):
    for eachValue in value:
        if (eachValue in temp_dict):
            temp_dict[eachValue] += int(1)
        else:
            temp_dict[eachValue] = int(1)

    return temp_dict

def second_largest(numbers):
    count = 0
    max1 = max2 = float('-inf')
    for x in numbers:
        count += 1
        if (x > max2):
            if (x >= max1):
                max1, max2 = x, max1
            else:
                max2 = x

    return max1, max2

def getValueLabel(number, final_dict):
    # print("Get Value label class: ")
    # print(pprint.pprint(final_dict))

    for eachClass in final_dict:
        # print("eachClass: ", eachClass)
        if (number == final_dict[eachClass]):
            return eachClass

def optimize(final, label1, label2):
    list = []

    for x in final:
        list.append(final[x])

    # if ((label1 is getLabel(final) )or (label2 is getLabel(final) )):
    if ((label2 is getLabel(final))):

        # get 2nd highest number and 1st highest number
        max1, max2 = second_largest(list)
        if (max2 / max1 > 0.50):
            return getValueLabel(max2, final)
        else:
            return None
    else:
        return None


def initConfusionMatrix(listOfLables):
    confusionMatrix = {}

    for lable in listOfLables:
        confusionMatrix[lable] = {}
        for innerLable in listOfLables:
            confusionMatrix[lable][innerLable] = 0

    # print(len(confusionMatrix), " ", len(confusionMatrix['BILL']))
    # print ("The confusion Matrix is: ", pprint.pprint (confusionMatrix))
    return confusionMatrix


def naive_bayes_and_normalization(train_Set, words_count_set, test_Set):
    totalCorrectPrediction = 0

    countTrainDict = {}
    countNumberList = []
    listOfLables = []

    # print("The Keys in test set are: ")
    # for key in test_Set:
    #     listOfLables.append (key)
    #     print(key)


    for key in train_Set:
        # print ("key: ", key, " =>", len (train_Set[key]))
        countTrainDict[key] = len(train_Set[key])
        countNumberList.append(len(train_Set[key]))
        listOfLables.append(key)


    listOfLables = list(set(listOfLables))

    confusionMatrix = initConfusionMatrix (listOfLables)

    max1, max2 = second_largest(countNumberList)
    max1Lable = getValueLabel(max1, countTrainDict)
    max2Lable = getValueLabel(max2, countTrainDict)
    # print("max1: ", max1Lable)
    # print("max2: ", max2Lable)

    for index, row in test_Set.iterrows():
        words = str(row[1]).strip().split(" ")
        final = {}

        for eachClass in train_Set:
            possibility = 0

            # eachWord = str.strip().split(" ")
            for eachWord in words:
                if (eachWord in train_Set[eachClass]):
                    possibility += train_Set[eachClass][eachWord] / words_count_set[eachWord]

            final[eachClass] = possibility

        if (optimize(final, max1Lable, max2Lable)):
            label = optimize(final, max1Lable, max2Lable)
        else:
            label = getLabel(final)

        if (label is row[0]):
            totalCorrectPrediction += 1

        # print("Done Calculation !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        confusionMatrix[row[0]][label] += 1

    correctPrediction = totalCorrectPrediction
    incorrectPrediction = len (test_Set) - correctPrediction
    print ("The confusion Matrix is: ", confusionMatrix)
    finalProbability = totalCorrectPrediction / len(test_Set)
    return totalCorrectPrediction, len(test_Set), finalProbability, max1Lable, max2Lable, confusionMatrix

def getLabel(input_dict):
    label = ""
    max = 0

    for key in input_dict:
        if (max < input_dict[key]):
            max = input_dict[key]
            label = key

    return label

def calculate(file):
    # df = pd.read_csv(file, header=None,
    #                  delimiter=",")
    df = file

    print(len(df))

    msk = np.random.rand (len (df)) < 0.8

    train = df[msk]

    test = df[~msk]



    # train, test = train_test_split(df, test_size=0.20)

    # print(len(train) , " ", len(test))

    train_set = {}
    words_count_set = {}

    temp_dict = {}

    for index, row in train.iterrows():
        value = str(row[1]).strip().split(" ")
        for eachValue in value:
            if (eachValue in words_count_set):
                words_count_set[eachValue] += int(1)
            else:
                words_count_set[eachValue] = int(1)

        if (row[0] in train_set):
            temp_dict = train_set[row[0]]
            train_set[row[0]] = generate_dict(temp_dict, value)
        else:
            temp_dict = {}
            train_set[row[0]] = generate_dict(temp_dict, value)



    totalCorrectPrediction, lenghtOfTestSet, finalProbability, max1Lable, max2Lable, confusionMatrix = naive_bayes_and_normalization(train_set, words_count_set, test)
    print ("#####################################################3")
    print("Before")
    print(totalCorrectPrediction, lenghtOfTestSet, finalProbability, max1Lable, max2Lable, confusionMatrix)
    print ("After")
    print("#####################################################3")
    # for key in train_set:
    #     print("key: ",key  , " =>" ,len(train_set[key]))
    #     for eachValue in train_set[key]:
    #         if (eachValue == 'NaN'):
    #             print("lol", key, " ", eachValue)
    #         if (eachValue == 'None'):
    #             print("lol", key, " ", eachValue)
    #
    #
    # for eachValue in words_count_set:
    #     if (eachValue == 'NaN'):
    #         print("lol", key, " ", eachValue)
    #     if (eachValue == 'None'):
    #         print("lol", key, " ", eachValue )

    return totalCorrectPrediction, lenghtOfTestSet, finalProbability, max1Lable, max2Lable, confusionMatrix

# naive_bayes()