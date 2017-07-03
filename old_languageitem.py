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
    @classmethod
    def accumulate (cls, self):
        visited_classes = set()
        def go_through_classes (cls, self):
            res = []
            if cls.__bases__:
                for i_class in cls.__bases__:
                    if i_class in visited_classes:
                        break
                    visited_classes.add (i_class)
                    res.extend (go_through_classes (i_class, self))
                
                return res + (cls.get_statements (self) if 'get_statements' in cls.__dict__ else [])
            else:
                if 'get_statements' in cls.__dict__ and not (cls in visited_classes):
                    visited_classes.add (cls)
                    res.extend ( cls.get_statements (self) )
                    return res
                else:
                    return []
        return  go_through_classes (cls, self)

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
    #def sentence (self):
    #    pass
    def question (self):
        pass
    def answer (self):
        return self.sentence()
    def sentence (self):
        #random.shuffle
        seq = self.accumulate(self) + (self.states if 'states' in self.__dict__ else [])
        #print ('seq:',seq)
        random.shuffle(seq)
        return random.choice(seq)

class Word (LanguageItem):
    pass

class Phrase (LanguageItem):
    pass
    
class Noun (Word):
    """Countable | Uncountable can be defined by context of sentence
Uncountable is the general form - do you like carrot
But how it is related to plural
"""
    fields = {'level': None, 'countable': True, 'uncountable': False, 'pluralform': None, 'plural': False, 'article': None, 'live': False}
    def question (self):
        return ' '.join(['who' if self.live else 'what', ToBe.form(plural=self.plural, person=3, time='presence'), this_pronoun.form(plural=self.plural)]) + '?'
    def answer (self):
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
        
    def get_statements (self):
        return [' '.join([this_pronoun.form(plural=self.plural), ToBe.form(plural=self.plural, person=3, time='presence'), self.usage_form()+'.'])]



class Adjective (Word):
    pass


class Food (Noun):
    def get_statements (self):
        return  list(map (lambda phrase:  phrase % self.general_form(), ['do you like %s?', 'i like %s.', "i don't like %s."] ))

class Eatable ():
    def get_statements (self):
        return ["i don't want to eat %s." % self.usage_form()]

class EatableFood (Food, Eatable):
    pass

class Drinkable ():
    def get_statements (self):
        return ["i don't want to drink %s." % self.usage_form()]

class Drinks (Food, Drinkable):
    pass

    
class DrinkThirsty (Drinks):
    def get_statements (self):
        return  list(map (lambda phrase:  phrase % self.usage_form(), ["i'm thirsty. i would like %s."] ))

class FoodHungry (Food):
    def get_statements (self):
        return list(map (lambda phrase:  phrase % self.usage_form(), ["i'm hungry. i would like %s."] ))

class Vegetables (Food, Eatable):
    pass

class Fruits (Food, Eatable):
    pass
class Berries (Food, Eatable):
    pass

#mixing classes
class Herbivore (Statements): #an animal that eats only plants
    def get_statements (self):
        return list(map (lambda phrase:  phrase % self.usage_form(), ['%s eats plants.', '%s eats grass, and, leaves.'] ))
class Carnivore (Statements): #an animal that eats meat
    def get_statements (self):
        return list(map (lambda phrase:  phrase % self.usage_form(), ['%s eats animals.', '%s eats meat.'] ))
class Land (Statements): #an animal what can live on land and has 4 legs, can walk and run
    def get_statements (self):
        return list(map (lambda phrase:  phrase % self.usage_form(), ['%s has four legs', '%s can walk.', '%s can run.'] ))
class Water (Statements): #an animal what can live in water and can swim
    def get_statements (self):
        return list(map (lambda phrase:  phrase % self.usage_form(), ['%s can swim.'] ))
class HasTail (Statements):
    def get_statements (self):
        return ['%s has a tail.' % self.usage_form()]
class FurSkin (Statements):
    def get_statements (self):
        return ["the body of %s is covered with fur." % self.usage_form()]


class Animals (Noun):
    pass

class Mammals (Animals):
    def get_statements (self):
        return list(map (lambda phrase:  phrase % self.usage_form(), ['%s feeds, its babies, on milk.'] ))
