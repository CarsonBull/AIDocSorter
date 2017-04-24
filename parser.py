#!/usr/bin/env python
import math
import os
import re
#import nltk
#from nltk.corpus import stopwords

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

    alphabetic_words_list = words(file_name)[0]
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
    #still working on, currently each class has same word counts for everything for some reason. 
    
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


# count number of each document in bag    255 of each class in bag 22914 unique words, 6,200,000 roughly words per class
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
        lprob+=math.log(((1.0+lcount)/52425.0+22914.0))     # 52425
        dtprob+=math.log(((1.0+dtcount)/1443244.0+22914.0))   # 1443244
        drprob+=math.log(((1.0+drcount)/82499.0+22914.0))   # 82499

    if(lprob>dtprob):
        if(lprob>drprob):
            print("l")
    if(drprob>dtprob):
        if(drprob>=lprob):
            print("dr")
    else:
        print("dt")
   


def intelli_grep(file_path):


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

    print("DT: "+ str(dtcount)+" DR: "+str(drcount)+" L: "+str(lcount))
    if(lcount>drcount):
        if(lcount>dtcount):
            print("L")
    if(dtcount>drcount):
        if(dtcount>lcount):
            print("DT")
    if(drcount>=dtcount):
        if(drcount>=lcount):
            print("DR")

def main():
##    nltk.download()
    #dirs = [('.//data//DR' , "DR") , ('.//data//DT' , "DT") , ('.//data//L' , "L")]
    #bag = create_bag(dirs , 0)
    #bayes("./data/TEST/WA_Grant_2009-01-06__1248482.txt",bag)
    intelli_grep("./data/TEST/OR_Lincoln_2008-04-02__08004083.txt")

    #j = 0

    #for i in bag[372][0]:
     #   if bag[372][0][i] > 0 and j < 30:
      #      print(i + ": " + str(bag[372][0][i]))
       #     j = j + 1


#Bag[item #]
    # Slot 0 dictionary
    # Slot 1 Class


    

if __name__ == "__main__":
    main()


















