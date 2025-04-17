import re
import zipfile

if __name__ == '__main__':
    with open('data/second_task.txt') as f:
        text = f.read()

    # количество предложений в тексте
    number_of_seqs = len(re.findall(r'[^.!?]+[.!?]', text))
    print(f'Количество предложений в тексте: {number_of_seqs}')
    # количество повествовательных, вопросительных и побудительных предложений
    number_of_statements = len(re.findall(r'[^.!?]+[.!?]', text))
    number_of_questions = len(re.findall(r'[^.!?]+[!?]', text))
    number_of_commands = len(re.findall(r'[^.!?]+[!?]', text))
    print(f'Количество повествовательных предложений: {number_of_statements}')
    print(f'Количество вопросительных предложений: {number_of_questions}')
    print(f'Количество побудительных предложений: {number_of_commands}')
    #среднюю длину предложений в символах (считаются только слова)
    average_length_of_sentence = len(re.findall(r'\w', text)) / number_of_seqs
    print(f'Средняя длина предложения в символах: {average_length_of_sentence}')
    average_word_len = len(re.findall(r'\w', text)) / len(re.findall(r'\w+', text))
    print(f'Средняя длина слова в символах: {average_word_len}')
    # количество смайликов в заданном тексте
    number_of_smiles = len(re.findall(r'(?<!\S)[:;][-]*([()\[\]])\1*(?!\S)', text))
    print(f'Количество смайликов в тексте: {number_of_smiles}')
    # вывести все слова, начинающиеся с заглавной буквы и содержащие цифры
    number_of_good_words = len(re.findall(r'[A-Z]\w*\d+\w*\b', text))
    print(f'Количество слов, начинающихся с заглавной буквы и содержащие цифры: {number_of_good_words}')
    is_color = re.match(r'#[0-9a-fA-F]{6}', text)
    print(f'Является ли данная строка шестнадцатеричным идентификатором цвета в HTML: {is_color is not None}')
    # определить, сколько слов имеют минимальную длину
    min_len = len(min(re.findall(r'\w+', text), key=len))
    min_len_words = len(re.findall(r'\b\w{%d}\b' % min_len, text))
    print(f'Количество слов минимальной длины: {min_len_words}')
    # вывести все слова, за которыми следует точка
    words_with_dot = re.findall(r'\b\w+\.', text)
    print(f'Слова, за которыми следует точка: {words_with_dot}')
    # найти самое длинное слово, которое заканчивается на 'r'
    longest_word = max(re.findall(r'\b\w*r\b', text), key=len)
    print(f'Самое длинное слово, которое заканчивается на "r": {longest_word}')

    with open('data/second_task_result.txt', 'w') as f:
        f.write(f'Количество предложений в тексте: {number_of_seqs}\n')
        f.write(f'Количество повествовательных предложений: {number_of_statements}\n')
        f.write(f'Количество вопросительных предложений: {number_of_questions}\n')
        f.write(f'Количество побудительных предложений: {number_of_commands}\n')
        f.write(f'Средняя длина предложения в символах: {average_length_of_sentence}\n')
        f.write(f'Средняя длина слова в символах: {average_word_len}\n')
        f.write(f'Количество смайликов в тексте: {number_of_smiles}\n')
        f.write(f'Количество слов, начинающихся с заглавной буквы и содержащие цифры: {number_of_good_words}\n')
        f.write(f'Является ли данная строка шестнадцатеричным идентификатором цвета в HTML: {is_color is not None}\n')
        f.write(f'Количество слов минимальной длины: {min_len_words}\n')
        f.write(f'Слова, за которыми следует точка: {words_with_dot}\n')
        f.write(f'Самое длинное слово, которое заканчивается на "r": {longest_word}\n')

    with zipfile.ZipFile('data/second_task_result.zip', 'w') as zipf:
        zipf.write('data/second_task_result.txt', arcname='second_task_result.txt')
        print(f'Файл {zipf.filename} успешно заархивирован.')

    with zipfile.ZipFile('data/second_task_result.zip', "r") as zf:
        print(zf.infolist())
        for item in zf.infolist():
            print(f"File name: {item.filename} Date: {item.date_time} Size: {item.file_size}")