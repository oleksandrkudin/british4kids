"""Learn each LanguageItem (words, phrases) via TextLearningMaterials (sensences/stories/dialogs) with assotiated visual data (image, animated image, video).
TextLearningMaterial is just a list of Sentences.
Sentence is list of LearningFrames.
LearningFrame is smallest learning frame that contains example sentence to remember LanguageItem and question/correct answer to check knowledge.
"""

import languageitem
import types
from nouns_test import dict_txt_nouns
from dialogs import dict_txt_dialogs
from interaction import dict_txt_interaction
import os.path
import time
from kivy.clock import Clock
import random

##############
#LearningFrame
##############
        
class LearningFrame ():
    """Smallest example of LanguageItem usage to be presented to student with single reaction (listen+remember or answer question).
Text contain audio resource (TxtAudioResource)
"""
    def __init__ (self, language_item, text, audio_resource = None):
        self.languageitem = language_item
        self.text = languageitem.TxtAudioResource (text, audio_resource)
    def __str__ (self):
        return self.text

class StatementFrame (LearningFrame):
    """Language sentence what require only watching+listening=remembering"""
    pass

class QuestionFrame (LearningFrame):
    """Language question what require watching + listening question + give answer = checking"""
    def __init__ (self, language_item, text, answer, audio_resource = None, audio_answer_resource = None):
       LearningFrame.__init__ (self, language_item, text, audio_resource)
       self.answer = languageitem.TxtAudioResource (answer, audio_answer_resource)
    def __str__ (self):
        return '%s -> %s' % (self.text, self.answer)

#################
#LearningMaterial
#################


class LearningMaterial ():
    """Base class to store and then provide text+voice and visual data for each request!"""
    def __init__ (self, visual_source):
        if visual_source: self.visual_source = visual_source
    

class TextLearningMaterial (list, LearningMaterial):
    """Text learning materials = sentence, story, dialog"""
    def __init__ (self, sentences = [], visual_source = None):
        list.__init__ (self, sentences)
        LearningMaterial.__init__ (self, visual_source)
    def get_sentence (self):
        for i_sentence in self:
            yield i_sentence
    def get_visual_source (self, container = None):
        if 'visual_source' in self.__dict__:
            return self.visual_source
        elif container:
            return container.get_visual_source()
        else:
            return ''
        #return self.visual_source if 'visual_source' in self.__dict__ else container.get_visual_source() #take visual source from container object if not exist in object 
        

class Sentence (TextLearningMaterial):
    """List of LearningFrame, 0 - StatementFrame, 1: - QuestionFrame"""
    def __init__ (self, learning_frames = [], visual_source = None):
        list.__init__ (self, learning_frames)
        LearningMaterial.__init__ (self, visual_source)
    def get_frame (self, learning_activity):
        if 'repeat' in learning_activity and 'answer' in learning_activity: return self.get_interator (slice(len(self)))
        elif 'repeat' in learning_activity: return self.get_interator (slice(0,1))
        elif 'answer' in learning_activity: return self.get_interator (slice(1,len(self)))
    def get_interator (self, index):
        for i_frame in self[index]:
            yield i_frame
    def get_sentence (self):
        yield self
    

class Dialog (TextLearningMaterial):
    """List of Sentences"""
    def get_visual_source (self):
        return self.visual_source if 'visual_source' in self.__dict__ else ''

class Story (TextLearningMaterial):
    """List of Sentences"""
    def get_visual_source (self):
        return self.visual_source if 'visual_source' in self.__dict__ else ''



