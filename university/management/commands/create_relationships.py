import numpy as np
from django.core.management.base import BaseCommand
from university.management.commands.relationships.stopwords import StopWords
from university.models import Area, Course, Lecture, Related

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.process_relations()

    def process_relations(self):
        areas = Area.objects.all()
        lecture_words_schema = {}

        for area in areas:
            lecture_words_schema[area.name] = {'id': area.id, 'courses': []}
            lectures = Lecture.objects.select_related('course').filter(course_id__area_id=area.pk).order_by('course_id')

            if len(lectures) > 0:
                current_course = {'course_name': lectures[0].course.name, 'id': lectures[0].course_id, 'keywords': {}}
            else:
                continue

            for lect in lectures:
                if current_course['id'] != lect.course_id:
                    lecture_words_schema[area.name]['courses'].append(current_course)
                    current_course = {'course_name': lect.course.name, 'id': lect.course_id, 'keywords': {}}

                curated_title = self.__normalize(lect.name.lower())
                lecture_words = curated_title.split()
                stop_words = StopWords.get()
                
                for w in list(lecture_words):
                    if w in stop_words:
                        lecture_words.remove(w)
                        continue
                    # these words are useless, remove
                    if w[0] == '(':
                        lecture_words.remove(w)
                        continue
                    if w == '':
                        continue
                    characters = ['*',',',':','.',')','(','-','_','+','?']
                    if w[-1] in characters:
                        w = w.rstrip(w[-1])
                    if w not in current_course['keywords']:
                        current_course['keywords'][w] = 1
                    else:
                        current_course['keywords'][w] += 1

            # create relationship matrix for each area
            for course_1 in lecture_words_schema[area.name]['courses']:

                for course_2 in lecture_words_schema[area.name]['courses']:
                    intersection = course_1['keywords'].keys() & course_2['keywords'].keys()
                    value = self.__cosine_similarity(course_1['keywords'], course_2['keywords'], intersection)
                    Related.objects.update_or_create(course_id=course_1['id'], related_id=course_2['id'],
                                                     defaults={'value': value})

    def __normalize(self, s):
        replacements = (
            ("á", "a"),
            ("é", "e"),
            ("í", "i"),
            ("ó", "o"),
            ("ú", "u"),
        )
        for a, b in replacements:
            s = s.replace(a, b).replace(a.upper(), b.upper())
        return s

    def __cosine_similarity(self, course_1, course_2, intersection):
        # no intersection, no relation
        if len(intersection) == 0:
            return 0.0
        # at the contrary, if both courses are the same one...
        if course_1 == course_2:
            return 1.0

        sumxx = 0
        sumyy = 0
        sumxy = 0

        for i in course_1:
            sumxx += int(course_1[i])**2
            if i in course_2:
                sumyy += int(course_2[i])**2
                sumxy += int(course_1[i])*int(course_2[i])
        return sumxy/np.sqrt(sumxx*sumyy)

