import os
import sys
import pygame
import sock
import time
import base64
import io
from node_runner import run_node
from keyb import keys_converter
try:
    import win_tools
    use_win_tools = True
except ImportError:
    use_win_tools = False


def p(*args, **kwargs):
    return os.path.join(cur_path, *args, **kwargs)


def resize_window(w: int, h: int) -> None:
    if use_win_tools:
        pygame.display.set_mode((w, h))
        hwnd_ = pygame.display.get_wm_info()['window']
        if not hwnd_:
            return
        hwnd = int(hwnd_)
        screen_width, screen_height = win_tools.get_screen_size()
        app_size = win_tools.get_app_rect(hwnd)[2:]
        need_x = round(screen_width / 2 - app_size[0] / 2)
        need_y = round(screen_height / 2 - app_size[1] / 2)
        win_tools.resize_app(
            hwnd, (
                need_x,
                need_y,
                app_size[0],
                app_size[1]
            )
        )
    else:
        infoObject = pygame.display.Info()
        screen_width, screen_height = infoObject.current_w, infoObject.current_h
        need_x, need_y = round(screen_width / 2 - w / 2), round(screen_height / 2 - h / 2)
        os.environ['SDL_VIDEO_WINDOW_POS'] = f'{need_x},{need_y}'
        pygame.display.set_mode((w, h))


def fix_color(color: list) -> tuple:
    return tuple(color)


pygame.init()
sock.init()
run_node()
sock.wait_for_connection()


cur_path = os.getcwd()
w, h = 720, 400
c_w, c_h = round(w / 2), round(h / 2)
running = True
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption('Starting localcpu.js...')
pygame.display.set_icon(pygame.image.load(p('icon.ico')).convert_alpha())
last_mouse_x, last_mouse_y = pygame.mouse.get_pos()
is_inited = False
is_mouse_locked = False
empty_cursor = pygame.cursors.compile((
    "        ",
    "        ",
    "        ",
    "        ",
    "        ",
    "        ",
    "        ",
    "        ",
))
is_graphical = False
text_multiplier = (9, 16)
text_mode_size = (80, 25)
text_size = (text_mode_size[0] * text_multiplier[0],
             text_mode_size[1] * text_multiplier[1])
text_font = pygame.font.Font(p('dejavu_sans_mono.ttf'), text_multiplier[1] - 2)
mouse_downs = [False, False, False]
aa = True
is_updated = False
send_keys = []
resize_window(w, h)


while running:
    events = {}
    for event in pygame.event.get():
        if not is_mouse_locked and event.type == pygame.QUIT:
            running = False
            events['q'] = True
        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if is_mouse_locked:
                if not mouse_x - c_w == 0:
                    events['x'] = mouse_x - c_w
                if not mouse_y - c_h == 0:
                    events['y'] = mouse_y - c_h
                pygame.mouse.set_pos((c_w, c_h))
                continue
            '''if not mouse_x - last_mouse_x == 0:
                events['x'] = mouse_x - last_mouse_x
                last_mouse_x = mouse_x
            if not mouse_y - last_mouse_y == 0:
                events['y'] = mouse_y - last_mouse_y
                last_mouse_y = mouse_y'''
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not is_mouse_locked and event.button == 1:
                continue
            if 3 >= event.button > 0:
                mouse_downs[event.button - 1] = True
            events['d'] = mouse_downs
        elif event.type == pygame.MOUSEBUTTONUP:
            if not is_mouse_locked and event.button == 1:
                is_mouse_locked = True
                pygame.mouse.set_pos((c_w, c_h))
                pygame.event.set_grab(True)
                pygame.mouse.set_cursor((8, 8), (0, 0), *empty_cursor)
                pygame.display.set_caption(
                    f'localcpu.js [{w}x{h}] (Press ESCape to unlock your mouse)')
                continue
            if 3 >= event.button > 0:
                mouse_downs[event.button - 1] = False
            events['d'] = mouse_downs
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                continue
            key_ = keys_converter.get(event.key)
            if key_ and key_ not in send_keys:
                send_keys.append(key_)
                if not events.get('a'):
                    events['a'] = []
                events['a'].append(key_)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                is_mouse_locked = False
                pygame.event.set_grab(False)
                pygame.display.set_caption(f'localcpu.js [{w}x{h}]')
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                continue
            key_ = keys_converter.get(event.key)
            if key_ and key_ in send_keys:
                send_keys.remove(key_)
                if not events.get('b'):
                    events['b'] = []
                events['b'].append(key_)
    msg = sock.get_msg()
    if not is_inited:
        if msg.get('init'):
            is_inited = True
            pygame.display.set_caption(f'localcpu.js [{w}x{h}]')
        else:
            continue
    if msg.get('m'):
        is_graphical = msg.get('m')
        if not is_graphical:
            w, h = text_size
            c_w, c_h = round(w / 2), round(h / 2)
            pygame.display.set_caption(f'localcpu.js [{w}x{h}]')
            resize_window(w, h)
        msg['c'] = True
    if msg.get('sg'):
        w, h = msg.get('sg')
        c_w, c_h = round(w / 2), round(h / 2)
        pygame.display.set_caption(f'localcpu.js [{w}x{h}]')
        resize_window(w, h)
    if msg.get('st'):
        text_mode_size = tuple(msg.get('st'))
        text_size = (text_mode_size[0] * text_multiplier[0],
                     text_mode_size[1] * text_multiplier[1])
        w, h = text_size
        c_w, c_h = round(w / 2), round(h / 2)
        pygame.display.set_caption(f'localcpu.js [{w}x{h}]')
        resize_window(w, h)
    if msg.get('c'):
        screen.fill((0, 0, 0))
        is_updated = True
    if is_graphical:
        buf = msg.get('g')
        if buf:
            screen.blit(
                pygame.image.load(
                    io.BytesIO(
                        base64.b64decode(
                            buf
                        )
                    )
                ),
                (0, 0)
            )
            is_updated = True
    else:
        buf = msg.get('v')
        if buf:
            pygame.draw.rect(
                screen,
                fix_color(buf[3]),
                (
                    text_multiplier[0] * buf[1],
                    text_multiplier[1] * buf[0],
                    text_multiplier[0],
                    text_multiplier[1]
                )
            )
            screen.blit(
                text_font.render(buf[2], aa, fix_color(buf[4])),
                (text_multiplier[0] * buf[1], text_multiplier[1] * buf[0])
            )
            is_updated = True
    if events:
        sock.send_msg(events)
    if is_updated:
        is_updated = False
        pygame.display.flip()


sock.quit()
pygame.quit()
