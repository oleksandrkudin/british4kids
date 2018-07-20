"""
Fabric to create UsageCases (examples) to better learn LanguageItem and different aspect of Language



Attributes:

Classes:

Function:

Example:
    LanguageItem='cat', noun; also it is necessary to have another Animal to build negative expr.
    Different type of UsageFrame differenciated by person reaction (repeat, ask, answer)
    statement is exression! grammar construction common for noun.
    So we learn LanguageItem + GrammarConstruction (not poppulated usagecase - we learn patterns)
    And so knowledge is orginized Pattern + LanguageItem
        repeat: statement: This is a cat -> This is a cat
        answer: yes_statement: This is not a cat -> No, it is = may be not good structure
        answer: no_statement: This is not a dog -> No, it is not; No, it's not = not good structure
        answer: yes_question: Is this a cat? -> Yes, it is
        answer: no_question: Is this a dog? -> No, it is not; No, it's not
        answer: not_no_question: Isn't this a dog? -> No, it is not; No, it's not
        answer: wh_question: What is this? -> This is a cat

        instruction: : 'Say that' This is not a cat -> This is not a cat
        instruction: : 'Ask if' This is a cat -> Is this a cat
        instruction: : 'Ask if' This is not a cat -> Isn't this a cat
        instruction: wh_instruction: 'Ask what it is' -> What is this?

    Dialog - List of UsageCase Frames populated by LanguageItem

TODO:
    @OK

"""
import random
import lexis
import languageitem

#difference in naming in 2.7 and 3.4
try:
    from itertools import zip_longest as zip_longest
except:
    from itertools import izip_longest as zip_longest

#
#Define different type of Sentences in form of pattern from Grammar view
#

class _GrammarSentence(str):
    """Grammar expression/sentence and reaction"""
    def __new__(cls, **kwargv):
        subject = kwargv['subject']
        verb = kwargv['verb']
        grammar_object = kwargv['object']
        tmp = ' '.join([subject, verb, grammar_object])
        self = str.__new__(cls, tmp)
        #self = tmp
        #print(tmp)
        return self

class _DeclarativeSentence(_GrammarSentence):
    """Makes a statement or expresses an opinion. 1 from 4 main setences type.
    Does not expect active reaction
    """
    pass

class _PositiveDeclarativeSentence(_DeclarativeSentence):
    """Makes a possitive statement or expresses a possitive opinion"""
    pass

class _NegativeDeclarativeSentence(_DeclarativeSentence):
    """Makes a negative statement or expresses a negative opinion"""
    pass


class _InterrogativeSentence(_GrammarSentence):
    """
    Sentence used when asking a question (asks for information). 1 from 4 main setences type.
    There are four main categories of direct questions, depending on the kind of answer you expect:
        Yes/No questions, WH questions, alternative questions and tag questions.
    """
    pass

class _YesQuestion(_InterrogativeSentence):
    """Answer to question will be yes.
    Auxiliary verb + subject + main verb
    """
    def __new__(cls, **kwargv):
        subject = kwargv['subject']
        verb = kwargv['verb']
        grammar_object = kwargv['object']
        tmp = ' '.join([verb, subject, grammar_object])
        self = str.__new__(cls, tmp)
        #print(tmp)
        return self

class _NoQuestion(_InterrogativeSentence):
    """Answer to question will be no
    Auxiliary verb + subject + main verb"""
    def __new__(cls, **kwargv):
        subject = kwargv['subject']
        verb = kwargv['verb']
        grammar_object = kwargv['object']
        tmp = ' '.join([verb, subject, grammar_object])
        self = str.__new__(cls, tmp)
        #print(tmp)
        return self

class _WhQuestion(_InterrogativeSentence):
    """Answer to question statement
    what, why, where, how, when, who, which"""
    pass

class _AlternativeQuestion(_InterrogativeSentence):
    """Question require an answer chosen from the options given in the question.
    Example: Do you like the ocean or the mountains?
    """
    pass

class _TagQuestion(_InterrogativeSentence):
    """statement followed by a short question
    Example: You like hamburgers, don't you"""
    pass

