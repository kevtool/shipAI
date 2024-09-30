import statistics
from game import Game
from algorithm import Algorithm

starting_brains = 20
brains_per_gen = 20
generations = 10

game = Game()

# human mode
# game.run(10)

model = Algorithm(starting_brains)

# for _ in range(brains_per_gen):
#     scores, dir_changes = game.run(10, mode='ai', brain=model.brain)
#     scores, dir_changes = statistics.fmean(scores), statistics.fmean(dir_changes)
#     model.get_score(scores, dir_changes)
#     model.next_brain()

for _ in range(generations):
    for index, brain_ in enumerate(model.brains):
        scores, dir_changes = game.run_no_render(10, brain=brain_)
        scores, dir_changes = statistics.fmean(scores), statistics.fmean(dir_changes)
        print(index, scores, dir_changes)
        model.record_score(index, scores, dir_changes)

    model.create_new_gen(brains_per_gen)

brain_ = model.brains[0]
game.run(1, mode='ai', brain=brain_, game_speed = 60)