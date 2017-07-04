"""Word to learn - should be every aspect of language and grammar.
Information about part of sentence.
Questions for better learning and understanding.


LanguageItem
    Word
        Noun
        Verb
        Adverb
    Phrase/Idiom
    

Behavior
    spelling (text) - it is a main thing = so it subclass of str + extra data attached to it :)
    Extra information could be used to build sentences/questions.

Levels
    A1 beginner (Basic)
    A2 elementary (Basic)
    A2+ pre-intermediate (Basic)
    B1 intermediate (Intependent)
    B2 upper intermediate (Intependent)
    C1 advanced (Proficient)
    C2 proficient (Proficient)
"""

#from nouns import dict_txt_nouns
from kivy.core.audio import SoundLoader
from kivy.utils import platform
from functools import partial
from kivy.clock import Clock
import os.path
from plyer import tts
import time


import random
import re
import operator

vowels = ['a', 'e', 'i', 'o', 'u']


def tts_speak (text, *largs):
    tts.speak (text)

class TxtAudioResource (str):
    """contain text + audio resource (audio file or TTS)"""
    def __new__ (cls, text, audio_source = None):
        self = str.__new__ (cls, text)
        self.audio_source = audio_source
        return self
    def play (self, delay = 0):
        Clock.schedule_once (partial(self.play_sound,self),delay)
    def play_sound (self, *largs):
        if self.audio_source and os.path.exists(self.audio_source):
            _sound = SoundLoader.load(self.audio_source)
            _sound.play()
        else:
            if platform == "android":
                tts.speak (self)

class Statements ():
    """ work with statments/questions/answers/instructions - means to learn language items."""
    @classmethod
    def accumulate (cls, self, get_values_function_name, accumulated_field):
        """ Walk via hierarchy of classes started from cls. If class has attribute 'accumulated_field', get values returned by 'get_values_function_name' function and extend resulting list with them.
Return summary list of values.
Problem: method influence 'answer' method - integrity is lost!!! Suggest that 'answer' is the first statement in first class in hierarchy - so depends on order of super classes and multiple inheritance.
Before adding values from list they must be added in reverse order.

Previous version:
There is a issue what we statically bind 'function' to upper class for which accumulate is invoked!!!
    pass function name - not a way as inheritance will not work - we need to pass classified name like cls.function"""
        visited_classes = set()
        def go_through_classes (cls, self):
            #print ('cls:', cls, cls.__dict__[accumulated_field] if accumulated_field in cls.__dict__ else [])
            res = []
            if cls.__bases__:
                #print ('bases')
                #res = res + (function (self)[::-1] if accumulated_field in cls.__dict__ else []) #old version - function in statically binded to highest class function.
                res = res + ( eval('cls.%s(self)' % get_values_function_name)[::-1] if accumulated_field in cls.__dict__ else [])
               
                #print ('res', cls, res)
                for i_class in cls.__bases__:
                    if i_class in visited_classes:
                        break
                    visited_classes.add (i_class)
                    res.extend (go_through_classes (i_class, self))
                
                return res
            else:
                #print ('not bases')
                if accumulated_field in cls.__dict__ and not (cls in visited_classes):
                    visited_classes.add (cls)
                    #res.extend ( function (self)[::-1] )
                    res.extend ( eval('cls.%s(self)' % get_values_function_name)[::-1] )
                    return res
                else:
                    return []
        return  go_through_classes (cls, self)
    @staticmethod
    def _format (patterns_groups, values): #static
        res = []
        for i_value, i_pattern_group in zip(values, patterns_groups):
            for i_pattern in i_pattern_group:
                #print ('i_pattern, i_value', i_pattern, i_value)
                res.append ( i_pattern % i_value if i_value else i_pattern)
        return res
    @classmethod 
    def get_statements (cls, self=None): #may be invoked by class.method or self.method
        return cls._format (cls._statement_patterns, cls._statement_values(self))
    @classmethod 
    def get_questions (cls, self=None): #may be invoked by class.method or self.method
        return cls._format (cls._question_patterns, cls._question_values(self))
    @classmethod
    def _statement_values (cls, self):
        return [(self)]
    @classmethod
    def _question_values (cls, self = None):
        return [(self)]
    @classmethod
    def question (cls, self=None):
        #print (cls._question_patterns, )
        seq = cls.accumulate(self,'get_questions','_question_patterns') + (self.questions if self and 'questions' in self.__dict__ else [])
        #print ('questions:', seq)
        random.shuffle(seq)
        return random.choice(seq)
    @classmethod
    def answer (cls, self=None):
        """ Method depends on order of values returned by 'accumulate' method - integrity is lost!!!
Should be implemented via more deterministic method = only one answer must correspond to one question"""
        #return self.sentence()
        #print ('answer:', self.accumulate(self))
        return cls.accumulate(self,'get_statements','_statement_patterns')[-1]
    @classmethod
    def sentence (cls, self=None):
        #random.shuffle
        seq = cls.accumulate(self,'get_statements','_statement_patterns') + (self.states if self and 'states' in self.__dict__ else [])
        print ('states:', seq)
        random.shuffle(seq)
        return random.choice(seq)

