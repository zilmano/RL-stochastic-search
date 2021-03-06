import sys
sys.path.append("./lib")
import numpy as np
import math
import copy
import utility as util
import policy
from GridWorldEnv import GridWorld, Item, Actions
from GridWorldEnvApprox import GridWorldApproxModel
from dynaQApprox import approx_dyna_q
from dynaQ import tabular_dyna_q
import MonteCarloControl as mc
from policy import PolicyType
import matplotlib.pyplot as plt


def testRandomPolicy(gridWorldModel):
    # Run two episodes with a random policy
    pi = policy.NewPolicy(gridWorldModel.spec.nA, gridWorldModel.spec.nS)
    i = 0

    visualizeGridValueFunc(gridWorldModel)
    while i < 2:
        a = pi.action(gridWorldModel.state)
        (s,r,final) = gridWorldModel.step(a)
        if final:
            gridWorldModel.reset()
            visualizeGridValueFunc(gridWorldModel)
            i += 1

def exec_policy_for_episode(env,pi,max_out_steps=math.inf):
    steps = 0
    final = False
    final = env.final
    while not final and steps <= max_out_steps:
        a = pi.action(env.state, greedy=False)
        (s, r, final) = env.step(a)
        #print("a {} --> s {}".format(a,s))
        steps += 1
    return steps

def exec_policy_for_episode_states(env,pi,max_out_steps=math.inf):
    steps = 0
    states = [0]
    final = False
    #print("start state:{}".format(env.state))
    final = env.final
    while not final and steps <= max_out_steps:
        a = pi.action(env.state,greedy=False)
        (s, r, final) = env.step(a)
        states.append(env._grid_cell)
        #print("a {} --> s {}".format(a,s))
        steps += 1
    return steps, states

def exec_policy_for_episode_approx(env,pi,max_out_steps=math.inf):
    steps = 0
    final = False
    final = env.final
    while not final and steps <= max_out_steps:
        if not pi.isApproxPi():
            a = pi.action(env.state, greedy=False)
        else:
            features = env.features
            a = pi.action(features, greedy=False)
        _, _, _, final, _ = env.step(a)
        steps += 1
    print(steps)
    return steps

def testDynaQ(gridWorldModel,plot=False):
    Q = np.zeros((gridWorldModel.spec.nS,gridWorldModel.spec.nA))
    training_steps = 10000000
    model_training_steps = 50
    learning_rate = 0.1

    q, pi, episode_steps = tabular_dyna_q(gridWorldModel, Q, learning_rate, training_steps, model_training_steps,
                                          num_of_episodes=1000, eps=0.3, plot=plot)
    gridWorldModel.setQ(q,pi)
    #gridWorldModel.heatMap()
    #gridWorldModel.reset(0)
    #(steps,states) = exec_policy_for_episode_states(gridWorldModel, pi)
    #gridWorldModel.heatMap_episode(states)

    print(q)
    return pi

