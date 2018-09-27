# @author : quynhtt1
# @release-date : 

import pickle 
from os.path import join
"""
this class provides methods to calculate based on probality
"""
class ProbalityModel () :
    
    def __init__ (self) :
        
        PATH = "../data/"
        BIGRAM_PATH = join(PATH, "bigram_top.dict")
        FREQUENCY_PATH = join(PATH, "frequency.dict")
        
        self.bigram = pickle.load(open(BIGRAM_PATH, 'rb'))
        self.frequency = pickle.load(open(FREQUENCY_PATH, 'rb'))

        return


## ===  PRIVATE METHODS  ===
# 


    
#
## ==========================



## === PUBLIC METHODS ===
#
    
    def get_frequency_score (self, word, prefix, suffix) :
        """ """
        FREQUENCY_MIN = 5
        if word not in self.frequency :
            return 0
        if self.frequency[word] < FREQUENCY_MIN :
            return 0
        suffix_probality1 = self.bigram.get(word + ' ' + suffix, 0) / (self.frequency.get(suffix, 0.1)+1)
        suffix_probality2 = self.bigram.get(word + ' ' + suffix, 0) / (self.frequency.get(word, 0.1)+1)
        prefix_probality1 = self.bigram.get(prefix + ' ' + word, 0) / (self.frequency.get(prefix, 0.1)+1)
        prefix_probality2 = self.bigram.get(prefix + ' ' + word, 0) / (self.frequency.get(word, 0.1)+1)
        #return max([suffix_probality1, prefix_probality1, suffix_probality2, prefix_probality2]), prefix_probality1, suffix_probality1, prefix_probality2, suffix_probality2
        return max([suffix_probality2, prefix_probality2, suffix_probality1, prefix_probality1])
    """
    def get_frequency_score (self, word, prefix, suffix) :
        """ """
        FREQUENCY_MIN = 5
        if word not in self.frequency :
            return 0
        if self.frequency[word] < FREQUENCY_MIN :
            return 0
        suffix_probality = self.bigram.get(word + ' ' + suffix, 0) / (self.frequency.get(suffix, 0.1) + 1)
        prefix_probality = self.bigram.get(prefix + ' ' + word, 0) / (self.frequency.get(prefix, 0.1) + 1)
        return max([suffix_probality, prefix_probality])
    """
#
## ======================