class LanguageItem (TxtAudioResource, Statements):
    """
Look like LanguageItem is static object what is not changing in time - state is the same!!! So we do direct access to data.
Extra information need to proper build LearningMaterial like sentences.
text should be object of TxtAudioResource what contain source to audio
"""
    fields = {'states': [], 'meaning': None}
    def __new__ (cls, text, audio_source = None, **extra):
        self = TxtAudioResource.__new__ (cls, text, audio_source)
        self.default()
        for parameter, value in extra.items():
            if parameter in self.fields or parameter in LanguageItem.fields:
                self.__dict__[parameter] = value
            else:
                print ('WARNING: Field %s is not supposed.' % parameter)
        return self
    def get_article (self):
        """Should be moved to other class (Noun, Adjective)"""
        if self.countable and not self.plural:
            if self[0] in vowels: return 'an'
            else: return 'a'
    def default (self):
        for key, value in self.fields.items():
            if value != None:
                self.__dict__[key] = value
    def __hash__ (self):
        if 'meaning' in self.__dict__:
            return hash(self + self.meaning)
        else:
            return str.__hash__(self)
    def __eq__ (self, other):
        if 'meaning' in self.__dict__:
            obj = self + self.meaning
        else:
            obj = str(self)
        if isinstance(other, LanguageItem) and 'meaning' in other.__dict__:
            other = other + other.meaning
        return str.__eq__(obj,other)



class Word (LanguageItem):
    pass

class Phrase (LanguageItem):
    @classmethod
    def _statement_values (cls, self):
        return [(None)]
    
class Noun (Word):
    """Countable | Uncountable can be defined by context of sentence
Uncountable is the general form - do you like carrot
But how it is related to plural


Each class to populate statements may define
    statement_patterns
    _statement_values

"""
    fields = {'level': None, 'countable': True, 'uncountable': False, 'pluralform': None, 'plural': False, 'article': None, 'live': False}
    #fields.update (Word.fields)
    _statement_patterns = [['%s %s %s.']] #defines patters for class, class related
    _question_patterns = [['%s %s %s?']]
    @classmethod
    def _statement_values (cls, self): #if patterns class related - then values should be class related too but add dynamic - should be redefined 
        return [(this_pronoun.form(plural=self.plural),  ToBe.form(plural=self.plural, person=3, time='presence'), self.usage_form())]
    @classmethod
    def _question_values (cls, self): #if patterns class related - then values should be class related too but add dynamic - should be redefined 
        return [('who' if self.live else 'what', ToBe.form(plural=self.plural, person=3, time='presence'), this_pronoun.form(plural=self.plural))]
        #return [('what' if not self or not self.live else 'who', ToBe.form(plural=self.plural, person=3, time='presence'), this_pronoun.form(plural=self.plural))]
    classmethod
    def answer (cls, self=None):
        return Noun.get_statements(self)[0]
    def get_pluralform (self):
        adding = 's'
        endings = ['s', 'x', 'z', 'ch', 'sh']
        if any ( map (lambda ending: re.search (ending+'$', self),  endings) ):
            adding = 'es'
        if self[-1] == 'y' and not self[-2] in vowels:
            adding = 'ies'
            return self[:-1] + adding
        return self + adding
    def general_form (self):
        if self.uncountable or self.plural:
            return self
        else:
            return self.get_pluralform()
    def usage_form (self):
        if self.uncountable or self.plural:
            return self
        else:
            return '%s %s' % (self.get_article(),self)

    