def parameterTest():

    train50eps1_avgs = []
    train50eps2_avgs = []
    train50eps3_avgs = []
    train70eps1_avgs = []
    train70eps2_avgs = []
    train70eps3_avgs = []
    train100eps1_avgs = []
    train100eps2_avgs = []
    train100eps3_avgs = []

    training_steps = 10000000

    for i in range(0,3):
        gridWorldModel = GridWorld(m,n,k,debug=False, gamma=1, no_stochastisity=False)

        Q1 = np.zeros((gridWorldModel.spec.nS,gridWorldModel.spec.nA))
        Q2 = np.zeros((gridWorldModel.spec.nS,gridWorldModel.spec.nA))
        Q3 = np.zeros((gridWorldModel.spec.nS,gridWorldModel.spec.nA))
        Q4 = np.zeros((gridWorldModel.spec.nS,gridWorldModel.spec.nA))
        Q5 = np.zeros((gridWorldModel.spec.nS,gridWorldModel.spec.nA))
        Q6 = np.zeros((gridWorldModel.spec.nS,gridWorldModel.spec.nA))
        Q7 = np.zeros((gridWorldModel.spec.nS,gridWorldModel.spec.nA))
        Q8 = np.zeros((gridWorldModel.spec.nS,gridWorldModel.spec.nA))
        Q9 = np.zeros((gridWorldModel.spec.nS,gridWorldModel.spec.nA))

        learning_rate = 0.1

        q1, pi1, episode_steps1 = tabular_dyna_q(gridWorldModel, Q1, learning_rate, training_steps, 50, num_of_episodes=1000, eps=0.1)
        q2, pi2, episode_steps2 = tabular_dyna_q(gridWorldModel, Q2, learning_rate, training_steps, 50, num_of_episodes=1000, eps=0.2)
        q3, pi3, episode_steps3 = tabular_dyna_q(gridWorldModel, Q3, learning_rate, training_steps, 50, num_of_episodes=1000, eps=0.3)

        #eps = range(len(episode_steps1))
        #plt.plot(eps, episode_steps1)
        #plt.plot(eps, episode_steps2)
        #plt.plot(eps, episode_steps3)
        #plt.xlabel('Episodes')
        #plt.ylabel('Steps')
        #plt.title('Steps per Episode')
        #plt.show()

        q4, pi4, episode_steps4 = tabular_dyna_q(gridWorldModel, Q4, learning_rate, training_steps, 70, num_of_episodes=1000, eps=0.1)
        q5, pi5, episode_steps5 = tabular_dyna_q(gridWorldModel, Q5, learning_rate, training_steps, 70, num_of_episodes=1000, eps=0.2)
        q6, pi6, episode_steps6 = tabular_dyna_q(gridWorldModel, Q6, learning_rate, training_steps, 70, num_of_episodes=1000, eps=0.3)

        #eps = range(len(episode_steps4))
        #plt.plot(eps, episode_steps4)
        #plt.plot(eps, episode_steps5)
        #plt.plot(eps, episode_steps6)
        #plt.xlabel('Episodes')
        #plt.ylabel('Steps')
        #plt.title('Steps per Episode')
        #plt.show()

        q7, pi7, episode_steps7 = tabular_dyna_q(gridWorldModel, Q7, learning_rate, training_steps, 100, num_of_episodes=1000, eps=0.1)
        q8, pi8, episode_steps8 = tabular_dyna_q(gridWorldModel, Q8, learning_rate, training_steps, 100, num_of_episodes=1000, eps=0.2)
        q9, pi9, episode_steps9 = tabular_dyna_q(gridWorldModel, Q9, learning_rate, training_steps, 100, num_of_episodes=1000, eps=0.3)

        #eps = range(len(episode_steps7))
        #plt.plot(eps, episode_steps7)
        #plt.plot(eps, episode_steps8)
        #plt.plot(eps, episode_steps9)
        #plt.xlabel('Episodes')
        #plt.ylabel('Steps')
        #plt.title('Steps per Episode')
        #plt.show()

        train50eps1_steps = 0
        train50eps2_steps = 0
        train50eps3_steps = 0
        train70eps1_steps = 0
        train70eps2_steps = 0
        train70eps3_steps = 0
        train100eps1_steps = 0
        train100eps2_steps = 0
        train100eps3_steps = 0

        for i in range(0, 10):
            #print("inst world model...")
            gridWorldModel.reset(start_cell=(m - 1))
            gw1 = copy.deepcopy(gridWorldModel)
            gw2 = copy.deepcopy(gridWorldModel)
            gw3 = copy.deepcopy(gridWorldModel)
            gw4 = copy.deepcopy(gridWorldModel)
            gw5 = copy.deepcopy(gridWorldModel)
            gw6 = copy.deepcopy(gridWorldModel)
            gw7 = copy.deepcopy(gridWorldModel)
            gw8 = copy.deepcopy(gridWorldModel)
            gw9 = copy.deepcopy(gridWorldModel)

            #visualizeGridValueFunc(gw)
            #print("exec sweep policy for episode...")
            train50eps1_steps += exec_policy_for_episode(gw1, pi1)
            train50eps2_steps += exec_policy_for_episode(gw2, pi2)
            train50eps3_steps += exec_policy_for_episode(gw3, pi3)
            train70eps1_steps += exec_policy_for_episode(gw4, pi4)
            train70eps2_steps += exec_policy_for_episode(gw5, pi5)
            train70eps3_steps += exec_policy_for_episode(gw6, pi6)
            train100eps1_steps += exec_policy_for_episode(gw7, pi7)
            train100eps2_steps += exec_policy_for_episode(gw8, pi8)
            train100eps3_steps += exec_policy_for_episode(gw9, pi9)
            #print("rl steps" + str(rl_steps))
            #print("sweep steps" + str(sweep_steps))
            # nn_tour_expected_steps += gw.graph.calc_path_cost(base_line_tour)

        train50eps1_avgs.append(train50eps1_steps / 10)
        train50eps2_avgs.append(train50eps2_steps / 10)
        train50eps3_avgs.append(train50eps3_steps / 10)
        train70eps1_avgs.append(train70eps1_steps / 10)
        train70eps2_avgs.append(train70eps2_steps / 10)
        train70eps3_avgs.append(train70eps3_steps / 10)
        train100eps1_avgs.append(train100eps1_steps / 10)
        train100eps2_avgs.append(train100eps2_steps / 10)
        train100eps3_avgs.append(train100eps3_steps / 10)



    experiment_nums = ('1', '2', '3')
    y_pos = np.arange(len(experiment_nums))

    bar_width = 0.075

    rects1 = plt.bar(y_pos, train50eps1_avgs, bar_width,
    color='b',
    label='train50eps.1')

    rects2 = plt.bar(y_pos + bar_width, train50eps2_avgs, bar_width,
    color='g',
    label='train50eps.2')

    rects3 = plt.bar(y_pos + 2*bar_width, train50eps3_avgs, bar_width,
    color='r',
    label='train50eps.3')

    rects4 = plt.bar(y_pos + 3*bar_width, train70eps1_avgs, bar_width,
    color='b',
    label='train70eps.1')

    rects5 = plt.bar(y_pos + 4*bar_width, train70eps2_avgs, bar_width,
    color='g',
    label='train70eps.2')

    rects6 = plt.bar(y_pos + 5*bar_width, train70eps3_avgs, bar_width,
    color='r',
    label='train70eps.3')

    rects7 = plt.bar(y_pos + 6*bar_width, train100eps1_avgs, bar_width,
    color='b',
    label='train100eps.1')

    rects8 = plt.bar(y_pos + 7*bar_width, train100eps2_avgs, bar_width,
    color='g',
    label='train100eps.2')

    rects9 = plt.bar(y_pos + 8*bar_width, train100eps3_avgs, bar_width,
    color='r',
    label='train100eps.3')

    plt.xticks(y_pos+bar_width, experiment_nums)
    plt.ylabel('Average Number of Steps')
    plt.xlabel('Experiment Number')
    plt.title('Average Number of Steps per Combination with Reward 20')
    plt.legend()
    plt.show()

