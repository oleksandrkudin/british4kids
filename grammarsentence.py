"""
Define language sentence structure from grammar perspective
"""

#import operator
import lexis


#difference in naming in 2.7 and 3.4
try:
    from itertools import zip_longest as zip_longest
except:
    from itertools import izip_longest as zip_longest

from speechparts import *

vowels = ['a', 'e', 'i', 'o', 'u']


class SentencePart():
    """

    """
    @classmethod
    def match_old(cls, rest_speech_parts, strict=True):
        """
        Check if speech parts correspond to sentence structure
        Main thing is a sentence structure - it should be checked
        Return
            True - match -
            False - not match ...
            None - not found - none of sentence part has been found the match

        """
        # Only first function (strict=True) invoke should copy list
        # in recursion first element is deleted after match is finding
        if strict:
            rest_speech_parts = rest_speech_parts[:]
        sentence_part_matches = []

        # Save matching result in list
        for sentence_part, optional in cls.structure:
            try:
                speech_part = rest_speech_parts[0]
            except IndexError:
                sentence_part_matches.append(0)
                break
            if issubclass(sentence_part, SentencePart):
                match_result = sentence_part.match_old(rest_speech_parts, strict=False)
                if match_result:
                    sentence_part_matches.append(1)
                    if issubclass(cls, SentenceBlock):
                        break
                elif match_result == None:
                    sentence_part_matches.append(0)
                else:
                    return False
            elif issubclass(sentence_part, SpeechPart):
                if sentence_part == speech_part.__class__:
                    sentence_part_matches.append(1)
                    rest_speech_parts.pop(0) #move next
                else:
                    sentence_part_matches.append(None)
            else:
                raise TypeError(sentence_part)

        # Inspect matching result and create return value
        #print('Debug', cls.__name__, cls.structure, sentence_part_matches)

        #no elements should be in original list of speech parts
        if strict and rest_speech_parts:
            return False
        #if no matches found - return None - we cannot define True or False
        if all(map(lambda match: match == None, sentence_part_matches)):
            if not strict:
                return None
            else:
                return False
        #check optinal and compalsory parts
        for (sentence_part, optional), match in zip(cls.structure, sentence_part_matches):
            if not match and not optional:
                return False
        return True



class ComplexItem(list, SentencePart):
    """
    Element to describe sentence/phrase structure what consist of elements with some logic
    """
    structure = []

    def __init__(self, speech_parts):
        """
        should check if speech_parts match specific SentencePhrase
        if self.match(speech_parts)
        for each class in structure create list except speech part, extend in resulting
        """
        list.__init__(self)
        # TODO: Necessary to define where to check if speech_parts compartible with self.__class__
        # now match return False that is not iterable and so TypeError (Interface error)
        for i_match in self.match(speech_parts):
            structure_item = i_match[0]
            i_speech_parts = i_match[1]
            
            if structure_item == SimpleSubject:
                # TODO: get basic_noun and conjugate verb
                pass
            
            if type(structure_item) == type and issubclass(structure_item, list):
                self.extend(structure_item(i_speech_parts))
            else:
                self.extend(i_speech_parts)
    def __str__(self):
        return ' '.join(self)

