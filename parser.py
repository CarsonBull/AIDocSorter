#!/usr/bin/env python
import math
import os
import re
import nltk
import sys
from nltk.corpus import stopwords
import random
from copy import deepcopy



def create_corpus(path):
    """Creates a dictionary of the txt files in the provided path. The contents
    of files will be mapped to the file name"""
    result_dict = {}
    file_list = os.listdir(path)
    for x in file_list:
        re_result = re.match( '.*\.txt\Z' , x )
        if re_result != None:
            with open(path + "//" + x , encoding = 'utf8') as file:
                data = file.read()
                result_dict[x] = data

    return result_dict

def words(data):
    """ This function takes a string then breakes it down into a two tuple. the first element is a list of the
    words that it finds in the string and the second is a list of the non char words also split by whitespace"""
    
    alpha_words = []
    other_words = []
    word = ""
    nonword = False

    # This creates a list of stop words that we wont use
    #stops = set(stopwords.words('english'))

    # Setting up the data so it is all lower case and has no trailing white space 
    lower_str = data.lower()
    lower_str = lower_str.rstrip()
    regex = re.compile('[^a-zA-Z1-9 ]')

    lower_str = regex. sub('', lower_str)

    # For loop that takes every character and sorts it to where it needs to go. 
    # Builds words and not charwords then add them to the list when if sees white space
    for x in lower_str:
        if x.isalpha():
##            if x not in stops:   probably create a second words function that takes out stop words for a modified bayes.
            word = word + x
        elif not x.isspace():
            nonword = True
            word = word + x
        else:
            # Checks if we have a word with only alphabetic characters or if it is a nonword. then adds it to the respective list
            if not nonword and word != "":
                alpha_words.append(word)
            elif word != "":
                other_words.append(word)
            word = ""
            nonword = False

    # Adds the final words and characters that were collected in the for loop    
    if not nonword and word != "":
        alpha_words.append(word)
    elif word != "":
        other_words.append(word)     

    
    return (alpha_words , other_words)

def words_no_stopwords(data):
    """ This function takes a string then breakes it down into a two tuple. the first element is a list of the
    words that it finds in the string and the second is a list of the non char words also split by whitespace"""
    
    alpha_words = []
    other_words = []
    word = ""
    nonword = False

    stops = stopwords.words("english")

    # This creates a list of stop words that we wont use
    #stops = set(stopwords.words('english'))

    # Setting up the data so it is all lower case and has no trailing white space 
    lower_str = data.lower()
    lower_str = lower_str.rstrip()
    regex = re.compile('[^a-zA-Z1-9 ]')

    lower_str = regex. sub('', lower_str)

    # For loop that takes every character and sorts it to where it needs to go. 
    # Builds words and not charwords then add them to the list when if sees white space
    for x in lower_str:
        if x.isalpha():
##            if x not in stops:
            word = word + x
        elif not x.isspace():
            nonword = True
            word = word + x
        else:
            # Checks if we have a word with only alphabetic characters or if it is a nonword. then adds it to the respective list
            if not nonword and word != "" and word not in stops:
                alpha_words.append(word)
            elif word != "":
                other_words.append(word)
            word = ""
            nonword = False

    # Adds the final words and characters that were collected in the for loop    
    if not nonword and word != "":
        alpha_words.append(word)
    elif word != "":
        other_words.append(word)     

    
    return (alpha_words , other_words)

def word_frequencies(corpus):
    
    lookup_dict = {}

    for file_name in corpus:
        alphabetic_words_list = words(corpus[file_name])[0]
        for word in alphabetic_words_list:
            if word in lookup_dict:
                lookup_dict[word] += 1
            else:
                lookup_dict[word] = 1

    return lookup_dict

def word_frequencies_x(word_dict , amount):

    word_list = []
    return_list = []
    
    for word in word_dict:
        word_list.append((word_dict[word] , word))

    word_list.sort(reverse=True)

    return_list = word_list[:amount]

##    for i in range(20):
##        return_list.append(word_list[i])

    return return_list


def create_bag(directory_list , smoothing_num):

    bag_of_words = []
    temp_bag = []
    dictionary= {}

    for x in directory_list:
        temp_corp = create_corpus(x[0])
        for y in temp_corp:
            temp_dict = word_frequencies_file(temp_corp[y])
            #for k in temp_dict:
            #    if k not in dictionary:
            #        dictionary[k] = 0
            bag_of_words.append((temp_dict , x[1]))

    #for item in temp_bag:
    #    temp_dict = dictionary
    #    for val in item[0]:
    #        temp_dict[val] = smoothing_num + item[0][val]    
    #    bag_of_words.append((temp_dict , item[1]))
    

    return bag_of_words

