#!/usr/bin/env python3

import os
import random
import copy
import tkinter as tk
from tkinter import Button, Label, Listbox, ttk

def main():
    global glo

    class glo:
        #Variables
        curDir = ""
        baseFolder = "Base"
        contentFolder = "content/"
        kana = ""
        kanji = ""
        answer = ""
        questionsCounter = 0
        trainArr = []
        trainArrNonPop = []
        trainArrOriginal = []
        curTrain = []
        curTrainSplit = []
        checking = False
        totalMisses = 0
        currentTotalMisses = 0
        uniqueMissedKanji = []
        currentUniqueMissedKanji = []
        folders = []
        files = []
        filePath = ""
        isOrder = False
        fileIndex = []
        fileNames = []
        numOfQuestionsArr = []
        numOfQuestions = 0

        #Variables for trainX
        trainX = 4
        trainXAdd = 0
        trainArrX = []
        trainArrXNonPop = []
        trainArrXOriginal = [] #Use len to figure out how many questions are in total
        trainArrXCorrect = [] #This holds all correct answers
        roundPass = False #If trainArrX is same lenth (all in this round answered correctly) trainArrXCorrect then this is true and shows btnAddNextX
        trainXFinished = False

        #Init GUI
        root = tk.Tk()
        mainTitle = "Flashcard bruteforcer"

        #Main GUI
        lblFolders = Label(root, text="Folders")
        cbxFolders = ttk.Combobox(root,width=20)
        lblFiles = Label(root, text="File - Question Count")
        lbxFiles = Listbox(root, height=20, width=30 ,exportselection=False, selectmode="multiple")
        btnSelAll = Button(root, text="Select All", command= lambda: selAllLbx())
        lblNumOfSelectedQuestions = Label(root, text="# of Questions: " + str(numOfQuestions))
        btnTrain = Button(root, text="Train - Randomised", command= lambda: trainButtonFunc())
        btnTrainOrder = Button(root, text="Train - Ordered", command= lambda: trainOrderButtonFunc())
        lblSeparator = Label(root, text="---------------------------")
        btnTrainMore = Button(root, text="+", command= lambda: trainMore())
        btnTrainX = Button(root, text="Train " + str(trainX) + " - At A Time", command= lambda: trainXButtonFunc())
        btnTrainLess = Button(root, text="-", command= lambda: trainLess())

        #Main GUI Bindings
        cbxFolders.bind("<<ComboboxSelected>>", func=lambda x: fillListBox())
        lbxFiles.bind("<<ListboxSelect>>", func=lambda x: updateQuesNumLabel())

        #Train GUI
        btnMainMenu = Button(root, text="Back to Main Menu", command= lambda: mainMenuButtonFunc())
        lblOrder = Label(root, text="")
        lblKana = Label(root, text="", font=(None, 20))
        lblKanji = Label(root,text=kanji, font=(None, 40))
        lblAnswer = Label(root, text="", font=(None, 15))
        lblQuestion = Label(root, text="Did you know?")
        btnNo = Button(root, text="No", command= lambda: noAnswer())
        btnYes = Button(root, text="Yes", command= lambda: yesAnswer())
        btnCheck = Button(root, text="Check", command= lambda: revealAnswer())
        lblCounter = Label(root, text="# of Questions: 0")

        #Train GUI Bindings
        lblKanji.bind("<Enter>", func=lambda x: showKana())
        lblKanji.bind("<Leave>", func=lambda x: hideKana())

        #Repeat GUI
        lblTotalMisses = Label(root,text="")
        lblCurrentTotalMisses = Label(root,text="")
        lblCurrentUniqueMisses = Label(root, text="")
        lblUniqueMisses = Label(root,text="")
        lblRepeat = Label(root,text="Do you want to repeat?")
        btnNoRepeat = Button(root, text="No", command= lambda: noRepeatButtonFunc())
        btnYesRepeat = Button(root, text="Yes - Current", command= lambda: repeatButtonFunc())
        btnOriginalRepeat = Button(root, text="Yes - Original", command= lambda: originalRepeatButtonFunc())
        btnMissesRepeat = Button(root, text="Yes - Misses", command= lambda: missedRepeatButtonFunc())

        #TrainX GUI
        btnXMainMenu = Button(root, text="Back to Main Menu", command= lambda: xMainMenuButtonFunc())
        btnAddNextX = Button(root, text="Add " + str(trainXAdd) + " Kanji to Train", command= lambda: addNextXButtonFunc()) #This should only show if all kanji in current round are remembered
        lblXKana = Label(root, text="temp kana", font=(None, 20))
        lblXKanji = Label(root,text=" temp kanji", font=(None, 40))
        lblXAnswer = Label(root, text="temp answer", font=(None, 15))
        lblXQuestion = Label(root, text="Did you know?")
        lblQuestionsNow = Label(root, text=str(len(trainArrX)) + " Questions Left of " + str(len(trainArrXNonPop)))
        lblQuestionsTotal = Label(root, text=str(len(trainArrXOriginal)) + " Questions in Total")
        btnXNo = Button(root, text="No", command= lambda: noXAnswer())
        btnXYes = Button(root, text="Yes", command= lambda: yesXAnswer())
        btnXCheck = Button(root, text="Check", command= lambda: revealXAnswer())

        #TrainX GUI Bindings
        lblXKanji.bind("<Enter>", func=lambda x: showXKana())
        lblXKanji.bind("<Leave>", func=lambda x: hideXKana())

    glo.root.title(glo.mainTitle)
    
    loadFolders()
    fillListBox()
    showMainMenu()

    glo.root.mainloop()

