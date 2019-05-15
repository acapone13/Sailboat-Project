import helpers
from AI import IAI

class Bot(IAI):
    def step(self, params):
        raise NotImplementedError
    def log(self, message):
        print(message)

def main():
    bot = Bot()
    bot.log("Hello World!")

if __name__ == "__main__":
    main()