class SentencePhrase(ComplexItem):
    """List of language_items of SpeechPart classes what satify phrase structure
    Define phrase structure in term of SpeechPart, SentencePhrase, SentenceBlock classes, their order and optionality
    """


    @classmethod
    def compatible(cls, speech_parts, strict=True):
        """
        Check if speech_parts and their order compatible with phrase
        strict define that ellements from speech_parts should be compatible,
        otherwise tail is possible
        Return
            True
            False
            None - can not be defined
        """
    @classmethod
    def compare(cls, speech_parts, strict=True):
        """
        Compare speech_parts to phrase structure and return result
        """
        if strict:
            speech_parts = speech_parts[:]
        speech_parts_copy = speech_parts[:]

        compare_list = []
        for structure_item_data in cls.structure:
            structure_item = structure_item_data[0] # 2-nd element is optionality
            if speech_parts_copy:
                compare_result = structure_item.compare(speech_parts_copy, strict=False)
                compare_list.append(compare_result)
            else:
                compare_list.append(False)

        # check optinal and compalsory parts
        # TODO: what if compare_list is empty - then return True - not correct
        # zip may truncate lists to least number of elements
        assert compare_list, ValueError(compare_list)
        assert len(cls.structure) == len(compare_list), ValueError(cls.structure, compare_list)
        for (structure_item, optional), match in zip_longest(cls.structure, compare_list):
            if not match and not optional:
                return False
        else:
            while speech_parts != speech_parts_copy:
                speech_parts.pop(0)
            if strict and speech_parts_copy:
                # no elements should be in original list of speech parts if strict
                return False
            else:
                return True

    @classmethod
    def match(cls, speech_parts, strict=True):
        """
        Return list of speech_parts matching phrase structure.
        Maps speech_parts to structure items 
        ((class, ()), )
        """
        if strict:
            speech_parts = speech_parts[:]
        speech_parts_copy = speech_parts[:]

        compare_list = []
        matches = []
        index_speech_parts = 0
        for structure_item_data in cls.structure:
            structure_item = structure_item_data[0] # 2-nd element is optionality
            if speech_parts_copy:
                compare_result = structure_item.compare(speech_parts_copy, strict=False)
                compare_list.append(compare_result)

                if compare_result:
                    matched_speech_parts = []
                    while index_speech_parts < len(speech_parts) - len(speech_parts_copy):
                        matched_speech_parts.append(speech_parts[index_speech_parts])
                        index_speech_parts += 1
                    matches.append((structure_item, matched_speech_parts))

            else:
                compare_list.append(False)

        # check optinal and compalsory parts
        # TODO: what if compare_list is empty - then return True - not correct
        # zip may truncate lists to least number of elements
        assert compare_list, ValueError(compare_list)
        assert len(cls.structure) == len(compare_list), ValueError(cls.structure, compare_list)
        for (structure_item, optional), match in zip_longest(cls.structure, compare_list):
            if not match and not optional:
                return False
        else:
            while speech_parts != speech_parts_copy:
                speech_parts.pop(0)
            if strict and speech_parts_copy:
                # no elements should be in original list of speech parts if strict
                return False
            else:
                return matches

class SentenceBlock(ComplexItem):
    """
    Structure is a list of possible elements.
    Only one element from block must match.
    """
    """
    def __init__(self, speech_parts):
        for sentence_part, optional in self.structure:
            if sentence_part.match(speech_parts):
                speech_parts = sentence_part(speech_parts)
                break
        else:
            raise AttributeError(speech_parts, self.__class__)
        list.__init__(self, speech_parts)
    """
    """
    @classmethod
    def match(cls, rest_speech_parts, strict=True):
        for sentence_part, optional in cls.structure:
    """
    @classmethod
    def compare(cls, speech_parts, strict=True):
        """
        Compare speech_parts to phrase structure and return result
        """
        speech_parts_copy = speech_parts[:]
        for structure_item in cls.structure:
            if not speech_parts_copy:
                return False
            if structure_item.compare(speech_parts_copy, strict=False):
                while speech_parts != speech_parts_copy:
                    speech_parts.pop(0)
                return True
        return False

    @classmethod
    def match(cls, speech_parts, strict=True):
        """
        Here we expect matching speech_parts and matching class from structure
        because we need to know what class should be passed matching speech_parts
        [class -> [speech_part, ...]]
        """

        speech_parts_copy = speech_parts[:]
        for structure_item in cls.structure:
            if not speech_parts_copy:
                return False
            if structure_item.compare(speech_parts_copy, strict=False):
                matched_speech_parts = []
                while speech_parts != speech_parts_copy:
                    matched_speech_parts.append(speech_parts.pop(0))
                return [[structure_item, matched_speech_parts]]
        return False


