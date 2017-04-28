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
            if not nonword and word != "" and word not in stops and len(word) > 2:
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


def bayes1(file_path,bag):
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

            if(item[1]=="L"): #sort document by class, then check if the word exists in the document
                if i in item[0]:
                    lcount+=1

            if(item[1]=="DT"):
                if i in item[0]:
                    dtcount+=1

            if(item[1]=="DR"):
                if i in item[0]:
                    drcount+=1

        #here we use sum of logs instead of product of small reals
        lprob+=math.log(((1.0+lcount)/52425.0+22914.0))     # 52425   these are total word counts for each class
        dtprob+=math.log(((1.0+dtcount)/1443244.0+22914.0))   # 1443244
        drprob+=math.log(((1.0+drcount)/82499.0+22914.0))   # 82499

    filename=file_path.split('/')
    if(lprob>=dtprob):
        if(lprob>=drprob):
            return((filename[len(filename)-1],"L"))            
            #print(filename[len(filename)-1]+": l") 
    if(drprob>=dtprob):
        if(drprob>=lprob):
            #print(filename[len(filename)-1]+": dr")
            return((filename[len(filename)-1],"DR"))
    if(dtprob>=drprob):
        if(dtprob>=lprob):
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
    if(lcount>=drcount):
        if(lcount>=dtcount):
            #print(filename[len(filename)-1]+": L")
            return((filename[len(filename)-1],"L"))
    if(dtcount>=drcount):
        if(dtcount>=lcount):
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
    if(lcount/2>=5*drcount):
        if(lcount/2>=dtcount):
            #print(filename[len(filename)-1]+": L")
            return((filename[len(filename)-1],"L"))
    if(dtcount>=5*drcount):
        if(dtcount>=lcount/2):
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
        
class Per:

    def __init__(self , dirs):
        self.bag = create_bag(dirs , 0)

        self.DT_dict = {}
        self.DR_dict = {}
        self.L_dict = {}

        self.DT_ratio = {}
        self.DR_ratio = {}
        self.L_ratio = {}

        self.DT_count = 0;
        self.DR_count = 0;
        self.L_count = 0;

        self.DT_bias = .5
        self.DR_bias = .5
        self.L_bias = .5

        self.alpha = .1

        self.decay = .99

        for item in self.bag:
            if item[1] == "DT":
                sorted_list = word_frequencies_x(item[0] , 20)
                for word_tuple in sorted_list:
                    self.DT_count += word_tuple[0]
                    if word_tuple[1] not in self.DT_dict:
                        self.DT_dict[word_tuple[1]] = word_tuple[0]
                    else:
                        self.DT_dict[word_tuple[1]] += word_tuple[0]
            elif item[1] == "DR":
                sorted_list = word_frequencies_x(item[0] , 20)
                for word_tuple in sorted_list:
                    self.DR_count += word_tuple[0]
                    if word_tuple[1] not in self.DR_dict:
                        self.DR_dict[word_tuple[1]] = word_tuple[0]
                    else:
                        self.DR_dict[word_tuple[1]] += word_tuple[0]
            else:
                sorted_list = word_frequencies_x(item[0] , 20)
                for word_tuple in sorted_list:
                    self.L_count += word_tuple[0]
                    if word_tuple[1] not in self.L_dict:
                        self.L_dict[word_tuple[1]] = word_tuple[0]
                    else:
                        self.L_dict[word_tuple[1]] += word_tuple[0]

        for word in self.DT_dict:
            self.DT_ratio[word] = self.DT_dict[word]/self.DT_count

        for word in self.DR_dict:
            self.DR_ratio[word] = self.DR_dict[word]/self.DR_count

        #print(self.L_count)

        for word in self.L_dict:
            self.L_ratio[word] = self.L_dict[word]/self.L_count

    def train(self):

        random_bag = deepcopy(self.bag)

        random.shuffle(random_bag)
        
        for doc in random_bag:
            DT_score = self.DT_bias;
            DR_score = self.DR_bias;
            L_score = self.L_bias;
            for word in doc[0]:
                if word in self.DT_ratio:
                    DT_score += self.DT_ratio[word]*doc[0][word]
                if word in self.DR_ratio:
                    DR_score += self.DR_ratio[word]*doc[0][word]
                if word in self.L_ratio:
                    L_score += self.L_ratio[word]*doc[0][word]

            DR_error = 0;
            DT_error = 0;
            L_error = 0;

            if doc[1] == "DR":
                if DR_score >= 0:
                    DR_error = 1
                else:
                    DR_error = -1
            else:
                if DR_score >= 0:
                    DR_error = -1
                else:
                    DR_error = 1

            if doc[1] == "DT":
                if DT_score >= 0:
                    DT_error = 1
                else:
                    DT_error = -1
            else:
                if DT_score >= 0:
                    DT_error = -1
                else:
                    DT_error = 1

            if doc[1] == "L":
                if L_score >= 0:
                    L_error = 1
                else:
                    L_error = -1
            else:
                if L_score >= 0:
                    L_error = -1
                else:
                    L_error = 1

            self.DT_bias = self.DT_bias + (self.alpha*DT_error)
            self.DR_bias = self.DR_bias + (self.alpha*DR_error)
            self.L_bias = self.L_bias + (self.alpha*L_error)

            for word in doc[0]:
                if word in self.DT_ratio:
                    self.DT_ratio[word] = self.DT_ratio[word] + (self.alpha*DT_error)
                if word in self.DR_ratio:
                    self.DR_ratio[word] = self.DR_ratio[word] + (self.alpha*DR_error)
                if word in self.L_ratio:
                    self.L_ratio[word] = self.L_ratio[word] + (self.alpha*L_error)
                    

            self.alpha = self.alpha * self.decay
                   
                

    def perceptron(self , file_path):

        #   open and preprocess file for testing
        with open(file_path, encoding = 'utf8') as file:
            data = file.read()

        myfile=words_no_stopwords(data)

        file_words = {}
        
        for word in myfile[0]:
            if word in file_words:
                file_words[word] += 1
            else:
                file_words[word] = 1


        DT_score = self.DT_bias;
        DR_score = self.DR_bias;
        L_score = self.L_bias;

        
        for word in file_words:
            
            if word in self.DT_ratio:
                DT_score += self.DT_ratio[word]*file_words[word]
                #print("DT HIT: " + word + ".." + str(DT_score))
            if word in self.DR_ratio:
                DR_score += self.DR_ratio[word]*file_words[word]
                #print("DR HIT: " + word + ".." + str(DR_score))
            if word in self.L_ratio:
                L_score += self.L_ratio[word]*file_words[word]
                #print("L HIT: " + word + ".." + str(L_score))

        return ( DT_score , DR_score , L_score )

    def test_file(self , file_path):
        result = self.perceptron(file_path)
        guess = self.get_win(result)

