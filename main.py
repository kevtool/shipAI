import statistics
from game import Game
from algorithm import Algorithm

brains_per_gen = 10

game = Game()

# human mode
# game.run(10)

model = Algorithm(brains_per_gen)

# for _ in range(brains_per_gen):
#     scores, dir_changes = game.run(10, mode='ai', brain=model.brain)
#     scores, dir_changes = statistics.fmean(scores), statistics.fmean(dir_changes)
#     model.get_score(scores, dir_changes)
#     model.next_brain()

for index, brain_ in enumerate(model.brains):
    scores, dir_changes = game.run(10, mode='ai', brain=brain_)
    scores, dir_changes = statistics.fmean(scores), statistics.fmean(dir_changes)
    model.record_score(index, scores, dir_changes)