class _ImperativeSentence(_GrammarSentence):
    """Sentence used to give a command or make a request. 1 from 4 main setences type
    Example: Please sit down. Ask [Dad] what it is"""
    pass

class _ExclamatorySentence(_GrammarSentence):
    """Sentence used to express strong emotions with statements. 1 from 4 main setences type
    Example: That red truck is really big! Surprise! Happy birthday, Ben!"""
    pass

#
#UsagePattern
#
class UsagePattern(str):
    """
    Common sentences structures(patterns) what are used in the language.
    Can be used with some types of words. These type of words = UsageCase class (semantic)
    Examples:
        This is {noun}
        These are {noun}
        It is {time} o'clock

    Generated from grammar sentence and pattern items.
    Comparing two lists and replacing grammar sentence items what are missed in pattern items
    with semantic (UsageCase class name where all letters are small)
    """
    def __new__(cls, format_spec, pattern_items, grammar_sentence, semantic):
        pattern_sentence_items = []
        for i_alligned_sentence_item in grammar_sentence:
            for i_pattern_item in pattern_items:
                if i_alligned_sentence_item == i_pattern_item:
                    pattern_sentence_items.append(i_alligned_sentence_item)
                    break
            else:
                # combine semantic for missed items in a row
                if pattern_sentence_items[-1] != semantic:
                    pattern_sentence_items.append('{%s}' % semantic)
        sentence = ' '.join(pattern_sentence_items) + alligned_sentence.ending_symbol()


        """
        OLD VERSION
        pattern_sentence_items = {}
        for sentence_part, value in alligned_sentence_items.items():
            if sentence_part in pattern_items:
                pattern_sentence_items[sentence_part] = value
            else:
                pattern_sentence_items[sentence_part] = '{%s}' % sentence_part
        sentence = format_spec.format(**pattern_sentence_items)
        """

        self = str.__new__(cls, sentence)
        return self

    """
    OLD VERSION
    def __init__(self, format_spec, pattern_items, alligned_sentence_items, semantic):
        self.semantic = semantic
    def __eq__(self, usage_pattern):
        return self == usage_pattern and self.semantic == usage_pattern.semantic
    """


#
#Main class to manage UsageFrames
#
class UsageFrame(str):
    """Learn + Check + Reply
    UsageFrame is just a sentence (common structure) to learn what may contain check_frame attribute.
    Check_frames are just UsageFrame-s what are used to check UsageFrame knowleadge.
    Also may contain reply_frames if frame suppose reaction from user

    UsageFrames are differ in user action and reaction like = could be different classes
        listen and repeat/say any
        listen and answer
        listen and 
        listen and do

    Attribute:
        check_frames
        reply_frames

    @TODO: If for question there are several correct answers, full and short forms
        Different ways to say the same! How to learn this???
    How is the weather? It is cold. The weather is cold. = full form
    How's the weather? It's cold. The weather's cold. = short from
    """
    def __new__(cls, format_spec, pattern_items, alligned_sentence_items, semantic, level=0):
        sentence = format_spec.format(**alligned_sentence_items)
        # TODO: sentence = SentenceStructure(sentence_items)
        self = str.__new__(cls, sentence)
        #print('UsageFrame ...', level, format_spec, semantic)
        return self

    def __init__(self, format_spec, pattern_items, alligned_sentence_items, semantic, level=0):
       self.level = level
       self.usage_pattern = UsagePattern(format_spec, pattern_items, alligned_sentence_items, semantic)
       # TODO: usage_pattern = UsagePattern(self._sentence, pattern_items, semantic)

    def __str__(self):
        """
        
        """
        return str(self.level) + ': ' +  self
        
        
        #return str(self.level) + ': ' + self
        #return '%s: %s' % (self.level, self + ', '.join(map(str, [self.check_frames, self.reply_frames])))

    def add_frame(self, frame_type, frame):
        if frame_type == 'check':
            self.check_frames.append(frame)
        elif frame_type == 'reply':
            self.reply_frames.append(frame)
        else:
            raise '%s frame type is not supported.' % frame_type

    #def get_statement(self):
            

