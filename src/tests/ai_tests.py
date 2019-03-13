import helpers
from AI import IAI

class Bot(IAI):
   def say_something(self, message):
       print(message)

def main():
    bot = Bot()
    bot.say_something("Hello World!")

if __name__ == "__main__":
    main()