import os,json
import  numpy as np
import math
from numpy import clip # for argcos or argsin
import string


with open("german-bav.json", "r+") as json_data_for_trans:
    json_data_for_trans.seek(0,0) # to beginn to read the file content
    result_json_trasn = json_data_for_trans.read()
#print("the result:")
#print(result_json_trasn)
#print("")

filepath_json=os.path.join(os.path.dirname(__file__), "german-bav.json")
with open(filepath_json) as json_file_local:
    parsed_json=json.loads(json_file_local.read())


#print("dic:", parsed_json["en-to-bav"])

#-- take items from dic in json file:
parsed_json_items = parsed_json["en-to-bav"].items()
#print("the items: ", parsed_json_items)

#--- alphapet
#alphabet_list=list(string.ascii_lowercase)
alphabet_list_with_space=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'," "]
default_alpha=30 # for defualt if the place empty for to make same len fpr word

#------- vector for alpha
def creat_vector_as_list_alphabet(dic):
    dic_vector = {}
    keys=list(dic.keys())
    for k in keys:
        vector_key = []
        for x in k:
            for w in alphabet_list_with_space:
                if x==w:
                    index_w=alphabet_list_with_space.index(w)
                    vector_key.append(index_w)
                else: pass
        dic_vector[k] = vector_key

    return dic_vector


#function to creat vector for ech word in dic(dic with items) with vector [1 1 ...]:

def creat_vector_as_list(dic):
    dic_vector={}
    for k,v in dic:
        vector_key=[]
        for x in range(0,len(k)):
            vector_key.append(1)
        dic_vector[k]=vector_key

    return dic_vector




word_from_json_with_vector_alpha=creat_vector_as_list_alphabet(creat_vector_as_list(parsed_json_items))


# functionto take word from dic, to translate
def tak_value_from_key_fromdic(key,dic):

    #vector_key=take_vector_for_word(key,word_from_json_with_vector_alpha)
    vector_key=input_st_to_vec_alpha(key)
    x={}
    value_default = "Sorry! the word is not in Dictionaries"
    value=""
    for k,v in dic:
        if k==key:
            x[k]=v
            value=x.get(k).upper()
            break
    if value!="":
        return value

    list_words_caluleted = []
    key_new=key
    if len(key)>0:
        #print(key_new)
        #print("vec input", input_st_to_vec_alpha(key))
        keys_of_json=[]
        x_l=0
        while x_l<len(list(dic)):
                keys_of_json.append(list(dic)[x_l][0])
                x_l=x_l+1
        #print("all key: ",keys_of_json)
        #print("vec_json_one=",input_st_to_vec_alpha(keys_of_json[0]))
        #print("vec first key of json",keys_of_json[0])
        for k in keys_of_json:
            vec_json=input_st_to_vec_alpha(k)
            pro_cal = samilir_calc_two_word(vector_key,vec_json)
            if pro_cal >= 60:
                list_words_caluleted.append(k)
            else:
                pass

    if len(list_words_caluleted) != 0:
        list_words_caluleted_to_str=", ".join(str(x) for x in list_words_caluleted)
        return "you mean mybe this: " + list_words_caluleted_to_str
    else:
        return value_default















#---- function




#function calculate the unit of vector
def calc_unit_vector(vector):
    x_unit_list=[]
    x_unit_result=0
    for x in vector:
        x_unit_list.append(x*x)
    x_unit_result= math.sqrt(sum(x_unit_list))
    return x_unit_result

#function calculate angle between 2 vecto( 2 vectors muss be np.array vector)r
def calc_angle_vetors(a,b):
    dot_vectors=np.dot(a,b)
    unit_vectors=calc_unit_vector(a)*calc_unit_vector(b)
    cos_angle=dot_vectors/unit_vectors
    return math.degrees(math.acos(cos_angle)) # change the result to degrees for angle

#function input word to np vectors:
'''
def input_st_to_npvec(stinput):
    l=[]
    for x in range(0,len(stinput)):
        l.append(1)
    return np.array(l)

'''
def input_st_to_vec_alpha(stinput):
    l = []
    posx2 = default_alpha
    for x in stinput:
        for x2 in alphabet_list_with_space:
            if x==x2:
                posx2=alphabet_list_with_space.index(x2)
                break
            else:
                posx2=default_alpha

        l.append(posx2)
    return l