def runApproximation():
    # Intitalize 4x4 gridworld with 2 items
    n = 8
    m = 8
    k = 2

    random_avgs = []
    sweep_avgs = []
    dyna_avgs = []

    util.logmsg("")
    util.logmsg("results for approximate",log_only=True)
    util.logmsg("experiment, average sweep steps, average rl steps, average random policy steps",log_only=True)

    # Run for 10 different distributions. Train RL, and then compare on 100 episodes each.
    for i in range(0, 6):
        gridWorldModel = GridWorldApproxModel(m, n, k, debug=False, gamma=1, no_stochastisity=False)
        #visualizeGridProbabilities(gridWorldModel, k, aggregate=True)
        eval_pi = testApproxDynaQ(gridWorldModel)
        (rand_avg, sweep_avg, dyna_avg) = compareToBaseLineApprox(gridWorldModel, eval_pi, k)
        random_avgs.append(rand_avg)
        sweep_avgs.append(sweep_avg)
        dyna_avgs.append(dyna_avg)
    experiment_nums = ('1', '2', '3', '4', '5', '6')
    y_pos = np.arange(len(experiment_nums))
    bar_width = 0.2
    rects1 = plt.bar(y_pos, random_avgs, bar_width,
                     color='b',
                     label='Random Policy')
    rects2 = plt.bar(y_pos + bar_width, sweep_avgs, bar_width,
                     color='g',
                     label='Handcrafted sweep policy')
    rects3 = plt.bar(y_pos + 2 * bar_width, dyna_avgs, bar_width,
                     color='r',
                     label='DynaQ')
    plt.xticks(y_pos + bar_width, experiment_nums)
    plt.ylabel('Average Number of Steps')
    plt.xlabel('Experiment Number')
    plt.title('Average Number of Steps per Algorithm')
    plt.legend()
    plt.savefig("results")
    plt.show()