def showMainMenu():
    setListboxHeight()
    updateQuesNumLabel()
    glo.lblFolders.pack(padx = 10, pady = 5)
    glo.cbxFolders.pack(padx = 10, pady = 5)
    glo.lblFiles.pack(padx = 10, pady = 5)
    glo.lbxFiles.pack(padx = 10, pady = 5)
    glo.btnSelAll.pack(padx = 10, pady = 5)
    glo.lblNumOfSelectedQuestions.pack(padx = 10, pady = 5)
    glo.btnTrain.pack(padx = 10, pady = 5)
    glo.btnTrainOrder.pack(padx = 10, pady = 5)
    glo.lblSeparator.pack(padx = 10, pady = 5)
    glo.btnTrainMore.pack(padx = 10, pady = 5)
    glo.btnTrainX.pack(padx = 10, pady = 5)
    glo.btnTrainLess.pack(padx = 10, pady = 5)

def fillListBox():
    glo.lblNumOfSelectedQuestions.config(text="# of Questions: 0")
    glo.lbxFiles.delete(0,tk.END)
    fileArr = os.listdir(glo.cbxFolders.get())
    fileArr = sorted(fileArr, key=str.casefold)
    index = 0
    questions = 0
    glo.fileIndex = []
    glo.fileNames = []
    glo.numOfQuestionsArr = []

    for item in fileArr:
        with open(os.path.join(glo.cbxFolders.get(), item), "r", encoding="utf8") as fr:
            questions = len(fr.readlines())
        glo.lbxFiles.insert(index, item + " - " + str(questions))
        glo.fileIndex.append(index)
        glo.fileNames.append(item)
        index = index + 1
        glo.numOfQuestionsArr.append(questions)
    
    setListboxHeight()

def hideMainMenu():
    glo.lblFolders.forget()
    glo.cbxFolders.forget()
    glo.lblFiles.forget()
    glo.lbxFiles.forget()
    glo.btnSelAll.forget()
    glo.lblNumOfSelectedQuestions.forget()
    glo.btnTrain.forget() 
    glo.btnTrainOrder.forget()
    glo.lblSeparator.forget()
    glo.btnTrainMore.forget()
    glo.btnTrainX.forget()
    glo.btnTrainLess.forget()

def showTrainMenu():
    glo.lblOrder.pack(padx = 10, pady = 5)
    glo.btnMainMenu.pack(padx = 10, pady = 5)
    glo.lblKana.pack(padx = 10, pady = 5)
    glo.lblKanji.pack(padx = 10, pady = 5)
    glo.lblAnswer.pack(padx = 10, pady = 5)
    glo.lblQuestion.pack(padx = 10, pady = 5)
    glo.lblCounter.pack(padx = 10, pady = 5)
    glo.btnCheck.pack(padx = 10, pady = 5)

    glo.btnNo.forget()
    glo.btnYes.forget()

def trainButtonFunc():
    glo.isOrder = False
    glo.lblOrder.config(text="Randomised")
    #Checks if selection was made
    if len(glo.lbxFiles.curselection()) > 0:
        getSelected()
        loadTrainingData()
        hideMainMenu()
        showTrainMenu()
    else:
        print("No selection")