class NounUsageForm (Noun):
    """provide values to format statements with acticle"""
    @classmethod
    def _statement_values (cls, self):
        return [(self.usage_form())]

class NounGeneralForm (Noun):
    """provide values to format statements without acticle, in plural form is supported"""
    @classmethod
    def _statement_values (cls, self):
        return [(self.general_form())]

class Adjective (Word):
    pass


class Food (NounGeneralForm):
    _statement_patterns = [['do you like %s?', 'i like %s.', "i don't like %s."]]


class Eatable (NounUsageForm):
    _statement_patterns = [["i don't want to eat %s."]]

class EatableFood (Food, Eatable):
    pass

class Drinkable (NounUsageForm):
    _statement_patterns = [["i don't want to drink %s."]]

class Drinks (Drinkable, Food):
    pass

    
class DrinkThirsty (Drinks):
    _statement_patterns = [["i'm thirsty. i would like %s."]]

class FoodHungry (Food):
    _statement_patterns = [["i'm hungry. i would like %s."]]
    @classmethod
    def _statement_values (cls, self):
        return NounUsageForm._statement_values(self)

class Vegetables (Food, Eatable):
    pass

class Fruits (Food, Eatable):
    pass
class Berries (Food, Eatable):
    pass

#mixing classes
class Herbivore (NounUsageForm): #an animal that eats only plants
    _statement_patterns = [['%s eats plants.', '%s eats grass, and, leaves.']]
class Carnivore (NounUsageForm): #an animal that eats meat
    _statement_patterns = [['%s eats animals.', '%s eats meat.']]
class Land (NounUsageForm): #an animal what can live on land and has 4 legs, can walk and run
    _statement_patterns = [['%s has four legs', '%s can walk.', '%s can run.']]
class Water (NounUsageForm): #an animal what can live in water and can swim
    _statement_patterns = [['%s can swim.']]
class HasTail (NounUsageForm):
    _statement_patterns = [['%s has a tail.']]
class FurSkin (NounUsageForm):
    _statement_patterns = [["the body of %s is covered with fur."]]
#end mixing classes

class Animals (NounUsageForm):
    pass

class Mammals (Animals):
    _statement_patterns = [['%s feeds, its babies, on milk.']]

class LandMammals (Mammals,Land,HasTail,FurSkin):
    pass
    
class LandHerbivoreMammals (LandMammals, Herbivore):
    pass

class LandCarnivoreMammals (LandMammals, Carnivore):
    pass

class WaterMammals (Mammals, Water, HasTail):
    _statement_patterns = [['%s eats fish.']]
class FishMammals (Mammals, Water, HasTail):
    _statement_patterns = [['%s eats fish.']]
class Whale (Mammals, Water, HasTail):
    _statement_patterns = [['%s is the biggest animal, on our planet.']]
class Fish (Animals, Water, HasTail):
    pass

class Birds (Animals):
    _statement_patterns = [['the body of %s, is covered, with feathers.', '%s can fly.']]
    
class WaterBirds (Birds,Water):
    pass



class Vehicles (NounUsageForm):
    pass

class RideVehicles (Vehicles):
    _statement_patterns = [['can you ride %s?','i can ride %s.',"i can't ride %s."]]
class DriveVehicles (Vehicles):
     _statement_patterns = [['can you drive %s?','i can drive %s.',"i can't drive %s."]]
class FlyVehicles (Vehicles):
    _statement_patterns = [['can you fly %s?','i can fly %s.',"i can't fly %s."]]
class SailVehicles (Vehicles):
    _statement_patterns = [['can you sail %s?','i can sail %s.',"i can't sail %s."]]
    

