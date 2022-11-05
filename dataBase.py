
import json

dataBase = {'Title': 'Predefined sentences',
         'Contexts': {
             'Work':[
                'I think that ...',
                'We could try to change ...',
                'Let\'s meet again on ...'
             ],
             'Greetings':[
                'Hello',
                'Nice to meet you',
                'I am Petra'
             ],
            'Everyday': [
                'Do you wanna go ... ?',
                'Let\'s have a coffee at...,
            ]},
         }

with open('dataBase.json', 'w') as f:
    json.dump(dataBase, f)



f = open('dataBase.json')
# returns JSON object as
# a dictionary
data = json.load(f)