def trainOrderButtonFunc():
    glo.isOrder = True
    glo.lblOrder.config(text="Ordered")
    #Checks if selection was made
    if len(glo.lbxFiles.curselection()) > 0:
        getSelected()
        loadTrainingData()
        hideMainMenu()
        showTrainMenu()
    else:
        print("No selection")

def loadTrainingData():
    readFiles()
    getCurrentQuestion()
    
#Loads selected listbox items into files
def getSelLbxItems():
    for i in glo.lbxFiles.curselection():
        glo.files.append(glo.lbxFiles.get(i))

#Reads the contents of each selected item into trainArr and into trainArrNonPop
def readFiles():
    for i in glo.lbxFiles.curselection():
        glo.filePath = os.path.join(glo.cbxFolders.get(), glo.fileNames[i])
        with open(glo.filePath, encoding="utf8") as file:
            for line in file:
                glo.trainArr.append(line)
    glo.trainArrNonPop = copy.deepcopy(glo.trainArr)
    glo.trainArrOriginal = copy.deepcopy(glo.trainArr)
    randomiseTrainArr()

def randomiseTrainArr():
    if glo.isOrder == False:
        random.shuffle(glo.trainArr)

def getCurrentQuestion():
    glo.questionsCounter = len(glo.trainArr)
    glo.curTrain = glo.trainArr.pop(0)
    glo.curTrainSplit = glo.curTrain.split(";")
    glo.kanji = glo.curTrainSplit.pop(0)
    glo.kana = glo.curTrainSplit.pop(0)
    glo.answer = glo.curTrainSplit.pop(0)
    glo.checking = False

    glo.lblKana.config(text="")
    glo.lblKanji.config(text=glo.kanji)
    glo.lblAnswer.config(text="")
    glo.lblCounter.config(text="# of Questions: " + str(glo.questionsCounter))

def getSelected():
    for i in glo.lbxFiles.curselection():
        glo.files.append(glo.lbxFiles.get(i))

def showKana():
    if glo.checking == False:
        glo.lblKana.config(text=glo.kana)

def hideKana():
    if glo.checking == False:
        glo.lblKana.config(text="")

def mainMenuButtonFunc():
    clearVariables()
    hideTrainMenu()
    showMainMenu()

def hideTrainMenu():
    glo.lblOrder.forget()
    glo.btnMainMenu.forget()
    glo.lblKana.forget()
    glo.lblKanji.forget()
    glo.lblAnswer.forget()
    glo.lblQuestion.forget()
    glo.lblCounter.forget()
    glo.btnCheck.forget()
    glo.btnNo.forget()
    glo.btnYes.forget()

def clearVariables():
    glo.kana = ""
    glo.kanji = ""
    glo.answer = ""
    glo.questionsCounter = 0
    glo.trainArr = []
    glo.trainArrOriginal = []
    glo.trainArrNonPop = []
    glo.curTrain = []
    glo.curTrainSplit = []
    glo.checking = False
    glo.totalMisses = 0
    glo.currentTotalMisses = 0
    glo.uniqueMissedKanji = []
    glo.currentUniqueMissedKanji = []
    glo.files = []
    glo.filePath = ""

def clearVariablesForRepeat():
    glo.kana = ""
    glo.kanji = ""
    glo.answer = ""
    glo.questionsCounter = 0
    glo.checking = False
    glo.currentTotalMisses = 0
    glo.currentUniqueMissedKanji = []

def revealAnswer():
    glo.checking = True

    glo.btnCheck.forget()
    glo.btnNo.pack(padx = 10, pady = 5)
    glo.btnYes.pack(padx = 10, pady = 5)

    glo.lblKana.config(text=glo.kana)
    glo.lblKanji.config(text=glo.kanji)
    glo.lblAnswer.config(text=glo.answer)

def noAnswer():
    addMisses()
    addMissedKanji()
    randomiseTrainArr()
    addCurTrainToTrainArr()
    getCurrentQuestion()
    hideTrainMenu()
    showTrainMenu()

def addMisses():
    glo.totalMisses = glo.totalMisses + 1
    glo.currentTotalMisses = glo.currentTotalMisses + 1

