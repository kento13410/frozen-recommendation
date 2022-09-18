import random
def makeRandomList(maxNumber):
    indexList = []
    if (maxNumber >= 5):
        for i in range(5):
            if (len(indexList) == 0):
                randomNumber = random.randrange(maxNumber)
                indexList.append(randomNumber)

            elif (len(indexList) == 1):
                randomNumber = random.randrange(maxNumber)
                while(indexList[0]== randomNumber):
                    randomNumber = random.randrange(maxNumber)
                indexList.append(randomNumber)

            elif (len(indexList) == 2):
                randomNumber = random.randrange(maxNumber)
                while(indexList[0]== randomNumber or indexList[1]== randomNumber):
                    randomNumber = random.randrange(maxNumber)
                indexList.append(randomNumber)

            elif (len(indexList) == 3):
                randomNumber = random.randrange(maxNumber)
                while(indexList[0]== randomNumber or indexList[1]== randomNumber or indexList[2]== randomNumber):
                    randomNumber = random.randrange(maxNumber)
                indexList.append(randomNumber)

            elif (len(indexList) == 4):
                randomNumber = random.randrange(maxNumber)
                while(indexList[0]== randomNumber or indexList[1]== randomNumber or indexList[2]== randomNumber or indexList[3]== randomNumber):
                    randomNumber = random.randrange(maxNumber)
                indexList.append(randomNumber)

            elif (len(indexList) == 5):
                randomNumber = random.randrange(maxNumber)
                while(indexList[0]== randomNumber or indexList[1]== randomNumber or indexList[2]== randomNumber or indexList[3]== randomNumber or indexList[4]== randomNumber):
                    randomNumber = random.randrange(maxNumber)
                indexList.append(randomNumber)
    else:
        indexList = [0,1,2,3,4]

    return indexList