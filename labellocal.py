from bottle import get, run, post, request, redirect
import shelve
from Cheetah.Template import Template
import math
import ConfigParser

db = shelve.open('labeldatabase.shelve')


@get('/')
def home():
    t = Template(file='templates/home.html')
    t.msg = request.get('msg')
    t.current = '<table cellpadding="0" cellspacing="0"><tr><th>#</th><th>Name</th><th>Item</th><th>Since</th><th>Place</th><th>Options</th></tr>'
    for m, (i, v) in enumerate(db.items()):
        t.current += '<tr class="%s">' % ('even' if m % 2 == 0 else 'odd')
        t.current += '<td>%s</td>' % i
        t.current += '<td>%s</td>' % v['name']
        t.current += '<td><table>'
        for n, item in enumerate(v['items']):
            t.current += '<tr><td class="%s">%s</td></tr>' % ('even' if n % 2 == 0 else 'odd', item)
        t.current += '</table></td>'
        t.current += '<td>%s</td>' % v['since']
        t.current += '<td>%s</td>' % v['place']
        t.current += '<td><a href="/view/%s">Show Content</a> | <a href="/delete/%s">Delete Box</a> | <a target="_blank" href="/print/%s">Print</a> | <a href="/edit/%s">Edit Box</a></td>' % (i, i, i, i)
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
    t.place = data['place']

    return str(t)


@get('/edit/<id>')
def edit(id):
    t = Template(file='templates/edit.html')
    data = db[id]
    t.identifier = id
    t.name = data['name']
    t.content = "\n".join(x for x in data['items'])
    t.since = data['since']
    t.place = data['place']

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
    items = data['items']
    items += ['']
    n = int(math.floor(len(items) / 2.0))
    item_pairs = [(k, items[n + m]) for m, k in enumerate(items[:n])]

    t.item_list = item_pairs
    t.since = data['since']

    return str(t)


@get('/<name>.css')
def stylesheet(name):
    if name not in ['print', 'home']:
        return ""
    with open('templates/%s.css' % name, 'r') as f:
        return f.read()


@post('/new')
def newlabel():
    #request.forms.get('index')
    nextnumber = max(map(int, db.keys()) + [0]) + 1
    name = request.forms.get('name')
    content = request.forms.get('content')
    since = request.forms.get('since')
    place = request.forms.get('place')
    items = [x.replace('\r', '') for x in content.split('\n') if x != '' and x != '\r']

    db[str(nextnumber)] = {'name': name, 'items': items, 'since': since, 'place': place}
    redirect('/')


@post('/editsave')
def editlabelsave():
    id = request.forms.get('id')
    name = request.forms.get('name')
    content = request.forms.get('content')
    since = request.forms.get('since')
    place = request.forms.get('place')
    items = [x.replace('\r', '') for x in content.split('\n') if x != '' and x != '\r']

    db[id] = {'name': name, 'items': items, 'since': since, 'place': place}
    redirect('/')


if __name__ == "__main__":
    config = ConfigParser.ConfigParser()
    config.read("labellocal.cfg")

    run(host=config.get("network", "ip"), port=config.get("network", "port"))