class LandMammals (Mammals,Land,HasTail,FurSkin):
    pass
    
class LandHerbivoreMammals (LandMammals, Herbivore):
    pass

class LandCarnivoreMammals (LandMammals, Carnivore):
    pass

class WaterMammals (Mammals, Water, HasTail):
    def get_statements (self):
        return list(map (lambda phrase:  phrase % self.usage_form(), ['%s eats fish.'] ))
class FishMammals (Mammals, Water, HasTail):
    def get_statements (self):
        return list(map (lambda phrase:  phrase % self.usage_form(), ['%s eats fish.'] ))
class Whale (Mammals, Water, HasTail):
    def get_statements (self):
        return list(map (lambda phrase:  phrase % self.usage_form(), ['%s is the biggest animal, on our planet.'] ))
class Fish (Animals, Water, HasTail):
    pass

class Birds (Animals):
    def get_statements (self):
        return list(map (lambda phrase:  phrase % self.usage_form(), ['the body of %s, is covered, with feathers.', '%s can fly.'] ))
class WaterBirds (Birds,Water):
    pass

class Vehicles (Noun):
    pass

class RideVehicles (Vehicles):
    def get_statements (self):
        return list(map (lambda phrase:  phrase % self.usage_form(), ['can you ride %s?','i can ride %s.',"i can't ride %s."] ))
class DriveVehicles (Vehicles):
    def get_statements (self):
        return list(map (lambda phrase:  phrase % self.usage_form(), ['can you drive %s?','i can drive %s.',"i can't drive %s."] ))
class FlyVehicles (Vehicles):
    def get_statements (self):
        return list(map (lambda phrase:  phrase % self.usage_form(), ['can you fly %s?','i can fly %s.',"i can't fly %s."] ))
class SailVehicles (Vehicles):
    def get_statements (self):
        return list(map (lambda phrase:  phrase % self.usage_form(), ['can you sail %s?','i can sail %s.',"i can't sail %s."] ))

    

class Clothes (Noun):
    def get_statements (self):
        return list(map (lambda phrase:  phrase % self.usage_form(), ['do you wear %s?','i wear %s.',"i don't wear %s."] ))

class Board (Noun):
    def get_statements (self):
        return list(map (lambda phrase:  phrase % self.usage_form(), ['there is %s, in the classroom.'] ))
class WrittenTool (Noun):
    def get_statements (self):
        return list(map (lambda phrase:  phrase % self.usage_form(), ['%s, is used, for writing, and drawing.'] ))


class Professions (Noun):
    def __new__ (cls, *args, **kwargs):
      self = Noun.__new__ (cls, *args, **kwargs)
      self.live = True
      return self
    def get_statements (self):
        return list(map (lambda phrase:  phrase % self.usage_form(), ["I'm %s by profession.", 'I want to be %s.', "I don't want to be %s.", 'Do you want to be %s.'] ))
      
class Feelings (Adjective):
    def question (self):
        questions = ["how are you?",'how do you feel?']
        return random.choice(questions)
    def get_statements (self):
        return list(map (lambda phrase:  phrase % self, ["I'm %s.", 'Are you %s.'] ))
    

class Weather (Adjective):
    def question (self):
        questions = ["what's the weather like?","how's the weather?"]
        return random.choice(questions)
    def get_statements (self):
        return  list(map (lambda phrase:  phrase % self, ["it's %s.",'do you like %s weather?', 'i like %s weather.', "i don't like %s weather."] ))


class Colour (Adjective):
    def question (self):
        questions = ["what colour is this?"]
        return random.choice(questions)
    def get_statements (self):
        return  list(map (lambda phrase:  phrase % self, ["this is the %s colour.",'is %s, your favourite colour?', 'the %s colour, is not my favourite.', "my favourite colour, is %s."] ))
    def answer (self):
        return Colour.get_statements(self)[0]
      
class Room (Noun):
    def question (self):
        return ' '.join(['what room', ToBe.form(plural=self.plural, person=3, time='presence'), this_pronoun.form(plural=self.plural)]) + '?'

