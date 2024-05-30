import json
import crafter
class WrapEnv(crafter.Recorder):
    def __init__(self, env, directory, save_stats=True, save_video=True,
      save_episode=True, video_size=(512, 512)):
        super(WrapEnv, self).__init__(env, directory, save_stats,save_video,save_episode, video_size)
        self.taskname = "collect_diamond"
        self.subgoal = dict() # 任务的subgoals的完成目标
        self.achievements = {'collect_coal': 0, 'collect_diamond': 0, 'collect_drink': 0, 'collect_iron': 0, 'collect_sapling': 0, 'collect_stone': 0, 'collect_wood': 0, 'defeat_skeleton': 0, 'defeat_zombie': 0, 'eat_cow': 0, 'eat_plant': 0, 'make_iron_pickaxe': 0, 'make_iron_sword': 0, 'make_stone_pickaxe': 0, 'make_stone_sword': 0, 'make_wood_pickaxe': 0, 'make_wood_sword': 0, 'place_furnace': 0, 'place_plant': 0, 'place_stone': 0, 'place_table': 0, 'wake_up': 0} # 所有subgoals的完成情况
        self.done = False
    
    
    def set_task(self, task):
        self.taskname = task # 使用 self 来引用类的属性
        # output
        with open('craft/subgoals.json', 'r') as file:    # ！这里得改路径
            subgoals = json.load(file)
        self.subgoal = subgoals[self.taskname] # 使用 self 来引用类的属性

    def cutoutObs(self, desc): # 添加 self 参数
        # 变化动作的表示形式
        action_space = ['Noop', 'Move West', 'Move East', 'Move North', 'Move South', 'Do', 'Sleep', 'Place Stone', 'Place Table', 'Place Furnace', 'Place Plant', 'Make Wood Pickaxe', 'Make Stone Pickaxe', 'Make Iron Pickaxe', 'Make Wood Sword', 'Make Stone Sword', 'Make Iron Sword']
        actions = [
            'noop', 'move_west', 'move_east', 'move_north', 'move_south',
            'do', 'sleep', 'place_stone', 'place_table', 'place_furnace',
            'place_plant', 'make_wood_pickaxe', 'make_stone_pickaxe',
            'make_iron_pickaxe', 'make_wood_sword', 'make_stone_sword', 'make_iron_sword'
        ]
        for action in actions:
            if action.lower() in desc.lower():
                # Find the corresponding action in action_space
                index = actions.index(action)
                new_action = action_space[index]
                # Replace the action
                desc = desc.replace(action, new_action)

        index_start = desc.find("Your status:")
        index_end = desc.find("energy:") + 13
        head = desc[:index_start]
        tail = desc[index_end:]
        return head + tail
    
    def convert_achievements_to_list(self, achievements): # 添加 self 参数
        achi_list = [[task, achievements[task]] for task in achievements]
        return achi_list
    
    def mystep(self,a):
        obs, reward, done, info = self.step(a)
        info['obs'] = self.cutoutObs(info['obs'])
        self.achievements = info['achievements']
        return obs, reward, done, info

    def steps(self, actions_list):
        indexs = [int(action.split('.')[0]) for action in actions_list]
        actions = [action.split('. ')[1] for action in actions_list]
        decs = list()
        
        for i in indexs:
            _, _, done, info = self.step(i)
            obs = self.cutoutObs(info['obs']) # 使用 self 来引用类的方法
            self.achievements = info['achievements'] # 使用 self 来引用类的属性
            
            decs.append(obs)

            if self.achievements[self.taskname] > 0: # 使用 self 来引用类的属性
                self.done = True

        return decs

    def subgoals_progress(self, all=False):
        if all:
            achievements = self.convert_achievements_to_list(self.achievements) # 使用 self 来引用类的方法和属性
            return achievements
        else:
            prog = list()
            for task, (task_name, num) in enumerate(self.subgoal):
                prog.append([task_name, (self.achievements[task_name], num)])
            #print(prog)
            return prog
        
    def subgoals_progress_str(self, all=False):
        subgoals = self.subgoals_progress(all)
        subgoals_str = ''
        for subgoal in subgoals:
            subgoals_str += f"{subgoal[0]}: {subgoal[1][0]}/{subgoal[1][1]}\n"
        return subgoals_str

    def curr_subgoal(self):
        subgoals = self.subgoals_progress()
        for subgoal in subgoals:
            if subgoal[1][0] < subgoal[1][1]:
                return subgoal
        return None
    
    def curr_subgoal_str(self):
        subgoal = self.curr_subgoal()
        if subgoal is None:
            return ""
        return f"{subgoal[0]}: {subgoal[1][0]}/{subgoal[1][1]}"