import re
from nltk.corpus import wordnet
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.wordnet import WordNetLemmatizer

lancaster=LancasterStemmer()
lmtzr = WordNetLemmatizer()

replace_these={'And ':',','Or ':',','Water':'','Pepper':'','Salt':'','Sugar':'','Pinch':'','Lb':'','Ounce':'Can Eden','','Large':'','Small':'','Cold',''}
peppers={'Bell Pepper':'bell pepper','Red Pepper':'red pepper','Green Pepper':'green pepper','Yellow Pepper':'yellow pepper','Black Pepper':'Pepper'}

if __name__ == "__main__":

    string=open('cleanmesmallerlasttime.csv').read()
    new_str=re.sub(r'"','',string)
    for word, replacement in peppers.items():
        new_str = new_str.replace(word, replacement)
    for word, replacement in replace_these.items():
        new_str = new_str.replace(word, replacement)
    new_str=new_str.lower()
    for line in new_str.splitlines():
        new_line=[]
        for ingredients in line.split(','):
            s=""
            for word in ingredients.split():
                d=wordnet.synsets(word)
                if d: 
                    part_of_speech=str(d[0]).split('.')[1]
                    if part_of_speech=='n':
                        lemma=lmtzr.lemmatize(word)+" "
                        #print(word+" "+lemma)
                        s=s+lemma
            if s:
                new_line.append(s.rstrip())
        if new_line:
            brand_new_line=','.join(new_line)+'\n'
            brand_new_line=re.sub(r', ',',',brand_new_line)
            with open("testsmallerlasttime.csv", "a") as myfile:
                myfile.write(brand_new_line)