class Clothes (NounUsageForm):
    _statement_patterns = [['do you wear %s?','i wear %s.',"i don't wear %s."]]


class Board (NounUsageForm):
    _statement_patterns = [['there is %s, in the classroom.']]
class WrittenTool (NounUsageForm):
    _statement_patterns = [['%s, is used, for writing, and drawing.']]



class Professions (NounUsageForm):
    _statement_patterns = [["I'm %s by profession.", 'I want to be %s.', "I don't want to be %s.", 'Do you want to be %s.']]
    def __new__ (cls, *args, **kwargs):
      self = Noun.__new__ (cls, *args, **kwargs)
      self.live = True
      return self
      
class Feelings (Adjective):
    _statement_patterns = [["I'm %s.", 'Are you %s?']]
    _question_patterns = [["how are you?",'how do you feel?']]
#    def question (self):
#        questions = ["how are you?",'how do you feel?']
#        return random.choice(questions)

    

class Weather (Adjective):
    _statement_patterns = [["it's %s.",'do you like %s weather?', 'i like %s weather.', "i don't like %s weather."]]
    _question_patterns = [["what's the weather like?","how's the weather?"]]
#    def question (self):
#        questions = ["what's the weather like?","how's the weather?"]
#        return random.choice(questions)


class Colour (Adjective):
    _statement_patterns = [["this is the %s colour.",'is %s, your favourite colour?', 'the %s colour, is not my favourite.', "my favourite colour, is %s."]]
    _question_patterns = [["what colour is this?"]]
#    def question (self):
#        questions = ["what colour is this?"]
#        return random.choice(questions)
      
class Room (Noun):
    _question_patterns = [["what room %s %s?"]]
    @classmethod
    def _question_values (cls, self):
        return [(ToBe.form(plural=self.plural, person=3, time='presence'), this_pronoun.form(plural=self.plural))]
#    def question (self):
#        return ' '.join(['what room', ToBe.form(plural=self.plural, person=3, time='presence'), this_pronoun.form(plural=self.plural)]) + '?'

class Furniture (NounUsageForm):
    _statement_patterns = [["where is %s, in your flat?"]]

class RoomPart (NounUsageForm):
    _statement_patterns = [["%s, is a part, of a room."]]

class OpenRoomPart (RoomPart):
    _statement_patterns = [["you can open %s.", "you can close %s."]]



class Time (Adjective):
    _statement_patterns = [["it's %s."]]
    _question_patterns = [['what time is it?']]
    fields = Noun.fields.copy()
    fields.update ({'order': 0})
#    def question (self):
#        return 'what time is it?'

class OrderedPeriod (Time):
    @classmethod
    def _statement_values (cls, self):
        return [(self,self.order)]
    @classmethod
    def _question_values (cls, self):
        return [(self.order)]

class Weekday (OrderedPeriod):
    _statement_patterns = [["%s, is the %s day, of the week."]]
    _question_patterns = [["what is, the %s day, of the week?"]]
#    def question (self):
#        return 'what is, the %s day, of the week?' % self.order

class Month (OrderedPeriod):
    _statement_patterns = [["%s, is the %s month, of the year."]]
    _question_patterns = [['what is, the %s month, of the year?']]
#    def question (self):
#        return 'what is, the %s month, of the year?' % self.order

class Season (Noun):
    _question_patterns = [['what season is this?']]
#    def question (self):
#        return 'what season is this?'

class Verb (Word):
    fields = {'level': None}

class ToBe (Verb):
    @staticmethod
    def form (person=3, time='presence', plural=False):
        if time == 'presence':
            if person == 1:
                return 'am'
            elif person == 2:
                return 'are'
            elif person == 3:
                if not plural:
                    return 'is'
                else:
                    return 'are'
    @staticmethod
    def short_form (person=3, time='presence', plural=False):
        if time == 'presence':
            if person == 1:
                return 'm'
            elif person == 2:
                return 're'
            elif person == 3:
                if not plural:
                    return 's'
                else:
                    return 're'
   
        



class Adverb (Word):
    pass










class Activity (Word):
    pass
        