'''

#function claculate the angle betweeen ech vector in dic with given vector
def calc_vec_angle_from_vec_in_dic (vec,dic):
    dic_key_angle={}
    for k,v in dic:
        key_v=dic.keys()[0]
        value_v=dic.get(key_v)
        angle=calc_angle_vetors(vec,np.array(key_v))
        dic_key_angle[key_v]=angle


    return dic_key_angle

print("the key with angle from vec: ", calc_vec_angle_from_vec_in_dic(input_vec_test,dic_test))
'''


#take vector of word from dic of vector
def take_vector_for_word(w,dic_of_vector):
    #list_keys=list(dic_of_vector.keys())
    #list_valuas=list(dic_of_vector.values())

    w_vec=[]
    for k,v in dic_of_vector.items():
        if k==w:
            w_vec=dic_of_vector[k]

    return w_vec









def samilir_calc_two_word(input_word_vec,dic_word_vec):

    mach = 0
    if len(input_word_vec)==len(dic_word_vec):
        #mach=0
        for x1 in input_word_vec:
            for x2 in dic_word_vec:
                if x1==x2:
                    mach= mach + 1

    elif len(input_word_vec) < len(dic_word_vec):
        add_elem = []
        for x in range(len(input_word_vec),len(dic_word_vec)):
            add_elem.append(default_alpha)

        new_input_word_vec=input_word_vec + add_elem
        #mach = 0
        for x1 in new_input_word_vec:
            for x2 in dic_word_vec:
                if x1 == x2:
                    mach = mach + 1

    alc_pro=(mach*100)/len(dic_word_vec)

    return alc_pro













'''


print(alphabet_list_with_space)
creat_vector_as_list(parsed_json_items)


print("the vector for words as position from Alphabet: ",word_from_json_with_vector_alpha)
#print("\nthe vector for word as 1s: ",creat_vector_as_list(parsed_json_items)) as 1s vectors

print("the value after change: ", np.array(list(word_from_json_with_vector_alpha.values())[0]))
print("type of value: ", type(np.array(list(word_from_json_with_vector_alpha.values())[0])))

print("the value 2 after change: ", np.array(list(word_from_json_with_vector_alpha.values())[1]))
print("the key 1 is: ",list(word_from_json_with_vector_alpha.keys())[0])

#-----------
#print(calc_unit_vector(np.array([2,2,1])))
#print(calc_unit_vector(np.array([1,1,0])))
#vec1=np.array([2,2,1])
#vec2=np.array([1,1,0])
#print(calc_angle_vetors (vec1,vec2))
#print("the vector of the firs key", creat_vector_as_list_alphabet(list(creat_vector_as_list(parsed_json_items).values())[0]))

input_vec_test=input_st_to_vec_alpha("youu")

#dic_test=creat_vector_as_list(parsed_json_items)
#print("dic_test: ",dic_test)
print("test vec: ", input_vec_test,"and the type is: ",type(input_vec_test))

print("test for word bye is vector:", take_vector_for_word("bye",word_from_json_with_vector_alpha))
test_num= [x for x in range(1,4+1)]
print(test_num)
print(test_num + [6,7])

print(samilir_calc_two_word(input_vec_test,list(word_from_json_with_vector_alpha.values())[1]))

print(samilir_calc_two_word([7,11,14],list(word_from_json_with_vector_alpha.values())[0]))

print(take_vector_for_word("bye",word_from_json_with_vector_alpha))
all_va=[]
for k, v in word_from_json_with_vector_alpha.items():
    all_va.append(v)
print("all val",all_va)
print("all key from json file:",list(parsed_json_items))
print("the frst from first: ",list(parsed_json_items)[0][0] )
print("the first of secuand: ",list(parsed_json_items)[1][0])

'''

#---------------------------------------------------
print("")
print("Translate from en to bav:")
x=True

while x==True:

    print("for finish press enter without any word")
    inputs_word = input("place writte a word to translate to bavarian language: ")
    #print(type(list(inputs_word)))
    #print(len(list(inputs_word)))
    len_word=len(list(inputs_word))
    try:

        #if not inputs_word
        #if len_word!=0:
        if  inputs_word:

            print("the word to bavarian language is: ", tak_value_from_key_fromdic(inputs_word.lower(),parsed_json_items))
        else:
            x=False
            print("Finish, thank you")
            break

    except EOFError:
        x=False
        print("Finisch")
        break





