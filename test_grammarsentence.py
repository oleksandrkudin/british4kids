"""
Test module for grammarsentence
"""
from grammarsentence import *
import lexis
import importlib
import sys

import unittest

all_speech_parts = []

class NounPhraseTest(unittest.TestCase):
    
    def test_noun_phrase(self):
        self.assertEqual(True, 1)
    def test_SpecificProperNounPhrase(self):
        self.assertTrue(SpecificProperNounPhrase.compare([DefiniteArticle('the'), SpecificProperNoun('Pacific')]))
        self.assertFalse(SpecificProperNounPhrase.compare([DefiniteArticle('the'), DefiniteArticle('the'), SpecificProperNoun('Pacific')]))
        self.assertFalse(SpecificProperNounPhrase.compare([SpecificProperNoun('Pacific')]))
        self.assertFalse(SpecificProperNounPhrase.compare([IndefiniteArticle('a'), SpecificProperNoun('Pacific')]))
        self.assertFalse(SpecificProperNounPhrase.compare([DefiniteArticle('the'), SpecificProperNoun('Pacific'), SpecificProperNoun('Pacific')]))
    
    def test_SimpleNoun_match(self):
        self.assertTrue(SimpleNoun.compare([Article('a'), Noun('cat')]))
        self.assertTrue(SimpleNoun.compare([Article('a'), Adjective('blue'), Noun('cat')]))
        self.assertTrue(SimpleNoun.compare([Article('a'), Adverb('very'), Adjective('blue'), Noun('cat')]))

        self.assertFalse(SimpleNoun.compare([Adjective('blue'), Adverb('very'), Noun('cat')]))
        self.assertFalse(SimpleNoun.compare([Adverb('very'), Noun('cat')]))
        self.assertFalse(SimpleNoun.compare([Noun('cat'), Adjective('blue')]))

    def test_SimpleNoun_init(self):
        
        self.assertEqual(SimpleNoun([Noun(text='cat')]),['a', 'cat'])
        self.assertEqual(SimpleNoun([Adjective('yellow'), Noun(text='car')]),['a', 'yellow', 'car'])
        self.assertEqual(SimpleNoun([Adverb('amazingly'), Adjective('blue'), Noun(text='owl')]),['an', 'amazingly', 'blue', 'owl'])

        self.assertEqual(CommonNounPossessive([NounPossessive("dog's"), Noun('tail')]), ['a', "dog's", 'tail'])
        self.assertEqual(CommonNounPossessive([NounPossessive("owl's"), Noun('tail')]), ['an', "owl's", 'tail'])

        self.assertEqual(PersonalPossessiveAdjectivePhrase([PersonalPossesiveAdjective('my'), Noun('book')]), ['my', 'book'])

        
        #self.assertTrue(DeclarativeSentence.compare([Adverb('amazingly'), Adjective('blue'), Noun(text='owl'), Verb('is')]))

        self.assertEqual(DeclarativeSentence([Adverb('amazingly'), Adjective('blue'), Noun(text='owl'), Verb('is'), Noun('cat')]),['an','amazingly','blue','owl','is','a','cat'])

    def test_sentence_item_compare(self):
        self.assertTrue(SpecificProperNounPhrase.compare([DefiniteArticle('the'), SpecificProperNoun('Pacific')]))
        self.assertFalse(SpecificProperNounPhrase.compare([DefiniteArticle('the'), DefiniteArticle('the'), SpecificProperNoun('Pacific')]))
        self.assertFalse(SpecificProperNounPhrase.compare([SpecificProperNoun('Pacific')]))
        self.assertFalse(SpecificProperNounPhrase.compare([IndefiniteArticle('a'), SpecificProperNoun('Pacific')]))
        self.assertFalse(SpecificProperNounPhrase.compare([DefiniteArticle('the'), SpecificProperNoun('Pacific'), SpecificProperNoun('Pacific')]))

        #self.assertFalse(DeclarativeSentence.compare([Adverb('amazingly'), Noun(text='owl'), Verb('is')]))

        #self.assertTrue(DeclarativeSentence.compare([Adverb('amazingly'), Adjective('blue'), Noun(text='owl'), Verb('is')]))
        self.assertTrue(DeclarativeSentence.compare([Adverb('amazingly'), Adjective('blue'), Noun(text='owl'), Verb('is'), Noun('mouse')]))
    def test_sentence_verb_conjugation(self):
        this = lexis.lexises.get(text='this')
        to_be = lexis.lexises.get(text='be')
        to_do = lexis.lexises.get(text='do')
        self.assertEqual(DeclarativeSentence([Adverb('amazingly'), Adjective('blue'), Noun(text='owl'), to_be, Noun('mouse')]), ['an','amazingly','blue','owl','is','a','mouse'])
        self.assertEqual(DeclarativeSentence([Adverb('amazingly'), Adjective('blue'), Noun(text='owls', plural=True), to_be, Noun('mouses', plural=True)]), ['amazingly','blue','owls','are','mouses'])
        self.assertEqual(DeclarativeSentence([this.form(plural=True), to_be, Adjective('blue'), Noun('mouses', plural=True)]), ['these','are','blue','mouses'])
        self.assertEqual(DeclarativeSentence([this, to_be, Adjective('blue'), Noun('mouse')]), ['this','is','a','blue','mouse'])

        self.assertEqual(InterrogativeSentence([to_do, Pronoun('she', plural=False, grammar_person=3), Verb('like'), Noun('cats', plural=True)]), ['does','she','like','cats'])
        self.assertEqual(InterrogativeSentence([to_do, Pronoun('he', plural=False, grammar_person=3), Verb('like'), Noun('cats', plural=True)]), ['does','he','like','cats'])
        self.assertEqual(InterrogativeSentence([to_do, Pronoun('they', plural=True, grammar_person=3), Verb('like'), Noun('cats', plural=True)]), ['do','they','like','cats'])
        self.assertEqual(InterrogativeSentence([to_do, Pronoun('i', grammar_person=1), Verb('like'), Noun('cats', plural=True)]), ['do','i','like','cats'])

        self.assertEqual(InterrogativeSentence([to_be, this.form(plural=True),  Noun('cats', plural=True)]), ['are','these','cats'])
        self.assertEqual(InterrogativeSentence([to_be, this,  Noun('cat')]), ['is','this','a','cat'])

if __name__ == '__main__':
    #add all SpeechPart classes to all_speech_parts
    for i_name, i_object in  sys.modules['grammarsentence'].__dict__.items():
        if isinstance(i_object, type) and issubclass(i_object, SpeechPart):
            all_speech_parts.append(i_object)
    suite = unittest.TestLoader().loadTestsFromTestCase(NounPhraseTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