#########################################
# Attempt to create interactive excercies
#########################################
"""
personal
talking about 2-st person (you), 3-rd person (he, she) = Subject
Object = me, you, him, her

Possessive determiners
    my
    your
    his
    her

Possessive pronouns
    mine
    yours
    his
    hers
    its
    ours
    yours
    theirs

interaction between PC(imagine person 1-st) and student (2-nd) about 1-st person(pc), 2-nd person (student), 3-rd person ()

we have
    interaction
    pc = 1-st person
    student = 2-nd person
    3-rd person(subject) = pc|student|3-rd person

"""
def part_of_day():
    hour = time.localtime().tm_hour
    if 0 <= hour <= 5:
        return 'night'
    if 6 <= hour <= 11:
        return 'morning'
    if 12 <= hour <= 17:
        return random.choice(['day','afternoon'])
    if 18 <= hour <= 23:
        return 'evening'

#
#Pronoun
#
class Pronoun (Word):
    fields = {'level': None, 'pluralform': None, 'plural': False, 'meaning': None}
    def form (self, plural=False):
        if plural:
            return self.pluralform
        else:
            return str(self)

def possessive_pronoun (grammar_person = 1, sex='male'):
    """ Implemented only for single form """
    if grammar_person == 1:
        return 'my'
    elif grammar_person == 2:
        return 'your'
    elif grammar_person == 3:
        if sex == 'male':
            return 'his'
        else:
            return 'her'

def personal_pronoun (grammar_person = 1, sex='male'):
    """ Implemented only for single form """
    if grammar_person == 1:
        return 'i'
    elif grammar_person == 2:
        return 'you'
    elif grammar_person == 3:
        if sex == 'male':
            return 'he'
        else:
            return 'she'

class Greetings (Phrase):
    _statement_patterns = [['Hi.','Hello.'],['Good %s.']]
    @classmethod
    def _statement_values (cls, self):
        return [(None),(part_of_day())]

class Farewell (Phrase):
    _statement_patterns = [['Goodbye!', 'Bye!', 'Bye bye!', 'See you.', 'See you soon.', 'Take care.']]

"""
use format method and named agruments
"""
class PersonRelatedProperty (Phrase):
    
    def __new__ (cls, property_name):
        class _ClassProperty(PersonRelatedProperty):
            #_question_patterns = [["what is %s {0}?".format(property_name),"what's %s {0}?".format(property_name)]]
            @classmethod
            def _question_values (cls, self):
                return [(possessive_pronoun(self.grammar_form, self.sex))]
        _ClassProperty.property_name = property_name
        return _ClassProperty
    @classmethod
    def instruction (cls, self):
                    kwargs = {'pronoun': possessive_pronoun(self.grammar_form, self.sex),
                              'property_name': cls.property_name}
                    instructions = list(map (lambda phrase: phrase.format (**kwargs), ["ask me about {pronoun} {property_name}."] ))
                    return random.choice(instructions)

class PossessiveProperty(PersonRelatedProperty):
    #property_name =
    def __new__ (cls, property_name):
        class _ClassProperty(PersonRelatedProperty(property_name)):
                _statement_patterns = [['%s {0} is %s.'.format(property_name), "%s {0}'s %s.".format(property_name)]]
                #_question_patterns = [["what is %s {0}?".format(property_name),"what's %s {0}?".format(property_name)]]
                @classmethod
                def _statement_values (cls, self):
                    return [(possessive_pronoun(self.grammar_form, self.sex), self.__dict__[property_name])]
                
#                @staticmethod
#                def question (self):
#                    kwargs = {'pronoun': possessive_pronoun(self.grammar_form, self.sex),
#                              'property_name': _ClassProperty.property_name}
#                    questions = list(map (lambda phrase: phrase.format (**kwargs), ["what is {pronoun} {property_name}?","what's {pronoun} {property_name}?"] ))
#                    return random.choice(questions)
                
        _ClassProperty.property_name = property_name
        return _ClassProperty

