"""
Catalog is the highest level object to contain learning data.
Has knowleadge about configuration files to take data from and create structure to be used
in learning activities.
Catalog may contain different type of data/learning_materials
    Vocabulary data
    Dialogs
    Text story ...

"""
import random
import languageitem
import usagecase
import nouns
#import auxiliary_words
import lexis

CATALOG_CONF = {}
CATALOG_CONF['data'] = []
CATALOG_CONF['data'].append({'vocabulary': nouns.dict_txt_nouns})


class Catalog(dict):
    """
    Catalog contain data to be loaded to learning activities.
    It takes data from configuration files. So it will differ on raw data.
    What type of data is supported by catalog?
        vocabulary
        dialog = ordered list of language_item usage cases
        interaction = ordered list of language_item usage cases
    memory and remember is not learning material but activities!

    Let's consider language_items as separate from Catalog! Why then it is should be loaded here?
    
    """
    def __init__(self):
        dict.__init__(self)
        self['data'] = {}
        #self.load(CATALOG_CONF)

    def load(self, catalog_conf):
        """loading order is important"""
        catalog_data = catalog_conf['data']
        for i_catalog_conf in catalog_data:
            data_type, catalog_data = list(i_catalog_conf.items())[0]
            self.load_specific(data_type, catalog_data)

    def load_specific(self, data_type, catalog_data):
        if data_type == 'vocabulary':
            """load vocabulary"""
            data_object = Vocabulary(catalog_data)
        else:
            raise Exception('Data type "" is not supported.' % data_type)
        self['data'][data_type] = data_object

class Vocabulary(dict):
    """
    What is vocabulary???
    option1. [topic]...[topic] = [list of VocabularyItem]
        possible to have some own bihaviour 
    
    option2. [topic]...[topic][language_item] = usage_cases
        no own behavior. All should be implemented in usage_cases.
        It may be OK if only one usage, but what if many usage_cases
    
    Represent single language_item and topic/category
    Example: ['animals'] = [list of animals VocabularyItem]
    """
    def __init__(self, data):
        dict.__init__(self)
        self.load(data)

    def load(self, data):
        """
        Data example:
            vehicles:
                car: {grammar: {part: Noun, level: A1}, usage: {part: Noun}}
        Creation of language_items should be in one place
        and it should be controlled by the same object type.
        It is necessary to create language_item and register it in lexis

        Problem here is that we need to populate lexises with language_items
        and only after that create vocabulary_items
            
        """
        #print(self, 'running load')
        # create list of language_item and UsageCase name so they will be mapped 1-to-1
        vocabulary_catalog_data = {}
        for topic, language_items_data in data.items():
            if not topic in self: # assign empty list if there is no such topic yet
                self[topic] = []
            for text, i_language_item in language_items_data.items():
                grammar_data = i_language_item['grammar']
                usage_case = i_language_item['usage']
                
                if not topic in vocabulary_catalog_data:
                    vocabulary_catalog_data[topic] = []
                vocabulary_catalog_data[topic].append((lexis.lexises.create(text, topic,
                                                                            grammar_data),
                                                    usage_case))
        
        # create VocabularyItem based on language_item and UsageCase class
        for topic, vocabulary_items_data in vocabulary_catalog_data.items():
            if len(vocabulary_items_data) == 1:
                raise IndexError('Not enough elements to choose wrong_language_item for %s topic.' % topic)
            for language_item, usage_case_data in vocabulary_items_data:

                # Add visual_source from data directory
                visual_source = grammar_data.pop('visual_source', None)
                if not visual_source:
                    visual_source_file = 'data/images/%s/%s.jpg' % (topic, language_item)
                    visual_source =  visual_source_file

                #add language_item to usage_case_data
                usage_case_data['languageitem'] = language_item

                # get random language_item from topic and add to usage_case_data
                # Where is issue if there is only one language_item in topic! = exception
                while True:
                    wrong_language_item = random.choice(vocabulary_items_data)[0]
                    if wrong_language_item != language_item:
                        break
                usage_case_data['wrong_languageitem'] = wrong_language_item
                
                self[topic].append(VocabularyItem(language_item, usage_case_data, visual_source))

    def learning_frames(self, topic, configuration):
        """
        Create and return learning items relevant to topic and based on configuration (language_item, frame_type, activities)  
        activities = ['learn', 'check', 'ask']
        frame_type = ['main', 'extra']
        
        @TODO: implement learning_frame(topic, configuration) - this is must method

        language_item => usage_frame_configuration
        what is the difference between no usage_frame_configuration and no frame for usage_frame_configuration
        """
        learning_frames = []
        for language_item, frame_type, activities in configuration:
            vocabulary_item = self.get_vocabulary_item(topic, language_item)
            usage_frame = vocabulary_item.frame(frame_type, activities)
            # @TODO: Return None or missed learning_frame if no frame?
            # Can learning_frame be with missed usage frame?
            # The point is vocabulary_item cannot be without usage_case and so frame
            # no requested frame - no learning_frame - return None 
            if usage_frame:
                visual_source = vocabulary_item.get_visual_source()
                learning_frame = LearningFrame(language_item, usage_frame, visual_source)
                learning_frames.append(learning_frame)
            else:
                learning_frames.append(None)
        return learning_frames
    def get_vocabulary_item(self, topic, language_item):
        for vocabulary_item in self[topic]:
            if vocabulary_item.language_item == language_item:
                return vocabulary_item
            