class Furniture (Noun):
    def get_statements (self):
        return  list(map (lambda phrase:  phrase % self.usage_form(), ["where is %s, in your flat?"] ))

class RoomPart (Noun):
    def get_statements (self):
        return  list(map (lambda phrase:  phrase % self.usage_form(), ["%s, is a part, of a room."] ))

class OpenRoomPart (RoomPart):
    def get_statements (self):
        return  list(map (lambda phrase:  phrase % self.usage_form(), ["you can open %s.", "you can close %s."] ))

class Time (Adjective):
    fields = Noun.fields.copy()
    fields.update ({'order': 0})
    """
    def sentence (self):
        return "it's %s." % self
        """
    def question (self):
        return 'what time is it?'
    def get_statements (self):
        return  list(map (lambda phrase:  phrase % self, ["it's %s."] ))
    def answer (self):
        return Time.get_statements(self)[0]

class Weekday (Time):
    """
    def sentence (self):
        return "%s, is the %s day, of the week." % (self,self.order)
        """
    def question (self):
        return 'what is, the %s day, of the week?' % self.order
    def get_statements (self):
        return  list(map (lambda phrase:  phrase % (self,self.order), ["%s, is the %s day, of the week."] ))
    def answer (self):
        return Weekday.get_statements(self)[0]

class Month (Time):
    """
    def sentence (self):
        return "%s, is the %s month, of the year." % (self,self.order)
        """
    def question (self):
        return 'what is, the %s month, of the year?' % self.order
    def get_statements (self):
        return  list(map (lambda phrase:  phrase % (self,self.order), ["%s, is the %s month, of the year."] ))
    def answer (self):
        return Month.get_statements(self)[0]

class Season (Noun):
    pass


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
    def get_statements (self):
        return  ['Hi.','Hello.', 'Good %s.' % part_of_day()]
class Farewell (Phrase):
    def get_statements (self):
        return  ['Goodbye!', 'Bye!', 'Bye bye!', 'See you.', 'See you soon.', 'Take care.']
"""
use format method and named agruments
"""
class PersonRelatedProperty (Phrase):
    def __new__ (cls, property_name):
        class _ClassProperty(PersonRelatedProperty):
            pass
        _ClassProperty.property_name = property_name
        return _ClassProperty
    @classmethod
    def sentence (cls, self):
                #seq = cls.get_statements (self)
                seq = cls.accumulate(self)
                random.shuffle(seq)
                return random.choice(seq)
    @classmethod
    def answer (cls,self):
                    return cls.sentence (self)
    @classmethod
    def instruction (cls, self):
                    kwargs = {'pronoun': possessive_pronoun(self.grammar_form, self.sex),
                              'property_name': cls.property_name}
                    instructions = list(map (lambda phrase: phrase.format (**kwargs), ["ask me about {pronoun} {property_name}."] ))
                    return random.choice(instructions)

class PossessiveProperty(PersonRelatedProperty):
    #property_name =
    def __new__ (cls, property_name):
        class _ClassProperty(PersonRelatedProperty):
                @staticmethod
                def get_statements (self):
                    kwargs = {'pronoun': possessive_pronoun(self.grammar_form, self.sex),
                              'property_name': _ClassProperty.property_name,
                              'value': self.__dict__[_ClassProperty.property_name]}
                    return  list(map (lambda phrase: phrase.format (**kwargs), ['{pronoun} {property_name} is {value}.', "{pronoun} {property_name}'s {value}."] ))
                @staticmethod
                def question (self):
                    kwargs = {'pronoun': possessive_pronoun(self.grammar_form, self.sex),
                              'property_name': _ClassProperty.property_name}
                    questions = list(map (lambda phrase: phrase.format (**kwargs), ["what is {pronoun} {property_name}?","what's {pronoun} {property_name}?"] ))
                    return random.choice(questions)
                """
                def instruction (self):
                    kwargs = {'pronoun': possessive_pronoun(self.grammar_form, self.sex),
                              'property_name': _ClassProperty.property_name}
                    instructions = list(map (lambda phrase: phrase.format (**kwargs), ["ask me about {pronoun} {property_name}."] ))
                    return random.choice(instructions)
                    """
        _ClassProperty.property_name = property_name
        return _ClassProperty