class PassiveFrame(UsageFrame):
    active = False
    """
    Usage frame with listen and repeat action/reaction
    Learning to repeat statement (Declarative Sentence) and words
    Should contain only statement
    Example:
        DeclarativeSentence = This is a cat
    """

class ActiveFrame(UsageFrame):
    active = True
    """
    Usage frame with listen and answer/ask
    Learning making questions, giving answers and asking
    Should contain question/answer or command/question
    Example:
        Question/Answer
        Instruction/Answer
        InterrogativeSentence = What is this? Is this a cat? Isn't this a cat?
        
    """
    def __new__(cls, format_spec, pattern_items, alligned_sentence_items, semantic, level=0, reply_frames=[]):
        self = UsageFrame.__new__(cls, format_spec, pattern_items, alligned_sentence_items, semantic, level)
        return self

    def __init__(self, format_spec, pattern_items, alligned_sentence_items, semantic, level=0, reply_frames=[]):
        UsageFrame.__init__(self, format_spec, pattern_items, alligned_sentence_items, semantic, level)
        self.reply_frames = reply_frames
        

    def __str__(self):
        #return '%s: %s => %s' % (self.level, repr(self), self.reply_frames)
        return UsageFrame.__str__(self) + ' => %s' % self.reply_frames

class StatementFrame(PassiveFrame):
    """
    This is a cat
    Listen and repeat the same
    StatementFrame may contain QuestionFrame to check knowledge of it.
    """

class QuestionFrame(ActiveFrame):
    """
    Question/Answer
    Listen and answer
    QuestionFrame may contain InstructionFrame to check knowledge of it.
    Should contain answer!!!
    """

class InstructionFrame(ActiveFrame):
    """
    Instruction/Reply
    Ask what it is. What is this?
    Listen and ask
    """

#
#Classes to manage LanguagePattern
#

class LanguagePattern():
    """
    http://www.scientificpsychic.com/grammar/enggramg.html#DEFSUBJ
    The main goal is to grammatically choose proper words form based on sentence.
    It may return formated sentence or negotiated words form.
    
    Contain format string and language_items to populate it.
    Object used to generate same structured sentence based on input paramaters.
    format_spec may contain object names and attributes

    Attributes:
        format string
        language_items
        grammar_spec
    Example:
        format_spec = '{pronoun} {verb} {object}' - static object
        sentence_items = {'pronoun': this, 'verb': to_be}
        grammar_spec = {'time': 'present', 'form': 'simple'}
        via sentence_items we learn sentence structure
        via grammar_spec we learn times
    Methods:
        get_sentence(sentence_items) - return complete string sentence to use
        alligned_sentence_items(sentence_items) - returned negotiated words form
    """

    def __init__(self, format_spec, sentence_items={}, grammar_spec=None):
        self.sentence_items = sentence_items
        self.format_spec = format_spec
    def get_sentence(self, sentence_items):
        """
        self.sentence_items | sentence_items = all necessary parts and words to build sentences
        It should be function to transform them to proper form!!!
        """
        alligned_items = self.alligned_sentence_items(sentence_items)

        #some words form depends on others
        #this/these depends on object plural form
        #verb depends on subject plural form, grammar person and time
        #object article depends on object many attributes
        #What/Who depends on liveliness of object
        return self.format_spec.format(**alligned_items)

    def alligned_sentence_items(self, sentence_items):
        sentence_items.update(self.sentence_items)
        alligned_items = {}
        #pronoun depends on object (in mind - even if object not mantioned in the sentence)
        # TODO: check language items class but not fields name!!!
        # if isinstance(language_item, Pronoun)
        if 'pronoun' in sentence_items:
            alligned_items['pronoun'] = sentence_items['pronoun'].form(noun=sentence_items['object'])
        if 'verb' in sentence_items:
            alligned_items['verb'] = sentence_items['verb'].form(subject=alligned_items.get('pronoun') or sentence_items.get('subject'))
        if 'subject' in sentence_items:
            alligned_items['subject'] = sentence_items['subject'].form(article=True)
        if 'object' in sentence_items:
            alligned_items['object'] = sentence_items['object'].form(article=True)
        #add other not formed words
        for i_part, i_language_item in sentence_items.items():
            if not i_part in alligned_items:
                alligned_items[i_part] = i_language_item
        return alligned_items
