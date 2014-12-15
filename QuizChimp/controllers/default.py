# -*- coding: utf-8 -*-

#@auth.requires_login()
def index():

    return dict()

@auth.requires_login()
def create():
    form = SQLFORM(db.surveys)
    if form.process().accepted:
        redirect(URL('default', 'sview', args=[form.vars.id]))
    return dict(form=form)

def sview():
    rows = db(db.surveys.id == request.args(0)).select()
    return dict(rows=rows)

def results():
    survey = request.args(0)
    rows = db(db.taken_surveys.survey == survey).select()
    return locals()

def add_q():
    db.questions.survey.default = request.args(0)
    db.questions.survey.writable = False
    form = SQLFORM(db.questions)
    survey = request.args(0)
    if form.process().accepted:
        redirect(URL('default', 'add_ans', args=[form.vars.id,form.vars.question_type,survey]))
    return locals()

def add_ans():
    qid = request.args(0)
    qtype = request.args(1)
    survey = request.args(2)
    return locals()

def submitQ():
    q = request.args(0)
    s = request.args(1)
    res = request.args(2)
    db.responses.insert(question=q,response=res,survey=s)
    return 'console.log("inserted");'

def leave():
    survey = request.vars.id
    return 'window.location = "%s";' % URL('default', 'sview', args=[survey])

def nextq():
    survey = request.vars.id
    qtype = request.vars.id
    return 'window.location = "%s";' % URL('default', 'add_q', args=[survey])


def answer():
    survey = request.args(0)
    qList = db(db.questions.survey == survey).select()
    rList = db(db.responses.survey == survey).select()
    return locals()

def submitSurvey():
    s = request.args(0)
    q = request.args(1)
    r = request.args(2)
    db.answered_questions.insert(survey=s, question=q, answer=r, author=get_email())
    return ''

def doneSurvey():
    s = request.args(0)
    db.taken_surveys.insert(survey=s, author=get_email())
    return 'window.location = "%s";' % URL('default', 'dashboard')

def dashboard():
    rows = db(db.surveys).select()
    return dict( rows = rows )

def view_q():
    rows = db(db.questions.survey == request.args(0)).select()
    return dict(rows=rows)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login()
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