class VocabularyItem():
    """
    State = language_item and usage_cases. Both elements are compulsory.
    The first usage case is the main and must be used to learn LanguageItem.
    All others are just extra and used to put language_item deeper in memory,
    learn language sentences and most usage cases in daily conversations.

    @TODO: some language_items does not suppose usage_cases.
    It is necessary to separatelly load vocabulary_items and extra language_items.!
    
    VocabularyItem is LanguageItem + UsageCase = proxy class
    

    Interface:
        frame(frame_scope, activities) - provides main or randomly choosen extra frame:
            according to activities:
                learn - to learn language_item and simple statement structure
                check - to check language_item and statement structure knowledge
                    to learn making question
                ask - to check knowledge of making question about language_item
            and frame_scope (main, extra)
            Return None if requested frame does not exist!

        
    Attributes:
        language_item
        usage_cases
            [0] - main usage_case to learn language_item
            [1:] - extra usage_cases for repeating language_item and learning more information
    """

    def __init__(self, language_item, usage_case_data, visual_source):
        """Must be accurate information about usage_case_data"""
        self.language_item = language_item
        self.visual_source = visual_source

        # @TODO: usage_case_data is compulsory
        # remove if statement
        if usage_case_data:
            part = usage_case_data.pop('part')
            #usage_case_data['languageitem'] = self.language_item # move it upper to VocabularyItem
            #sort usage cases so maximum deep level will be the first = usage_case to learn LI
            self.usage_cases = sorted(getattr(usagecase, part).usage_cases(**usage_case_data), reverse=True)
            for i in self.usage_cases:
                print(i)

    def frame(self, frame_scope, activities):
        if frame_scope == 'main':
            return self.main_frame(activities)
        elif frame_scope == 'extra':
            return self.extra_frame(activities)
        else:
            raise Exception('Frame scope "%s" is not supported.' % frame_scope)

    def main_frame(self, frame_type):
        usage_case = self.usage_cases[0] #get main usage_case
        return self._frame_by_type(usage_case, frame_type)

    def extra_frame(self, frame_type):
        """Randomly choosen usage_case from usage_cases[1:] range"""
        if self.is_extra_usage_cases():
            usage_case = random.choice(self.usage_cases[1:])
            return self._frame_by_type(usage_case, frame_type)

    def is_extra_usage_cases(self):
        """Check if there is extra usage cases"""
        return len(self.usage_cases) > 1

    def get_visual_source(self):
        """Return visual_source"""
        return self.visual_source

    def __getattr__(self, attr):
        """delegation to language_item"""
        return getattr(self.language_item, attr)

    @staticmethod
    def _frame_by_type(usage_case, frame_type):
        """Delegation to usage_case to get proper frame type"""
        if frame_type == 'learn':
            return usage_case.statement_frame()
        elif frame_type == 'check':
            return usage_case.question_frame()
        elif frame_type == 'ask':
            return usage_case.instruction_frame()
        else:
            raise Exception("frame_type '%s' is not supported." % frame_type)


class LearningFrame():
    """
    Combination of language_item, usage_frame, usage_pattern and visual_source
    Is usage_frame is compulsory or not??? How to get only language_item and visual_source?
    Is it new learning_frame type? 
    """
    def __init__(self, language_item, usage_frame, visual_source):
        self.language_item = language_item
        self.usage_frame = usage_frame
        self.visual_source = visual_source
        self.usage_pattern = usage_frame.usage_pattern if usage_frame else None
    def __str__(self):
        fields = [self.language_item]
        if self.usage_frame:
            fields.append(self.usage_frame)
            fields.append(self.usage_pattern)
        if self.visual_source:
            fields.append(self.visual_source)
        else:
            fields.append('None')
        return '; '.join(fields)

catalog = Catalog()
catalog.load(CATALOG_CONF)

if __name__ == '__main__':
    #vocabulary = Vocabulary(nouns.dict_txt_nouns)
    """
    for i_topic, language_items in vocabulary.items():
        print(i_topic)
        for i_language_item in language_items:
            print('\t', i_language_item)
    """
