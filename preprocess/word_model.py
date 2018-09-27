# @author : quynhtt1
# @release-date : 

import pickle
from os.path import join
from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance as distance
from operator import itemgetter

"""
this class provide methods to process all word problems, such as typing distance and telex convert
"""
class WordModel () :

    def __init__(self) :
        
        PATH = "../data"
        
        
        DICTIONARY = join(PATH, "resources/dictionary")
        TELEX = join(PATH, "resources/telex")
        UNIT = join(PATH, "resources/unit")
        


        self.telex = {}
        self.typing = {}
        lines = open(TELEX,"r").readlines()
        for line in lines :
            a,b,c = line.rstrip().split()
            self.telex[a] = [b,c]
            self.typing[(b,c)] = [a]
        a = pickle.load(open('../data/bigram_top.dict', 'rb'))
        self.raw_bigram = set(a.keys())
        self.raw_dictionary = [x.rstrip() for x in open(DICTIONARY).readlines()]
        #self.raw_dictionary = pickle.load(open(DICTIONARY, 'rb')).keys()
        self.raw_dictbi = pickle.load(open(DIC_BI, 'rb'))
        self.set_dictionary = set(self.raw_dictionary)
        self.convert_dictionary = {}
        for word in self.raw_dictionary :
            telex_word = self.__convert_typing(word)
            self.convert_dictionary[telex_word] = word
        ''' VARIABLE understading 
            convert_dictionary : (dict) => { key (a telex word from convert_typing() func)
                                             : value (original word)   }
        '''

        self.unit = set([x.rstrip() for x in open(UNIT, "r").readlines()])

        #self.raw_viet = pickle.load(open('../dictionary/1/viet.dict', 'rb'))
        #self.raw_viet_h = pickle.load(open('../dictionary/1/viet_h.dict', 'rb'))

        return 


## ==== PRIVATE METHOD ======
#
    def __convert_typing (self, word="") :
        """convert a word to typing format (telex used)"""
        result = ""
        tones = set()
        tone_set = set(['r','x','z','j','w','s','f'])
        for _ in range(len(word)) :
            char = word[_]
            if char in self.telex : 
                result += self.telex[char][0]
                for x in self.telex[char][1] : tones.add(x) 
            else :
                if (_ > 2) and (char in tone_set) : tones.add(char)
                else :
                    result += char
        tones = sorted(tones)
        for char in tones : 
            if char != "_" : result += char
        return result 

#
## ==========================




## ==== PUBLIC METHOD ======
#
    def is_right_word (self, word) :
        """ check if a word is right format of vietnamese or not """
        if word in self.set_dictionary :
            return True
        return False

    def is_right_bigram (self, word) :
        if word in self.raw_dictbi :
            return True
        return False


    def convert_typing (self, word) :
        """ convert a word to telex format of itself """
        return self.__convert_typing(word)


    def get_convert_dictionary (self) :
        """ return convert dictionary (dictionary which contain all telex converted word) """
        return self.convert_dictionary

    def get_suggestion (self, word) :
        """ return all suggestion for an input word, used a thres to filter distance  """
        thres = 0.6
        word = self.__convert_typing(word)
        
        result = []
        for token in self.raw_dictionary :
            typing_distance = distance(word, self.__convert_typing(token))
            if typing_distance < thres :
                result.append((token, typing_distance))
        return result

    def is_unit (self, word) :
        if word in self.unit :
            return True 
        return False
#
## =========================
