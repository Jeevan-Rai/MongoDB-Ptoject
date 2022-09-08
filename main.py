from http import client
from logging import warning
from pprint import PrettyPrinter, pprint
from flask import Flask, flash, render_template, request
from itsdangerous import json
import json
import pymongo
from werkzeug.utils import redirect

#################################################################################################
# load JSON file and insert data to mongodb #
#################################################################################################

with open('jsondata.json', 'r', encoding="utf8") as c:
    data = json.load(c)

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['netclan']
collection = db['sample']
content = collection.find()
# collection.insert_many(data)

#################################################################################################
#  Flask minimal application  #
#################################################################################################

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


#################################################################################################
#  Creating dictionary for graph data  #
#################################################################################################

valdict = {}
sector = collection.find({}, {'sector': 1})
sectorslist = []
for i in sector:
    if i['sector'] == '':
        i['sector'] = 'not defined'
    if i['sector'] not in sectorslist:
        sectorslist.append(i['sector'])
sectorslist.sort()
valdict.setdefault('sector', sectorslist)

end_year = collection.find({}, {'end_year': 1})
endyearlist = []
for i in end_year:
    if i['end_year'] == '':
        i['end_year'] = 0
    if i['end_year'] not in endyearlist:
        endyearlist.append(i['end_year'])
endyearlist.sort()
endyearlist[0] = 'not defined'
valdict.setdefault('end_year', endyearlist)

topic = collection.find({}, {'topic': 1})
topiclist = []
for i in topic:
    if i['topic'] == '':
        i['topic'] = 'not defined'
    if i['topic'] not in topiclist:
        topiclist.append(i['topic'])
topiclist.sort()
valdict.setdefault('topic', topiclist)

region = collection.find({}, {'region': 1})
regionlist = []
for i in region:
    if i['region'] == '':
        i['region'] = 'not defined'
    if i['region'] not in regionlist:
        regionlist.append(i['region'])
regionlist.sort()
valdict.setdefault('region', regionlist)


pestle = collection.find({}, {'pestle': 1})
pestlelist = []
for i in pestle:
    if i['pestle'] == '':
        i['pestle'] = 'not defined'
    if i['pestle'] not in pestlelist:
        pestlelist.append(i['pestle'])
pestlelist.sort()
valdict.setdefault('pestle', pestlelist)


source = collection.find({}, {'source': 1})
sourcelist = []
for i in source:
    if i['source'] == '':
        i['source'] = 'not defined'
    if i['source'] not in sourcelist:
        sourcelist.append(i['source'])
sourcelist.sort()
valdict.setdefault('source', sourcelist)


country = collection.find({}, {'country': 1})
countrylist = []
for i in country:
    if i['country'] == '':
        i['country'] = 'not defined'
    if i['country'] not in countrylist:
        countrylist.append(i['country'])
countrylist.sort()
valdict.setdefault('country', countrylist)


#################################################################################################
#  Function that returns vales from database according to the filter passsed  #
#################################################################################################

a = 0
conditions = []


