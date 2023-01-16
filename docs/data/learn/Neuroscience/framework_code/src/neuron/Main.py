from actor_framework.World import World
from neuron.SomaActor import SomaActor

if __name__ == '__main__':
    w = World(lambda src, dst, msg: 1)
    w.add_actor('test:a', SomaActor(), 'DECREASE_ENERGY')
    while True:
        w.step()
