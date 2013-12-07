from bottle import *
import shelve
from Cheetah.Template import Template

db = shelve.open('labeldatabase.shelve')

@get('/')
def home():
    t = Template(file='templates/home.html')
    t.msg = request.get('msg')
    t.current = "<table>"
    for i, v in db.items():
        t.current += '<tr>'
        t.current += '<td>%s</td>' %i
        t.current += '<td>%s</td>' %v['name']
        t.current += '<td>%s Items</td>' %len(v['items'])
        t.current += '<td>%s</td>' %v['since']
        t.current += '<td><a href="/view/%s">Show Content</a> | <a href="/delete/%s">Delete Box</a> | <a href="/print/%s">Print</a></td>' %(i,i,i)
        t.current += '</tr>'

    t.current += '</table>'

    return str(t)

@get('/view/<id>')
def view(id):
    t = Template(file='templates/view.html')
    data = db[id]
    t.name = data['name']
    t.item_list = data['items']
    t.since = data['since']

    return str(t)

@get('/delete/<id>')
def delete(id):
# FIXME
    db.__delitem__(id)
    redirect('/')

@get('/print/<id>')
def printer(id):
    t = Template(file='templates/print.html')
    data = db[id]
    t.id = id
    t.name = data['name']
    t.item_list = data['items']
    t.since = data['since']

    return str(t)

@post('/new')
def newlabel():
    #request.forms.get('index')
    
    nextnumber = max(map(int, db.keys())+[0])+1
    name =  request.forms.get('name')
    content =  request.forms.get('content')
    since =  request.forms.get('since')
    items =  [x.replace('\r', '') for x in content.split('\n') if x != '' and x != '\r']

    db[str(nextnumber)] = {'name': name, 'items': items, 'since': since}
    redirect('/')


if __name__ == "__main__":
    run(host="127.0.0.1", port="8080")