#
#Main class to manage UsageCases for LanguageItem
#

class UsageCase(list):
    """Usagecase is just ordered list of UsageFrames with
    deep_level attribute. Usagecase may contain all necessary frames to learn to make statement,
    question, answering. Class itself contain common language structures in the form of patterns.
    These patterns are populated with different type of languageitems to get sentences
    and then frames.
    Frame order define priority for learning.

    In real life usage of sentence type are not equal = weight should be configured, that
    influence appearence to Student.
    Order of sentence also influence = you cannot learn 3 without knowledge of 1 and 2
    Algorithm should be clear
        within UsageCase
            Next Sentence is activated if Previous in Knowledge
        among LanguageItem
            Pure random(shuffle) without weight
            50/50 Known and Unknown

    Example:


    Attributes:
        _frames_data()
        _get_language_items (kwargv)
        _pattern_normalization_data = {}
        _pattern_sentence_items = []

        deep_level = number to define how far is user_case in the hierachy.
            0 - start, means user_case for base class, X(maximum) - usage_case for root class
            X(maximum) - most common usage_case; 0 - most specific usage_case

        usage_cases() - class method that accumulate and return all usage_cases in the hierachy.
            Proxy method for accumulate() method

        _format() - static method what just maps patterns list and dict agrument to get list of
            setences. Method uses format str method to format patterns with values
        _create_frames() - class method to build list of frames
        _accumulate() - class method to walk via hierarchy of classes started from cls derived
            from self value and return all usage_cases in the hierachy.


        usage_cases() -> _accumulate() -> __new__() -> __init__ -> create_frames()

    """

    _pattern_normalization_data = {}
    _pattern_sentence_items = []
    
    def __new__(cls, deep_level=0, **kwargv):
        """create usage_case from list of frames and assigning deep_level"""
        self = list.__new__(cls)
        return self

    def __init__(self, deep_level=0, **kwargv):
        self.extend(self._create_frames(kwargv))
        self.deep_level = deep_level

    @classmethod
    def usage_cases(cls, **kwargv):
        """
        accumulate and return all usage_cases in the hierachy
        """
        return cls._accumulate(kwargv, '_frames_data')

    def get_frame(self, frame_class):
        def is_frame_class(frame):
            return frame.__class__ == frame_class
        frames = list(filter(is_frame_class, self))
        if frames:
            return random.choice(frames)

    def statement_frame(self):
        """ramdomly return statement frame or None if no frame"""
        return self.get_frame(StatementFrame)

    def question_frame(self):
        """ramdomly return question frame or None if no frame"""
        return self.get_frame(QuestionFrame)

    def instruction_frame(self):
        """ramdomly return instruction frame or None if no frame"""
        return self.get_frame(InstructionFrame)

    @staticmethod
    def _format(patterns_groups, kwargv): #static
        sentences = []
        for i_patterns in patterns_groups:
            sentences.append(list(map(lambda i_pattern: str.format(i_pattern, **kwargv), i_patterns)))
        return sentences

    @classmethod
    def _create_frames(cls, kwargv):
        """
        Get usagecase for particular class.
        """

        #NEW VERSION
        def create_frames(frames_data, language_items):
            frames = []
            for i_frame_data in frames_data:
                frames.append(create_frame(i_frame_data, language_items))
            return frames
        
        def create_frame(frame_data, language_items):
            #print('frame_data', frame_data)
            frame_class = frame_data.get('class')
            level = frame_data.get('level', 0)
            pattern_class = frame_data.get('pattern_class')
            format_spec = frame_data.get('format_spec')
            format_spec, norm_language_items = cls._pattern_normalization(format_spec, language_items)
            #sentence = pattern_class(format_spec).get_sentence(norm_language_items)
            alligned_sentence_items = pattern_class(format_spec).alligned_sentence_items(norm_language_items)
            pattern_items = cls._pattern_sentence_items
            
            reply_frames_data = frame_data.get('reply_frames', [])
            semantic = cls.__name__

            #print('create_frame', frame_data)
            
            if reply_frames_data:
                reply_frames = create_frames(reply_frames_data, language_items)
                return frame_class(format_spec, pattern_items, alligned_sentence_items, semantic, level, reply_frames=reply_frames)
            else:
                return frame_class(format_spec, pattern_items, alligned_sentence_items, semantic, level)
            
        #get frames_data and values
        language_items = cls._get_language_items(kwargv)
        #first create sentence based on LanguagePattern and values
        return create_frames(cls._frames_data(), language_items)

    @classmethod
    def _pattern_normalization(cls, format_spec, language_items):
        if '_pattern_normalization_data' in cls.__dict__:
            new_language_items = {}
            for sentence_part, replacing_part in cls._pattern_normalization_data.items():
                if format_spec.find(sentence_part) >= 0:
                    new_language_items[replacing_part] = language_items[sentence_part]
                    format_spec = format_spec.replace(sentence_part, replacing_part)

            for i_part, i_language_item in language_items.items():
                if not i_part in new_language_items:
                    new_language_items[i_part] = i_language_item
            return (format_spec, new_language_items)
        else:
            return (format_spec, language_items)

    @classmethod
    def _accumulate(cls, kwargv, accumulated_field, deep_level=0):
        """ Walk via hierarchy of classes started from cls derived from self value.
        If class has attribute 'accumulated_field',
        get values returned by 'get_values_function_name' function and extend resulting list with them.
        Return summary list of values.
        Problem: method influence 'answer' method - integrity is lost!!!
        Suggest that 'answer' is the first statement in first class in hierarchy -
        so depends on order of super classes and multiple inheritance.
        Before adding values from list they must be added in reverse order.

        """
        visited_classes = set()
        def go_through_classes(cls, kwargv, deep_level):
            res = []
            if cls.__bases__:
                #res = res + (eval('cls.%s(kwargv)' % get_values_function_name)[::-1] if accumulated_field in cls.__dict__ else [])
                if accumulated_field in cls.__dict__:
                    res.append(cls(deep_level, **kwargv))
                    #print(res[-1])

                deep_level += 1
                for i_class in cls.__bases__:
                    if i_class in visited_classes:
                        break
                    visited_classes.add(i_class)
                    res.extend(go_through_classes(i_class, kwargv, deep_level))
                
                return res
            else:
                if accumulated_field in cls.__dict__ and not (cls in visited_classes):
                    visited_classes.add(cls)
                    res.append(cls(deep_level, **kwargv))
                    #print(cls.__name__, deep_level)
                    return res
                else:
                    return []
        return  go_through_classes(cls, kwargv, deep_level)

    def __str__(self):
        return self.__class__.__name__ + ':' +  str(self.deep_level) +  ': [' + ', '.join(map(str, self)) + ']'
    
