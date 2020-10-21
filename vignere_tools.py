from functools import reduce
from encrypt import vinegar_it

with open("words.txt") as word_file:
    english_words = set(word.strip().lower() for word in word_file)

def is_english_word(word):
    return word.lower() in english_words

#print(is_english_word("hello"))

def find_IC(text:str)->float:
    occurence_list = [text.count(i) for i in set(text)]
    text_length = len(text)
    #print(reduce(lambda x,y: x*(x-1) + y*(y-1),occurence_list))
    #index_of_coincidence = reduce(lambda x,y: x*(x-1) + y*(y-1),occurence_list) / text_length*(text_length-1)
    index_of_coincidence = 0
    for x in occurence_list:
        index_of_coincidence += x*(x-1)
    index_of_coincidence /= text_length*(text_length-1)
    return index_of_coincidence

def find_key_length(text:str) ->float:
    key_length = 1

    #IC is not mono
    previous_IC = find_IC(text)
    if(previous_IC > 0.06):
        return key_length
    

    while True:
        key_length += 1
        text_groups = [[] for _ in range(key_length)]

        for i in range(len(text)):
            text_groups[i % key_length].append(text[i])

        current_IC = 0
        for text_group in text_groups:
            current_IC += find_IC(''.join(text_group))
        current_IC /= key_length   
        
        if(current_IC > 0.06):
            break

        #if(current_IC > previous_IC):
        #    return key_length
        #else:
        #    current_IC = previous_IC
    return key_length

if __name__ == '__main__':
    path = './corpus_new.txt'
    source_file = open(path,'r')
    text = source_file.read().rstrip()
    key = 'asdjada' 
    cypher_text = vinegar_it(text, key)
    print(find_key_length(cypher_text))

