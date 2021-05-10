### Prevent GPU memory lock
import tensorflow as tf
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

import pandas as pd
import matplotlib.pyplot as plt
import gym

import multiprocessing

env = gym.make("LunarLander-v2")
spec = gym.spec("LunarLander-v2")
num_episodes = 5000


def run(lr, gamma):
    
    import DQN as model ### CHOOSE DQN OR DuelingDQN
    
    graph = False
    earlystopping = True
    
    try:
        agent = model.Agent(lr=lr, gamma=gamma, epsilon=1.0, epsilon_decay=0.995, batch_size=64)
        scores, avg_scores = agent.train_model(env, num_episodes, graph, earlystopping=earlystopping)
        return {'lr':lr, 'gamma':gamma, 'scores':scores, 'avg_scores':avg_scores}
    
    except Exception as e:
        print("Error occurred:")
        print(e)
        data.append({'lr':lr, 'gamma':gamma, 'scores':None, 'avg_scores':None})


if __name__ == '__main__':
    
    
    ### HYPERPARAMETER GRIDS
    lr_grid = [0.001, 0.0001]
    gamma_grid = [0.99, 0.999]
    
    hyper_sets = []
    
    for lr in lr_grid:
        for gamma in gamma_grid:
            hyper_sets.append(tuple([lr, gamma]))

    with multiprocessing.Pool(processes=4) as pool:
        data_all = pool.starmap(run, hyper_sets)
        print('data_all:', data_all)
       
    df_data = pd.DataFrame(data_all)
    df_data.to_csv("df_data_DQN.csv") ### CHOOSE DQN OR DuelingDQN
        
    print("Processes are successfully finished.")
    
