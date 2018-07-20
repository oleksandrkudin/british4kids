"""
All language speech parts and their subclasses
"""
import languageitem

class SpeechPart(languageitem.TxtAudioResource):
    """
    Base class for all language speech part from grammar perspective.
    Each speech part has fields dictionary with default values.
    Corresponding attributes will be added to object.
    
    Example:
        Adjective
        Article
        Adverb
        Noun

    fields
        states - old feature to define usage cases
        mearning - each word may have different mearning
            cat - maybe PET or defining whole WILD ANIMAL class
        part - particular SubClass of SpeechPart
             

    """
    fields = {'level': 0, 'states': [], 'meaning': '', 'part': None}
    def __new__(cls, text, audio_source=None, **extra):
        self = languageitem.TxtAudioResource.__new__(cls, text, audio_source)
        self.default(self)

        for parameter, value in extra.items():
            if parameter in self.__dict__:
                self.__dict__[parameter] = value
            else:
                print('WARNING: Field %s is not supposed for %s.' % (parameter, self.__class__.__name__))

        return self

    @classmethod
    def default(cls, self):
        """
        Add attributes corresponding to fields list and intitialize with default values.
        """
        if 'fields' in cls.__dict__:
            for key, value in cls.__dict__['fields'].items():
                #if value != None:
                self.__dict__[key] = value
        #recursive set default values
        for i_cls in cls.__bases__:
            if getattr(i_cls, 'default', None):
                #if 'default' in i_cls.__dict__:
                i_cls.default(self)

    @classmethod
    def compare(cls, speech_parts, strict=True):
        """
        If first element of speech_parts list corresponds to cls class.
        Used to check correctness of sentence and phrase structure
        """
        # TODO: wrong to change initial speech_parts list by removing element
        # move to logic that suppose element removal
        assert speech_parts, ValueError(speech_parts)
        if isinstance(speech_parts[0], cls):
            speech_parts.pop(0)
            return True
        else:
            return False

    def contain(self, **kwargv):
        """evaluate if object contain attr = value from kwargv"""
        for attr, value in kwargv.items():
            if attr == 'text':
                if not str(self) == value:
                    return False
            elif attr == 'part':
                if not self.__class__.__name__ == value:
                    return False
            else:
                if not attr in self.__dict__ or not self.__dict__[attr] == value:
                    return False
        return True


    def __hash__(self):
        if 'meaning' in self.__dict__:
            return hash(self + self.meaning)
        else:
            return str.__hash__(self)
    def __eq__(self, other):
        if 'meaning' in self.__dict__:
            obj = self + self.meaning
        else:
            obj = str(self)
        if isinstance(other, SpeechPart) and 'meaning' in other.__dict__:
            other = other + other.meaning
        return str.__eq__(obj,other)


class SpeechPartForm(SpeechPart):
    def __new__(cls, text, languageitem, audio_source = None, **extra):
        self = languageitem.__class__.__new__(languageitem.__class__, text, audio_source)
        self._languageitem = languageitem
        for parameter, value in extra.items():
            self.__dict__[parameter] = value
        return self
    def __getattr__(self, attr):
        return getattr(self._languageitem, attr)


#
#Base classes for speech parts
#

class Adjective(SpeechPart):
    """
    modifies a noun.
    Examples: yellow, pretty, useful
    """

class Article(SpeechPart):
    """
     specifies whether the noun is specific or a member of a class.
     The definite article "the" refers to specific objects.
     The indefinite articles "a", and "an" refer to an unspecified member of a class.
     Examples: a, an, the
    """

class Adverb(SpeechPart):
    """
    modifies a verb or an adjective. Many adverbs have the suffix -ly.
    Examples: very, extremely, carefully
    """

class Noun(SpeechPart):
    """Countable | Uncountable can be defined by context of sentence
    Uncountable is the general form - do you like carrot
    But how it is related to plural

        Attributes:
            level: should be moved to LanguageItem as it is common for all words and phrases
            countable:
            uncountable:
            pluralform:
            plural:
            article:
            live:
            grammar_person:
                first-person - refer to the speaker, singular - I, plural - WE
                second-person - person or persons being addressed, singular = plural - YOU
                third-person - normally refer to third parties, singular - HE, SHE, IT,
                    plural - THEY

    """
    fields = {'countable': True, 'uncountable': False, 'pluralform': None,
              'plural': False, 'article': None, 'live': False, 'grammar_person': 3}



class Pronoun(SpeechPart):
    fields = {'pluralform': '', 'plural': False, 'grammar_person': 3}
    """
    Pronouns are a major subclass of nouns
    Pronoun replace noun and has direct relation with noun
        this(noun=cat) -> this
        this(noun=cats) -> these
        personal_pronoun(noun=sophia, grammar_person=1)
    Example:
        Personal subject pronoun: I, WE, YOU, HE, SHE, IT, THEY
        Personal object pronoun: me, you, him. her, it, us, you, them
        Possessive: mine, yours, his, hers, ours, theirs
        Reflexive: myself, yourself, himself, herself, itself, oneself, ourselves, yourselves,
            themselves
        Reciprocal: each other, one another
        Relative: that, which, who, whose, whom, where, when
        Demonstrative pronoun: THIS, THESE, THAT, THOSE
        Interrogative: who, what, why, where, when, whatever
        Indefinite: anything, anybody, anyone, something, somebody, someone, nothing, nobody, none,
            no one
    """
    def form(self, plural=False, noun=None):
        if noun:
            plural = noun.plural
    
        if plural:
            return SpeechPartForm(self.pluralform, self, plural=plural)
        else:
            # TODO: it is necessary to define singularform
            return self
        