class PersonalProperty(PersonRelatedProperty):
    #property_name = 
    def __new__ (cls, property_name):
        class _ClassProperty(PersonRelatedProperty(property_name)):
            _statement_patterns = [['%s %s %s.'], ["%s'%s %s."]]
            _question_patterns = [["what is %s {0}?".format(property_name),"what's %s {0}?".format(property_name)]]
            @classmethod
            def _statement_values (cls, self):
                return [(personal_pronoun(self.grammar_form, self.sex), ToBe.form(person=self.grammar_form), self.__dict__[property_name]),
                        (personal_pronoun(self.grammar_form, self.sex), ToBe.short_form(person=self.grammar_form), self.__dict__[property_name])]
            
        _ClassProperty.property_name = property_name
        #print ('PersonalProperty, _question_patterns', _ClassProperty._question_patterns)
        return _ClassProperty

class AbstractProperty(PersonRelatedProperty):
    #property_name = 
    def __new__ (cls, property_name):
        class _ClassProperty(PersonRelatedProperty(property_name)):
            pass
        _ClassProperty.property_name = property_name
        return _ClassProperty
            
class Name (PersonalProperty('name'), PossessiveProperty('name')):
    pass
#print ('Name, _question_patterns', Name._question_patterns)
    

#class Age (PersonalProperty('age'), PersonalProperty('age long')):
class Age (AbstractProperty('age')):
    _statement_patterns = [['%s %s %s.', '%s %s %s years old.'], ["%s'%s %s.", "%s'%s %s years old."]]
    _question_patterns = [["how old %s %s?"]]
    @classmethod
    def _statement_values (cls, self):
        return [(personal_pronoun(self.grammar_form, self.sex), ToBe.form(person=self.grammar_form), self.__dict__[cls.property_name]),
                (personal_pronoun(self.grammar_form, self.sex), ToBe.short_form(person=self.grammar_form), self.__dict__[cls.property_name])]
    @classmethod
    def _question_values (cls, self):
        return [(ToBe.form(person=self.grammar_form), personal_pronoun(self.grammar_form, self.sex))]
#    @staticmethod
#    def question (self):
#            kwargs = {'pronoun': personal_pronoun(self.grammar_form, self.sex),
#                      'to_be': ToBe.form(person=self.grammar_form)}
#            questions = list(map (lambda phrase: phrase.format (**kwargs), ["how old {to_be} {pronoun}?"] ))
#            return random.choice(questions)
class Country (PersonRelatedProperty('country')):
    _statement_patterns = [['%s %s from %s.'], ["%s'%s from %s."]]
    _question_patterns = [["where %s %s from?"]]
    @classmethod
    def _statement_values (cls, self):
        return [(personal_pronoun(self.grammar_form, self.sex), ToBe.form(person=self.grammar_form), self.__dict__[Country.property_name]),
                (personal_pronoun(self.grammar_form, self.sex), ToBe.short_form(person=self.grammar_form), self.__dict__[Country.property_name])]
    @classmethod
    def _question_values (cls, self):
        return [(ToBe.form(person=self.grammar_form), personal_pronoun(self.grammar_form, self.sex))]
#    @staticmethod
#    def question (self):
#        kwargs = {'pronoun': personal_pronoun(self.grammar_form, self.sex),
#                  'to_be': ToBe.form(person=self.grammar_form)}
#        questions = list(map (lambda phrase: phrase.format (**kwargs), ["where {to_be} {pronoun} from?"] ))
#        return random.choice(questions)

class Nationality (PersonalProperty('nationality')):
    pass
#    @staticmethod
#    def question (self):
#        return PossessiveProperty('nationality').question (self)

class Person (Noun):
    """Include name, age, nationality and other behaviour via mixing classes or via LearningItem -> Interaction???
name: Sophia
age: 5
country: Ukraine
city: Kyiv
sex: male|femail
"""
    fields = {'name': '', 'sex': '', 'favourite colour': '', 'favourite drink': '', 'age': '', 'country': '', 'nationality': '', 'visual_source': '', 'plural': False, 'uncountable': False, 'countable': True}
    def __init__ (self, **kwargs):
        self.set_grammar_form()
        if 'age' in self.__dict__:
            self.__dict__['age long'] = self.age + ' years old'
    def set_grammar_form (self, grammar_form = 1):
        self.grammar_form = grammar_form
        #self.__dict__['favorite color'] = 'blue'
        return self
       

