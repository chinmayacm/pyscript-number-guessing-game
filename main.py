from pyscript import document

# from pyodide.ffi.wrappers import add_event_listener
from pyodide.ffi import create_proxy

from random import randint


class GuessGame:
    def __init__(self, min_number, max_number, attempts):
        self.min_number = min_number
        self.max_number = max_number
        self.attempts = attempts
        self.reset_game()

    def reset_game(self):
        self.attempts_left = self.attempts
        self.attempts_made = 0
        self.numbers_entered = []
        self.random_number = randint(self.min_number, self.max_number)

    def is_game_over(self):
        return self.attempts_left == 0

    def number_submit(self, number):
        if self.is_game_over():
            return "You have exhausted your attempts. Reset to play again."
        self.numbers_entered.append(number)
        self.attempts_made += 1
        self.attempts_left -= 1

        if number == self.random_number:
            response = f"You guessed right! Congratulations!<br>You guessed in {self.attempts_made} attempts."
            self.attempts_left = 0
            return response
        elif number > self.random_number:
            response = (
                f"Your guess is high. You have {self.attempts_left} attempts left."
            )
        else:  # number < self.random_number
            response = (
                f"Your guess is low. You have {self.attempts_left} attempts left."
            )

        if self.is_game_over():
            response += (
                "<br>The random number was "
                + str(self.random_number)
                + ". Reset to play again."
            )

        return response


game = GuessGame(1, 10, 4)


def submit_guess(*args):
    guess = document.querySelector("#guess").value

    try:
        guess = int(guess)
        if 1 <= guess <= 10:
            result = game.number_submit(guess)
            document.querySelector("#message").innerHTML = result
            attempts_left = game.attempts_left
            document.querySelector("#attemptsLeft").textContent = (
                str(attempts_left) + "/" + str(game.attempts)
            )
            numbers_entered = game.numbers_entered
            document.querySelector("#guessList").textContent = str(numbers_entered)
            document.querySelector("#guess").value = ""
        else:
            document.querySelector("#message").textContent = (
                "Please enter a number between 1 and 10."
            )
    except Exception:
        document.querySelector("#message").textContent = (
            "Please enter a number between 1 and 10."
        )


#     document.querySelector(".log p").textContent = game.random_number


def reset(*args):
    game.reset_game()
    document.querySelector("#message").textContent = "Game has been reset!"
    document.querySelector("#guessList").textContent = "[None]"
    document.querySelector("#guess").value = ""
    document.querySelector("#guess").focus()


submit_btn = document.querySelector("#submit")
# add_event_listener(submit_btn,'click',submit_guess)
submit_btn.addEventListener("click", create_proxy(submit_guess))

reset_btn = document.querySelector("#reset")
# add_event_listener(reset_btn,'click',reset)
reset_btn.addEventListener("click", create_proxy(reset))