#
#Noun phrases block
#


class NounPhrase(SentencePhrase):
    """Base class for all NounPhrase without accurate structure - so it is abstruct class
    Accurate structure is defined in subclass.
    This class cannot be used as object!!!
    Define phrase structure in term of Phrase or SpeechPart and optional flag
    """
    structure = []

    def __init__(self, speech_parts):
        SentencePhrase.__init__(self, speech_parts)
        article = self.get_article()
        if article:
            self.insert(0, article)

    def get_article(self):
        return None

class SpecificProperNounPhrase(NounPhrase):
    """the <specific proper noun>
    Example:
        the Atlantic Ocean, the Sahara
    """
    structure = [(DefiniteArticle, 0), (SpecificProperNoun, 0)]
    def get_article(self):
        return lexis.lexises.get(text='the')

class NonPersonalPronoun(NounPhrase):
    """<non-personal pronoun>
    Example:
        this, someone, anyone
    """
    structure = [(Pronoun, 0)]

class AdverbAdjective(SentencePhrase):
    """Base class for  [<adverb>* <adjective>]<noun> structure"""
    structure = [(Adverb, 1), (Adjective, 0)]

class SimpleNoun(NounPhrase):
    """
    <article> [<adverb>* <adjective>] <noun>
    [<adverb>* <adjective>] <noun-plural>
    Example:
        a very long bridge
        the book
        the extremely pretty dress

        very yellow flowers
        books
    """
    structure = [(Article, 1), (AdverbAdjective, 1), (Noun, 0)]
    def get_article(self):
        """Depends on speech parts - so """
        noun = self[-1] # last speech part in the list
        if noun.countable and not noun.plural:
            if self[0][0].lower() in vowels: return IndefiniteArticle('an')
            else: return IndefiniteArticle('a')

class ProperNounPossesivePhrase(NounPhrase):
    """<proper noun-possessive> [<adverb>* <adjective>] <noun>
    Example:
        John's very long sentence
        Mary's shoes
    """
    structure = [(ProperNounPossesive, 0), (AdverbAdjective, 1), (Noun, 0)]

class PersonalPossessiveAdjectivePhrase(NounPhrase):
    """<personal possessive adjective> [<adverb>* <adjective>] <noun>
    Example:
        his book
        my very long hair
    """
    structure = [(PersonalPossesiveAdjective, 0), (AdverbAdjective, 1), (Noun, 0)]

class CommonNounPossessive(NounPhrase):
    """<article> <common noun-possessive>  [<adverb>* <adjective>] <noun>
    Example:
        a dog's tail
        the book's very difficult style
    """
    structure = [(Article, 1), (NounPossessive, 0), (AdverbAdjective, 1), (Noun, 0)]

    def get_article(self):
        return SimpleNoun.get_article(self)


class NounBlock(SentenceBlock):
    structure = [SpecificProperNounPhrase, NonPersonalPronoun, SimpleNoun,
                 ProperNounPossesivePhrase, PersonalPossessiveAdjectivePhrase, CommonNounPossessive]



#
#Complement block
#


#
# High level Sentence structure
#

class SimpleSubject(SentenceBlock):
    """
    """
    structure = [NounBlock, NominativePersonalPronoun]

    @staticmethod
    def get_basic_noun(subject_speech_parts):
        """
        Return Noun or Pronoun object, otherwise raise exception.
        """
        for i_speech_part in subject_speech_parts:
            if isinstance(i_speech_part, Noun) or isinstance(i_speech_part, Pronoun):
                return i_speech_part
        raise TypeError(self)

class Subject(SentenceBlock):
    """
    Missed CompoundSubject
    """
    structure = [SimpleSubject]

