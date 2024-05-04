import random

NOT_ENOUGH_WORDS_MSG = "Not enough words in dict. Write more messages."

NOT_ENOUGH_WORDS_ERR = -1
NOT_FOUND = -1

class SLM:

    def __init__(self, custom_dict = {}, words_range = [5, 15], sentences_range = [1, 1], forbidden_words = ["@", "discord.gg"]):
        self._dict = custom_dict
        self._forbidden_words = forbidden_words
        self._words_range = words_range
        self._sentences_range = sentences_range

    def learn(self, text: str):
        print(text.split())

        #try:
        last_word = None

        for word in (text.split()):
            #filter which returns when the word is ban word
            for forbidden_word in self._forbidden_words:
                    if (word.find(forbidden_word) != NOT_FOUND):
                        return
            
            if last_word == None:
                last_word = word
                continue
            
            if not (last_word in self._dict.keys()):
                self._dict[last_word] = []
            
            if not (containts_target(self._dict[last_word], word)):
                self._dict[last_word].append(word)
            
            last_word = word

        return 0
        
        print(self._dict)
        #except:
            #return 1
    
    #Generates text with few genereted sentences
    def generate_text(self, root: str):
        result = ""
        sentence_count = random.randint(self._sentences_range[0], self._sentences_range[1])

        for i in range(sentence_count):
            generated_sentence = self.generate_sentence(root=root)
            if (generated_sentence == NOT_ENOUGH_WORDS_ERR):
                return NOT_ENOUGH_WORDS_MSG
            
            result += generated_sentence + random.choice([". ", ". ", ". ", "! ", "!!! ", "? "])

        return result

    #generetes sentence with random words from dict
    def generate_sentence(self, root: str):
        result = ""
        sentence_lenght = random.randint(self._words_range[0], self._words_range[1])
        
        if (self._dict == None):
            return NOT_ENOUGH_WORDS_ERR
        
        dict_keys = list(self._dict.keys())

        if (dict_keys == []):
            return NOT_ENOUGH_WORDS_ERR

        if (root != None) & (root in dict_keys):
            word = root
        else:
            word = random.choice(dict_keys)

        result += word
        
        for i in range(sentence_lenght):
            current_words = self._dict.get(word, [])

            if current_words == []:
                break
            else:
                word = random.choice(current_words)
                result += ' ' + word
        
        return result

    ###Getters/Setters
    def dict_set(self, new_dict: dict):
        self._dict = new_dict
    
    def dict_get(self):
        return self._dict



#Checks if list containts target
def containts_target(object, target):

    target_lenght = len(target)
    i = 0
    for char in object:
        if char == target[i]:
            i += 1
            if i >= target_lenght:
                return True
        else:
            i = 0