def values(req):
    if not req:
        data = collection.find()
        intensity = []
        insum = 0
        likelihood = []
        liksum = 0
        relevance = []
        relsum = 0
        country = []
        topic = []
        tosum = 0
        region = []
        regsum = 0
        tabcontent = {}
        for i in data:
            if i['intensity'] == '':
                i['intensity'] = 0
            intensity.append(i['intensity'])
            tabcontent.setdefault('intensity', [])
            tabcontent['intensity'].append(i['intensity'])
            insum += i['intensity']
            if i['likelihood'] == '':
                i['likelihood'] = 0
            likelihood.append(i['likelihood'])
            tabcontent.setdefault('likelihood', [])
            tabcontent['likelihood'].append(i['likelihood'])
            liksum += i['likelihood']
            if i['relevance'] == '':
                i['relevance'] = 0
            relsum += i['relevance']
            relevance.append(i['relevance'])
            tabcontent.setdefault('relevance', [])
            tabcontent['relevance'].append(i['relevance'])
            if i['country'] not in country:
                country.append(i['country'])
                tabcontent.setdefault('country', [])
                tabcontent['country'].append(i['country'])
            if i['topic'] not in topic:
                topic.append(i['topic'])
                tabcontent.setdefault('topic', [])
                tabcontent['topic'].append(i['topic'])
            if i['region'] not in region:
                region.append(i['region'])
                tabcontent.setdefault('region', [])
                tabcontent['region'].append(i['region'])
            tabcontent.setdefault('pestle', [])
            tabcontent['pestle'].append(i['pestle'])
            tabcontent.setdefault('source', [])
            tabcontent['source'].append(i['source'])
            tabcontent.setdefault('end_year', [])
            tabcontent['end_year'].append(i['end_year'])
            tabcontent.setdefault('sector', [])
            tabcontent['sector'].append(i['sector'])
        inavg = insum/len(intensity)
        likavg = liksum/len(likelihood)
        relavg = relsum/len(relevance)
        res = []
        res.append(inavg)
        res.append(likavg)
        res.append(relavg)
        res.append(len(country))
        res.append(len(topic))
        res.append(len(region))
        for k in tabcontent.keys():
            tabcontent[k] = list(dict.fromkeys(tabcontent[k]))
        return res, tabcontent
    else:
        for i in req:
            for j, k in i.items():
                key = j
                val = k
                if val.isnumeric():
                    val = int(val)
        global conditions
        cont = {key: {'$eq': val}}
        conditions.append(cont)
        # print(conditions)
        if len(conditions) > 1:
            data = collection.find({'$and': conditions})
        else:
            data = collection.find({key: {'$eq': val}})
        intensity = []
        insum = 0
        likelihood = []
        liksum = 0
        relevance = []
        relsum = 0
        country = []
        topic = []
        tosum = 0
        region = []
        regsum = 0
        temp = []
        tabcontent = {}
        for i in data:
            if i['intensity'] == '':
                i['intensity'] = 0
            intensity.append(i['intensity'])
            tabcontent.setdefault('intensity', [])
            tabcontent['intensity'].append(i['intensity'])
            insum += i['intensity']
            if i['likelihood'] == '':
                i['likelihood'] = 0
            likelihood.append(i['likelihood'])
            tabcontent.setdefault('likelihood', [])
            tabcontent['likelihood'].append(i['likelihood'])
            liksum += i['likelihood']
            if i['relevance'] == '':
                i['relevance'] = 0
            relsum += i['relevance']
            relevance.append(i['relevance'])
            tabcontent.setdefault('relevance', [])
            tabcontent['relevance'].append(i['relevance'])
            if i['country'] not in country:
                country.append(i['country'])
                tabcontent.setdefault('country', [])
                tabcontent['country'].append(i['country'])
            if i['topic'] not in topic:
                topic.append(i['topic'])
                tabcontent.setdefault('topic', [])
                tabcontent['topic'].append(i['topic'])
            if i['region'] not in region:
                region.append(i['region'])
                tabcontent.setdefault('region', [])
                tabcontent['region'].append(i['region'])
            tabcontent.setdefault('pestle', [])
            tabcontent['pestle'].append(i['pestle'])
            tabcontent.setdefault('source', [])
            tabcontent['source'].append(i['source'])
            tabcontent.setdefault('end_year', [])
            tabcontent['end_year'].append(i['end_year'])
            tabcontent.setdefault('sector', [])
            tabcontent['sector'].append(i['sector'])
        inavg = insum/len(intensity)
        likavg = liksum/len(likelihood)
        relavg = relsum/len(relevance)
        res = []
        res.append(inavg)
        res.append(likavg)
        res.append(relavg)
        res.append(len(country))
        res.append(len(topic))
        res.append(len(region))
        for k in tabcontent.keys():
            tabcontent[k] = list(dict.fromkeys(tabcontent[k]))
        return res, tabcontent


#################################################################################################
#  route '/'  #
#################################################################################################

@app.route('/')
def home():
    tabcontent = []
    global conditions
    conditions = []
    result, tabcontent = values(a)
    return render_template('index.html', res=result, valdict=valdict, tabcontent=tabcontent)

#################################################################################################
#  route for filters  #
#################################################################################################


@app.route('/filter/<sector>/<k>')
def filter(sector, k):
    try:
        if sector == 'not defined':
            sector = ''
        tabcontent = []
        result, tabcontent = values([{k: sector}])
        return render_template('index.html', res=result, valdict=valdict, tabcontent=tabcontent)
    except:
        return redirect('/')

#################################################################################################
#  route for reset  #
#################################################################################################


@app.route('/reset')
def reset():
    return redirect('/')

#################################################################################################

app.run(debug=True)