class Verb(SpeechPart):
    """
    Represent verb from grammar perspective.
    Verb forms
        base form: go, work
        present form: go, goes; work, works;
        past form: went; worked;
        -ed form: gone; worked;
        -ing form: going; working;
    Regular
        past form = -ed form: base + ed
        -ing form: base + ing 
    Irregular
    Verb form depend on:
        tence(time)
        subject (noun in subject)
            person (1, 2, 3)
            number (plural/singular)
            *gender - not in English
        aspect (continuous, perfect, simple)
        mood (statement, interrogative, conditional, hypothetical)
        voice (passive, active)
        
    Example: work, works, worked, working
    grammar_person:
        first-person - refer to the speaker, singular - I, plural - WE
        second-person - person or persons being addressed, singular = plural - YOU
        third-person - normally refer to third parties, singular - HE, SHE, IT, plural - THEY
    
    """
    def form(self, person=3, time='presence', plural=False, noun=None):
        """
        time = present, past, future, future-in-the-past
        person = 1,2,3
        plural/singular
        """
        return self


#
#Subclasses
#

# ADJECTIVE sub classes

class PersonalPossesiveAdjective(Adjective):
    """
    Examples: my, your, his, her, its, our, your, their
    """

# ARTICLE sub classes
class DefiniteArticle(Article):
    """ The article"""
    pass

class IndefiniteArticle(Article):
    """ A, an article"""
    pass


# NOUN sub classes

class ProperNoun(Noun):
    """<proper noun>
    Example:
        John, America, Dr. Allen, State Street
    """

class SpecificProperNoun(Noun):
    """
    Example:
        the Atlantic Ocean
        the Sahara 
    """

class ProperNounPossesive(Noun):
    """
    Example:
        Oleksandr's book
    """

class NounPossessive(Noun):
    """
    Example: a dog's tail
    """

#PRONOUNS sub classes

class NominativePersonalPronoun(Pronoun):
    """
    Example:
        Personal object pronoun: me, you, him. her, it, us, you, them
    """
class ObjectivePersonalPronoun(Pronoun):
    """
    Example:
        Personal subject pronoun: I, WE, YOU, HE, SHE, IT, THEY
    """

#VERBS sub classes

class AuxiliaryVerb(Verb):
    """
    A verb used in forming the tenses, moods, and voices of other verbs.
    """

class PrincipalAuxiliaryVerb(AuxiliaryVerb):
    """
    The principal AuxiliaryVerb are be, do, and have.
    """

class ModalAuxiliaryVerb(AuxiliaryVerb):
    """
    These combine with other verbs to express necessity, possibility, intention, or ability.
    The modal auxiliary verbs are must, shall, will, should, would, ought (to), can, could, may, and might. 
    """

class ToBe(Verb):
    """
    """
    def form(self, person=3, time='present', plural=False, noun=None):
        if time == 'present':
            if noun:
                plural = noun.plural
                person = noun.grammar_person
            
            if person == 1:
                return SpeechPartForm('am', self)
            elif person == 2:
                return SpeechPartForm('are', self)
            elif person == 3:
                if not plural:
                    return SpeechPartForm('is', self)
                else:
                    return SpeechPartForm('are', self)

    def short_form(self, person=3, time='present', plural=False):
        if time == 'present':
            if person == 1:
                return SpeechPartForm('m', self)
            elif person == 2:
                return SpeechPartForm('re', self)
            elif person == 3:
                if not plural:
                    return SpeechPartForm('s', self)
                else:
                    return SpeechPartForm('re', self)


class ToDo(Verb):
    """
    """
    def form(self, person=3, time='present', plural=False, noun=None):
        if time == 'present':
            if noun:
                plural = noun.plural
                person = noun.grammar_person
            
            if person == 1:
                return SpeechPartForm('do', self, grammar_person=person, plural=plural)
            elif person == 2:
                return SpeechPartForm('do', self, grammar_person=person, plural=plural)
            elif person == 3:
                if not plural:
                    return SpeechPartForm('does', self, grammar_person=person, plural=plural)
                else:
                    return SpeechPartForm('do', self, grammar_person=person, plural=plural)

#PERSONS

class Person(Noun):
    """Include name, age, nationality and other behaviour via mixing classes or via LearningItem -> Interaction???
name: Sophia
age: 5
country: Ukraine
city: Kyiv
sex: male|femail
"""
    fields = {'name': '', 'sex': '', 'favourite colour': '', 'favourite drink': '', 'age': '', 'country': '', 'nationality': '', 'visual_source': '', 'plural': False, 'uncountable': False, 'countable': True}
    def __init__(self, text, **__):
        self.set_grammar_form()
        if 'age' in self.__dict__:
            self.__dict__['age long'] = self.age + ' years old'
    def set_grammar_form(self, grammar_form = 1):
        self.grammar_form = grammar_form
        #self.__dict__['favorite color'] = 'blue'
        return self
