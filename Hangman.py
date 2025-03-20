import random
from random import choice

word_list = ['apple','banana','eagle','book','byte','first']

def get_word():
    return choice(word_list).upper()

# функция получения текущего состояния
def display_hangman(tries):
    stages = [  # финальное состояние: голова, торс, обе руки, обе ноги
                '''
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / \\
                   -
                ''',
                # голова, торс, обе руки, одна нога
                '''
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / 
                   -
                ''',
                # голова, торс, обе руки
                '''
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |      
                   -
                ''',
                # голова, торс и одна рука
                '''
                   --------
                   |      |
                   |      O
                   |     \\|
                   |      |
                   |     
                   -
                ''',
                # голова и торс
                '''
                   --------
                   |      |
                   |      O
                   |      |
                   |      |
                   |     
                   -
                ''',
                # голова
                '''
                   --------
                   |      |
                   |      O
                   |    
                   |      
                   |     
                   -
                ''',
                # начальное состояние
                '''
                   --------
                   |      |
                   |      
                   |    
                   |      
                   |     
                   -
                '''
    ]
    return stages[tries]

def play(word):
    word_completion = '_' * len(word)  # строка, содержащая символы _ на каждую букву задуманного слова
    guessed = False  # сигнальная метка
    guessed_letters = []  # список уже названных букв
    guessed_words = []  # список уже названных слов
    tries = 6  # количество попыток
    print('Давайте играть в угадайку слов!')
    print(word_completion)
    ans = ''
    while tries > 0:
        shot = input().upper()
        print(display_hangman(tries))
        if not shot.isalpha():
            print('Введите буквы или слово')
            shot = input('Введите опять')
            continue
        if shot in guessed_letters:
            print('Вы уже вводили эту букву')
            shot = input('Введите опять')
            continue
        if shot in guessed_words:
            print('Вы уже вводили это слово')
            shot = input('Введите опять')
            continue
        if shot in word:
            print('Вы угадали букву')
            guessed_letters.append(shot)
            for j in range(len(word)):
                if shot in word:
                    print(j,end='')
                    ans += word[j]
                else:
                    print('_',end='')
                    ans += '_'
        else:
            tries -= 1
            guessed_letters.append(shot)
            print(f'Вы не угадали, осталось {tries} попыток')

    if ans == word:
        print('Поздравляем, вы угадали слово! Вы победили!')
        guessed = True
    else:
        print(word)


play(get_word())