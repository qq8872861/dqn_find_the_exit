import numpy as np
import pygame


class mygame:
    def __init__(self):
        # 游戏环境设置
        self.grid_size = 10
        self.state_num = 5
        self.action_num = 4  # 上，下，左，右
        self.max_steps = 50
        #终点位置
        self.goal_pos = [self.grid_size - 1, self.grid_size - 1]
        self.dis2End = 0
        #终点所在方向
        self.goal_dir = 0
        
        # 初始化游戏
        self.reset()
        
    def reset(self):
        # 重置游戏状态
        self.agent_pos = [0, 0]  # 智能体起始位置
        self.steps = 0
        self.total_reward = 0
        #随机终点位置
        self.goal_pos = [np.random.randint(1, self.grid_size - 1), np.random.randint(1, self.grid_size - 1)]
        self.dis2End = np.sqrt((self.agent_pos[0]-self.goal_pos[0])**2+(self.agent_pos[1]-self.goal_pos[1])**2)
        #agent_pos到终点的方向
        if self.agent_pos[0] < self.goal_pos[0]:
            self.goal_dir = 1  # 0:上 1:下 2:左 3:右
        elif self.agent_pos[0] > self.goal_pos[0]:
            self.goal_dir = 0
        elif self.agent_pos[1] < self.goal_pos[1]:
            self.goal_dir = 3
        else:
            self.goal_dir = 2
        
        return self.get_state()
        
    def get_state(self):
        return np.array([*self.agent_pos, self.steps, self.dis2End, self.goal_dir], dtype=np.float32)
    
    def step(self, action):
        #距离终点的距离
        dis2EndOld = np.sqrt((self.agent_pos[0]-self.goal_pos[0])**2+(self.agent_pos[1]-self.goal_pos[1])**2)
        # 根据动作更新智能体的位置
        if action == 0:  # 上
            self.agent_pos[0] = max(0, self.agent_pos[0] - 1)
        elif action == 1:  # 下
            self.agent_pos[0] = min(self.grid_size - 1, self.agent_pos[0] + 1)
        elif action == 2:  # 左
            self.agent_pos[1] = max(0, self.agent_pos[1] - 1)
        elif action == 3:  # 右
            self.agent_pos[1] = min(self.grid_size - 1, self.agent_pos[1] + 1)
            
        #agent_pos到终点的方向
        if self.agent_pos[0] < self.goal_pos[0]:
            self.goal_dir = 1  # 0:上 1:下 2:左 3:右
        elif self.agent_pos[0] > self.goal_pos[0]:
            self.goal_dir = 0
        elif self.agent_pos[1] < self.goal_pos[1]:
            self.goal_dir = 3
        else:
            self.goal_dir = 2

        # 计算奖励
        reward = 0
        game_over = False
        if self.agent_pos == [self.goal_pos[0], self.goal_pos[1]]:
            reward = 100  # 到达终点给予奖励
            game_over = True
        else:
            # 计算距离终点的距离
            dis2EndNew = np.sqrt((self.agent_pos[0]-self.goal_pos[0])**2+(self.agent_pos[1]-self.goal_pos[1])**2)
            self.dis2End = dis2EndNew
            if dis2EndNew < dis2EndOld:  # 行动有效，奖励增加
                reward = 2
            else:  # 行动无效，奖励减少
                reward = -2  # 每步行动扣分
                
        if self.steps >= self.max_steps:  # 超过最大步数，游戏结束
            game_over = True
            reward = -100  # 超过最大步数扣分
            
        #使用步数约束，行动扣分
        if self.steps > 20:
            reward -= 1
        
        self.total_reward += reward
        self.steps += 1
        
        done = reward > 50 or game_over # 游戏结束条件
        return self.get_state(), reward, done, {}
    
    def render(self):

        # 游戏主循环
        # running = True
        # while running:
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             running = False

            # 绘制网格
            screen.fill((255, 255, 255))
            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    rect = pygame.Rect(j * 60, i * 60, 60, 60)
                    pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # 绘制边框

            # 绘制智能体
            agent_x, agent_y = self.agent_pos
            pygame.draw.rect(screen, (255, 0, 0), (agent_y * 60 + 1, agent_x * 60 + 1, 58, 58))  # 绘制智能体
            
            # 绘制终点（绿色）
            goal_x, goal_y = self.goal_pos[0], self.goal_pos[1] # 终点位置
            pygame.draw.rect(screen, (0, 255, 0), (goal_y * 60 + 1, goal_x * 60 + 1, 58, 58))  # 绘制终点

            # 更新显示
            pygame.display.flip()
            #pygame.time.delay(200)  # 控制游戏速度
            
        # pygame.quit()
        
# 可视化游戏过程
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Simple Game')


# 测试游戏
if __name__ == '__main__':
    game = mygame()
    game.render()