def word_frequencies_file(file_name):
    """ May not end up using this. The idea is to make it with a file path and not a folder."""

    lookup_dict = {}

    alphabetic_words_list = words_no_stopwords(file_name)[0]
    for word in alphabetic_words_list:
        if word in lookup_dict:
            lookup_dict[word] += 1
        else:
            lookup_dict[word] = 1

    return lookup_dict

##    for key in list(lookup_dict):
##        freq_list.append((lookup_dict[key] , key))
##
##    return sorted(freq_list , key=lambda x: x[0])



def bayes(file_path,bag):
    #currently uses all words as feature vector, assignment wants top 20 words from each class (frequency)
    
    lprob=math.log(1.0/3.0)
    dtprob=lprob
    drprob=lprob
    
    #   open and preprocess file for testing
    with open(file_path, encoding = 'utf8') as file:
        data = file.read()
        myfile=words(data)
        


   
    for i in myfile[0]:
        lcount=0
        dtcount=0
        drcount=0


# count number of each document in bag  255 of each class in bag 22914 unique words, roughly words per class
        for item in bag:

            if(item[1]=="L"):
                if i in item[0]:
                    lcount+=item[0][i]

            if(item[1]=="DT"):
                if i in item[0]:
                    dtcount+=item[0][i]

            if(item[1]=="DR"):
                if i in item[0]:
                    drcount+=item[0][i]

        #here we use sum of logs instead of product of small reals
        lprob+=math.log(((1.0+lcount)/52425.0+22914.0))     # 52425   these are total word counts for each class
        dtprob+=math.log(((1.0+dtcount)/1443244.0+22914.0))   # 1443244
        drprob+=math.log(((1.0+drcount)/82499.0+22914.0))   # 82499

    filename=file_path.split('/')
    if(lprob>dtprob):
        if(lprob>drprob):
            return((filename[len(filename)-1],"L"))            
            #print(filename[len(filename)-1]+": l")
    if(drprob>dtprob):
        if(drprob>=lprob):
            #print(filename[len(filename)-1]+": dr")
            return((filename[len(filename)-1],"DR"))
    if(dtprob>drprob):
        if(dtprob>lprob):
            #print(filename[len(filename)-1]+": dt")
            return((filename[len(filename)-1],"DT"))

def intelli_grep1(file_path):  #original intelligrep function

    filename=file_path.split('/')
    time=0
    dtcount=0
    drcount=0
    lcount=0
    flag1=False  #flags used to check consecutive words
    flag2=False


    with open(file_path, encoding = 'utf8') as file:
        data = file.read()
        myfile=words(data)


    for i in myfile[0]:
        if (i=="deed"):
            flag1=True
            time+=1
        if (i=="of" and flag1):
            flag2=True
            time+=1
        if (i=="trust" and flag2):
            dtcount+=1
        if (i=="reconveyance" and flag2):
            drcount+=1
        if(i=="lien"):
            lcount+=1

        
        if (time == 0):
            flag1=False
            flag2=False
        if (time>0):        
            time-=1

    #print("DT: "+ str(dtcount)+" DR: "+str(drcount)+" L: "+str(lcount)) #word counts for each class
    if(lcount>drcount):
        if(lcount>dtcount):
            #print(filename[len(filename)-1]+": L")
            return((filename[len(filename)-1],"L"))
    if(dtcount>drcount):
        if(dtcount>lcount):
            #print(filename[len(filename)-1]+": DT")
            return((filename[len(filename)-1],"DT"))
    if(drcount>=dtcount):
        if(drcount>=lcount):
            #print(filename[len(filename)-1]+": DR")
            return((filename[len(filename)-1],"DR"))