class VerbBlock(SentenceBlock):
    """
    Missed VerbPhrase
    """
    structure = [Verb]

    @staticmethod
    def conjugate(verbs, noun_basic):
        #print('noun_basic=', noun_basic, verbs[0].__class__)
        return [verbs[0].form(noun=noun_basic)]



class SimpleObject(SentenceBlock):
    """
    """
    structure = [NounBlock, ObjectivePersonalPronoun]

class Object(SentenceBlock):
    """
    Missed CompoundObject
    """
    structure = [SimpleSubject]

class Complement(SimpleObject):
    """
    [<indirect object>] <object>
    <adverb>* <adjective>
    <prep phr>*
    "to" <Vinf> [<object>]
    <Ving>
    """
    structure = [(Object, 0)]

#
#Subclasses to build interrogative sentence
#
class InterrogativePronounBlock(SentenceBlock):
    """
    "What" |"Which" |"When" |"Where" |"Who" |"To whom" | "Why"
    """
    structure = [lexis.lexises.get(text='what'), lexis.lexises.get(text='which'),
                 lexis.lexises.get(text='when'), lexis.lexises.get(text='where')]

class InterrogativePredicate(SentencePhrase):
    """
    <verb block> <object>
    """
    structure = [(Verb, 1), (Object, 1)]

class EndingBlock1(SentenceBlock):
    """
    <adverb>* <adjective> | <prep phr>* | <predicate>
    """
    structure = [AdverbAdjective, InterrogativePredicate]

class QuestionPhrase():
    @classmethod
    def conjugate_verb(cls, speech_parts):
        mappings = cls.match(speech_parts)
        for i_structure, i_speech_parts in mappings:
            if isinstance(i_structure, Verb):
                verb_block = i_speech_parts
                verb_block_start_index = speech_parts.index(verb_block[0])
            if type(i_structure) == type and issubclass(i_structure, Subject):
                subject = i_speech_parts
                break
        basic_noun = SimpleSubject.get_basic_noun(subject)
        conjugated_verb_block = VerbBlock.conjugate(verb_block, basic_noun)

        speech_parts[verb_block_start_index:verb_block_start_index+len(verb_block)] = conjugated_verb_block

class QuestionPhrase1(SentencePhrase, QuestionPhrase):
    """
    ["What" |"Which" |"When" |"Where" |"Who" |"To whom" | "Why"] 
    ("are" |"is" |"was" |"were" | "aren't" |"isn't" |"wasn't" |"weren't") 
    <subject> 
    [<adverb>* <adjective> | <prep phr>* | <predicate>]"?" 
    """
    structure = [(InterrogativePronounBlock, 1), (lexis.lexises.get(text='be'), 0), (Subject, 0), (EndingBlock1, 1)]

 


class QuestionPhrase2(SentencePhrase, QuestionPhrase):
    """
    ["What" |"When" |"Where" |"Who" |"To whom" |"Why"] 
    ("do" |"does" |"don't" |"doesn't" |"did" |"didn't")
    <subject> <predicate>"?"

    Where does John live?
    Does John go to Manhattan? 
    """
    structure = [(InterrogativePronounBlock, 1), (lexis.lexises.get(text='do'), 0), (Subject, 0), (InterrogativePredicate, 0)]

#
#Different type os Sentences
#
    

class DeclarativeSentence(SentencePhrase):
    """
    """
    #structure = [(Subject, 0), (VerbPhrase, 0), (Complement, 0)]
    structure = [(Subject, 0), (VerbBlock, 0), (Object, 0)]

    def __init__(self, speech_parts):
        """
        should check if speech_parts match specific SentencePhrase
        if self.match(speech_parts)
        for each class in structure create list except speech part, extend in resulting
        """
        SentencePhrase.__init__(self, speech_parts)
        self.conjugate_verb(self)

    @classmethod
    def conjugate_verb(cls, speech_parts):
        """
        find subject and verb and send conjugate to verb with noun from subject
        """
        mappings = cls.match(speech_parts)

        subject = mappings[0][1]
        basic_noun = SimpleSubject.get_basic_noun(subject)

        verb_block = mappings[1][1]
        conjugated_verb_block = VerbBlock.conjugate(verb_block, basic_noun)

        speech_parts[len(subject):len(subject)+len(verb_block)] = conjugated_verb_block

    def __str__(self):
        return SentencePhrase.__str__(self) + self.ending_symbol()

    @staticmethod
    def ending_symbol():
        return '.'    

