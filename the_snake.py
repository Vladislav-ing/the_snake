from random import choice, randint

import pygame

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

dict_input = {pygame.K_UP: UP, pygame.K_DOWN: DOWN,
              pygame.K_LEFT: LEFT, pygame.K_RIGHT: RIGHT}

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

SPEED = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()


class GameObject:
    """Родительский клас(Общие атрибуты: цвет, позиция, метод для отрисовки)"""

    def __init__(self, body_color=None):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def checking_occupied(self, snake):
        """Формирование рандомных координат для яблока."""
        while self.position in snake.positions:
            self.position = self.randomize_position()

    def draw(self):
        """Родительский метод, переопределяется в дочерних классах"""
        pass


class Snake(GameObject):
    """Обрабатывает действия, состояние, отрисовывет змейку."""

    def __init__(self, body_color=SNAKE_COLOR, length=1,
                 direction=RIGHT):

        super().__init__(body_color)
        self.length = length
        self.direction = direction
        self.positions = [self.position]
        self.last = None

    def update_direction(self, next_path, actuall_path):
        """Метод проверяющий направление, после нажатия"""
        if abs(actuall_path[0]) != abs(next_path[0]):
            self.direction = next_path

    def move(self):
        """Метод для обновления позиции змейки."""
        head, direct = self.get_head_position(), self.direction
        new_head_position = ((head[0] + (direct[0] * GRID_SIZE))
                             % SCREEN_WIDTH, (head[1] + (direct[1] * GRID_SIZE)
                                              ) % SCREEN_HEIGHT)

        if len(self.positions) > 2 and new_head_position in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_head_position)
            self.position = new_head_position
            self.last = (self.positions.pop()
                         if len(self.positions) > self.length else None)

    def reset(self):
        """Сброс змейки в рандомное положение"""
        new_direct = choice((RIGHT, LEFT, UP, DOWN))
        self.__init__(SNAKE_COLOR, 1,
                      direction=new_direct)
        screen.fill(BOARD_BACKGROUND_COLOR)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def draw(self, surface):
        """Отрисовка змейки"""
        for position in self.positions:
            rect = (pygame.Rect(
                (position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]), (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)


class Apple(GameObject):
    """Дочерний класс, инициализирует яблоко, действия, отрисовывает."""

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color)
        self.position = self.randomize_position()

    def randomize_position(self):
        """Генерируются рандомные координаты"""
        return (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self, surface):
        """Отрисовка яблока"""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """Обработка нажатий клавиш или кнопки закрытия окна"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key in dict_input:
                next_path = dict_input.get(event.key)
                actuall_path = game_object.direction
                game_object.update_direction(
                    next_path=next_path, actuall_path=actuall_path)


def main():
    """Тут нужно создать экземпляры классов."""
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()

        apple.draw(screen)
        snake.draw(screen)

        if snake.position == apple.position:
            snake.length += 1
            snake.positions.append(snake.last)

            apple = Apple()
            apple.checking_occupied(snake)

        pygame.display.update()


if __name__ == '__main__':
    main()