class Noun(UsageCase):
    """'This is .../There are ...' language structure. Class name could be ThisIs

    Example:
        repeat: statement: This is a cat -> This is a cat
        answer: yes_statement: This is not a cat -> No, it is = may be not good structure
        answer: no_statement: This is not a dog -> No, it is not; No, it's not = not good structure
        answer: yes_question: Is this a cat? -> Yes, it is
        answer: no_question: Is this a dog? -> No, it is not; No, it's not
        answer: not_no_question: Isn't this a dog? -> No, it is not; No, it's not
        answer: wh_question: What is this? -> This is a cat

        instruction: : 'Say that' This is not a cat -> This is not a cat
        instruction: : 'Ask if' This is a cat -> Is this a cat
        instruction: : 'Ask if' This is not a cat -> Isn't this a cat
        instruction: wh_instruction: 'Ask what it is' -> What is this?

    Declarative Sentence = <subject> <predicate> = <My name> <is Mary>
        subject may be a simple subject or a compound subject
        A simple subject consists of a noun phrase or a nominative personal pronoun
        Compound subjects are formed by combining several simple subjects with conjunctions.
        <predicate> = <verb> <complement>
        <complement> =
           [[<indirect object>] <object>] |
           [<adverb>* <adjective>] |
           [<prep phr>*] |
           ["to" <Vinf> [<object>]] |
           [<Ving>]

           [<indirect object>] <object> 
            I spent the money.
            John gave me the little book. 

            <adverb>* <adjective>
            Mary became very angry. 

            <prep phr>* 
            John slept until 10:00 AM on Thursday. 

            "to" <Vinf> [<object>] 
            John went to pay the rent.
            I want to drink water. 

            <Ving> 
            John went shopping.

    The question here is what shold be in class and what should be passed to class.
    """

    #Class could be contains list of LanguagePattern
    #
    @staticmethod
    def _frames_data():
        frames_data = []
        # this is ... frame
        frames_data.append({'class': StatementFrame, 'level': 0, 'pattern_class': LanguagePattern, 'format_spec': '{pronoun} {verb} {object}.'})
        frames_data.append({'class': QuestionFrame, 'level': 0, 'pattern_class': LanguagePattern, 'format_spec': '{what_pronoun} {verb} {pronoun}?', 'reply_frames': [frames_data[-1]]})
        frames_data.append({'class': InstructionFrame, 'level': 0, 'pattern_class': LanguagePattern, 'format_spec': 'ask {what_pronoun} it is.', 'reply_frames': [frames_data[-1]]})

        # is this ... correct frame
        answer = {'class': StatementFrame, 'level': 0, 'pattern_class': LanguagePattern, 'format_spec': 'yes, {pronoun} {verb} {object}.'}
        frames_data.append({'class': QuestionFrame, 'level': 0, 'pattern_class': LanguagePattern, 'format_spec': '{verb} {pronoun} {object}?', 'reply_frames': [answer]})
        frames_data.append({'class': InstructionFrame, 'level': 0, 'pattern_class': LanguagePattern, 'format_spec': 'ask if {pronoun} {verb} {object}.', 'reply_frames': [frames_data[-1]]})

        # is this ... wrong frame
        answer = {'class': StatementFrame, 'level': 0, 'pattern_class': LanguagePattern, 'format_spec': 'no, {pronoun} {verb} {object}.'}
        frames_data.append({'class': QuestionFrame, 'level': 0, 'pattern_class': LanguagePattern, 'format_spec': '{verb} {pronoun} {wrong_object}?', 'reply_frames': [answer]})
        frames_data.append({'class': InstructionFrame, 'level': 0, 'pattern_class': LanguagePattern, 'format_spec': 'ask if {pronoun} {verb} {wrong_object}.', 'reply_frames': [frames_data[-1]]})
        
        return frames_data

    _pattern_normalization_data = {'wrong_object': 'object', 'wrong_pronoun': 'pronoun'}

    _pattern_sentence_items = ['pronoun', 'verb', 'what_pronoun', 'it_pronoun']

    @classmethod
    def _get_language_items (cls, kwargv):
        grammar_object = kwargv['languageitem']
        wrong_object = kwargv['wrong_languageitem']
        #print(grammar_object, wrong_object)
        this = lexis.lexises.get(text='this').form(noun=grammar_object) # necessary to return object but not string
        wrong_this = lexis.lexises.get(text='this').form(noun=wrong_object)
        to_be = lexis.lexises.get(text='be', part='ToBe')
        #dog = lexis.lexises.get(text='dog', part='Noun')
        return {'pronoun': this,
                'verb': to_be,
                'object': grammar_object,
                'what_pronoun': 'what',
                'wrong_object': wrong_object,
                'it_pronoun': 'it'}


