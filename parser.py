#!/usr/bin/env python

import os
import re
import nltk
from nltk.corpus import stopwords

def create_corpus(path):
    """Creates a dictionary of the txt files in the provided path. The contents
    of files will be mapped to the file name"""
    result_dict = {}
    file_list = os.listdir(path)
    for x in file_list:
        re_result = re.match( '.*\.txt\Z' , x )
        if re_result != None:
            with open(path + "\\" + x , encoding = 'utf8') as file:
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
    stops = set(stopwords.words('english'))

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
            for k in temp_dict:
                if k not in dictionary:
                    dictionary[k] = 0
            temp_bag.append((temp_dict , x[1]))

    for item in temp_bag:
        temp_dict = dictionary
        for val in item[0]:
            temp_dict[val] = smoothing_num + item[0][val]    
        bag_of_words.append((temp_dict , item[1]))
    

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



def main():
##    nltk.download()
    dirs = [('.\\data\\DR' , "DR") , ('.\\data\\DT' , "DT") , ('.\\data\\L' , "L")]
    bag = create_bag(dirs , 1)

    j = 0

    for i in bag[372][0]:
        if bag[372][0][i] > 0 and j < 30:
            print(i + ": " + str(bag[372][0][i]))
            j = j + 1


#Bag[item #]
    # Slot 0 dictionary
    # Slot 1 Class


    

if __name__ == "__main__":
    main()


















