import random
import sys
import wikipedia
import argparse

DEFAULT_MAX_LIVES = 5
DEFAULT_MINIMUM_LENGTH = 4


# clean up words with unwanted characters
def clean_word_list(word_list, minimum_length):
    clean_list = []
    for word in word_list:
        symbols = '!@#$%^&*()_-+={[}]|\\;:"<>?/., '
        for i in range(0, len(symbols)):
            word = word.replace(symbols[i], '')

        no_numbers = True
        for i in range(9):
            if str(i) in word:
                no_numbers = False

        if len(word) >= minimum_length and word not in clean_list and no_numbers:
            clean_list.append(word)
    return clean_list


# print out word with guessed letters and underscores for non-guessed letters
def display_word(word, guessed_letters):
    for char in word:
        if char.lower() in guessed_letters:
            print(char, end="")
        else:
            print("_", end="")
    print("")


# get a letter from user
def get_input():
    print("Please enter your guess")
    while True:
        letter = input().lower()
        if len(letter) > 1:
            print("Please enter a single letter")
        else:
            return letter


# check if all letters have been guessed
def check_win(word, guesses):
    for char in word:
        if char.lower() not in guesses:
            return False
    return True


def main(argv):
    # parse arguments
    parser = argparse.ArgumentParser(description="play hangman against the computer with words from a Wikipedia page")
    parser.add_argument("page_name", help="The name of the Wikipedia Page")
    parser.add_argument("-l", "--lives", type=int, help="The number of lives you get")
    parser.add_argument("-m", "--minimum_length", type=int, help="the minimum length of words to play with")
    args = parser.parse_args()

    # assign arguments

    if args.lives is not None and args.lives >= 1:
        lives = args.lives
    else:
        lives = DEFAULT_MAX_LIVES

    if args.minimum_length is not None:
        minimum_length = args.minimum_length
    else:
        minimum_length = DEFAULT_MINIMUM_LENGTH

    words = []
    try:
        print("Collecting words from Wikipedia page for {}".format(args.page_name))
        page = wikipedia.page(args.page_name)
        word_list = page.content.split()
        words.extend(clean_word_list(word_list, minimum_length))
    except wikipedia.exceptions.PageError:
        print("Page Error found. Please enter a valid wikipedia page name.")
        sys.exit(-1)

    # pick random word and begin game
    word = words[random.randint(0, len(words) - 1)]
    guessed_letters = []
    print("Welcome to Hangman.")
    game_active = True
    while game_active:
        display_word(word, guessed_letters)
        print("You have {} lives left".format(lives))

        # print letters that have already been guessed
        if len(guessed_letters) != 0:
            guessed_letters.sort()
            print("You've already guessed: ", end="")
            print(', '.join(guessed_letters))

        # get a valid guess
        guess = None
        while guess is None:
            guess = get_input().lower()
            if guess in guessed_letters:
                print("You've already guessed that!")
                guess = None

        # resolve guess
        if guess in word.lower():
            print("You guessed correctly!", "\n")
        else:
            print("You guessed incorrectly.", "\n")
            lives = lives - 1

        # check if game is over
        if lives == 0:
            print("Game over!")
            print("The word was:", word)
            game_active = False
        else:
            guessed_letters.append(guess)
            if check_win(word, guessed_letters):
                print("Congratulations, you won!")
                print("The word was:", word)
                game_active = False
    print("Thanks for playing!")


if __name__ == "__main__":
    while True:
        main(sys.argv)
        check = input("Type anything to play again, or N/No to quit \n").capitalize()
        if check == "N" or check == "NO":
            print("Bye!")
            break
