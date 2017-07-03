"""Student recognized by name attends lessons to learn English Language (vocabulary + usage = communicate) improving knowledge with each lesson.
Student can have specific learning plan what defines LearningMaterials and Activities
Student with each lesson improve knowledge
Student = name, knowledge, learning plan = class to manipulate all these stuff/things
"""


import functools
import operator
import pickle
import os.path
import random

class KnowledgeRate ():
    """ number representing knowledge rate and manipulating it. Knowledge is as trigger = learn, learn, know. Correct/Wrong answer = +- 0.2 (delta)"""
    def __init__ (self, rate = 0.0):
        self.rate = rate
        self._appearence = 0
        self._correct = 0
        self._delta = 0.2
    def add_appearence (self):
        self._appearence += 1
        #self._recalculate()
    def increase (self):
        self._correct += 1
        self._recalculate(self._delta)
    def decrease (self):
        self._recalculate(-self._delta)
    def _recalculate (self, delta):
        self.rate += delta
        if self.rate > 1.0:
            self.rate = 1.0
        if self.rate < 0.0:
            self.rate = 0.0
    def probability (self):
        if self.rate != 0 or self._appearence == 0: return self.rate
        elif self._correct > 0: return 0.3
        elif self._appearence >= 5: return 0.5
        else: return 1 - 1/(self._appearence*1.5) 
    def efficiency (self):
        return round(self._correct/self._appearence, 2) if self._appearence != 0 else 0
    def rate (self):
        return self.rate
    def __str__ (self):
        return  '{0:.2f} {1} {2} {3}'.format(self.rate, self.efficiency(), self._appearence, self._correct)

class Knowledge ():
    """Dictionary to map LanguageItem to KnowledgeRate and method to manipulate it"""
    def __init__ (self, items=None):
        self._knowledge = {} if not items else dict(items)
        self.knowledge = self._knowledge
    def load (self, knowledge_file): #load dictionary from pickle file
        if os.path.exists(knowledge_file):
            f_knowledge = open(knowledge_file, 'rb')
            self._knowledge = pickle.load(f_knowledge)
            f_knowledge.close()
        else:
            print ('File {} does not exist!'.format(knowledge_file))
        
    def save (self, knowledge_file): #save current dictionary to pickle file
        f_knowledge = open(knowledge_file, 'wb')
        pickle.dump(self._knowledge, f_knowledge)
        f_knowledge.close()
        
    def update (self, languageitem, update_type = 'appearence'): #add new/unknown LanguageItem + update rate after appearence or correct answer
        if not languageitem in self._knowledge:
            self.extend ([languageitem])
        if update_type == 'appearence':
            self._knowledge[languageitem].add_appearence()
        if update_type == 'correct':
            self._knowledge[languageitem].increase()
        if update_type == 'wrong':
            self._knowledge[languageitem].decrease()
        
    def extend (self, seq): #extend knowleadge with new/unknown LanguageItems
        for i_lang_item in seq:
            if not i_lang_item in self._knowledge: self._knowledge[i_lang_item] = KnowledgeRate ()
    def filter_rate (self, low_rate = 0, high_rate = 1.1):
        return Knowledge(filter ( lambda item: high_rate > item[1].rate >= low_rate,  self._knowledge.items()))
    def filter (self, seq):
        return Knowledge(filter (lambda item: item[0] in seq, self._knowledge.items()))
    def keys (self):
        return self._knowledge.keys()
    def __getitem__ (self, index):
        return self._knowledge[index]
    def __str__ (self):
        return '\n'.join ( map(lambda item: '{}\t{}'.format(*item), self._knowledge.items()) )
    


class Student ():
    """Person with name, knowledge, learning plan and behaivior to manipulate all these stuff/things"""
    def __init__ (self, name):
        self.name = name
        self.knowledge = Knowledge()
        self.knowledge.load ('{}.pkl'.format(self.name)) #load knowledge during student creation
    def __del__ (self):
        self.knowledge.save ('{}.pkl'.format(self.name))
        





    
    

#learn_words = functools.reduce (operator.add, word.words_by_topic.values())




import learningmaterials

if __name__ == '__main__':
    oleksandr = Student ('Oleksandr')
    oleksandr.knowledge.update (learningmaterials.dog,'appearence')
    oleksandr.knowledge.update (learningmaterials.sheep,'appearence')
    oleksandr.knowledge.update (learningmaterials.cow,'appearence')
    
    
    oleksandr.knowledge.update (learningmaterials.cat,'correct')
    #oleksandr.knowledge.update (learningmaterials.dog,'correct')
    #oleksandr.knowledge.update (learningmaterials.cat,'correct')
    #oleksandr.knowledge.update (learningmaterials.dog,'wrong')
    print (oleksandr.knowledge)
    print (oleksandr.knowledge.filter_rate(0,0.41))
    del (oleksandr)


    
    """
    if os.path.exists('olya.pkl'):
        f_student = open('olya.pkl', 'rb')
        olya = pickle.load(f_student)
    else:
        olya = Student ('Olya','A1')
    olya.add_words ( learn_words )

    if os.path.exists('sophia.pkl'):
        f_student = open('sophia.pkl', 'rb')
        sophia = pickle.load(f_student)
    else:
        sophia = Student ('Sophia','A2')
    sophia.add_words ( learn_words )

    
    progress = sophia.get_progress()
    for i_word in progress:
        print (i_word.get_text(), progress[i_word])
"""