class Animals(Noun):
    
    @staticmethod
    def _frames_data():
        frames_data = []

        frames_data.append({'class': StatementFrame, 'level': 0, 'pattern_class': LanguagePattern, 'format_spec': '{subject} {verb} an animal.'})
        answer = {'class': StatementFrame, 'pattern_class': LanguagePattern, 'format_spec': 'yes, {subject} {verb} an animal.'}
        frames_data.append({'class': QuestionFrame, 'level': 0, 'pattern_class': LanguagePattern, 'format_spec': '{verb} {subject} an animal?', 'reply_frames': [answer]})
        frames_data.append({'class': InstructionFrame, 'level': 0, 'pattern_class': LanguagePattern, 'format_spec': 'ask if {subject} {verb} an animal.', 'reply_frames': [frames_data[-1]]})
        
        return frames_data

    _pattern_sentence_items = ['verb']

    @classmethod
    def _get_language_items (cls, kwargv):
        grammar_subject = kwargv['languageitem']
        to_be = lexis.lexises.get(text='be', part='ToBe')
        return {'subject': grammar_subject,
                'verb': to_be}

class Land(UsageCase):
    
    @staticmethod
    def _frames_data():
        frames_data = []
        frames_data.append({'class': StatementFrame, 'level': 0, 'pattern_class': LanguagePattern, 'format_spec': '{subject} has four legs.'})
        frames_data.append({'class': StatementFrame, 'level': 0, 'pattern_class': LanguagePattern, 'format_spec': '{subject} can walk.'})
        frames_data.append({'class': StatementFrame, 'level': 0, 'pattern_class': LanguagePattern, 'format_spec': '{subject} can run.'})
        return frames_data

    _pattern_sentence_items = []
    
    @classmethod
    def _get_language_items (cls, kwargv):
        grammar_subject = kwargv['languageitem']
        return {'subject': grammar_subject}

