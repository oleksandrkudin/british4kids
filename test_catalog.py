"""
Test module for languageitem
"""
from catalog import *
import importlib

import unittest
import lexis
import usagecase

class VocabularyTest(unittest.TestCase):
    def setUp(self):
        if not 'vocabulary' in self.__dict__:
            importlib.reload(nouns)
            self.vocabulary = Vocabulary(nouns.dict_txt_nouns)
            #self.vocabulary.update(Vocabulary(nouns.dict_txt_nouns))
            #print(self.vocabulary)

    def test_vocabulary(self):
        """
        check if all items are loaded, nothing more
        check that loaded language_items converted to string equal to manualy defined dictionary.
        only text data is evaluated.
        language_item attributes are not avaluated.
        usage_cases are not avaluated
        """
        nouns = {'animals': set(['cat', 'dog', 'cow', 'horse', 'sheep', 'rabbit']),
                 'vehicles': set(['car', 'bus', 'tram', 'trolleybus', 'bicycle']),
                 'clothes': set(['trousers', 'dress'])}

        vocabulary = {}
        for topic, vocabulary_items in self.vocabulary.items():
            vocabulary[topic] = set(map(lambda v_i: str(v_i.language_item), vocabulary_items))

        self.assertEqual(vocabulary, nouns)

    def test_lexis_filter(self):
        #print(lexis.lexises.get(text='cat').usage_case)
        this = lexis.lexises.get(text='this')
        #print('this', languageitem.LanguageItemForm(this.form(plural=True),this,plural=True).level)
        
        
        self.assertEqual(str(lexis.lexises.get(text='cat').form(plural=True)), 'cats')
        self.assertEqual(str(lexis.lexises.get(text='cat', meaning='pet')), 'cat')
        self.assertEqual(set(map(str, lexis.lexises.filter(level='A1'))), set(['cat', 'dog', 'cow', 'horse', 'car', 'bus', 'be', 'trousers', 'dress', 'what', 'colour']))

    def test_usage_case(self):
        
        for i_vocabulary_item in self.vocabulary['animals']:
            #print(i_vocabulary_item.language_item)
            print(i_vocabulary_item.main_frame('learn'))
            print(i_vocabulary_item.main_frame('check'))
            print(i_vocabulary_item.main_frame('ask'))
            if i_vocabulary_item.is_extra_usage_cases():
                print(i_vocabulary_item.extra_frame('learn'))
    def test_learning_frames(self):
        configuration = []
        topic = 'animals'
        for i_vocabulary_item in self.vocabulary[topic]:
            language_item = i_vocabulary_item.language_item
            frame_type = random.choice(['main','extra'])
            #frame_type = 'main'
            activities = random.choice(['learn','check','ask'])
            #activities = 'learn'
            configuration.append((language_item, frame_type, activities))
        
        learning_frames = self.vocabulary.learning_frames(topic, configuration)
        for i in learning_frames:
            print(i)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(VocabularyTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
