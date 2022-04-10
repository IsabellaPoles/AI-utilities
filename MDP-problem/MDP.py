# CS 411 - Assignment 7
# MDP problem for a generic grid world
# Isabella Poles UIN 673937460

from matplotlib import pyplot as plt


# Each state is represented by its position, whether it is a terminal state, its reward, and a list of its utility values
class State:
    def __init__(self, position, is_terminal, reward, utility):
        self.position = position
        self.is_terminal = is_terminal
        self.reward = reward
        self.utility = [utility]

    def __str__(self):
        return str([self.position[0] + 1, self.position[1] + 1]) + ', ' + str(self.is_terminal) + ', ' + str(self.reward) + ', ' + str(self.utility);


class MDP:
    def __init__(self, size, walls, terminal_states, t_rewards, nt_reward, transitions, gamma, epsilon):
        self.size = size
        self.states = {}
        self.walls = walls
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                position = [i, j]
                if position not in walls:
                    self.states[tuple(position)] = State(position,
                                                  True if position in terminal_states else False,
                                                  t_rewards[terminal_states.index(position)] if position in terminal_states else nt_reward,
                                                  0)
        self.transitions = transitions
        self.gamma = gamma
        self.epsilon = epsilon

    def blocked_left(self, s):
        if s.position[0] == 0 or [s.position[0] - 1, s.position[1]] in self.walls:
            return True
        return False

    def blocked_right(self, s):
        if s.position[0] == self.size[0] - 1 or [s.position[0] + 1, s.position[1]] in self.walls:
            return True
        return False

    def blocked_down(self, s):
        if s.position[1] == 0 or [s.position[0], s.position[1] - 1] in self.walls:
            return True
        return False

    def blocked_up(self, s):
        if s.position[1] == self.size[1] - 1 or [s.position[0], s.position[1] + 1] in self.walls:
            return True
        return False

    # Probability computation of reaching state s1 from state s by performing action a
    def P(self, s1, s, a):
        if s.is_terminal:
            return 0
        elif (s1.position[1] == s.position[1] + 1) and (s1.position[0] == s.position[0]):
            if a == 'N':
                return self.transitions[0]
            elif a == 'E':
                return self.transitions[1]
            elif a == 'W':
                return self.transitions[2]
            elif a == 'S':
                return self.transitions[3]
        elif (s1.position[1] == s.position[1]) and (s1.position[0] == s.position[0] - 1):
            if a == 'W':
                return self.transitions[0]
            elif a == 'N':
                return self.transitions[1]
            elif a == 'S':
                return self.transitions[2]
            elif a == 'E':
                return self.transitions[3]
        elif (s1.position[1] == s.position[1]) and (s1.position[0] == s.position[0] + 1):
            if a == 'E':
                return self.transitions[0]
            elif a == 'S':
                return self.transitions[1]
            elif a == 'N':
                return self.transitions[2]
            elif a == 'W':
                return self.transitions[3]
        elif (s1.position[1] == s.position[1] - 1) and (s1.position[0] == s.position[0]):
            if a == 'S':
                return self.transitions[0]
            elif a == 'W':
                return self.transitions[1]
            elif a == 'E':
                return self.transitions[2]
            elif a == 'N':
                return self.transitions[3]
        elif (s1.position[1] == s.position[1]) and (s1.position[0] == s.position[0]):
            p = 0
            if self.blocked_left(s):
                if a == 'N':
                    p += self.transitions[2]
                elif a == 'S':
                    p += self.transitions[1]
                elif a == 'W':
                    p += self.transitions[0]
                elif a == 'E':
                    p += self.transitions[3]
            if self.blocked_right(s):
                if a == 'N':
                    p += self.transitions[1]
                elif a == 'S':
                    p += self.transitions[2]
                elif a == 'W':
                    p += self.transitions[3]
                elif a == 'E':
                    p += self.transitions[0]
            if self.blocked_down(s):
                if a == 'N':
                    p += self.transitions[3]
                elif a == 'S':
                    p += self.transitions[0]
                elif a == 'W':
                    p += self.transitions[2]
                elif a == 'E':
                    p += self.transitions[1]
            if self.blocked_up(s):
                if a == 'N':
                    p += self.transitions[0]
                elif a == 'S':
                    p += self.transitions[3]
                elif a == 'W':
                    p += self.transitions[1]
                elif a == 'E':
                    p += self.transitions[2]
            return p
        else:
            return 0

    # Computation of the expected utility for state s if action a is performed
    def exp_utility(self, s, a):
        u = 0
        for s1 in self.states.values():
            u += self.P(s1, s, a) * s1.utility[-1]
        return u

    def print_u(self):
        for j in range(self.size[1] - 1, -1, -1):
            temp = ''
            for i in range(self.size[0]):
                position = [i, j]
                if position in self.walls:
                    temp += '------------------' + '\t'
                else:
                    temp += str(self.states[tuple(position)].utility[-1]) + '\t'
            print(temp)
        print('\n\n')

    def plot_u(self):
        # plot of the state utilities after each iteration
        for s in self.states.values():
            plt.plot(s.utility, label=str([s.position[0] + 1, s.position[1] + 1]))
        plt.legend()
        plt.xlabel = "Iterations"
        plt.ylabel = 'Utility'
        plt.show()

    def value_iteration(self):
        converged = False
        print('Iteration: 0')
        self.print_u()
        iterations = 0
        while not converged:
            delta = 0
            u = {}
            for key, s in self.states.items():
                exp_u = []
                for a in ['N', 'S', 'W', 'E']:
                    exp_u.append(self.exp_utility(s, a))
                u[key] = s.reward + self.gamma * max(exp_u)
                diff = abs(u[key] - s.utility[-1])
                if diff > delta:
                    delta = diff
            # utilities update 
            for i in u:
                self.states[i].utility.append(u[i])
            if delta <= self.epsilon * (1 - self.gamma) / self.gamma:
                converged = True
            iterations += 1
            print('Iteration: ' + str(iterations))
            self.print_u()

    def print_policy(self, policy):
        for j in range(self.size[1] - 1, -1, -1):
            temp = ''
            for i in range(self.size[0]):
                position = [i, j]
                if position in self.walls:
                    temp += '-' + '\t'
                elif self.states[tuple(position)].is_terminal:
                    temp += 'T' + '\t'
                else:
                    temp += str(policy[tuple(position)]) + '\t'
            print(temp)
        print('\n\n')

    def compute_policy(self):
        policy = {}
        for key, s in self.states.items():
            if s.is_terminal:
                policy[key] = 'T'
                continue
            max_a = 'N'
            max_u = self.exp_utility(s, 'N')
            for a in ['S', 'W', 'E']:
                exp_u = self.exp_utility(s, a)
                if exp_u > max_u:
                    max_u = exp_u
                    max_a = a
            policy[key] = max_a
        return policy

    def approx_policy_evaluation(self, policy, k):
        for j in range(k):
            u = {}
            for key, s in self.states.items():
                u[key] = s.reward + self.gamma * self.exp_utility(s, policy[key])
            for i in u:
                self.states[i].utility.append(u[i])

    def modified_policy_iteration(self, k):
        # Random policy initialization
        policy = {}
        for key, s in self.states.items():
            if s.is_terminal:
                policy[key] = 'T'
            else:
                policy[key] = 'S'

        unchanged = False
        while not unchanged:
            self.approx_policy_evaluation(policy, k)
            unchanged = True
            for key, s in self.states.items():
                if s.is_terminal:
                    continue
                max_a = 'N'
                max_u = self.exp_utility(s, 'N')
                for a in ['S', 'W', 'E']:
                    exp_u = self.exp_utility(s, a)
                    if exp_u > max_u:
                        max_u = exp_u
                        max_a = a
                if max_u > self.exp_utility(s, policy[key]):
                    policy[key] = max_a
                    unchanged = False
        return policy


