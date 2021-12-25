import pygame as a


keys_converter = {}


def get_key_slow(c: int):
    if c == a.K_a:
        return 0x1E
    elif c == a.K_b:
        return 0x30
    elif c == a.K_c:
        return 0x2E
    elif c == a.K_d:
        return 0x20
    elif c == a.K_e:
        return 0x12
    elif c == a.K_f:
        return 0x21
    elif c == a.K_g:
        return 0x22
    elif c == a.K_h:
        return 0x23
    elif c == a.K_i:
        return 0x17
    elif c == a.K_j:
        return 0x24
    elif c == a.K_k:
        return 0x25
    elif c == a.K_l:
        return 0x26
    elif c == a.K_m:
        return 0x32
    elif c == a.K_n:
        return 0x31
    elif c == a.K_o:
        return 0x18
    elif c == a.K_p:
        return 0x19
    elif c == a.K_q:
        return 0x10
    elif c == a.K_r:
        return 0x13
    elif c == a.K_s:
        return 0x1F
    elif c == a.K_t:
        return 0x14
    elif c == a.K_u:
        return 0x16
    elif c == a.K_v:
        return 0x2F
    elif c == a.K_w:
        return 0x11
    elif c == a.K_x:
        return 0x2D
    elif c == a.K_y:
        return 0x15
    elif c == a.K_z:
        return 0x2C
    elif c == a.K_0:
        return 0x0B
    elif c >= a.K_0 and c <= a.K_9:
        result = c - a.K_0 + 1
        if not result:
            result = 10
        return result
    elif c == a.K_EQUALS:
        return 0x0D
    elif c == a.K_RETURN:
        return 0x1C
    elif c == a.K_BACKSPACE:
        return 0x0E
    elif c == a.K_LEFT:
        return 0xE04B
    elif c == a.K_DOWN:
        return 0xE050
    elif c == a.K_RIGHT:
        return 0xE04D
    elif c == a.K_UP:
        return 0xE048
    elif c == a.K_SPACE:
        return 0x39
    elif c == a.K_PAGEUP:
        return 0xE04F
    elif c == a.K_PAGEDOWN:
        return 0xE051
    elif c == a.K_DELETE:
        return 0xE053
    elif c >= a.K_F1 and c <= a.K_F12:
        return 0x3B + (c - a.K_F1)
    elif c == a.K_SLASH:
        return 0x35
    elif c == a.K_LALT:
        return 0x38
    elif c == a.K_RALT:
        return 0xE038
    elif c == a.K_LCTRL:
        return 0x1D
    elif c == a.K_RCTRL:
        return 0xe01d
    elif c == a.K_LSHIFT:
        return 0x2A
    elif c == a.K_RSHIFT:
        return 0x36
    elif c == a.K_EQUALS:
        return 0x0D
    elif c == a.K_SEMICOLON:
        return 0x27
    elif c == a.K_BACKSLASH:
        return 0x28
    elif c == a.K_COMMA:
        return 0x33
    elif c == a.K_PERIOD:
        return 0x34
    elif c == a.K_MINUS:
        return 0x0C
    elif c == a.K_RIGHTBRACKET:
        return 0x1A
    elif c == a.K_LEFTBRACKET:
        return 0x1B
    elif c == a.K_QUOTE:
        return 0x28
    elif c == a.K_BACKQUOTE:
        return 0x29
    elif c == a.K_TAB:
        return 0x0F
    elif c == a.K_ESCAPE:
        return 0x01
    elif c == 0x137:  # Left WIN
        return 0xE05B
    elif c == 0x138:  # Right WIN
        return 0xE05B
    return None


for i in range(500):
    key_ = get_key_slow(i)
    if not key_:
        continue
    keys_converter[i] = key_