class InterrogativeSentence(SentenceBlock):
    """
    There is no clear structure.
    """
    structure = [QuestionPhrase1, QuestionPhrase2]

    def __init__(self, speech_parts):
        """
        should check if speech_parts match specific SentencePhrase
        if self.match(speech_parts)
        for each class in structure create list except speech part, extend in resulting
        """
        SentenceBlock.__init__(self, speech_parts)
        self.conjugate_verb(self)

    @classmethod
    def conjugate_verb(cls, speech_parts):
        """
        find subject and verb and send conjugate to verb with noun from subject
        """
        mappings = InterrogativeSentence.match(speech_parts[:])
        question_phase_class = mappings[0][0]
        question_phase_class.conjugate_verb(speech_parts)

    def __str__(self):
        return SentenceBlock.__str__(self) + self.ending_symbol()

    @staticmethod
    def ending_symbol():
        return '?'

if __name__ == '__main__':
    this = lexis.lexises.get(text='this')
    to_be = lexis.lexises.get(text='be')
    to_do = lexis.lexises.get(text='do')
    
    #print('Check SpecificProperNounPhrase')
    #print(SpecificProperNounPhrase.compare([DefiniteArticle('the'), SpecificProperNoun('Pacific')]))
    #print(SpecificProperNounPhrase.compare([DefiniteArticle('the'), Noun('cat')]))
    print(DeclarativeSentence.compare([Adverb('amazingly'), Adjective('blue'), Noun(text='owl'), Verb('is')]))
    print(SpecificProperNounPhrase.compare([DefiniteArticle('the'), SpecificProperNoun('Sahara')]))
    print(NounBlock.compare([DefiniteArticle('the'), SpecificProperNoun('Sahara')]))
    print(DeclarativeSentence.compare([Adverb('amazingly'), Adjective('blue'), Noun(text='owl')]))
    print(DeclarativeSentence.match([Adverb('amazingly'), Adjective('blue'), Noun(text='owl'), Verb('is'), Noun('dog')]))

    print(Subject([Adverb('amazingly'), Adjective('blue'), Noun(text='owl', plural=False)]))
    print(DeclarativeSentence([Adverb('amazingly'), Adjective('blue'), Noun(text='owl'), ToBe('be'), Noun('cat')]))
    print(InterrogativePronounBlock([lexis.lexises.get(text='when')]))
    print(InterrogativePronounBlock([Pronoun('what')]))
    print(InterrogativeSentence([lexis.lexises.get(text='what'), to_be, this]))
    print(InterrogativeSentence([lexis.lexises.get(text='what'), to_be, Pronoun('you', grammar_person=2), Verb('doing')]))

    #my_to_be = ToBe('be').form(noun=these)
    #my_to_be.form()

    cats = Noun(text='cats', plural=True)
    
    these = lexis.lexises.get(text='this').form(noun=cats)
    #this = this.form(noun=cats)
    
    #print (this.__class__, this)
    print(InterrogativeSentence([to_be, these, cats]))
    print(DeclarativeSentence([this.form(plural=True), to_be, Adverb('amazingly'), Adjective('blue'), Noun(text='owls', plural=True)]))

    you = Pronoun('she', plural=False, grammar_person=3)
    print(InterrogativeSentence([to_do, you, Verb('like'), cats]))
    
    #print(ToBe('be').form(plural=True), ToBe('be').form(plural=True).__class__)


