import math
import pygame
from pygame import Color, gfxdraw


WIDTH, HEIGHT = 600, 600
ROWS, COLS = 6,6
SQUARE_SIZE = WIDTH/COLS

WHITE = (235, 235, 220)               
BLACK = (51, 51, 51)
RED = (178, 34, 34)
BLUE = (25, 25, 185)
MOVABLE_PIECE = (0, 200, 0, 100)
SELECTED_PIECE = (255, 255, 0, 50)
VALID_MOVE = Color(155, 215, 255, 100)
GOLD = Color(255, 215, 0)
LIME_GREEN = Color(124, 252, 0)
AMBER = Color(255, 165, 0)


screen = pygame.display.set_mode((WIDTH, HEIGHT))


def draw_piece(x, y, color, is_king=False):
    # Draw piece with anti-aliased circle and 3D effect
    radius = int(SQUARE_SIZE // 3)
    
    # Shadow
    shadow_offset = 3
    pygame.gfxdraw.filled_circle(screen, x + shadow_offset, y + shadow_offset, radius, Color(0, 0, 0, 100))
    
    # Main piece body
    pygame.gfxdraw.filled_circle(screen, x, y, radius, color)
    pygame.gfxdraw.aacircle(screen, x, y, radius, Color(0, 0, 0))
    
    # Highlight (for 3D effect)
    highlight_radius = radius - 3
    highlight_offset = -2
    pygame.gfxdraw.filled_circle(screen, x + highlight_offset, y + highlight_offset, 
                                highlight_radius, Color(color.r + 50, color.g + 50, color.b + 50, 150))
    
    # King crown
    if is_king:
        points = []
        for i in range(5):
            angle = math.pi / 2 + i * 2 * math.pi / 5
            inner_x = x + int(radius * 0.5 * math.cos(angle))
            inner_y = y + int(radius * 0.5 * math.sin(angle))
            points.append((inner_x, inner_y))
            
            angle += math.pi / 5
            outer_x = x + int(radius * 0.8 * math.cos(angle))
            outer_y = y + int(radius * 0.8 * math.sin(angle))
            points.append((outer_x, outer_y))
        
        pygame.gfxdraw.filled_polygon(screen, points, GOLD)
        pygame.gfxdraw.aapolygon(screen, points, Color(0, 0, 0))



draw_piece(1,2, RED, True)