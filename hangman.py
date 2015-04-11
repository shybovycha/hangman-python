import sys, re, random

class HangmanGame(object):
    VERSION = '0.1'

    def __init__(self, dictionary_path, max_mistakes = 6):
        self.dictionary = self.parse_dictionary(dictionary_path)
        # self.dictionary = ['ala', 'alabama', 'moofoo']        
        self.max_mistakes = max_mistakes

    def get_word_length(self):
        return len(self.word)

    def parse_dictionary(self, path):
        words = set()

        with open(path) as f:
            lines = f.readlines()
            error_lines = [ l for l in lines if not re.match(r"[a-zA-Z]", l) ]

            if len(error_lines) > 0:
                raise Exception("This file is not a Hangman's dictionary file: `{0}`".format(path))
            
            return lines

    def start(self):
        self.errors = set()
        self.guesses = []

        self.generate_word()

    def ask_for_letter(self):
        print("Enter the word you want to guess, placing underscores where the unguessed letters should be")
        text = raw_input()  # enter_text(' '.join(list(self.word))).split(' ')
        pairs = [ (i, e) for i, e in enumerate(text) if text[i] != '_' and self.guesses[i] != text[i] and self.guesses[i] == '_' ]
        pair = ()

        if len(pairs) < 1:
            raise Exception("You have not entered anything `{0}`".format(text))
        elif len(pairs) > 1:
            raise Exception("You have entered too much: {0} == {1}".format(self.guesses, text.split('')))
        else:
            pair = pairs[0]

        return pair

    def show_status(self):
        word = ' '.join(list(self.guesses))

        bad_guesses = "Bad guesses: {0}/{1} [{2}]".format(
            len(self.errors),
            self.max_mistakes,
            ', '.join(self.errors)
        )
        
        print("""
            Hangman game v {0}

            {1}

            {2}
        """.format(self.VERSION, bad_guesses, word))

    def generate_word(self):
        self.word = self.dictionary[random.randint(0, len(self.dictionary) - 1)]
        self.guesses = list('_' * len(self.word))

    def guess(self, letter, position = None):
        if position == None:
            return [ i for i, e in enumerate(self.word) if e == letter ]
        
        if self.word[position] == letter:
            self.guesses[position] = letter
            return True
        else:
            self.errors.add(letter)
            return False

    def finished(self):
        if len(self.errors) >= self.max_mistakes:
            self.loose()
            return self.ask_for_restart()
        elif ''.join(self.guesses) == self.word:
            self.win()
            return self.ask_for_restart()
        else:
            return False

    def did_I_won(self):
        if not finished() or len(self.errors) >= self.max_mistakes:
            return False

        return True

    def win(self):
        print("""
            YOU WIN!
        """)

    def loose(self):
        print("""
            YOU LOST!
            The word you were looking for is: %s
        """ % self.word)

    def ask_for_restart(self):
        while True:
            print("Do you want to play again? (Y/n): ")

            ans = raw_input().lower()

            if ans == "y":
                self.generate_word()
                return False
            elif ans == "n":
                print("Ok, good bye!")
                return True
            else:
                print("I did not understand you. Please, enter either Y or N")

if __name__ == "__main__":
    if len(sys.argv) < 1:
        raise "Not enough arguments. Usage: python hangman.py [dictionary_file]"

    game = HangmanGame(sys.argv[1])
    game.start()

    while not game.finished():
        game.show_status()
        pos, letter = game.ask_for_letter()
        game.guess(letter, pos)
