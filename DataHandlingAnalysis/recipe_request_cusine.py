import pymongo
import requests
import json
import time

api_key_1='58RxI6clGvQj87yeXMrdcJ7Y55sOlDoQ'
api_key_2='QP81d0EB12afy94IDZ925k7xcta0gO82'
connection=pymongo.MongoClient("mongodb://localhost")
cuisines=['Afghan', 'African', 'Taiwanese','Shanghainese', 'American-South', 'Asian', 'Australian', 'Brazilian', 'Cajun', 'Canadian', 'Caribbean', 'Chinese', 'Croatian', 'Cuban', 'Dessert', 'Eastern European', 'English', 'French', 'German', 'Greek', 'Hawaiian','Hungarian', 'India', 'Indian', 'Irish', 'Italian', 'Japanese', 'Jewish','Jamaican' 'Korean', 'Latin', 'Mediterranean', 'Mexican', 'Middle Eastern', 'Moroccan', 'Polish', 'Russian', 'Scandanavian', 'Seafood', 'Southern', 'Southwestern', 'Spanish', 'Tex-Mex', 'Thai', 'Vegan', 'Vegetarian', 'Vietnamese','Fusion','Cuban','Breakfast']



def request_recipes(current_hour,cuisines):
    recipe_list=[]
    recipe_json_list=[]
    for cuisine in cuisines:
       r=requests.get('http://api.bigoven.com/recipes?api_key=58RxI6clGvQj87yeXMrdcJ7Y55sOlDoQ&any_kw='+cuisine+'&&pg='+str(current_hour)+'+&rpp=10',headers={"Content-Type":"application/json","Accept":"application/json"})
       test=json.loads(r.text)
       try:
           for recipe in test['Results']:
               recipe_list.append(recipe['RecipeID'])
       except:
           pass

    print(recipe_list)
    for recipe_number in recipe_list:
        r=requests.get("http://api.bigoven.com/recipe/"+str(recipe_number)+"?api_key="+api_key_2,headers={"Content-Type":"application/json","Accept":"application/json"})   
        try:
            recipe_json_list.append(json.loads(r.text))
        except Exception as e:
            pass
    print(recipe_json_list)
    recipes=connection['recipes']['recipes']
    for rec in recipe_json_list:
        recipes.replace_one(rec,rec,upsert=True)


if __name__ == "__main__":
    for current_hour in range(1,10):
        request_recipes(current_hour,cuisines)
        print('Sleeping')
        time.sleep(3600)  # Titles are acquired every 30 mins
        
        