class Catalog (dict):
    def __init__ (self):
        dict.__init__ (self)
        self['vocabulary'] = {}
        self['dialogs'] = {}
        self['memory'] = {}
        self['remember'] = {}
    def load_vocabulary (self, topic, dict_data = dict_txt_nouns):
        self['vocabulary'][topic] = {}
        words = dict_txt_nouns[topic]
        for i_word, i_parameters in words.items():
            i_parameters = i_parameters.copy() #as we do pop and refreshing catalog several time we need to create copy of original data
            part = i_parameters.pop('part')
            text_sentence = i_parameters.pop('sentence',None)
            text_question = i_parameters.pop('question',None)
            text_answer = i_parameters.pop('answer',None)
            visual_source = i_parameters.pop('visual_source','')
            
            audio_source = 'data/sounds/%s/%s.mp3' % (topic,i_word)
            visual_source_file = 'data/images/%s/%s.jpg' % (topic,i_word)
            visual_source = visual_source if visual_source or not os.path.exists(visual_source_file) else visual_source_file
            
            li = languageitem.__dict__[part](i_word,audio_source,**i_parameters)
            lm = Sentence ([StatementFrame (li, text_sentence if text_sentence else li.sentence(li)),
                            QuestionFrame (li, text_question if text_question else li.question(li), text_answer if text_answer else li.answer(li))
                ], visual_source)

            self['vocabulary'][topic][li] = lm
    def load_dialogs (self, dialog_name, dict_data = dict_txt_dialogs):
        self['dialogs'] = {}
        sentences = dict_data[dialog_name]
        dialog = Dialog()
        self['dialogs'][dialog_name] = dialog
        for i_sentence in sentences:
            i_sentence = i_sentence.copy()
            i_word = i_sentence['word']
            text_sentence = i_sentence.pop('text',None)
            text_answer = i_sentence.pop('answer',None)
            visual_source = i_sentence.pop('visual_source','')

            li = languageitem.Word (i_word)

            dialog.append ( Sentence([None,
                                      QuestionFrame (li, text_sentence, text_answer)
            ], visual_source) )
   
    def load_cards (self, topic, scenario, dict_data = dict_txt_nouns):
        self[scenario][topic] = {}
        words = dict_txt_nouns[topic]
        for i_word, i_parameters in words.items():
            i_parameters = i_parameters.copy() #as we do pop and refreshing catalog several time we need to create copy of original data
            part = i_parameters.pop('part')
            text_sentence = i_parameters.pop('sentence',None)
            text_question = i_parameters.pop('question',None)
            text_answer = i_parameters.pop('answer',None)
            visual_source = i_parameters.pop('visual_source','')
            
            audio_source = 'data/sounds/%s/%s.mp3' % (topic,i_word)
            visual_source_file = 'data/images/%s/%s.jpg' % (topic,i_word)
            visual_source = visual_source if visual_source or not os.path.exists(visual_source_file) else visual_source_file
            
            li = languageitem.__dict__[part](i_word,audio_source,**i_parameters)
            lm = LearningMaterial (visual_source = visual_source)
            self[scenario][topic][li] = lm
    def load_interaction (self, interation_name, dict_data = dict_txt_interaction, student = None):

        def person_by_name (persons, name):
            for i_person, i_params in persons.items():
                if i_params.name == name:
                    return i_person

        #load persons
        persons = {}
        audio_source = None
        for i_person, i_parameters in dict_data['persons'].items():
            i_parameters = i_parameters.copy()
            part = i_parameters.pop('part')
            #visual_source = i_parameters.pop('visual_source','')
            li = languageitem.__dict__[part](text=i_person,**i_parameters)
            persons[i_person]=li
        if student:
            persons['student'] = persons[person_by_name(persons, student.name)]
        
        self['interactions'] = {}
        sentences = dict_data[interation_name]['interaction']
        dialog = Dialog()
        self['interactions'][interation_name] = dialog

        pairs = []
        for person1 in dict_data[interation_name].get('person1',[]):
            #print ('person1:', person1)
            person1 = persons[person1]
            for person2 in  dict_data[interation_name].get('person2',[]):
                pairs.append ({})
                person2 = persons[person2]
                pairs[-1] = {'person1': person1, 'person2': person2}
                
            if not pairs or not 'person2' in pairs[-1]:
                pairs.append ({})
                pairs[-1]['person1'] = person1
                
        #print ('pairs:', pairs)
        for i_pair in pairs:
                visual_source = i_pair['person1'].visual_source #picture only 1-st person = drawback!
                person1 = i_pair.get('person1')
                person2 = i_pair.get('person2')
                for i_sentence in sentences:
                    i_sentence = i_sentence.copy()
                    part = i_sentence.pop('part')
                    word = i_sentence['word']
                    states = i_sentence.pop('states')
                    answers = i_sentence.pop('answer')

                    if issubclass (languageitem.__dict__[part], languageitem.PersonRelatedProperty):
                        if part in ['PossessiveProperty','PersonalProperty']:
                            method = "languageitem.%s('%s').{operator}({person}.set_grammar_form({grammar_form}))" % (part, word)
                        else:
                            method = "languageitem.%s.{operator}({person}.set_grammar_form({grammar_form}))" % (part)

                        states_method_list = list ( map (lambda state : method.format (operator=state[0], person=state[1], grammar_form=state[2]), states))
                        answer_method_list = list ( map (lambda answer : method.format (operator=answer[0], person=answer[1], grammar_form=answer[2]), answers))
                    else:
                        method1 = method2 = "languageitem.{part}('{word}').%s()".format(part=part, word=word)
                        states_method_list = list ( map (lambda state: method1 % state, states))
                        answer_method_list = list ( map (lambda answer: method2 % answer, answers))

                    #print ('method:', method1, method2)
                    #print ('states_method_list:', states_method_list)

                    text_sentence = ' '.join(map(eval,states_method_list))
                    text_answer = ' '.join(map(eval,answer_method_list))

                    print (text_sentence, text_answer)

                    li = languageitem.Word (word)
                    dialog.append ( Sentence([None,
                                              QuestionFrame (li, text_sentence, text_answer)], visual_source = visual_source) )
  
            
    def load (self, scenario, topic, student = None):
        if scenario == 'vocabulary':
            self.load_vocabulary (topic)
        if scenario == 'dialogs':
            self.load_dialogs (topic)
        if scenario in ['memory','remember']:
            self.load_cards (topic,scenario)
        if scenario == 'interactions':
            self.load_interaction (topic, student=student)

