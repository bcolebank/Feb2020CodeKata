from sys import argv
class Game:
    Frames = []
    def __init__(self):
        self.Frames = []

    def __str__(self):
        x = 0
        selfScore = 0
        line = ""
        if len(self.Frames) == 10:
            line += "Complete Game\r\n"
        else:
            line += "Partial Game\r\n"
        while x < len(self.Frames):
            selfScore += self.Frames[x].Total
            line += "[{}] - {} : {}\r\n".format(x + 1, self.Frames[x], selfScore)
            x += 1
        return line

    def AddFrames(self, frames):
        self.Frames = frames

    def AddFrame(self, frame):
        self.Frames.append(frame)
    
    def FrameCount(self):
        return len(self.Frames)

class Frame:
    FirstBall = None
    SecondBall = None
    ThirdBall = None
    Total = 0
    def __init__ (self, firstBall):
        self.FirstBall = firstBall
        self.SecondBall = None
        self.ThirdBall = None
        self.Total = firstBall

    def __str__ (self):
        if self.ThirdBall is None:
            return "[{}][{}] = {}".format(self.FirstBall, self.SecondBall, self.Total)
        else:
            return "[{}][{}][{}] = {}".format(self.FirstBall, self.SecondBall, self.ThirdBall, self.Total)

    def AddBall(self, ball):
        if self.SecondBall is None:
            self.SecondBall = ball
        else:
            self.ThirdBall = ball
        self.Total += ball

    def AddScore(self, score):
        self.Total += score

def Parse(scores):
    games = []
    game = Game()
    currentFrame = None
    x = 0
    while x < len(scores):
        if scores[x] < 0 or scores[x] > 10:
            raise Exception('Pin count of a single ball can not be less than zero or more than ten. The value of was: {}'.format(scores[x]))

        if currentFrame is None:
            currentFrame = Frame(scores[x])
        else:
            currentFrame.AddBall(scores[x])

        if game.FrameCount() < 9:
            if currentFrame.SecondBall is not None and currentFrame.FirstBall + currentFrame.SecondBall > 10:
                raise Exception('Pin count of a single frame can not be more than ten. The value of was: {}'.format(currentFrame.FirstBall + currentFrame.SecondBall))

            if currentFrame.FirstBall == 10: #strike
                if (x + 1) < len(scores):
                    currentFrame.AddScore(scores[x + 1])
                    if (x + 2) < len(scores):
                        currentFrame.AddScore(scores[x + 2])
                game.AddFrame(currentFrame)    
                currentFrame = None
            elif currentFrame.Total == 10: #spare
                if (x + 1) < len(scores):
                    currentFrame.AddScore(scores[x + 1])
                game.AddFrame(currentFrame)
                currentFrame = None
            elif currentFrame.SecondBall is not None:
                game.AddFrame(currentFrame)
                currentFrame = None
        else:
            if currentFrame.ThirdBall is not None: #Frame is complete
                if (currentFrame.SecondBall < 10):
                    if currentFrame.SecondBall + currentFrame.ThirdBall > 10:
                        raise Exception('Pin count of a single frame can not be more than ten. The value of was: {}'.format(currentFrame.SecondBall + currentFrame.ThirdBall))
                game.AddFrame(currentFrame)
                currentFrame = None
            elif currentFrame.SecondBall is not None and currentFrame.Total < 10: #Two balls without a mark
                game.AddFrame(currentFrame)
                currentFrame = None
        x += 1
        if game.FrameCount() == 10:
            print("Game over man!")
            games.append(game)
            game = Game()
    if (game.FrameCount() < 10):
        games.append(game)
    return games

inputs = argv[1]

scores = inputs.split(",")
map_object = map(int, scores)
list_of_scores = list(map_object)
games = Parse(list_of_scores)
print("Scoring")

for game in games:
    print(game)