def main():
    # Parsing input file
    f_name = str(input('Input file: '))
    f = open(f_name, 'r')
    mdp_info = f.readlines()
    f.close()
    size = [int(i) for i in mdp_info[0].split()]
    walls = [[int(j) - 1 for j in i.split()] for i in mdp_info[1]. split(',')]
    terminal_states = [[int(j) - 1 for j in i.split()] for i in mdp_info[2]. split(',')]
    terminal_rewards = [float(i) for i in mdp_info[3].split(',')]
    nonterm_rewards = float(mdp_info[4].strip())
    transitions = [float(i) for i in mdp_info[5].split()]
    gamma = float(mdp_info[6].strip())
    espilon = float(mdp_info[7].strip())

    mdp_val = MDP(size, walls, terminal_states, terminal_rewards, nonterm_rewards, transitions, gamma, espilon)
    mdp_val.value_iteration()
    policy_val = mdp_val.compute_policy()
    print('Value iteration policy: ')
    mdp_val.print_policy(policy_val)

    mdp_pol = MDP(size, walls, terminal_states, terminal_rewards, nonterm_rewards, transitions, gamma, espilon)
    policy_pol = mdp_pol.modified_policy_iteration(5)
    print('Modified iteration policy: ')
    mdp_pol.print_policy(policy_pol)


if __name__ == '__main__': main()
