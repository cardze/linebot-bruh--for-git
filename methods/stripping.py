import string
words_dont_want=['give', 'me', 'pic']
def get_the_targetWord_in_string(input_string):
    
    word_list=[]
    for i in input_string.split():
        if not i in words_dont_want :
            word_list.append(i)
    return word_list[0]

def is_input_have_words_in_index(input_string):
    result = False
    for word in words_dont_want:
        if word in input_string.split():
            result = True
        else:
            result = False
    return result
            
if __name__ == '__main__':   
    test='give me cows pic'
    print(is_input_have_words_in_index(test))
    print(get_the_targetWord_in_string(test))
    # print (get_the_targetWord_in_string(test))
    # words_dont_want=['give', 'me', 'pic']
    # word_list=[]
    # for i in test.split():
    #     if not i in words_dont_want :
    #         word_list.append(i)
    # print(word_list)
    