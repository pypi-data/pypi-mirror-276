#!/usr/bin/env python
# coding: utf-8

# In[132]:

import argparse

import tqdm, sys, os
import numpy as np

import time

timestamp = str(int(time.time()))

class Object(object):
    pass

args = Object()
args.outdir='logs/craft_llama_feedback' + '/' + timestamp
if not os.path.exists(args.outdir):
    os.makedirs(args.outdir)
log = open(args.outdir+'/logger.txt','w')
sys.stdout = log
args.window = (600, 600)
args.fps=5
# parser.add_argument('--window', type=int, nargs=2, default=(600, 600))
# args.wandb_log_interval=10


# 用llama2充当stu，llama3充当assistant
import openai
openai.api_key = "LL-dEBQ9q3WmuekIxqotWBuDUYHQGfs70OugfL11O67VVJpXK7NuzsBeKK27vxMbbMd"
openai.api_base = "https://api.llama-api.com"

from feedback_api import Feedback
assistant = Feedback('sk-5RmCNtBIMBYgQu1H47DcB6879b5c4d09A56578FeB8675737')
#assistant = Feedback(Llama_query())

# In[134]:


import gym
import crafter
from craft.craft_env import WrapEnv
env = gym.make("smartplay:Crafter-v0")
#env = crafter.Recorder(env, args.outdir,save_video=True,save_episode=False)
env = WrapEnv(env, args.outdir,save_video=True,save_episode=False)  # 用包装函数
env.set_task("collect_diamond")
feedback_type = 'history_action_positive'
max_step = 2
action_list = env.action_list


# In[135]:

print(action_list)


# In[136]:


def match_act(string):
    for i, act in enumerate(action_list):
        if "next action:" in string:
            string = string.split("next action:")[-1].strip()
        if act.lower() in string.lower():
            # action_str = f"{i}. {act}"
            # if action_str in string:
            return i, act
    print("LLM failed with output \"{}\", taking action Do...".format(string))
    return action_list.index("Do"), "Do"


def compose_prompt(CTXT, text_obs, feedback=None):

    sys_str = "You’re a player trying to play the game of crafter.\nAction Space:\n" + CTXT + \
    "\nGive you the observation and the task, please choose the next executable action. You should think step by step and output the answer in the last sentence with this format: 'The next action: xx.'"
    
    user_str = "Most recent 4 steps of the player's in-game observation:\n{}".format(text_obs) + \
    "\n\nThe task is to {}".format(env.taskname)
    if feedback:
        user_str += "\nFeedback of the last action:\n{}".format(feedback)
    user_str += "\nPlease generate the next action. Let's think step by step. "

    messages = [
        [
            {"role": "system", "content" : sys_str},
            {"role": "user", "content": user_str},
        ]
    ]
    #print("\nAgent Sys_str: "+sys_str)
    #print("\nAgent User_str: "+user_str)

    return messages   # 规范输入


def policy_by_agent(CTXT, text_obs, feedback=None):
    prompt = compose_prompt(CTXT, text_obs, feedback)
    action = client.chat_completion(prompt)[0]['generation']['content'] # 直接把输出作为动作
    print("Action: ", action)
    return action



achievements = ['collect_coal',
 'collect_diamond',
 'collect_drink',
 'collect_iron',
 'collect_sapling',
 'collect_stone',
 'collect_wood',
 'defeat_skeleton',
 'defeat_zombie',
 'eat_cow',
 'eat_plant',
 'make_iron_pickaxe',
 'make_iron_sword',
 'make_stone_pickaxe',
 'make_stone_sword',
 'make_wood_pickaxe',
 'make_wood_sword',
 'place_furnace',
 'place_plant',
 'place_stone',
 'place_table',
 'wake_up']


# In[144]:


done = True
step = 0
_, info = env.reset()
CTXT = '''1. Move West: Flat ground west of the agent.
2. Move East: Flat ground east of the agent.
3. Move North: Flat ground north of the agent.
4. Move South: Flat ground south of the agent.
5. Do: Facing creature or material; have necessary tool.
6. Sleep: Energy level is below maximum.
7. Place Stone: Stone in inventory.
8. Place Table: Wood in inventory.
9. Place Furnace: Stone in inventory.
10. Place Plant: Sapling in inventory.
11. Make Wood Pickaxe: Nearby table; wood in inventory.
12. Make Stone Pickaxe: Nearby table; wood, stone in inventory.
13. Make Iron Pickaxe: Nearby table, furnace; wood, coal, iron an inventory.
14. Make Wood Sword: Nearby table; wood in inventory.
15. Make Stone Sword: Nearby table; wood, stone in inventory.
16. Make Iron Sword: Nearby table, furnace; wood, coal, iron in inventory.
17. Noop: Always applicable.'''
trajectories = []
mytrajectories = []
R = 0
a = action_list.index("Noop")
curr_action = "Noop"

# columns=["Step", "OBS", "Score", "Reward"] + ["Lvl-{}: {}".format(i,q) for i, q in enumerate(questions_lvls)] + ["Action"]
# wandb_table = wandb.Table(columns=columns)
# achievement_table = wandb.Table(columns=achievements)

last_log = 0

actions = list()


import pygame
from PIL import Image
pygame.init()
screen = pygame.display.set_mode(args.window)
clock = pygame.time.Clock()
size = [600,600]

while step < max_step:

    if done:
        env.reset()
    done = False
    # a_row = [0] * len(questions_lvls)

    last_action = curr_action

    _, reward, done, info = env.mystep(a)
    R += reward

    
     # Rendering.
    image = env.render(size)
    if size != args.window:
        image = Image.fromarray(image)
        image = image.resize(args.window, resample=Image.NEAREST)
        image = np.array(image)
    surface = pygame.surfarray.make_surface(image.transpose((1, 0, 2)))
    screen.blit(surface, (0, 0))
    pygame.display.flip()
    clock.tick(args.fps)
    

    print("=="*15, "Step: {}, Reward: {}".format(step, R), "=="*15)
    desc = info['obs']
    print(desc)
    

    trajectories.append((step, desc))
    '''text_obs = "\n\n".join(["Player Observation Step {}:\n{}".format(i,d) for i, d in trajectories[-4:]])'''
    mytrajectories.append((step, env.curr_subgoal_str(), desc, env.subgoals_progress_str()))
    text_obs = "\n\n".join(["Step {}:\n{}".format(i,d) for i, d in trajectories[-4:]])
    mytext = "\n\n".join("Step {}:\nGold truth for task: {}\n\nObservation:\n{}\n\nCurrent achievement of student:\n{}".format(a,b,c,d) for a,b,c,d in mytrajectories[-4:])
    
    
    # 加入feedback
    subgoals = str(env.subgoals_progress())
    feedback = None
    feedback = assistant.get_feedback(task=env.taskname, solution=last_action, obs=desc, feedback_type=feedback_type, gold_truth=env.curr_subgoal_str(), addition=CTXT, fewshots='craft')
    

    print("--"*10 + " policy " + "--"*10)
    action = policy_by_agent(CTXT, text_obs, feedback)
    # results = topological_traverse(CTXT, text_obs, question_dependencies)
    
    # for (q,a) in results.items():
    #     a_row[questions_lvls.index(q)] = a
    #     if q == q_act:
    #         answer_act = a

    # new_row = new_row + a_row

    a, curr_action = match_act(action)
    actions.append(a)
    step += 1
    
    if info['achievements'][env.taskname] >= 1 :
        print("finish task!!!")
        break
    
    if done:
        break

pygame.quit()

env._save()


# In[ ]:


sys.stdout.flush()
sys.stdout = sys.__stdout__
log.close()

