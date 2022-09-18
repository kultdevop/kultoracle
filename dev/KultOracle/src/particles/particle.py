import pygame,random

def ascending(speed):
    def _ascending(particle):
        particle.y -= speed
    return _ascending

def kill_at(max_x, max_y):
    def _kill_at(particle):
        if particle.x < -max_x or particle.x > max_x or particle.y < -max_y or particle.y > max_y:
            particle.kill()
    return _kill_at

def age(amount):
    def _age(particle):
        particle.alive += amount
    return _age

def fan_out(modifier):
    def _fan_out(particle):
        d = particle.alive / modifier
        d += 1
        particle.x += random.randint(-d, d)
    return _fan_out

def wind(direction, strength):
    def _wind(particle):
        if random.randint(0,100) < strength:
            particle.x += direction
    return _wind

class Particle():
    def __init__(self, col, size, *strategies):
        self.x, self.y = 0, 0
        self.col = col
        self.alive = 0
        self.strategies = strategies
        self.size = size

    def kill(self):
        self.alive = -1 # alive -1 means dead

    def move(self):
        for s in self.strategies:
            s(self)        

black = (0,0,0)
grey = (145,145,145)
light_grey = (192,192,192)
dark_grey = (183, 183, 183)

def smoke_machine():
    colors = {0: grey,
              1: dark_grey,
              2: light_grey}
    def create():
        for _ in xrange(random.choice([0,0,0,0,0,0,0,1,2,3])):
            behaviour = ascending(1), kill_at(1000, 1000), fan_out(400), wind(1, 15), age(1)
            p = Particle(colors[random.randint(0, 2)], random.randint(10, 15), *behaviour)
            yield p

    while True:
        yield create()

class Emitter(object):
    def __init__(self, pos=(0, 0)):
        self.particles = []
        self.pos = pos
        self.factories = []

    def add_factory(self, factory, pre_fill=300):
        self.factories.append(factory)
        tmp = []
        for _ in xrange(pre_fill):
            n = next(factory)
            tmp.extend(n)
            for p in tmp:
                p.move()
        self.particles.extend(tmp)

    def update(self):
        for f in self.factories:
            self.particles.extend(next(f))

        for p in self.particles[:]:
            p.move()
            if p.alive == -1:
                self.particles.remove(p)

    def draw(self, screen, position_translater_func):
        for p in self.particles:
            target_pos = position_translater_func(map(sum, zip((p.x, p.y), self.pos)))
            pygame.draw.circle(screen, p.col, target_pos, int(p.size))
            
            