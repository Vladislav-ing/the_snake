from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

dict_input = {pygame.K_UP: UP, pygame.K_DOWN: DOWN,
              pygame.K_LEFT: LEFT, pygame.K_RIGHT: RIGHT}

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Родительский клас(Общие атрибуты: цвет, позиция, метод для отрисовки)"""

    position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def __init__(self, body_color=None):
        self.position = GameObject.position
        self.body_color = body_color

    @staticmethod
    def checking_occupied(apple, snake):
        """Формирование рандомных координат для яблока."""
        while apple.position in snake.positions:
            apple.position = apple.randomize_position()

    @staticmethod
    def draw(self, surface):
        """Отрисовка объектов объединена в 1 метод"""
        if 'positions' not in dir(self) or len(self.positions) < 2:
            rect = pygame.Rect(
                (self.position[0], self.position[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)
        else:
            for position in self.positions[:-1]:
                rect = (pygame.Rect(
                    (position[0], position[1]), (GRID_SIZE, GRID_SIZE))
                )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)
        # Отрисовка головы змейки.
            head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, head_rect)
            pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента змейки.
        if 'last' in dir(self) and self.last is not None:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]), (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)


class Snake(GameObject):
    """Обрабатывает действия, состояние, отрисовывет змейку."""

    def __init__(self, body_color=SNAKE_COLOR, length=1,
                 direction=RIGHT, next_direction=None):

        super().__init__(body_color)
        self.length = length
        self.direction = direction
        self.next_direction = next_direction
        self.positions = [self.position]
        self.last = None

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод для обновления позиции змейки."""
        head, direct = self.get_head_position(), self.direction
        update_head = [head[0] + (direct[0] * GRID_SIZE),
                       head[1] + (direct[1] * GRID_SIZE)]

        if (0 >= update_head[0] or update_head[0] >= SCREEN_WIDTH) or (
                0 >= update_head[1] or update_head[1] >= SCREEN_HEIGHT):
            update_head = [update_head[0] % SCREEN_WIDTH,
                           update_head[1] % SCREEN_HEIGHT]

        update_head = tuple(update_head)

        if len(self.positions) > 2 and update_head in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, update_head)
            self.position = update_head
            self.last = (self.positions.pop()
                         if len(self.positions) > self.length else None)

    def reset(self):
        """Сброс змейки в рандомное положение"""
        new_direct = choice((RIGHT, LEFT, UP, DOWN))
        self.__init__(SNAKE_COLOR, 1,
                      direction=new_direct, next_direction=None)
        screen.fill(BOARD_BACKGROUND_COLOR)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]


class Apple(GameObject):
    """Дочерний класс, инициализирует яблоко, действия, отрисовывает."""

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color)
        self.position = self.randomize_position()

    def randomize_position(self):
        """Генерируются рандомные координаты"""
        return (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE)


def handle_keys(game_object):
    """Обработка нажатий клавиш или кнопки закрытия окна"""
    global SPEED
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key in dict_input:
                next_path = dict_input.get(event.key)
                actuall_path = game_object.direction
                game_object.next_direction = (next_path if abs(actuall_path[0])
                                              != abs(next_path[0]) else None)


def main():
    """Тут нужно создать экземпляры классов."""
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        GameObject.draw(apple, screen)
        GameObject.draw(snake, screen)

        if snake.position == apple.position:
            snake.length += 1
            snake.positions.append(snake.last)

            apple = Apple(APPLE_COLOR)
            GameObject.checking_occupied(apple, snake)

        pygame.display.update()


if __name__ == '__main__':
    main()