class MemoryGame (list):
    def __init__ (self, cols=4, rows=3):
        list.__init__ (self)
        self.opened_card = None
        self.back_image = 'data/images/card-game.png'
        self.cols = cols
        self.rows = rows
    def play (self, card):
        
        def cards_clear (*args):
            opened_card.canvas.clear()
            card.canvas.clear()
            self.opened_card = None
        def cards_flip (*args):
            opened_card.flip()
            card.flip()
            self.opened_card = None

        opened_card = self.opened_card   
        card.flip ()
        card.languageitem.play()
        if self.opened_card:
            if card.equal (self.opened_card):
                opened_card.active = False
                card.active = False
                Clock.schedule_once (cards_clear,1)
            else:
                Clock.schedule_once (cards_flip,1)
        else:
            self.opened_card = card
    def load (self, learningmaterials): #load data from learningmaterials = catalog['memory'][topic] = return list of (languageitem, card_type, image)
        #load catalog
        #catalog.load ('vocabulary', topic)
        seq = learningmaterials.keys()
        li_number = int(self.cols * self.rows/2)
        items = random.sample (seq, li_number if len(seq) >= li_number else len(seq))
                
        cards_data = [(li,card_type) for li in items for card_type in ['text','picture']]
        random.shuffle(cards_data)

        for (li, card_type) in cards_data:
                image = learningmaterials[li].visual_source
                self.append ((li,card_type,image))
                
class RememberGame (list):
    def __init__ (self, number=9):
        list.__init__ (self)
        self.number = number
        self.frame = 1
        self.remember = []
        self.selected = set()
        self.counter = None
    def load (self, learningmaterials):
        seq = learningmaterials.keys()
        li_number = int(self.number * 2.5)
        items = random.sample (seq, li_number if len(seq) >= li_number else len(seq))
        for li in items:
            image = learningmaterials[li].visual_source
            self.append ((li,image))
        self.remember = random.sample (self, self.number)
    def play (self):
        if self.frame == 1:
            #self.next_frame()
            delay = 2
            """
            #replaced by new version of play card with the same interval 
            for card in self.remember:
                card[0].play (delay)
                delay += 2
            """
            #new version
            remember_languageitem_list = [card[0] for card in self.remember] #get languageitem to play
            languageitem.TxtAudioResource.play_list (remember_languageitem_list,delay)
            
        elif self.frame == 2:
            pass
            #self.next_frame()
        elif self.frame == 3:
            pass
    def next_frame (self):
        self.frame +=  1
        return self.frame
    def on_press (self, btn):
        if len(self.selected) < self.number or btn.selected:
            btn.click()
            if btn.selected:
                self.selected.add((btn.languageitem,btn.image))
            else:
                self.selected.remove((btn.languageitem,btn.image))
            self.update_counter ()
    def update_counter (self):
        self.counter.text = 'Select %s pictures.' % str(self.number - len(self.selected))

catalog = Catalog ()


"""
catalog = {}
catalog['vocabulary'] = {}


#
#ADD NOUNS TO CATALOG 
#
for topic, words in dict_txt_nouns.items():
    catalog['vocabulary'][topic] = {}
    for i_word, i_parameters in words.items():
        part = i_parameters.pop('part')
        text_sentence = i_parameters.pop('sentence',None)
        text_question = i_parameters.pop('question',None)
        text_answer = i_parameters.pop('answer',None)
        visual_source = i_parameters.pop('visual_source','')
        
        audio_source = 'data/sounds/%s/%s.mp3' % (topic,i_word)
        visual_source_file = 'data/images/%s/%s.jpg' % (topic,i_word)
        visual_source = visual_source if visual_source or not os.path.exists(visual_source_file) else visual_source_file
        
        li = languageitem.__dict__[part](i_word,audio_source,**i_parameters)
        lm = Sentence ([StatementFrame (li, text_sentence if text_sentence else li.sentence()),
                        QuestionFrame (li, text_question if text_question else li.question(), text_answer if text_answer else li.answer())
            ], visual_source)

        catalog['vocabulary'][topic][li] = lm


#
#LOAD DIALOGS TO CATALOG
#
catalog['dialogs'] = {}
for dialog_name, sentences in dict_txt_dialogs.items():
    dialog = Dialog()
    catalog['dialogs'][dialog_name] = dialog
    for i_sentence in sentences:
        i_word = i_sentence['word']
        text_sentence = i_sentence.pop('text',None)
        text_answer = i_sentence.pop('answer',None)
        visual_source = i_sentence.pop('visual_source','')

        li = languageitem.Word (i_word)

        dialog.append ( Sentence([None,
                                  QuestionFrame (li, text_sentence, text_answer)
            ], visual_source) )
        #print (dialog[-1])


"""

