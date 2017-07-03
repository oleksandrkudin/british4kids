import tools
import learningmaterials
from student import *


class LearningApproach ():
    pass


class LessonConstructor ():
    """Get different sets of N LanguageItem based on KnowledgeRate with correct Activity. = Lesson constructor.
take knowledge, catalog[path], Number, approach
return [[material,activity], ]

LearningApproach
    10 word = 10 repeat, 10 answer - stupid approach, better look below (based on rate)
        0, 20, 40, 60, 80, 100; what if rate = probability of answer
        30%    [0]          repeat + answer
        50%    [20,40,60]   repeat or answer
        20%    [80, 100]    answer only
    """


class Exercise ():
    def __init__ (self, frame, activity, visual_source):
        self.frame = frame
        self.activity = activity
        self.visual_source = visual_source
        self.checked = False
    def __str__ (self):
        return '{}; {}; {}'.format(self.frame, self.activity, self.visual_source)
    

approach = [[[0, 0.19], 0.5],
                [[0.19, 0.79], 0.4],
                [[0.79, 1.1], 0.1]]


class Lesson ():
    def __init__ (self, student, scenario, learningmaterials, approach, count = 1):
        #print ('learningmaterials:',learningmaterials)
        if scenario == 'vocabulary':
            #get learning_materials: learnt + new
            knowledge = student.knowledge.filter (learningmaterials)
            knowledge.extend (learningmaterials)
            
            #group knowledge by rate
            knowledge_by_rates = [list(knowledge.filter_rate(*i_conf[0]).keys()) for i_conf in approach]
            #print ('knowledge_by_rates:', knowledge_by_rates)

            #get randomly totaly N items from groups based on persent coded in approach
            weights = [i_conf[1] for i_conf in approach]
            #print ('weights:', weights)
            grouped_learningitems = tools.percent_reduce (knowledge_by_rates,weights,count)
            print ('grouped_learningitems:', grouped_learningitems)

            #construct learning process = material + activity
            _process = []
            choices = ['answer','repeat']
            for learningitems in grouped_learningitems:
                for i_item in learningitems:
                
                    rate = knowledge[i_item].rate
                    #print ('i_item:', i_item, rate)
                    weights = [knowledge[i_item].probability(), 1-rate if rate < 0.5 else 0.5] #after rate 0.5 answer probability is 50%
                    activity = tools.weighted_choice (choices, weights)
                    _process.append ([i_item, learningmaterials[i_item], activity])
                
            #[i_item, learningmaterial, activity]
            self.process = _process

            #create iterator
            self.iter = self.two_way_iter()


        if scenario in ['dialogs','interactions']:
            _process = []
            for lm in learningmaterials:
                i_item = lm[1].languageitem
                _process.append ([i_item, lm, 'answer'])

            #[i_item, learningmaterial, activity]
            self.process = _process

            #create iterator
            self.iter = self.two_way_iter()
            
    def two_way_iter (self):
        """ function is generator. __iter__ - should return iterator. Iterator should contain __next__ method"""
        i=0
        x=1
        m_len = len(self.process)
        while True:
            i_task = self.process[i]
            i_li, learningmaterial, activity = i_task
            for i_sentence in learningmaterial.get_sentence():
                visual_source = i_sentence.get_visual_source (learningmaterial)
                for i_frame in i_sentence.get_frame(activity):
                    self.exercise = Exercise (i_frame,activity,visual_source)
                    x = yield self.exercise
            i = (i+x) % m_len
    def __iter__ (self):
        for i_task in self.process:
            i_li, learningmaterial, activity = i_task
            for i_sentence in learningmaterial.get_sentence():
                visual_source = i_sentence.get_visual_source (learningmaterial)
                for i_frame in i_sentence.get_frame(activity):
                    self.exercise = Exercise (i_frame,activity,visual_source)
                    yield self.exercise
    def __next__ (self):
        return self.exercise
    def move (self, move=1):
        return self.iter.send (move)
    def __str__ (self):
        return '\n'.join ( map ('{}'.format, self) )
            


if __name__ == '__main__':
    oleksandr = Student ('Oleksandr')
    learningmaterials.catalog.load_vocabulary ('animals')
    lesson = Lesson (oleksandr, 'vocabulary', learningmaterials.catalog['vocabulary']['animals'],approach,3)
    for i_act in lesson.process:
            print ('\n',i_act[0], i_act[2])
            i_lm = i_act[1]
            iter_sentence = i_lm.get_sentence()
            for i_sentence in iter_sentence:
                print (i_sentence.get_visual_source (i_lm))
                for i_frame in i_sentence.get_frame(i_act[2]): #third iteration
                    print (i_frame)
    print ('\n')
    print (lesson)
    #for i_exercise in lesson: print (i_exercise)
    #my_iter = iter(lesson)
    #for i in range(3):
        #print (next(lesson))
        #print (lesson.exercise)
