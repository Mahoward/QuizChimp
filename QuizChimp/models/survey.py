# -*- coding: utf-8 -*-
from datetime import datetime

def get_email():
    if auth.user:
        return auth.user.email
    else:
        return 'None'

db = DAL('sqlite://storage.sqlite',pool_size=1)

db.define_table('surveys',
                Field('title', 'string'),
                Field('description', 'string'),
                Field('author', default = get_email()))


db.surveys.id.readable = False
db.surveys.title.requires = IS_NOT_EMPTY()
db.surveys.description.requires = IS_NOT_EMPTY()

db.surveys.author.label = 'Author'
db.surveys.author.writable = False
db.surveys.author.requires = IS_NOT_EMPTY()
db.surveys.author.requires = IS_EMAIL()

db.define_table('q_type',
                Field('type', 'string'))

db.define_table('questions',
                Field('question', 'string'),
                Field('question_type', 'reference q_type', requires=IS_IN_DB(db, db.q_type, '%(type)s')),
                Field('survey', 'reference surveys'),
                Field('author', default = get_email()))
db.questions.question.requires = IS_NOT_EMPTY()

db.questions.author.label = 'Author'
db.questions.author.writable = False
db.questions.author.requires = IS_NOT_EMPTY()
db.questions.author.requires = IS_EMAIL()

db.define_table('responses',
                Field('question', 'reference questions'),
                Field('response', 'string'),
                Field('author', default = get_email()),
                Field('survey', 'reference surveys'))


db.define_table('taken_surveys',
                Field('survey', 'reference surveys'),
                Field('author', default = get_email()))

db.taken_surveys.author.label = 'Author'
db.taken_surveys.author.writable = False
db.taken_surveys.author.requires = IS_NOT_EMPTY()
db.taken_surveys.author.requires = IS_EMAIL()

db.define_table('answered_questions',
                Field('survey', 'reference surveys'),
                Field('question', 'reference questions'),
                Field('answer', 'string'),
                Field('author', default = get_email()))

db.answered_questions.author.label = 'Author'
db.answered_questions.author.writable = False
db.answered_questions.author.requires = IS_NOT_EMPTY()
db.answered_questions.author.requires = IS_EMAIL()
