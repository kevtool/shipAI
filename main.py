import statistics
from game import Game
from algorithm import Algorithm

starting_brains = 10
brains_per_gen = 12

game = Game()

# human mode
# game.run(10)

model = Algorithm(starting_brains)

# for _ in range(brains_per_gen):
#     scores, dir_changes = game.run(10, mode='ai', brain=model.brain)
#     scores, dir_changes = statistics.fmean(scores), statistics.fmean(dir_changes)
#     model.get_score(scores, dir_changes)
#     model.next_brain()

for index, brain_ in enumerate(model.brains):
    print(brain_.layers[0].weights)

    scores, dir_changes = game.run(10, mode='ai', brain=brain_)
    scores, dir_changes = statistics.fmean(scores), statistics.fmean(dir_changes)
    print(index, scores, dir_changes)
    model.record_score(index, scores, dir_changes)

model.create_new_gen(brains_per_gen)