class LandAnimals(Animals, Land):
    """ """

class UsageCaseBuilder():
    """
    Used to build UsageCase based on UsageCase data
    """


class PossessiveProperty(UsageCase):
    """
    Something related to object or person from possessive perspective.

    Example:
    My name is Oleksandr. 'name' - possesive propery, use determiner (my, his, her, ...)
    {determiner} {property_name} {verb} {property_value}
    My favourit color is blue.
    {determiner} {adjective} {property_name} {verb} {property_value}
    """
    @staticmethod
    def _frames_data():
        frames_data = []
        frames_data.append({'class': StatementFrame, 'level': 0, 'pattern_class': LanguagePattern, 'format_spec': '{determiner} {adjective} {subject} {verb} {complement}.'})
        frames_data.append({'class': QuestionFrame, 'level': 0, 'pattern_class': LanguagePattern, 'format_spec': 'what {verb} {determiner} {adjective} {subject}?'})
        """NEW VERSION
        frames_data.append({'class': StatementFrame, 'level': 0, 'format_spec': ['determiner', 'adjective_1', 'noun', 'verb', 'adjective_2']})
        """
        return frames_data

    _pattern_sentence_items = ['determiner', 'adjective', 'noun', 'verb']

    @classmethod
    def _get_language_items (cls, kwargv):
        adjective = kwargv.get('adjective') # is optional, so None is possible
        person = kwargv['person']
        grammar_person = kwargv['grammar_person']
        subject = kwargv['subject']
        to_be = lexis.lexises.get(text='be', part='ToBe')
        determiner = languageitem.PossessiveDeterminer.form(grammar_person=grammar_person, noun=person)
        grammar_object = kwargv['object']
        return {'determiner': determiner,
                'adjective': adjective,
                'subject': subject,
                'verb': to_be,
                'complement': grammar_object}
    

if __name__ == '__main__':
    """
    pass
    cat = Noun()
    print(cat.get_usagecases('cat', 'dog'))
    """
    #print(Noun(0, **{'languageitem': 'cat'}))
    #print(Noun._frames_data())
    person = lexis.lexises.get(text='oleksandr')
    print(PossessiveProperty.usage_cases(person=person, grammar_person=1, adjective='favourite', subject=lexis.lexises.get(text='colour'), **{'object': person.__dict__['favourite colour']}))
    print(PossessiveProperty.usage_cases(person=person, grammar_person=2, adjective='favourite', subject=lexis.lexises.get(text='colour'), **{'object': person.__dict__['favourite colour']}))
    print(PossessiveProperty.usage_cases(person=person, grammar_person=3, adjective='favourite', subject=lexis.lexises.get(text='colour'), **{'object': person.__dict__['favourite colour']}))
