import numpy as np


class EnvironmentModel:
    def __init__(self, n_states, n_actions, seed=None):
        self.n_states = n_states
        self.n_actions = n_actions
        self.randomstate = np.random.RandomState(seed)

    def p(self, next_state, state, action):
        raise NotImplementedError()

    def r(self, next_state, state, action):
        raise NotImplementedError()

    def draw(self, state, action):
        p = [self.p(ns, state, action) for ns in range(self.n_states)]
        next_state = self.randomstate.choice(self.n_states, p=p)
        reward = self.r(next_state, state, action)
        return next_state, reward


class Environment(EnvironmentModel):
    def __init__(self, actions, n_states, n_actions, max_steps, dist, seed=None):
        EnvironmentModel.__init__(self, n_states, n_actions, seed)
        self.actions = actions
        self.n_steps = None
        self.state = None
        self.max_steps = max_steps
        self.dist = dist
        if self.dist is None:
            self.dist = np.full(n_states, 1 / n_states)

    def p(self, next_state, state, action):
        state = state
        if action == 0:
            state -= 4
            if state < 0:
                state += 4
        elif action == 1:
            if state % 4 != 0:
                state -= 1
        elif action == 2:
            state += 4
            if state > 11:
                state -= 4
        elif action == 3:
            if state % 4 != 3:
                state += 1
        if next_state == state:
            return 1
        else:
            return 0

    def r(self, next_state, state, action):
        pass

    def reset(self):
        self.n_steps = 0
        print(self.dist)
        self.state = self.randomstate.choice(self.n_states, p=self.dist)
        return self.state

    def step(self, action):
        if action < 0 or action >= self.n_actions:
            raise Exception("invalid action")
        self.n_steps += 1
        done = (self.n_steps >= self.max_steps)
        self.state, reward = self.draw(self.state, action)
        return self.state, reward, done

    def render(self):
        done = False
        while not done:
            c = input("Move:\n")
            if c not in actions:
                raise Exception("invalid action")
            state, r, done = self.step(actions.index(c))
            self.render()


if __name__ == '__main__':
    actions = ["w", "a", "s", "d"]  # Numpad directions
    env = Environment(actions, 12, 4, 20, None)
    env.state = env.reset()
    env.render()
