import statistics
from game import Game
from algorithm import Algorithm

game = Game()

# human mode
# game.run(10)

model = Algorithm()
num_brains = 10

for _ in range(num_brains):
    scores, dir_changes = game.run(10, mode='ai', brain=model.brain)
    scores, dir_changes = statistics.fmean(scores), statistics.fmean(dir_changes)
    model.get_score(scores, dir_changes)
    model.next_brain()