class PersonalProperty(PersonRelatedProperty):
    #property_name = 
    def __new__ (cls, property_name):
        class _ClassProperty(PersonRelatedProperty):
            @staticmethod
            def get_statements (self):
                #print ('PersonalProperty:',PersonalProperty.property_name)
                kwargs = {'pronoun': personal_pronoun(self.grammar_form, self.sex),
                          'to_be': ToBe.form(person=self.grammar_form),
                          'value': self.__dict__[_ClassProperty.property_name],
                          'to_be_short': ToBe.short_form(person=self.grammar_form)}
                return  list(map (lambda phrase: phrase.format (**kwargs), ['{pronoun} {to_be} {value}.', "{pronoun}'{to_be_short} {value}."] ))
            
        _ClassProperty.property_name = property_name
        return _ClassProperty
            
class Name (PersonalProperty('name'), PossessiveProperty('name')):
    pass
    
class Age (PersonalProperty('age long'), PersonalProperty('age')):
    @staticmethod
    def question (self):
            kwargs = {'pronoun': personal_pronoun(self.grammar_form, self.sex),
                      'to_be': ToBe.form(person=self.grammar_form)}
            questions = list(map (lambda phrase: phrase.format (**kwargs), ["how old {to_be} {pronoun}?"] ))
            return random.choice(questions)
class Country (PersonRelatedProperty('country')):
    @staticmethod
    def get_statements (self):
            #print ('Country.property_name:',Country.property_name, self.__dict__)
            kwargs = {'pronoun': personal_pronoun(self.grammar_form, self.sex),
                      'to_be': ToBe.form(person=self.grammar_form),
                      'value': self.__dict__[Country.property_name],
                      'to_be_short': ToBe.short_form(person=self.grammar_form)}
            return  list(map (lambda phrase: phrase.format (**kwargs), ['{pronoun} {to_be} from {value}.',"{pronoun}'{to_be_short} from {value}."] ))
    @staticmethod
    def question (self):
        kwargs = {'pronoun': personal_pronoun(self.grammar_form, self.sex),
                  'to_be': ToBe.form(person=self.grammar_form)}
        questions = list(map (lambda phrase: phrase.format (**kwargs), ["where {to_be} {pronoun} from?"] ))
        return random.choice(questions)

class Nationality (PersonalProperty('nationality')):
    @staticmethod
    def question (self):
        return PossessiveProperty('nationality').question (self)

class Person (Word):
    """Include name, age, nationality and other behaviour via mixing classes or via LearningItem -> Interaction???
name: Sophia
age: 5
country: Ukraine
city: Kyiv
sex: male|femail
"""
    fields = {'name': '', 'sex': '', 'favourite colour': '', 'favourite drink': '', 'age': '', 'country': '', 'nationality': '', 'visual_source': ''}
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
    #print (cat.sentence())
    #print (cat.question())
    #print (cat.answer())

    
    olya = Person (text = 'Olya', name = 'Olya', age='three', sex= 'female', country= 'Ukraine', nationality='ukrainian',
                   **{'favourite colour': 'blue', 'favourite drink': 'orange juice', 'age long': 'three years old'})
    #sophia = Person (name = Name('Sophia'), determiner = 'her', pronoun = 'she')
    #print (olya)
    #print ('Good',part_of_day())
    #print (Name('Sophia').get_statements(olya))
    #print (Name('Sophia').question('her'))
    #print (PersonalName.get_statements(olya))
    #print (PossesiveName.get_statements(olya))
    print (Name.accumulate(olya.set_grammar_form(1)))
    #print ( property_class(PossessiveProperty, 'name').get_statements(olya.set_grammar_form(1)), property_class(PersonalProperty, 'name').get_statements(olya.set_grammar_form(1)) )
    #print (Name.accumulate(olya.set_grammar_form(1)))
    
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
    print (Country.get_statements(olya.set_grammar_form(3)))

    print (Greetings.get_statements(olya))
    print (Greetings('greetings').sentence())
    print (Greetings('greetings').answer())

    print (Nationality.answer(olya.set_grammar_form(2)))


    