def intelli_grep2(file_path): #modified intelligrep with pattern matching and weighted word counts

    filename=file_path.split('/')
    time=0
    dtcount=0
    drcount=0
    lcount=0
    flag1=False  #flags used to check consecutive words
    flag2=False


    with open(file_path, encoding = 'utf8') as file:
        data = file.read()
        myfile=words(data)


    for i in myfile[0]:
        if (i=="deed"):
            flag1=True
            time+=1
        if (i=="of" and flag1):
            flag2=True
            time+=1
        if (i=="trust" and flag2):
            dtcount+=1
        if (re.match("recon",i) and flag2):
            drcount+=1
        if(i=="lien"):
            lcount+=1

        
        if (time == 0):
            flag1=False
            flag2=False
        if (time>0):        
            time-=1

    #print("DT: "+ str(dtcount)+" DR: "+str(drcount)+" L: "+str(lcount)) #word counts for each class
    if(lcount/2>5*drcount):
        if(lcount/2>dtcount):
            #print(filename[len(filename)-1]+": L")
            return((filename[len(filename)-1],"L"))
    if(dtcount>5*drcount):
        if(dtcount>lcount/2):
            #print(filename[len(filename)-1]+": DT")
            return((filename[len(filename)-1],"DT"))
    if(5*drcount>=dtcount):
        if(5*drcount>=lcount/2):
            #print(filename[len(filename)-1]+": DR")
            return((filename[len(filename)-1],"DR"))

def make_dict(bag):
    dictionary = {}

    for item in bag:
        for word in item[0]:
            if word not in dictionary:
                dictionary[word] = 0

    return dictionary
        

def perceptron(dictionary , bag , file_path):

    #   open and preprocess file for testing
    with open(file_path, encoding = 'utf8') as file:
        data = file.read()
        file_words = words_no_stopwords(data)

    DT_dict = {}
    DR_dict = {}
    L_dict = {}

    DT_count = 0;
    DR_count = 0;
    L_count = 0;

    for item in bag:
        if item[1] == "DT":
            sorted_list = word_frequencies_x(item[0] , 20)
            for word_tuple in sorted_list:
                DT_count += word_tuple[0]
                if word_tuple[1] not in DT_dict:
                    DT_dict[word_tuple[1]] = word_tuple[0]
                else:
                    DT_dict[word_tuple[1]] += word_tuple[0]
        elif item[1] == "DR":
            sorted_list = word_frequencies_x(item[0] , 20)
            for word_tuple in sorted_list:
                DR_count += word_tuple[0]
                if word_tuple[1] not in DR_dict:
                    DR_dict[word_tuple[1]] = word_tuple[0]
                else:
                    DR_dict[word_tuple[1]] += word_tuple[0]
        else:
            sorted_list = word_frequencies_x(item[0] , 20)
            for word_tuple in sorted_list:
                L_count += word_tuple[0]
                if word_tuple[1] not in L_dict:
                    L_dict[word_tuple[1]] = word_tuple[0]
                else:
                    L_dict[word_tuple[1]] += word_tuple[0]
            

    print(word_frequencies_x(L_dict , 60))

def check_result(file_path , file_name , result):

    with open(file_path, encoding = 'utf8') as file:
        data = file.read()

    match_string = file_name + ',(.*)'

    match = re.findall(match_string , data)

    if(len(match) == 1 and match[0] == result):
        return True
    else:
        return False


        

def main():

    #nltk.download()
    
    #bayes("./data/TEST/OR_Deschutes_2008-06-03__2008-023914.txt",bag)
    #intelli_grep1("./data/TEST/OR_Coos_2008-04-04__08003341.txt")
    #intelli_grep2("./data/TEST/OR_Coos_2008-04-04__08003341.txt")
##    path="./data/TEST/"
##    file_list = os.listdir(path)
##    if (len(sys.argv) ==2): 
##        if(sys.argv[1]=="a"):
##            for x in file_list:
##                intelli_grep1(path+x)
##        if(sys.argv[1]=="b"):
##            for x in file_list:
##                intelli_grep2(path+x)
##        if(sys.argv[1]=="c"):
##            dirs = [('.//data//DR' , "DR") , ('.//data//DT' , "DT") , ('.//data//L' , "L")]
##            bag = create_bag(dirs , 0)
##            for x in file_list:
##                bayes(path+x,bag)
##    else:
##        print()
##        print("Pass exactly 1 argument with program to select classifier method.") 
##        print()        
##        print("a-intelligrep, b-modified intelligrep, c-naive bayes")
##        print()
    
    dirs = [('.//data//DR' , "DR") , ('.//data//DT' , "DT") , ('.//data//L' , "L")]
    bag = create_bag(dirs , 0)
##    bayes("./data/TEST/WA_Grant_2009-01-07__1248514.txt",bag)
##    intelli_grep("./data/TEST/OR_Lincoln_2008-04-02__08004083.txt")

##    j = 0
##
    dic = make_dict(bag)
##
##
    perceptron(dic , bag , "./data/TEST/OR_Lincoln_2008-04-02__08004083.txt")


##    print(check_result(".\\data\\test-results.txt" , 'OR_Coos_2008-04-07__08003475.txt' , 'L'))

    

if __name__ == "__main__":
    main()


















