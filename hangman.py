import sys
import random
import curses
import curses.textpad as textpad

def enter_text(placeholder = ''):
    s = ''

    try:
        curses.initscr()
        mainwindow = curses.newwin(1, len(placeholder), 0, 0) #initscr()
        # Some curses-friendly terminal settings
        curses.cbreak(); mainwindow.keypad(1); curses.noecho()
        mainwindow.addstr(0, 0, placeholder)
        s = textpad.Textbox(mainwindow).edit()
    finally:
        # Reverse curses-friendly terminal settings
        curses.nocbreak(); mainwindow.keypad(0); curses.echo()
        curses.endwin()
        return s
        # print("You've entered: {0}".format(s))

class HangmanGame(object):
    VERSION = '0.1'

    def __init__(self, dictionary_path, max_mistakes = 6):
        self.check_dictionary(dictionary_path)
        self.dictionary = self.parse_dictionary(dictionary_path)
        self.dictionary = ['ala', 'alabama', 'moofoo']
        self.errors = []
        self.guesses = []
        self.max_mistakes = max_mistakes

    def get_word_length(self):
        return len(self.word)

    def check_dictionary(self, path):
        pass

    def parse_dictionary(self, path):
        return None

    def start(self):
        self.generate_word()

        """while True:
            if self.check_endgame():
                break

            self.show_status()

            letter, position = self.ask_for_letter()
            self.guess(letter, position)"""

    def ask_for_letter(self):
        text = enter_text(' '.join(list(self.word))).split(' ')
        pairs = [ (i, e) for i, e in enumerate(text) if self.word[i] != text[i] ]
        pair = ()

        if len(pairs) < 1:
            raise "You have not entered anything"
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
            self.errors.append(letter)
            return False

    def finished(self):
        if len(self.errors) >= self.max_mistakes:
            self.loose()
            return True
        elif ''.join(self.guesses) == self.word:
            self.win()
            return True
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

        self.ask_for_restart()

    def loose(self):
        print("""
            YOU LOST!
            The word you were looking for is: %s
        """ % self.word)

        self.ask_for_restart()

    def ask_for_restart(self):
        while True:
            print("Do you want to play again? (Y/n): ")

            ans = raw_input().lower()

            if ans == "y":
                restart = True
                break
            elif ans == "n":
                print("Ok, good bye!\n")
                return
            else:
                print("I did not understand you. Please, enter either Y or N\n")

        start()

if __name__ == "__main__":
    if len(sys.argv) < 1:
        raise "Not enough arguments. Usage: python hangman.py [dictionary_file]"

    game = HangmanGame(sys.argv[1])
    game.start()

    while not game.finished():
        game.show_status()
        pos, letter = game.ask_for_letter()
        game.guess(letter, pos)