def addMissedKanji():
    exists = False

    for i in glo.uniqueMissedKanji:
        if exists == True:
            break
        if glo.curTrain == i:
            exists = True

    if exists == False:
        glo.uniqueMissedKanji.append(glo.curTrain)

    existsCurrent = False

    for i in glo.currentUniqueMissedKanji:
        if existsCurrent == True:
            break
        if glo.curTrain == i:
            existsCurrent = True

    if existsCurrent == False:
        glo.currentUniqueMissedKanji.append(glo.curTrain)

def addCurTrainToTrainArr():
    glo.trainArr.append(glo.curTrain)

def yesAnswer():

    if len(glo.trainArr) == 0:
        hideTrainMenu()
        showRepeatQuestion()
    else:
        getCurrentQuestion()
        hideTrainMenu()
        showTrainMenu()

def showRepeatQuestion():
    glo.lblTotalMisses.config(text="Total misses: " + str(glo.totalMisses))
    glo.lblCurrentTotalMisses.config(text="Current total misses: " + str(glo.currentTotalMisses))
    glo.lblCurrentUniqueMisses.config(text="Current unique misses: " + str(len(glo.currentUniqueMissedKanji)))
    glo.lblUniqueMisses.config(text="Unique misses: " + str(len(glo.uniqueMissedKanji)))

    glo.lblTotalMisses.pack(padx = 10, pady = 5)
    glo.lblCurrentTotalMisses.pack(padx = 10, pady = 5)
    glo.lblCurrentUniqueMisses.pack(padx = 10, pady = 5)
    glo.lblUniqueMisses.pack(padx = 10, pady = 5)
    glo.lblRepeat.pack(padx = 10, pady = 5)
    glo.btnNoRepeat.pack(padx = 10, pady = 5)
    glo.btnYesRepeat.pack(padx = 10, pady = 5)
    if len(glo.trainArrOriginal) is not len(glo.trainArrNonPop):
        glo.btnOriginalRepeat.pack(padx = 10, pady = 5)
    if len(glo.currentUniqueMissedKanji) > 0:
        glo.btnMissesRepeat.pack(padx = 10, pady = 5)

def noRepeatButtonFunc():
    clearVariables()
    hideRepeatQuestion()
    showMainMenu()

def hideRepeatQuestion():
    glo.lblTotalMisses.forget()
    glo.lblCurrentTotalMisses.forget()
    glo.lblCurrentUniqueMisses.forget()
    glo.lblUniqueMisses.forget()
    glo.lblRepeat.forget()
    glo.btnNoRepeat.forget()
    glo.btnYesRepeat.forget()
    glo.btnOriginalRepeat.forget()
    glo.btnMissesRepeat.forget()

def repeatButtonFunc():
    clearVariablesForRepeat()
    loadNonPopToTrainArr()
    randomiseTrainArr()
    getCurrentQuestion()
    hideRepeatQuestion()
    showTrainMenu()

def loadNonPopToTrainArr():
    glo.trainArr = copy.deepcopy(glo.trainArrNonPop)

def missedRepeatButtonFunc():
    loadCurUniqueMissedKanjiToTrainArr()
    clearVariablesForRepeat()
    randomiseTrainArr()
    getCurrentQuestion()
    hideRepeatQuestion()
    showTrainMenu()

def loadCurUniqueMissedKanjiToTrainArr():
    glo.trainArr = copy.deepcopy(glo.currentUniqueMissedKanji)
    glo.trainArrNonPop = copy.deepcopy(glo.currentUniqueMissedKanji)

def loadFolders():
    glo.curDir = os.path.dirname(os.path.realpath(__file__))
    for root, dirs, files in os.walk(glo.curDir):
        if dirs:
            #folders.append(dirs)
            glo.folders = dirs

    glo.folders = sorted(glo.folders, key=str.casefold)
    glo.cbxFolders["values"] = glo.folders

    index = -1
    #If baseFolder exists in current directory loads baseFolder as current selected value in cbxFolders
    if glo.baseFolder in glo.folders:
        for i in glo.folders:
            index = index + 1
            if i == glo.baseFolder:
                glo.cbxFolders.current(index)

def setListboxHeight():
    if glo.lbxFiles.size() > 30:
        glo.lbxFiles.config(height=30)
    else:
        glo.lbxFiles.config(height=glo.lbxFiles.size())