this_pronoun = Pronoun ('this',pluralform = 'these')



def load_nouns (dict_yaml):

    dict_yaml = { 'animals': [['a', 'cat', 'A1'], ['a', 'dog', 'A1'], ['a', 'cow', 'A1']], 'vehicles': [['a','car', 'A1'], ['a','bus','A1']], 'clothes': [['a','dress','A1'], ['a','t-shirt','A1']] }
    
    dict_nouns = {}
    for topic in dict_yaml:
        dict_nouns[topic] = []
        for i_obj in dict_yaml[topic]:
            text = i_obj[1]
            level = i_obj[2]
            extra = i_obj[0]
            dict_nouns[topic].append(Noun(text))
    return dict_nouns


#words_by_topic = load_nouns (dict_txt_nouns)


if __name__ == '__main__':
    pass
    #import yaml
    str_yaml = """animals:
    black cat: {part: Noun, level: A1, countable: True, pluralform: cats, plural: False, article: a, sentence: &sentence 'This is a cat.', question: 'What is this?', answer: *sentence}
"""
    #dict_yaml = yaml.load (str_yaml.replace('\t','  '))
    #print (dict_yaml)

    #cat = Noun ('shorts',plural=True)
    #print (cat.sentence(cat))
    #print (cat.get_statements(cat))
    #print ('cat', cat.accumulate(cat,cat.get_statements,'_statement_patterns'))
    #print (cat.question())
    #print (cat.answer())

    
    olya = Person (text = 'Olya', name = 'Olya', age='three', sex= 'female', country= 'Ukraine', nationality='ukrainian',
                   **{'favourite colour': 'blue', 'favourite drink': 'orange juice', 'age long': 'three years old'})
    
    #sophia = Person (name = Name('Sophia'), determiner = 'her', pronoun = 'she')
    #print (olya.accumulate(olya))
    #print ('Good',part_of_day())
    #print (Name('Sophia').get_statements(olya))
    #print (Name('Sophia').question('her'))
    #print (PersonalName.get_statements(olya))
    #print (PossesiveName.get_statements(olya))
    
    #print ( property_class(PossessiveProperty, 'name').get_statements(olya.set_grammar_form(1)), property_class(PersonalProperty, 'name').get_statements(olya.set_grammar_form(1)) )
    #print (Name.accumulate(olya.set_grammar_form(1)))
    """
    print ( PossessiveProperty('favourite colour').get_statements(olya.set_grammar_form(2)) )
    print ( PossessiveProperty('favourite drink').get_statements(olya.set_grammar_form(3)) )
    
    print ('Age:',Age.sentence(olya.set_grammar_form(3)))
    

    print (Name.question(olya.set_grammar_form(3)))
    print (PossessiveProperty('favourite colour').question(olya.set_grammar_form(3)))
    print (PossessiveProperty('favourite drink').question(olya.set_grammar_form(3)))
    print ('Age:', Age.question(olya.set_grammar_form(2)))

    print ('favourite drink:', PossessiveProperty('favourite drink').answer(olya.set_grammar_form(1)))

    print (PossessiveProperty('name').instruction(olya.set_grammar_form(2)))
    print (PossessiveProperty('age').instruction(olya.set_grammar_form(2)))
    print (PossessiveProperty('favourite colour').instruction(olya.set_grammar_form(2)))
    print (PossessiveProperty('favourite drink').instruction(olya.set_grammar_form(2)))
    

    print (Greetings.get_statements(olya))
    
    print (Greetings('greetings').answer())

    print (Nationality.answer(olya.set_grammar_form(2)))
"""
    #print ('Greeting:', Greetings('greetings').answer())
    print ('Name:', Name.question(olya.set_grammar_form(2)))
    #print ('Favourite colour:', PossessiveProperty('favourite colour').question(olya.set_grammar_form(2)))
    #print ('Age:',Age.question(olya.set_grammar_form(2)))
    #print ('Country:', Country.question(olya.set_grammar_form(2)))

    