def testApproxDynaQ(gridWorldModel):
    # Test approximate DynaQ ( it is not really DynaQ, just semi-gradient Sarsa.
    training_steps = 10000
    model_training_steps = None
    learning_rate = 0.0001
    pi = approx_dyna_q(gridWorldModel, learning_rate, training_steps, model_training_steps,
                            num_of_episodes=40000)
    #gridWorldModel.heatMap()
    return pi

def testMonteCarlo(gw):
    Q = np.zeros((gridWorldModel.spec.nS, gridWorldModel.spec.nA))
    randomPi = policy.NewPolicy(gridWorldModel.spec.nA, gridWorldModel.spec.nS)
    sim = util.Simulator(gw, randomPi)

    eps = 0.01
    training_episodes = 10000

    (Q, V, pi) = mc.on_policy_mc_control(Q, eps, sim, training_episodes)
    gw.setQ = Q

    visualizeGridPolicy(pi, gw.m, gw.n, policy_type=PolicyType.e_soft, eps=eps)
    visualizeGridValueFunc(gw)
    return pi

def compareToBaseLine(gw, eval_pi, k, episodes_num=100):
    sweep_pi = policy.HandMadeSweepPolicy(4, m, n)
    sweep_steps = 0
    rl_steps = 0

    visualizeGridProbabilities(gw, k, aggregate=True)
    base_line_tour, nn_tour_expected_steps = gw.graph.get_approximate_best_path(start_vertex=m - 1)
    #print("nearest_neighbor_tour:" + str(base_line_tour))

    for i in range(0, episodes_num):
        gw.reset(start_cell=(m - 1))
        gw_twin = copy.deepcopy(gw)
        #visualizeGridValueFunc(gw)
        sweep_steps += exec_policy_for_episode(gw, sweep_pi)
        rl_steps += exec_policy_for_episode(gw_twin, eval_pi)

    avg_nn_steps = nn_tour_expected_steps
    avg_sweep_steps = sweep_steps / episodes_num
    avg_rl_steps = rl_steps/episodes_num

    print("avg_sweep={} avg_rl={} avg_nearest_neigbor={}".format(avg_sweep_steps, avg_rl_steps,avg_nn_steps))
    return avg_nn_steps, avg_sweep_steps, avg_rl_steps

