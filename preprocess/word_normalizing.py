# @author : quynhtt1
# @release-date : 

import re
from word_model import WordModel
"""
This class convert and preprocessing a Vietnamese token into standard form 
In this case, 
"""
class WordNormalizing :

    def __init__ (self) :
        
        self.word_model = WordModel()
        self.convert_dictionary = self.word_model.get_convert_dictionary()

        return 

    
    def __normalize (self, input_text) :
        """normalize sentence into a list of norm format """
        input_list = input_text.split()
        special_list = self.__special_char_detect(input_text)
        special_digit_list = self.__speical_digit_detect(input_text)
        # print (special_digit_list)
        result = []
        for token in input_list :
            if token in special_list :
                result.append(token)
                continue
            """
            if token not in special_digit_list :
                token = self.__remove_nonword(token)
            """

            token = self.__split_num (token)
            result += token
        return result         

    # normalize inner method ########################
    def __special_char_detect(self, text):
        # findall() has been used with valid conditions for urls in string
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
        email = re.findall(r'[\w\.-]+@[\w\.-]+', text)
        return set(urls + email)
    

    def __speical_digit_detect (self, text) :
        percent = re.findall(r'[\d]+%',text)
        digit = re.findall(r'[\d]+[,.][\d]+[\w]+', text)
        digit += re.findall(r'[\d]+[,.][\d]+', text)
        return set(percent + digit)
    

    def __remove_nonword (self, text) :
        return re.sub(r'([^%\w])+', '', text)


    
    
    def __split_num (self, text) :
        return [i for i in re.split(r'([0-9.,]+)', text) if i]
    ######################################
    

    ## PUBLIC METHOD ##
    # 
    def normalize (self, input_text) :
        """ normalize sentence into a list of norm format """
        input_list = self.__normalize(input_text)
        for _ in range(len(input_list)) :
            telex_word = self.word_model.convert_typing(input_list[_])
            if telex_word in self.convert_dictionary :
                input_list[_] = self.convert_dictionary[telex_word]
        return input_list      

    def normalize2 (self, input_text) :
        """ normalize sentence into a list of norm format bigram """
        x = WordNormalizing()
        normalize = x.normalize(input_text)
        t = []
        for i in range(len(normalize)-1) :
            t.append(normalize[i] + str(' ') + normalize[i +1])
        return t




