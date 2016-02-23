#To Do- Daring Selections, Add more to list to get more combinations(lower percentage?),Remove double quotes in single lists, Remove Black Pepper, oz other measurement words

from flask import render_template,request
from app import app
import re
import pandas as pd
import numpy as np
import random

#Description=pd.read_csv('recipes_csv.csv')
Description=pd.read_csv('Final_Recipes.csv') 
Description.set_index('Title')

def process_rules(line):
    first=re.search(r'\(.*\)',line.split('==>')[0]).group().rstrip(')').lstrip('(').split(',')
    second=re.search(r'\(.*\)',line.split('==>')[1]).group().rstrip(')').lstrip('(').split(',')
    percentage=float(re.search(r'\d+\.\d+',line.split('==>')[1]).group())*100
    first=[x.strip() for x in first if x is not '']
    second=[x.strip() for x in second if x is not '']
    return {'first':first,'second':second,'percentage':percentage}


def process_item_list(line):
    percentage=re.search(r'\d+\.\d+',line).group()
    items=re.search(r'\(.*\)',line).group().rstrip(')').lstrip('(').split(',')
    items=[x.strip() for x in items if x !='']
    return set(items)

def get_results(filename,item,process_function):
    occurances=[]
    with open(filename) as f:
        for line in f.readlines():
            if item in line:
                #print(line)
                occurances.append(process_function(line.rstrip().replace("'","")))
                #if len(occurances)>30:
                    #break
    f.close()
    return occurances

def get_combo_results(filename,combo_items,process_function):
    occurances=[]
    with open(filename) as f:
        for line in f.readlines():
            if all(x in line for x in combo_items):
                occurances.append(process_function(line.rstrip().replace("'","")))
                if len(occurances)>40:
                    break
    f.close()
    return occurances

def clean_my_list(query,item_list):
    item_list=list(item_list)
    for ingredient in query:
        for item in item_list:
            if item.startswith(ingredient+" ") or " "+ingredient in item:
                item_list.remove(item)
    return item_list

def print_results(query,item_set,rules):
    if item_set:
        print("Try these combinations")
        for item in item_set:
            print(item)
    print("Here are some rules related to the ingredients you entered")
    if rules:
        for dicts in rules:
            print("In "+str(dicts['percentage'])+"% of recipes with "+ str(dicts['first'])+", the recipe also contained "+str(dicts['second']))

@app.route('/')
@app.route('/index')
def index():
    user = { 'nickname': 'Miguel' } # fake user
    print(user)
    return render_template("input.html")

@app.route('/output')
def cities_output():
    print('Hello')
    city = request.args.get('ID')
    if city=="":
        return render_template("error.html")
    ing_type=request.args.get('type')
    query=city.split(',')
    item_set=[]
    rules=[]
    for item in query:
        i=get_results('SatItems.txt',item,process_item_list)
        if i:
            if ing_type=='standard':
                item_set.append(max(enumerate(i), key = lambda tup: len(tup[1]))[1])
            if ing_type=='feelinglucky':
                item_set.append(random.choice(i))
            r=get_results('SatRules.txt',item,process_rules)
            for rule in r:
                #print(item)
                it=set(item_set[query.index(item)])
                if set(rule['first']+rule['second'])< it:
                    rules.append(rule)
                    break
            if len(rules)<=query.index(item):
                rules.append({'first':'','second':'','percentage':''})
        else:
            item_set.append([])
            rules.append({'first':'','second':'','percentage':''})
            print('1st Here')

    combo_rules=get_combo_results('SatRules.txt',query,process_rules)
    combo_item=get_combo_results('SatItems.txt',query,process_item_list)
    if combo_item:
        item_set.append(max(enumerate(combo_item), key = lambda tup: len(tup[1]))[1])
        for rule in combo_rules:
            it=set(item_set[-1])
            if set(rule['first']+rule['second']) < it:
                rules.append(rule)
                break

            if len(rules)<len(query)+1:
                rules.append({'first':'','second':'','percentage':''})

    else:
            print('2nd Here')
            item_set.append([])
            rules.append({'first':'','second':'','percentage':''})

    #union=set.union(*item_sets)
    #if "" in union:
        #union.remove("")
    results=[]


    print_results(query,item_set,rules)
    for flavor_profile in item_set:
        if not flavor_profile:
            results.append({'Title':'','Ingredients List':'',
                            'Instructions':'','Image_URL':'','URL':''})
        elif not Description[np.logical_and.reduce([Description['Ingredients_y'].str.lower().str.contains(word,na=False) for word in flavor_profile])].empty:
            x=Description[np.logical_and.reduce([Description['Ingredients_y'].str.lower().str.contains(word, na=False) for word in flavor_profile])]
            recipe_dict={}
            index=random.randint(0,len(x)-1)
            recipe_dict['Title']=x.iloc[index]['Title']
            recipe_dict['Ingredients List']=x.iloc[index]['Ingredients_y']
            recipe_dict['Instructions']=x.iloc[index]['Instructions']
            recipe_dict['Image_URL']='http://images.bigoven.com/image/upload/t_recipe-640/'+recipe_dict['Title'].replace(' ','-')+'.jpg'
            recipe_dict['URL']=x.iloc[index]['WebURL']
            results.append(recipe_dict)
        else:
            print('We are here')
            if not Description[np.logical_and.reduce([Description['Ingredients_y'].str.lower().str.contains(word, na=False) for word in query])].empty:
                print('We are good')
                x=Description[np.logical_and.reduce([Description['Ingredients_y'].str.lower().str.contains(word,na=False) for word in query])][0]['Instructions']
                print(x)
            else:
                test=pd.DataFrame()
                for ingredient in query:
                    test=pd.concat([test,Description[Description['Ingredients_y'].str.lower().str.contains(ingredient, na=False)][:1]])
                    print(test)
                    if test.empty:
                        print('Our apologies the culinary skills are limited')



    return render_template("output.html",item_set=item_set, rules=rules,results=results)

