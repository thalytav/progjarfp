import pygame
from network import Network
import pickle
pygame.font.init()

width, height = 700, 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

# Warna dari palet
CREAM = (255, 251, 222)
TEAL = (144, 209, 202)
EMERALD = (18, 153, 144)
DARK = (9, 107, 104)

# Font
FONT_UI = "Segoe UI"
FONT_EMOJI = "Segoe UI Emoji"

class Button:
    def __init__(self, text, x, y, color, label, width=150, height=100):
        self.text = text
        self.label = label
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height

    def draw(self, win, is_hover=False):
        draw_color = tuple(min(c + 25, 255) for c in self.color) if is_hover else self.color
        pygame.draw.rect(win, draw_color, (self.x, self.y, self.width, self.height), border_radius=20)
        font = pygame.font.SysFont(FONT_EMOJI, 50)
        text = font.render(self.label, True, CREAM)
        win.blit(text, (
            self.x + self.width//2 - text.get_width()//2,
            self.y + self.height//2 - text.get_height()//2
        ))

    def click(self, pos):
        x1, y1 = pos
        return self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height

# Tooltip label
hover_labels = {
    "Rock": "You chose Rock 👊",
    "Scissors": "You chose Scissors ✌️",
    "Paper": "You chose Paper 🖐"
}

# Tooltip renderer
def draw_hover_popup(win, btn, text):
    font = pygame.font.SysFont(FONT_EMOJI, 24)  # fixed here
    popup_text = font.render(text, True, (255, 255, 255))
    padding = 10
    box_w = popup_text.get_width() + padding * 2
    box_h = popup_text.get_height() + padding * 2

    popup_x = btn.x + btn.width // 2 - box_w // 2
    popup_y = btn.y - box_h - 10

    pygame.draw.rect(win, DARK, (popup_x, popup_y, box_w, box_h), border_radius=8)
    win.blit(popup_text, (popup_x + padding, popup_y + padding))

def redrawWindow(win, game, p, score):
    win.fill(CREAM)

    font = pygame.font.SysFont(FONT_UI, 36)
    score_text = font.render(f"Score: {score}", True, DARK)
    win.blit(score_text, (20, 20))

    if not game.connected():
        font = pygame.font.SysFont(FONT_UI, 72, bold=True)
        text = font.render("Waiting for Player...", True, EMERALD)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont(FONT_UI, 48, bold=True)
        win.blit(font.render("Your Move", True, EMERALD), (80, 200))
        win.blit(font.render("Opponent", True, EMERALD), (400, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)

        emoji_map = {"R": "👊", "P": "🖐", "S": "✌️"}
        font_emoji = pygame.font.SysFont(FONT_EMOJI, 60)

        if game.bothWent():
            text1 = font_emoji.render(emoji_map.get(move1[0].upper(), move1), True, DARK)
            text2 = font_emoji.render(emoji_map.get(move2[0].upper(), move2), True, DARK)
        else:
            text1 = font.render("Waiting...", True, DARK)
            text2 = font.render("Waiting...", True, DARK)
            if game.p1Went:
                text1 = font.render("Locked In", True, DARK)
            if game.p2Went:
                text2 = font.render("Locked In", True, DARK)
            if p == 0 and game.p1Went:
                text1 = font_emoji.render(emoji_map.get(move1[0].upper(), move1), True, DARK)
            if p == 1 and game.p2Went:
                text2 = font_emoji.render(emoji_map.get(move2[0].upper(), move2), True, DARK)

        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        mouse_pos = pygame.mouse.get_pos()
        for btn in btns:
            is_hover = btn.click(mouse_pos)
            btn.draw(win, is_hover)
            if is_hover and btn.text in hover_labels:
                draw_hover_popup(win, btn, hover_labels[btn.text])

    pygame.display.update()

btns = [
    Button("Rock",     50, 500, DARK, "👊"),
    Button("Scissors", 250, 500, EMERALD, "✌️"),
    Button("Paper",    450, 500, TEAL, "🖐")
]

def draw_popup_result(text_obj):
    popup_width = 400
    popup_height = 200
    popup_x = (width - popup_width) // 2
    popup_y = (height - popup_height) // 2
    border_radius = 20

    shadow_color = (220, 220, 220)
    pygame.draw.rect(win, shadow_color, (popup_x + 5, popup_y + 5, popup_width, popup_height), border_radius=border_radius)
    popup_color = (255, 255, 255)
    pygame.draw.rect(win, popup_color, (popup_x, popup_y, popup_width, popup_height), border_radius=border_radius)

    text_rect = text_obj.get_rect(center=(width // 2, height // 2))
    win.blit(text_obj, text_rect)
    pygame.display.update()
    pygame.time.delay(2000)

def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)

    score = 0

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.bothWent():
            redrawWindow(win, game, player, score)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't reset game")
                break

            font = pygame.font.SysFont(FONT_UI, 60, bold=True)
            winner = game.winner()

            if (winner == 1 and player == 1) or (winner == 0 and player == 0):
                score += 1
                result_text = font.render("You Won!", True, EMERALD)
            elif winner == -1:
                result_text = font.render("Tie Game!", True, DARK)
            else:
                result_text = font.render("You Lost...", True, (255, 70, 70))

            draw_popup_result(result_text)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0 and not game.p1Went:
                            n.send(btn.text)
                        elif player == 1 and not game.p2Went:
                            n.send(btn.text)

        redrawWindow(win, game, player, score)

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    btn_width = 300
    btn_height = 100
    btn_x = (width - btn_width) // 2
    btn_y = (height - btn_height) // 2
    default_color = EMERALD
    hover_color = (25, 180, 170)

    play_btn = Button("Play", btn_x, btn_y, default_color, "Click to Play!", width=btn_width, height=btn_height)

    while run:
        clock.tick(60)
        win.fill(CREAM)

        mouse_pos = pygame.mouse.get_pos()
        is_hover = play_btn.click(mouse_pos)
        current_color = hover_color if is_hover else default_color

        pygame.draw.rect(win, current_color, (play_btn.x, play_btn.y, play_btn.width, play_btn.height), border_radius=20)

        font = pygame.font.SysFont(FONT_UI, 48, bold=True)
        label = font.render("Click to Play!", True, CREAM)
        win.blit(label, (
            play_btn.x + play_btn.width // 2 - label.get_width() // 2,
            play_btn.y + play_btn.height // 2 - label.get_height() // 2
        ))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_hover:
                    run = False

    main()

while True:
    menu_screen()
