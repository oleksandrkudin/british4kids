"""
Set to contain all language_items with different searching criteria.

Attributes:

Classes:

Function:

Example:

TODO:
    @OK
"""

import sys

import auxiliary_words
import languageitem
import speechparts

LEXIS_CONF = {}
LEXIS_CONF.update(auxiliary_words.dict_txt_auxiliary_words)

class Lexis(set):
    """
    Responsible for language_item creation - this is the only class to create language_item.
    Set to store all LanguageItem with possibility to look for them
    """
    def load(self, lexis_data):
        """Create language items from dict data and add them to set"""
        for group_name, language_items_data in lexis_data.items():
            for text, i_language_item_data in language_items_data.items():
                self.add(self.create(text, group_name, i_language_item_data))

    def create(self, text, group_name, language_item_data):
        """Create, add to set and return language_item from conf data"""
        try:
            part = language_item_data['part'] # Raise exception if no part key but no language_item_data
        except KeyError as error:
            print('Language item data: ', text, group_name, language_item_data)
            raise error
            #new_error = '%s in %s' % (error, language_item_data)
            #raise KeyError(new_error)
        #if not part:
        #    raise Exception('There is no part fild in Language item data: %s.' % language_item_data)
        # Add audio_source from data directory
        if not 'audio_source' in language_item_data:
            audio_source = 'data/sounds/%s/%s.mp3' % (group_name, text)
            language_item_data['audio_source'] = audio_source
        #language_item = languageitem.LanguageItem.create(part, text, **language_item_data)
        language_item = speechparts.__dict__[part](text, **language_item_data)
        self.add(language_item)
        return language_item

    def add(self, language_item):
        """add language_item"""
        set.add(self, language_item)

    def get(self, **kargv):
        """return LanguageItem what satisfy kargv parameters"""
        _language_items = self.filter(**kargv)
        if len(_language_items) == 1:
            return _language_items[0]
        elif len(_language_items) == 0:
            msg = 'LanguageItem has not been found. Parameters = {0}'.format(kargv)
        else:
            msg = 'Dublicate LanguageItems. Parameters = %s' % kargv
        raise BaseException(msg)

    def filter(self, **kargv):
        """return languageitems what satisfy kargv parameters"""
        _language_items = []
        for i_languageitem in self:
            if i_languageitem.contain(**kargv):
                _language_items.append(i_languageitem)
        return _language_items

lexises = Lexis()
lexises.load(LEXIS_CONF)

if __name__ == '__main__':
    for i in lexises:
        print(i)
