def get_every_nth_word(words : list, n: int):
    for word in words[::n]:
        yield word

def print_text_before_solve(func):
    def wrapper(*args, **kwargs):
        print("Before solving the task:")
        print("Text:", args[0])
        return func(*args, **kwargs)
    return wrapper

@print_text_before_solve
def solve(text: str):
    '''
    function to solve the task, it counts the number of words that end with a vowel, average word length, every fifth word
    :param text:
    :return:
    '''
    words = text.split()
    count_words_ends_with_vowel = sum(1 for word in words if word[-1].lower() in 'aeiou')
    average_word_len = round(sum(len(word) for word in words) / len(words))
    print(f"Количество слов, оканчивающихся на гласную букву: {count_words_ends_with_vowel}")
    print(f"Средняя длина слова: {average_word_len}")
    print("Каждое пятое слово:")
    for i, word in enumerate(get_every_nth_word(words, 5)):
        print((i * 5 + 1), word)


if __name__ == '__main__':
    text = 'So she was considering in her own mind, as well as she could, for the hot day made her feel very sleepy and stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her.'
    solve(text)