def updateQuesNumLabel():
    glo.numOfQuestions = 0
    for i in glo.lbxFiles.curselection():
        glo.numOfQuestions = glo.numOfQuestions + glo.numOfQuestionsArr[i]
    glo.lblNumOfSelectedQuestions.config(text="# of Questions: " + str(glo.numOfQuestions))

def selAllLbx():
    lbxSize = glo.lbxFiles.size()
    selItems = glo.lbxFiles.curselection()
    numSelItems = 0
    for x in selItems: #Counts how many entries are in the tuple for returned curselection()
        numSelItems += 1

    if numSelItems is not lbxSize:
        glo.lbxFiles.select_set(0, lbxSize)
        updateQuesNumLabel()
    else:
        glo.lbxFiles.select_clear(0,lbxSize)
        updateQuesNumLabel()

def originalRepeatButtonFunc():
    clearVariablesForRepeat()
    glo.trainArrNonPop = copy.deepcopy(glo.trainArrOriginal)
    loadNonPopToTrainArr()
    randomiseTrainArr()
    getCurrentQuestion()
    hideRepeatQuestion()
    showTrainMenu()

#TrainX functions, many parts repeated. Refactor/Rewrite later!!!

def trainMore():
    if glo.trainX < 10:
        glo.trainX = glo.trainX + 1

    glo.btnTrainX.config(text="Train " + str(glo.trainX) + " - At A Time")

def trainLess():
    if glo.trainX > 2:
        glo.trainX = glo.trainX - 1

    glo.btnTrainX.config(text="Train " + str(glo.trainX) + " - At A Time")

def trainXButtonFunc():
    #Checks if selection was made
    if len(glo.lbxFiles.curselection()) == 1 and glo.trainX <= countLines():
        getSelected()
        loadTrainingXData()
        hideMainMenu()
        showTrainXMenu()

def countLines():
    lines = 0
    for i in glo.lbxFiles.curselection():
        glo.filePath = os.path.join(glo.cbxFolders.get(), glo.fileNames[i])
        with open(glo.filePath, encoding="utf8") as file:
            lines = len(file.readlines())

    return lines
    pass

def showTrainXMenu():
    glo.btnXMainMenu.pack(padx = 10, pady = 5)

    if glo.trainXFinished:
        glo.btnAddNextX.config(text="Finished: All Correct")
        glo.btnAddNextX.pack(padx = 10, pady = 5)
    elif glo.roundPass:
        glo.btnAddNextX.config(text="Add " + str(glo.trainXAdd) + " Kanji to Train")
        glo.btnAddNextX.pack(padx = 10, pady = 5)

    glo.lblXKana.pack(padx = 10, pady = 5)
    glo.lblXKanji.pack(padx = 10, pady = 5)
    glo.lblXAnswer.pack(padx = 10, pady = 5)
    glo.lblXQuestion.pack(padx = 10, pady = 5)
    glo.lblQuestionsNow.pack(padx = 10, pady = 5)
    glo.lblQuestionsTotal.pack(padx = 10, pady = 5)
    glo.btnXCheck.pack(padx = 10, pady = 5)

    glo.btnXNo.forget()
    glo.btnXYes.forget()

def hideTrainXMenu():
    glo.btnXMainMenu.forget()
    glo.btnAddNextX.forget()
    glo.lblXKana.forget()
    glo.lblXKanji.forget()
    glo.lblXAnswer.forget()
    glo.lblXQuestion.forget()
    glo.lblQuestionsNow.forget()
    glo.lblQuestionsTotal.forget()
    glo.btnXNo.forget()
    glo.btnXYes.forget()
    glo.btnXCheck.forget()

def xMainMenuButtonFunc():
    clearVarsX()
    hideTrainXMenu()
    showMainMenu()

def loadTrainingXData():
    readFileX()
    getCurrentQuestionX()
    pass

def readFileX():
    for i in glo.lbxFiles.curselection():
        glo.filePath = os.path.join(glo.cbxFolders.get(), glo.fileNames[i])
        with open(glo.filePath, encoding="utf8") as file:
            for line in file:
                glo.trainArrXOriginal.append(line)

    #randomiseTrainArrXOriginal() #If this is commented it will load them in original order
    
    for i in range(glo.trainX):
        glo.trainArrX.append(glo.trainArrXOriginal[i])
        glo.trainArrXNonPop.append(glo.trainArrXOriginal[i])