if __name__ == '__main__':
    notebook1 = languageitem.Noun ('notebook', audio_source = r'data/sounds/school/notebook.mp3', countable=True, meaning='book')
    notebook2 = languageitem.Noun ('notebook', audio_source = r'data/sounds/school/notebook.mp3', countable=True, meaning='book')
    print ('notebook1 == notebook2', notebook1 == notebook2)

    

    dog = languageitem.Noun ('dog', audio_source = r'data/sounds/animals/dog.mp3', countable=True, plural='dogs')
    cat = languageitem.Noun ('cat', audio_source = r'data/sounds/animals/cat.mp3', countable=True, plural='cats')
    cow = languageitem.Noun ('cow', audio_source = r'data/sounds/animals/cow.mp3', countable=True)
    sheep = languageitem.Noun ('sheep', audio_source = r'data/sounds/animals/sheep.mp3', countable=True)
    goat = languageitem.Noun ('goat', audio_source = r'data/sounds/animals/goat.mp3', countable=True)

    white = languageitem.Adjective ('white', audio_source = r'data/sounds/white.mp3')
    black = languageitem.Adjective ('black', audio_source = r'data/sounds/black.mp3')
    spot = languageitem.Noun ('spot', audio_source = r'data/sounds/spot.mp3',countable=True)

    this_dog = Sentence (
            [  StatementFrame ( dog, 'This is a dog.'),
               QuestionFrame ( dog, 'What is this?', 'This is a dog.')
                ],  visual_source = r'data/images/animals/dog.jpg')

    this_cat = Sentence (
            [  StatementFrame ( cat, 'This is a cat.'),
               QuestionFrame ( cat, 'What is this?', 'This is a cat.'),
               QuestionFrame ( cat, 'What do you see?', 'I see a cat.')
                ],  visual_source = r'data/images/animals/cat.jpg')

    this_cow = Sentence (
            [  StatementFrame ( cow, 'This is a cow.'),
               QuestionFrame ( cow, 'What is this?', 'This is a cow.'),
               QuestionFrame ( cow, 'What do you see?', 'I see a cow.')
                ],  visual_source = r'data/images/animals/cow.jpg')


    this_sheep = Sentence (
            [  StatementFrame ( sheep, 'This is a sheep.'),
               QuestionFrame ( sheep, 'What is this?', 'This is a sheep.'),
               QuestionFrame ( sheep, 'What do you see?', 'I see a sheep.')
                ],  visual_source = r'data/images/animals/sheep.jpg')

    this_goat = Sentence (
            [  StatementFrame ( goat, 'This is a goat.'),
               QuestionFrame ( goat, 'What is this?', 'This is a goat.'),
               QuestionFrame ( goat, 'What do you see?', 'I see a goat.')
                ],  visual_source = r'data/images/animals/goat.jpg')
        
    white_dog_black_spot = Sentence (
            [ StatementFrame ( dog, 'This is a white dog with black spots.'),
              QuestionFrame ( white, 'What colour is the dog?', 'The dog is white.'),
              QuestionFrame ( spot, 'What does the dog have on its body?', 'The dog has black spots on its body.')
              ])

    story_dog = Story ([this_dog,white_dog_black_spot], visual_source = r'data/images/white_dog_story.jpg')

    #catalog['vocabulary']['animals'] = {}
    #catalog['vocabulary']['animals'][dog] = this_dog
    #catalog['vocabulary']['animals'][cat] = this_cat
    #catalog['vocabulary']['animals'][cow] = this_cow
    #catalog['vocabulary']['animals'][sheep] = this_sheep
    #catalog['vocabulary']['animals'][goat] = this_goat

    #catalog['story'] = {}
    #catalog['story']['Story about a dog'] = story_dog

    catalog.load_interaction ('give personal information')
