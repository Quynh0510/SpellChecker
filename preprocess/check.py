# @author : quynhtt1
# @release-date : 
from word_normalizing import WordNormalizing
from word_model import WordModel
from probality_model import ProbalityModel
import pickle
from pyvi import ViTokenizer

"""
detect and fix spell error in sentence
input : a list which is sentence after normalizing
output : a list which fixed spell errors
"""
class SpellCheck () :

    def __init__ (self) :
        self.word_normalizing = WordNormalizing()
        self.word_model = WordModel()
        self.probality_model = ProbalityModel()
        self.dictionary = set(open('../data/dictionary', 'r').read().split('\n'))
        self.bigram = pickle.load(open('../data/bigram/bigram.dict', 'rb'))
        #self.DIC_BI = pickle.load(open('../data/bigram/Viet.dict', 'rb'))
        #self.DIC_BI = set(open('../dictionary/wordlist.txt', 'r').read().split('\n'))
        self.pre = pickle.load(open('../data/bigram/viet.dict', 'rb'))
        self.suf = pickle.load(open('../data/bigram/viet_h.dict', 'rb'))
        a = pickle.load(open('../data/bigram_top.dict', 'rb'))
        self.raw_bigram = set(a.keys())
        return

    
## ==== PRIVATE METHODS =====
#    
    def __fix_nonword (self, word, prefix, suffix) :
        """ get suggestion and ranking them to return the best suggestion 
            ranking-1 :ranking by typing distance
            raking-2 : ranking by probality score    
            score = m1 * ranking1 + m2 * ranking2 """
        def sorting_algo (input_list) :
            filter_list = sorted(list(set(input_list)))
            result_list = [filter_list.index(x) for x in input_list]
            return result_list
        # --
        suggestions = self.word_model.get_suggestion(word)
        result = [[], [], []]  # [sg, distance_score, probality_score]

        for sg, distance_score in suggestions :
            frequency_score = self.probality_model.get_frequency_score(sg, prefix, suffix)
            if frequency_score != 0 :
                result[0].append(sg)
                result[1].append(distance_score)
                result[2].append(1-frequency_score)
        
        result[1] = sorting_algo (result[1])
        result[2] = sorting_algo (result[2])
        
        result = [(result[0][i], result[1][i], result[2][i]) for i in range(len(result[0]))]
        
        M_1 = 5
        M_2 = 5
        best_option = ['', 1000]   # 100 : just a big number
        for sg, score_1, score_2 in result :
            score = M_1 * score_1 + M_2 * score_2
            if score < best_option[1] :
                best_option = [sg, score]
                # print (best_option)
                
        return best_option[0]
    

    def __fix (self, sentence) :
        '''return fixed sentence (type list) '''
        def is_unit (word, prefix) :
            if len(prefix) < 1 : return False
            if word[0].isdigit() : return True
            if prefix[0].isdigit() and self.word_model.is_unit(word) :
                return True
            return False
        def is_pronoun (word) :
            if word[0].isupper() : return True
            return False
        # --
        result = []
        for i in range(len(sentence)) :
            word = sentence[i]
            prefix = '' if i == 0 else result[i-1] if len(result)==i else sentence[i-1]
            suffix = '' if i == len(sentence)-1 else sentence[i+1]
            # print (word, prefix, suffix)
            if is_unit(word, prefix) or is_pronoun(word) :
                result.append(word)
                continue


            if (prefix + ' ' + word) not in self.raw_bigram or (word + ' ' + suffix) not in self.raw_bigram :
                replacing_word = self.__fix_nonword (word, prefix, suffix)
                if replacing_word != '' :
                    result.append(replacing_word)
                else :
                    result.append(word)
            else :
                result.append(word)
            
        return result    

#
## ==========================
    """
    def fix_nonword (self, word, prefix, suffix) :
        return self.__fix_nonword(word, prefix, suffix)
    """

## ==== PUBLIC METHODS =====
#    
    def check(self, sentence) :
        
        # normalize 
        sentence = self.word_normalizing.normalize(input_text=sentence) 
        # detect and fix
        sentence = self.__fix(sentence=sentence)
        return ' '.join(sentence)


from datetime import datetime
s = datetime.now()
x = SpellCheck()
#text = "Thu Trang: Xuất thân danh đình giàu có, phá sả xống khổ cực và cuộc tình đắc biệt vúi Tiến Luật?"
text = '''
Trong bài văn, Thảo viết: “Máy quay giường như đang chậm lại, 
từng cảnh từng nét hiện nên rõ dàng. 
Tôi thấy thầy đang lụi hụi trồng rau, 
chăm sóc con chó loong trắng đen già khụ, thấy cả chúng tôi ngày đó, 
trong những ngày vất vả nhưng yên bình. 
Tôi nghĩ, có lẽ đó là những ngày hạnh phúc và vui vẻ nhất tôi từng có. 
Sau này, khi bước đi trên đường đờij chông gai, 
có thể sẽ chẳng còn ai chỉ bảo, dạy dỗ tôi tận tình như thầy đã từng, 
có thể sẽ chẳng có ai lo tôi liệu có ngủ đủ giấc, 
liệu có stress khi nhồi nhét quá nhiều. Nhưng, cố nhân từng nói, 
cuộc đời chỉ cần một người khiến ta ngưỡng mộ, để cả đời noi gương, 
cả đời thương mến. Vậy nà quá đủ rồi”.
'''
import string
punct = set(string.punctuation)
for i in punct :
    text = text.replace(i, "@")
text = text.split('@') 
for i in text :
    print(x.check(i))
e = datetime.now()
print(e-s)

