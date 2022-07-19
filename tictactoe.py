import pygame
pygame.font.init()

NODE_SIZE = int(150)

WIDTH = 3*NODE_SIZE+NODE_SIZE//5
HEIGHT = 3*NODE_SIZE+NODE_SIZE//5
pygame.display.set_caption("tictactoe")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 60
TEXT_FONT = pygame.font.SysFont('comicsans', int(0.4*NODE_SIZE))
TEXT_FONT_2 = pygame.font.SysFont('comicsans', int(0.2*NODE_SIZE))
PIECE_FONT = pygame.font.SysFont('comicsans', int(0.6*NODE_SIZE))

END_SCREEN = pygame.Rect(NODE_SIZE//2, NODE_SIZE//2, 2*NODE_SIZE+NODE_SIZE//5, 2*NODE_SIZE+NODE_SIZE//5)

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0 , 0)
GREEN = (0, 255, 0)
RED = (255, 0 , 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
GREY = (169, 169, 169)
DARK_BROWN = (179,133,100)
LIGHT_BROWN = (210,179,140)

class Node():

    def __init__(self, x, y, piece = None):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x*(NODE_SIZE+NODE_SIZE//10), y*(NODE_SIZE+NODE_SIZE//10), NODE_SIZE, NODE_SIZE)
        self.piece = piece
        self.clicked = False
        self.ghost = False

    def highlight(self):
        self.ghost = True

    def unhighlight(self):
        self.ghost = False

    def draw(self, turn):
        piece_text = PIECE_FONT.render("", 1, WHITE)

        action = None

        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos) and self.piece == None:

            action = 'hover'

            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = 'clicked'

            elif pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        if self.ghost:
            piece_text = PIECE_FONT.render(str(turn), 1, GREY)

        if self.piece == 'X':
            piece_text = PIECE_FONT.render(str(self.piece), 1, RED)
        elif self.piece == 'O':
            piece_text = PIECE_FONT.render(str(self.piece), 1, BLUE)

        screen.blit(piece_text, (self.rect.x + (self.rect.width - piece_text.get_width())//2, self.rect.y + (self.rect.width - piece_text.get_height())//2))

        return action

class Game():

    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.board = self.new_board()
        self.turn = 'X'
        self.winner = None

    def new_board(self):
        return [[Node(x, y) for x in range(3)] for y in range(3)]

    def next_turn(self):
        self.turn = 'O' if self.turn == 'X' else 'X'

    def show_place_location(self, node):
        node.highlight()

        for y in self.board:
            for x in y:
                if x == node:
                    continue
                x.unhighlight()

    def place_piece(self, node):
        if node.piece == None:
            node.piece = self.turn

        self.winner = self.check_tictactoe(node)

        self.next_turn()

    def check_next_node(self, node, x1, y1):
        # out of bounds check
        if node.y+y1 < 0 or node.y+y1 > 2 or node.x+x1 < 0 or node.x+x1 > 2:
            return False
        next_node = self.board[node.y+y1][node.x+x1]
        if next_node.piece == self.turn:
            return True
        return False

    def check_tictactoe(self, node):
        horizontal = 1
        vertical = 1
        diagonal_1 = 1
        diagonal_2 = 1
        for c in {(1,0),(-1,0)}:
            for n in range(1,3):
                if self.check_next_node(node,c[0]*n,c[1]*n):
                    horizontal += 1
        for c in {(0,1),(0,-1)}:
            for n in range(1,3):
                if self.check_next_node(node,c[0]*n,c[1]*n):
                    vertical += 1
        for c in {(-1,1),(1,-1)}:
            for n in range(1,3):
                if self.check_next_node(node,c[0]*n,c[1]*n):
                    diagonal_1 += 1
        for c in {(1,1),(-1,-1)}:
            for n in range(1,3):
                if self.check_next_node(node,c[0]*n,c[1]*n):
                    diagonal_2 += 1
        if any(v == 3 for v in (horizontal, vertical, diagonal_1, diagonal_2)):
            return self.turn

        tie = 0
        for y in self.board:
            for x in y:
                if x.piece == None:
                    tie += 1
        if tie == 0:
            return 'TIE'

        return None

    def draw(self):
        # draw board background
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLACK, (NODE_SIZE, 0, 10, 3*NODE_SIZE+NODE_SIZE//5))
        pygame.draw.rect(screen, BLACK, (2*NODE_SIZE+NODE_SIZE//10, 0, 10, 3*NODE_SIZE+NODE_SIZE//5))
        pygame.draw.rect(screen, BLACK, (0, NODE_SIZE, 3*NODE_SIZE+NODE_SIZE//5, 10))
        pygame.draw.rect(screen, BLACK, (0, 2*NODE_SIZE+NODE_SIZE//10, 3*NODE_SIZE+NODE_SIZE//5, 10))

        # draw pieces
        for y in self.board:
            for x in y:
                action = x.draw(self.turn)
                if action == 'hover' and not self.winner:
                    self.show_place_location(x)
                elif action == 'clicked' and not self.winner:
                    self.place_piece(x)

        # winner screen
        if self.winner:
            pygame.draw.rect(screen, WHITE, END_SCREEN)
            pygame.draw.rect(screen, BLACK, END_SCREEN, 5)
            end_text = TEXT_FONT.render(str(self.winner)+" WON!", 1, BLACK)
            if self.winner == 'TIE':
                end_text = TEXT_FONT.render(str(self.winner)+"!", 1, BLACK)
            screen.blit(end_text, (END_SCREEN.x+(END_SCREEN.width - end_text.get_width())//2, END_SCREEN.y+END_SCREEN.height//10))
            end_text = TEXT_FONT_2.render("Press 'r' to", 1, BLACK)
            screen.blit(end_text, (END_SCREEN.x+(END_SCREEN.width - end_text.get_width())//2, END_SCREEN.y+END_SCREEN.height//2))
            end_text = TEXT_FONT_2.render("reset game.", 1, BLACK)
            screen.blit(end_text, (END_SCREEN.x+(END_SCREEN.width - end_text.get_width())//2, END_SCREEN.y+END_SCREEN.height//1.6))

def main():

    tictactoe = Game()
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    tictactoe.reset_game()
        tictactoe.draw()

        pygame.display.update()

if __name__ == '__main__':
    main()
