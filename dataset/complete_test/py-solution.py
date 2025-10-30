#Completely written with GitHub Copilot.

#load json file
import json

#print('loading old.json')
with open('old.json') as data_file:
    olddata = json.load(data_file)

#get fragment of olddata
oldparams = olddata['parameters']

#print('loading new.json')
with open('new.json') as data_file:
    newdata = json.load(data_file)

#get fragment of newdata
newparams = newdata['parameters']

#create a new list
differences = []

#compare oldparams to newparams
for key, value in oldparams.items():
    if key in newparams:
        if value != newparams[key]:
            #print('parameter %s differs' % key)

            #for each property in value compare to newparams[key]
            for key2, value2 in value.items():
                if key2 in newparams[key]:
                    if value2 != newparams[key][key2]:
                        #print('parameter %s differs' % key2)

                        #add to list of differences
                        differences.append({'name': key, 'meta': key2, 'oldvalue': newparams[key][key2], 'newvalue': value2})
    else:
        print('parameter %s missing' % key)
        differences.append({'name': key, 'meta': 'missing', 'oldvalue': '', 'newvalue': ''})

for key, value in newparams.items():
    if key in oldparams:
        #don't care
        pass
    else:
        print('parameter %s missing' % key)
        differences.append({'name': key, 'meta': 'is new', 'oldvalue': '.', 'newvalue': '.'})

#convert array to html
differences_html = '<table border="1">'
differences_html += '<tr><th>name</th><th>meta</th><th>oldvalue</th><th>newvalue</th></tr>'

for difference in differences:
    differences_html += '<tr>'
    differences_html += '<td>%s</td>' % difference['name']
    differences_html += '<td>%s</td>' % difference['meta']
    differences_html += '<td>%s</td>' % difference['oldvalue']
    differences_html += '<td>%s</td>' % difference['newvalue']
    differences_html += '</tr>'

differences_html += '</table>'

#save differences_html to file
with open('py-differences.html', 'w') as f:
    f.write(differences_html)