def randomiseTrainArrXOriginal():
    if glo.isOrder == False:
        random.shuffle(glo.trainArrXOriginal)

def getCurrentQuestionX():
    glo.curTrain = glo.trainArrX.pop(0)
    glo.curTrainSplit = glo.curTrain.split(";")
    glo.kanji = glo.curTrainSplit.pop(0)
    glo.kana = glo.curTrainSplit.pop(0)
    glo.answer = glo.curTrainSplit.pop(0)
    glo.checking = False

    glo.lblXKana.config(text="")
    glo.lblXKanji.config(text=glo.kanji)
    glo.lblXAnswer.config(text="")
    glo.lblQuestionsNow.config(text=str(len(glo.trainArrX) + 1) + " Questions Left of " + str(len(glo.trainArrXNonPop)))
    glo.lblQuestionsTotal.config(text=str(len(glo.trainArrXOriginal)) + " Questions in Total")

def clearVarsX():
    glo.curTrain = []
    glo.curTrainSplit = ""
    glo.kanji = ""
    glo.kana = ""
    glo.answer = ""
    glo.checking = False
    glo.trainXAdd = 0
    glo.trainArrX = []
    glo.trainArrXNonPop = []
    glo.trainArrXOriginal = []
    glo.trainArrXCorrect = [] 
    glo.roundPass = False 
    glo.trainXFinished = False
    
def showXKana():
    if glo.checking == False:
        glo.lblXKana.config(text=glo.kana)

def hideXKana():
    if glo.checking == False:
        glo.lblXKana.config(text="")

def revealXAnswer():
    glo.checking = True
    
    glo.btnXCheck.forget()
    glo.btnXNo.pack(padx = 10, pady = 5)
    glo.btnXYes.pack(padx = 10, pady = 5)

    glo.lblXKana.config(text=glo.kana)
    glo.lblXKanji.config(text=glo.kanji)
    glo.lblXAnswer.config(text=glo.answer)

def noXAnswer():
    randomiseTrainArrX()
    addCurTrainToTrainArrX()
    getCurrentQuestionX()
    hideTrainXMenu()
    showTrainXMenu()

def randomiseTrainArrX():
    if glo.isOrder == False:
        random.shuffle(glo.trainArrX)

def randomiseTrainArrXNonPop():
    if glo.isOrder == False:
        random.shuffle(glo.trainArrXNonPop)

def addCurTrainToTrainArrX():
    glo.trainArrX.append(glo.curTrain)

def yesXAnswer():
    addCurTrainToXCorrectArr()
    checkTrainXFinished()

    if len(glo.trainArrX) == 0:
        checkRemainingX()
        repeatTrainX()
        getCurrentQuestionX()
        hideTrainXMenu()
        showTrainXMenu()
    else:
        getCurrentQuestionX()
        hideTrainXMenu()
        showTrainXMenu()

def addCurTrainToXCorrectArr():
    if glo.curTrain not in glo.trainArrXCorrect:
        glo.trainArrXCorrect.append(glo.curTrain)

def checkRemainingX():
    if glo.trainX > len(glo.trainArrXOriginal) - len(glo.trainArrXNonPop):
        glo.trainXAdd = len(glo.trainArrXOriginal) - len(glo.trainArrXNonPop)
    else:
        glo.trainXAdd = glo.trainX

def repeatTrainX():
    glo.roundPass = True
    random.shuffle(glo.trainArrXNonPop)
    glo.trainArrX = copy.deepcopy(glo.trainArrXNonPop)

def checkTrainXFinished():
    if glo.trainXFinished == False and len(glo.trainArrXOriginal) == len(glo.trainArrXCorrect):
        glo.trainXFinished = True

def addNextXButtonFunc():
    if glo.trainXFinished == False:
        glo.roundPass = False
        checkRemainingX()
        loadNextRound()
        getCurrentQuestionX()
        hideTrainXMenu()
        showTrainXMenu()

def loadNextRound():
    count = len(glo.trainArrXNonPop)
    
    glo.trainArrXNonPop = []
    glo.trainArrX = []
    glo.trainArrXCorrect = []

    numToAdd = count + glo.trainXAdd

    for i in range(numToAdd):
        glo.trainArrXNonPop.append(glo.trainArrXOriginal[i])

    randomiseTrainArrXNonPop()

    glo.trainArrX = copy.deepcopy(glo.trainArrXNonPop)

main()
