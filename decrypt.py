from functools import reduce

from alphabet import dict_words, dict_length
from vignere_tools import is_english_word
from itertools import product


def un_shifting(character: str, shift: str) -> str:
    new_index = (dict_words.index(character) -
                 dict_words.index(shift)) % dict_length
    return dict_words[new_index]


def decrypt_with_key(cypher_text: str, key: str) -> str:
    key_length = len(key)
    return ''.join(
        [un_shifting(value, key[index % key_length])
         for (index, value) in enumerate(cypher_text)]
    )


def get_occurrence_map(text: str) -> dict:
    """Return percentage of each character in text. Expect text to have length > 0"""
    total_length = len(text)
    return {i: (text.count(i) / total_length) for i in set(text)}


def get_key_of_highest_value_from_dict(occurrence_dict: dict) -> str:
    return reduce(
        lambda current_max_entry, next_entry:
        current_max_entry if current_max_entry[1] > next_entry[1] else next_entry,
        occurrence_dict.items(),
        ['Emptyness', -1000]
    )[0]

# Get group of highest value from dict


def get_group_of_key_of_highest_value_from_dict(occurrence_dict: dict) -> []:
    sorted_occurence_dict = sorted(occurrence_dict.items(), key=lambda x: x[1],reverse = True)
    sorted_symbol_list = [sorted_occurence_dict[x][0] for x in range(len(occurrence_dict))]
    if(not bool(sorted_occurence_dict)):
        return None
    else:
        return [sorted_symbol_list[x] for x in range(5)]


def decrypt_with_key_length(cypher_text: str, key_length: int) -> str:
    # Divide into groups.
    # --> each group will have character frequency similar to English?
    # So 'e' usually has the highest frequency for each group
    text_groups = [[] for _ in range(key_length)]
    for i in range(len(cypher_text)):
        text_groups[i % key_length].append(cypher_text[i])

    # convert back to list of strings
    text_groups = [''.join(characters) for characters in text_groups]
    # get occurrence map for each group
    character_occurrences = [get_occurrence_map(text) for text in text_groups]
    # for x in character_occurrences:
    # 	print(x)

    # for each group, take out the character with highest occurrence
    # might change to percentage threshold later for accuracy
    # (ex: max_percentage +- 0.2 * max_percentage)
    # TODO: resolve ties?

    most_frequent_characters = [get_key_of_highest_value_from_dict(character_dict) for character_dict in
                                character_occurrences]
    # print(most_frequent_characters)
    # each highest occurrence correspond to 'e'. Calculate distance from 'e' ---> key
    index_of_e = dict_words.index('e')
    possible_key = ''.join(
        [dict_words[(dict_words.index(character) - index_of_e) % dict_length]
         for character in most_frequent_characters]
    )

    print("is this the key: %s" % possible_key)

    return decrypt_with_key(cypher_text, possible_key)


def decrypt_with_key_length_and_frequency_collision(cypher_text: str, plain_text: str, key_length: int) -> str:
    text_groups = [[] for _ in range(key_length)]
    for i in range(len(cypher_text)):
        text_groups[i % key_length].append(cypher_text[i])
    text_groups = [''.join(characters) for characters in text_groups]
    character_occurrences = [get_occurrence_map(text) for text in text_groups]

    most_frequent_characters_groups = [get_group_of_key_of_highest_value_from_dict(character_dict) for character_dict in
                                character_occurrences]
    index_of_e = dict_words.index('e')

    possible_keys_unhandled = [element for element in product(*most_frequent_characters_groups,repeat= 1)]

    possible_keys = [''.join(
        (dict_words[(dict_words.index(character) - index_of_e) % dict_length]
         for character in most_frequent_characters)) for most_frequent_characters in possible_keys_unhandled]
    for possible_key in possible_keys:
        print("testing key:" + possible_key)
        text = decrypt_with_key(cypher_text,possible_key) 
        if(text_is_english(text)):
            return text

    # print("is this the key: %s" % possible_key)
    # print("foo")

    return None

def text_is_english(text: str) -> bool:
    try:
        test_words = ''.join([text.split(' ')[x] for x in range(5)])
    except:
        return False
    for word in test_words:
        if(not is_english_word(word)):
            return False
    return True