##        print(file_path + ": " + str(result) + " , " + str(guess))

        return guess

    def test_folder(self , folder_path):

        result_list = [] 

        file_list = os.listdir(folder_path)
        for file in file_list:
            guess  = self.test_file(folder_path + file)
            result_list.append((file , guess))

        return result_list

    def get_win(self , result_tuple):

        max_val = 0
        max_pos = 0
        i = 0

        if result_tuple[2] > 40:
            return "L"

        for guess in result_tuple:
            if guess > max_val:
                max_pos = i
                max_val = guess
            i+=1

        if max_pos == 0:
            return "DT"
        elif max_pos == 1:
            return "DR"
        else:
            return "L"

        
        

def check_result(file_path , file_name , result):

    with open(file_path, encoding = 'utf8') as file:
        data = file.read()

    match_string = file_name + ',(.*)'

    match = re.findall(match_string , data)

    if(len(match) == 1 and match[0] == result):
        return True
    else:
        return False


        
# IMPORTANT 
#call function like so: python3 parser.py ./data/DT ./data/DR ./data/L ./data/TEST
def main():

    if (len(sys.argv) ==5): 
        path=sys.argv[4]
    
        class1=sys.argv[1].split('/')
        class2=sys.argv[2].split('/')
        class3=sys.argv[3].split('/')
    
        
        dirs = [(sys.argv[1] , class1[len(class1)-1]) , (sys.argv[2] , class2[len(class2)-1]) , (sys.argv[3] , class3[len(class3)-1])]
        bag = create_bag(dirs , 0)
        file_list = os.listdir(path)


        with open('output.txt', 'a') as out_file:
            

            for x in file_list:
                result=intelli_grep1(path+'/'+x)
                out_file.write('IG 1,'+result[0]+','+result[1])
                out_file.write('\n')
    
            for x in file_list:
                result=intelli_grep2(path+'/'+x)
                out_file.write('IG 2,'+result[0]+','+result[1])
                out_file.write('\n')

            for x in file_list:
                result=bayes1(path+'/'+x,bag)
                out_file.write('Bayes 2,'+result[0]+','+result[1])
                out_file.write('\n')

            for x in file_list:            
                result=bayes(path+'/'+x,bag)
                out_file.write('Bayes 1,'+result[0]+','+result[1])
                out_file.write('\n')

            per = Per(dirs)
            per.train()
            results = per.test_folder(path+'/')

            for result in results:
                out_file.write('Preceptron,'+result[0]+','+result[1])
                out_file.write('\n')

            
          

    else:
        print()
        print("Pass exactly 4 arguments with program to specify document directories in this fashion.") 
        print()        
        print("parser.py path/to/trainingdr path/to/tainingdt path/to/trainingl path/to/testdocuments")
        print()
        return()

    



#    per = Per()

#    per.train()

#    per.perceptron("./data/TEST/WA_Benton_2009-04-03__2009-008875.txt")
#    per.perceptron("./data/TEST/OR_Lincoln_2008-04-07__08004274.txt")


##    print(check_result(".\\data\\test-results.txt" , 'OR_Coos_2008-04-07__08003475.txt' , 'L'))

    

if __name__ == "__main__":
    main()


















