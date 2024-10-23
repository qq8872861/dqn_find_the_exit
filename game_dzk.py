import numpy as np
import pygame
import random

# 游戏常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BRICK_WIDTH = 75
BRICK_HEIGHT = 20
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
BALL_RADIUS = 10
BRICK_ROWS = 5
BRICK_COLS = 10

class game_dzk:
    def __init__(self):
        # 初始化pygame
        pygame.init()
        self.state_num = 6
        self.action_num = 3
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('打砖块游戏')

        # 初始化游戏状态
        self.reset()
        
    def reset(self):
        # 初始化砖块
        self.bricks = [[1 for _ in range(BRICK_COLS)] for _ in range(BRICK_ROWS)]
        self.paddle_pos = [SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - PADDLE_HEIGHT - 10]
        self.ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        self.ball_vel = [random.choice([-4, 4]), -4]  # 随机水平速度
        self.score = 0
        self.game_over = False
        return self.get_state()

    def get_state(self):
        # 获取游戏状态，包含球和挡板的位置、速度以及砖块的状态且归一化到0-1之间
        state = np.array(self.ball_pos + self.ball_vel + self.paddle_pos, dtype=np.float32)
        state = state / [SCREEN_WIDTH, SCREEN_HEIGHT, 4, 4, SCREEN_WIDTH, SCREEN_HEIGHT]
        return state
        #return np.array(self.ball_pos + self.ball_vel + self.paddle_pos, dtype=np.float32)

    def step(self, action):
        self.score = 0
        
        # 挡板和球之间的水平距离
        self.dis2boll_old = abs(self.ball_pos[0] - self.paddle_pos[0]) - (PADDLE_WIDTH // 2 )
        
        # 更新挡板位置
        if action == 0:  # 向左移动
            self.paddle_pos[0] = max(0, self.paddle_pos[0] - 10)
        elif action == 1:  # 向右移动
            self.paddle_pos[0] = min(SCREEN_WIDTH - PADDLE_WIDTH, self.paddle_pos[0] + 10)

        # 更新球的位置
        self.ball_pos[0] += self.ball_vel[0]
        self.ball_pos[1] += self.ball_vel[1]
        
        # 如果挡板向球的方向移动
        self.dis2boll_new = abs(self.ball_pos[0] - self.paddle_pos[0]) - (PADDLE_WIDTH // 2 )
        if(self.dis2boll_new < self.dis2boll_old):
            self.score += 0.1
        
        # 如果球的水平位置和挡板的水平位置不同
        if self.ball_pos[0] < self.paddle_pos[0] or self.ball_pos[0] > self.paddle_pos[0] + PADDLE_WIDTH:
            self.score -= 0.1
        else:
            self.score += 0.15

        # 碰撞检测
        if self.ball_pos[0] <= BALL_RADIUS or self.ball_pos[0] >= SCREEN_WIDTH - BALL_RADIUS:  # 左右边界
            self.ball_vel[0] = -self.ball_vel[0]
        if self.ball_pos[1] <= BALL_RADIUS:  # 上边界
            self.ball_vel[1] = -self.ball_vel[1]
        if self.ball_pos[1] >= SCREEN_HEIGHT - BALL_RADIUS:  # 球掉落
            self.score -= 10
            self.game_over = True

        # 检测碰撞挡板
        if (self.paddle_pos[0] < self.ball_pos[0] < self.paddle_pos[0] + PADDLE_WIDTH and
                self.ball_pos[1] + BALL_RADIUS >= self.paddle_pos[1] - 1):
            self.ball_vel[1] = -self.ball_vel[1]
            #self.score += 1

        # 检测碰撞砖块
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                if self.bricks[row][col] == 1:
                    brick_pos = [col * BRICK_WIDTH, row * BRICK_HEIGHT]
                    if (brick_pos[0] < self.ball_pos[0] < brick_pos[0] + BRICK_WIDTH and
                            brick_pos[1] < self.ball_pos[1] < brick_pos[1] + BRICK_HEIGHT):
                        self.bricks[row][col] = 0
                        self.ball_vel[1] = -self.ball_vel[1]
                        self.score += 1
                        
        # 所有砖块都被消除，游戏结束
        if all(all(brick == 0 for brick in row) for row in self.bricks):
            self.game_over = True

        done = self.game_over
        return self.get_state(), self.score, done, {}

    def render(self):
        self.screen.fill((255, 255, 255))  # 清屏

        # 绘制砖块
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                if self.bricks[row][col] == 1:
                    pygame.draw.rect(self.screen, (0, 0, 255),
                                     (col * BRICK_WIDTH, row * BRICK_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT))

        # 绘制挡板
        pygame.draw.rect(self.screen, (255, 0, 0),
                         (self.paddle_pos[0], self.paddle_pos[1], PADDLE_WIDTH, PADDLE_HEIGHT))

        # 绘制小球
        pygame.draw.circle(self.screen, (0, 255, 0), (int(self.ball_pos[0]), int(self.ball_pos[1])), BALL_RADIUS)

        pygame.display.flip()  # 更新显示

    # def play(self):
    #     while not self.game_over:
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 self.game_over = True
            
    #         self.render()
    #         action = random.choice([0, 1])  # 随机选择动作（左或右）
    #         self.step(action)

    #     pygame.quit()


if __name__ == '__main__':
    game = game_dzk()
    game.play()
