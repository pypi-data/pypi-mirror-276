from pgzero.screen import Screen
from pygame import transform, Surface
from pygame import font as f
import pygame, requests
import pygame.image
import io
import copy
from random import randint
from pgzero import rect
from pgzero.actor import Actor
from pgzero.game import PGZeroGame
from pgzero.runner import prepare_mod
import pgzero
import sys

FPS = 30
def set_fps(fps):
    global FPS
    FPS = fps

def load_background(url):
    r = requests.get(url)
    img = io.BytesIO(r.content)
    loaded_img = pygame.image.load(img)
    orig_surf = loaded_img
    new_surf = transform.scale(loaded_img, [680, int((640/orig_surf.get_size()[0]) * orig_surf.get_size()[1])])
    return new_surf

def initialize_screen(width, height):
    pygame.init()
    pygame.display.init()
    pygame.display.set_mode((width, height))

    return Screen(Surface([width, height]))

def run_game():
    mod = sys.modules['__main__']
    prepare_mod(mod)
    game = CustomGame(mod)
    game.run()
def render_game(player_alive, screen, background, player, target, danger, mysteries, title, score, color, width, height):
    font = f.Font(None, 25)
    screen.clear()
    screen.blit(background, [0, 0])
    if player_alive:
        score_string = title + "     Score: " + str(score)
        player.draw()
        target.draw()
        danger.draw()
        for m in mysteries:
            m.draw()
        text_1 = font.render(score_string, True, color)
        text_2 = font.render(len(score_string) * "_", True, color)
        text_1_rect = text_1.get_rect(center=(width / 2, 20))
        text_2_rect = text_2.get_rect(center=(width / 2, 20))
        screen.blit(text_1, text_1_rect)
        screen.blit(text_2, text_2_rect)
    else:
        text_1 = font.render("You Died!", True, color)
        text_2 = font.render("Press ESC to Restart", True, color)
        text_1_rect = text_1.get_rect(center=(width / 2, height / 2 - 20))
        text_2_rect = text_2.get_rect(center=(width / 2, height / 2 + 20))
        screen.blit(text_1, text_1_rect)
        screen.blit(text_2, text_2_rect)
def update_cycle(player, danger, target, mystery, mysteries, is_onscreen, update_player, update_target, update_danger, update_mystery, is_collision, score, width, height, k, m_lag, d_lag, t_lag, p_alive, p_spos, t_spos, d_spos):
    if p_alive:
        m_lag -= 1
        d_lag -= 1
        t_lag -= 1
        commanded_player_pos = update_player(player.x, player.y)
        if is_onscreen(commanded_player_pos[0], commanded_player_pos[1]):
            player.pos = commanded_player_pos
        else:
            player.pos = player.pos

        if d_lag < 0:
            commanded_danger_pos = update_danger(danger.x, danger.y)
            if is_onscreen(commanded_danger_pos[0], commanded_danger_pos[1]):
                danger.pos = commanded_danger_pos
            else:
                danger.pos = (-1000, -1000)
                d_lag = 30
            if is_collision(player.x, player.y, danger.x, danger.y):
                danger.pos = (-1000, -1000)
                d_lag = 30
                score -= 50

        if t_lag < 0:
            commanded_target_pos = update_target(target.x, target.y)
            if is_onscreen(commanded_target_pos[0], commanded_target_pos[1]):
                target.pos = commanded_target_pos
            else:
                target.pos = (-1000, -1000)
                t_lag = 30
            if is_collision(player.x, player.y, target.x, target.y):
                target.pos = (-1000, -1000)
                t_lag = 30
                score += 20

        if k.space and m_lag <= 0:
            new_mystery = copy.copy(mystery)
            new_mystery.pos = player.pos
            mysteries.append(copy.copy(new_mystery))
            m_lag = 10

        for mystery in mysteries:
            commanded_mystery_pos = update_mystery(mystery.x, mystery.y)
            if is_collision(mystery.x, mystery.y, danger.x, danger.y):
                mysteries.remove(mystery)
                danger.pos = (-1000, -1000)
                d_lag = 30
                score += 20
            elif is_collision(mystery.x, mystery.y, target.x, target.y):
                mysteries.remove(mystery)
                target.pos = (-1000, -1000)
                t_lag = 30
                score += 20
            elif is_onscreen(commanded_mystery_pos[0], commanded_mystery_pos[1]):
                mystery.pos = commanded_mystery_pos
            else:
                mysteries.remove(mystery)

        if t_lag == 0:
            if update_target(0, 0)[0] > 0:
                target.pos = (0, randint(50, height - 50))
            else:
                target.pos = (width, randint(50, height - 50))
        if d_lag == 0:
            if update_danger(0, 0)[0] > 0:
                danger.pos = (0, randint(50, height - 50))
            else:
                danger.pos = (width, randint(50, height - 50))

        if score <= 0:
            p_alive = False

    else:
        player.pos = p_spos
        danger.pos = d_spos
        target.pos = t_spos
        mysteries.clear()
        if k.escape:
            score = 100
            m_lag = 0
            d_lag = 0
            t_lag = 0
            p_alive = True

    return score, m_lag, d_lag, t_lag, p_alive

##########################################################################
# Modified Actor class to add scale, flip and loading images from urls
##########################################################################
class GameElement(Actor):
    def __init__(self, url, pos=None, anchor=None, **kwargs):
        self._handle_unexpected_kwargs(kwargs)

        self.__dict__["_rect"] = rect.ZRect((0, 0), (0, 0))
        # Initialise it at (0, 0) for size (0, 0).
        # We'll move it to the right place and resize it later

        self.url = url
        self._init_position(pos, anchor, **kwargs)

    @property
    def url(self):
        return self._url_name

    @url.setter
    def url(self, url):
        self._url_name = url
        r = requests.get(url)
        img = io.BytesIO(r.content)
        loaded_img = pygame.image.load(img)
        self._orig_surf = self._surf = loaded_img
        self._update_pos()

    def scale(self, scale):
        orig_surf = self._surf
        new_surf = transform.scale(self._surf,
                                   [int(orig_surf.get_size()[0] * scale), int(orig_surf.get_size()[1] * scale)])
        self._surf = new_surf

    def flip_horizontal(self):
        new_surf = transform.flip(self._surf, True, False)
        self._surf = new_surf

    def flip_vertical(self):
        new_surf = transform.flip(self._surf, False, True)
        self._surf = new_surf
##########################################################################
# Modified Game class to run at 30fps
##########################################################################

class CustomGame(PGZeroGame):
    def mainloop(self):
        """Run the main loop of Pygame Zero."""
        clock = pygame.time.Clock()
        self.reinit_screen()

        update = self.get_update_func()
        draw = self.get_draw_func()
        self.load_handlers()

        pgzclock = pgzero.clock.clock

        self.need_redraw = True
        while True:
            dt = clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q and \
                            event.mod & (pygame.KMOD_CTRL | pygame.KMOD_META):
                        sys.exit(0)
                    self.keyboard._press(event.key)
                elif event.type == pygame.KEYUP:
                    self.keyboard._release(event.key)
                self.dispatch_event(event)

            pgzclock.tick(dt)

            if update:
                update(dt)

            screen_change = self.reinit_screen()
            if screen_change or update or pgzclock.fired or self.need_redraw:
                draw()
                pygame.display.flip()
                self.need_redraw = False
