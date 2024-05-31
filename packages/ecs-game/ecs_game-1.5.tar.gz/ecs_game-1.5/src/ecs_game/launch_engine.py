from pgzero.screen import Screen
from pygame import transform, Surface
from pygame import font as f
import pygame, requests
import pygame.image
import io
from pgzero.keyboard import keyboard as k
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

def render_game(screen, background, rocket, time, width, height, update_rocket):
    font = f.Font(None, 21)
    screen.clear()
    screen.blit(background, [0, 0])
    score_string = "Altitude: " + str(update_rocket(time))+ "    Time: " + str(time)
    rocket.draw()
    text_1 = font.render(score_string, True, (255, 255, 255))
    text_2 = font.render(len(score_string) * "_", True, (255, 255, 255))
    text_1_rect = text_1.get_rect(center=(width / 2, 20))
    text_2_rect = text_2.get_rect(center=(width / 2, 20))
    screen.blit(text_1, text_1_rect)
    screen.blit(text_2, text_2_rect)

def update_cycle(rocket, update_rocket, time, HEIGHT):
    if time == 0:
        rocket.y = HEIGHT
    new_height = HEIGHT - update_rocket(time)
    rocket.y = new_height
    if k.space:
        time += 1
    if k.b:
        time -= 1
    return time

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