def compareToBaseLineApprox(gw, eval_pi, k, episodes_num=100):
    sweep_pi = policy.HandMadeSweepPolicy(4, m, n)
    sweep_steps = 0
    rl_steps = 0
    random_pi = policy.NewPolicy(gw.spec.nA, gw.grid_size)
    rand_pi_steps = 0

    for i in range(0, episodes_num):
        print("doing comparsion, episode {} out of {}...".format(i,episodes_num))
        gw.reset(start_cell=(m - 1))
        '''Re-use the same model to be the same for all evaluated policies. No stochastisity.'''
        gw_twin = copy.deepcopy(gw)
        gw_twin2 = copy.deepcopy(gw)
        sweep_steps += exec_policy_for_episode_approx(gw, sweep_pi)
        rl_steps += exec_policy_for_episode_approx(gw_twin, eval_pi)
        rand_pi_steps += exec_policy_for_episode_approx(gw_twin2, random_pi)

    avg_sweep_steps = sweep_steps / episodes_num
    avg_rl_steps = rl_steps/episodes_num
    avg_random_pi_steps = rand_pi_steps/episodes_num
    print("avg_sweep={} avg_rl={} avg_random_pi_steps={}".format(avg_sweep_steps, avg_rl_steps, avg_random_pi_steps))
    util.logmsg("{},{},{}",(avg_sweep_steps, avg_rl_steps, avg_random_pi_steps),log_only=True)
    return avg_random_pi_steps, avg_sweep_steps, avg_rl_steps


def visualizeGridPolicy(pi, m, n, item_status=0,policy_type=PolicyType.greedy,eps=0.1):
    util.visualizePolicyTxt(pi, m, n, item_status,policy_type=policy_type,eps=eps)


def visualizeGridValueFunc(gridWorldModel):
    util.visualizeGridTxt(gridWorldModel,gridWorldModel.V)


def visualizeGridProbabilities(gridWorldModel, k, aggregate=False):
    if not aggregate:
        for i in range(0, k):
            util.visualizeGridTxt(gridWorldModel, gridWorldModel.item_loc_probabilities[i])
    else:
        util.visualizeGridTxt(gridWorldModel,np.sum(gridWorldModel.item_loc_probabilities,axis=0))


if __name__ == "__main__":
    util.openlog('results.csv')

    # Intitalize 4x4 gridworld with 2 items
    n = 8
    m = 8
    k = 2

    nn_avgs = []
    sweep_avgs = []
    dyna_avgs = []

    # Run for 10 different distributions. Train RL, and then compare on 100 episodes each.
    plot_learning_curve = True
    for i in range(0,10):
        gridWorldModel = GridWorld(m,n,k,debug=False, gamma=1, no_stochastisity=False)
        #visualizeGridValueFunc(gridWorldModel)
        visualizeGridProbabilities(gridWorldModel, k, aggregate=True)

        # Testing
        # testRandomPolicy(gridWorldModel)
        eval_pi = testDynaQ(gridWorldModel,plot = plot_learning_curve)
        #parameterTest()
        (nn_avg, sweep_avg, dyna_avg) = compareToBaseLine(gridWorldModel,eval_pi, k)
        nn_avgs.append(nn_avg)
        sweep_avgs.append(sweep_avg)
        dyna_avgs.append(dyna_avg)
        plot_learning_curve = False

    experiment_nums = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
    y_pos = np.arange(len(experiment_nums))

    bar_width = 0.2

    rects1 = plt.bar(y_pos, nn_avgs, bar_width,
    color='b',
    label='Nearest Neighbor')

    rects2 = plt.bar(y_pos + bar_width, sweep_avgs, bar_width,
    color='g',
    label='Prioritized Sweep')

    rects3 = plt.bar(y_pos + 2*bar_width, dyna_avgs, bar_width,
    color='r',
    label='DynaQ')

    #averages = [nn_avgs, sweep_avgs, dyna_avgs]

    plt.xticks(y_pos+bar_width, experiment_nums)
    plt.ylabel('Average Number of Steps')
    plt.xlabel('Experiment Number')
    plt.title('Average Number of Steps per Algorithm')
    plt.legend()
    plt.savefig("results.png")
    plt.show()


    #runApproximation()
