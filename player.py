import pygame

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.color = (0, 200, 255)
        self.vel_y = 0
        self.on_ground = False
        self.on_ladder = False
        self.speed = 3.5
        self.climb_speed = 2.5
    def move(self, keys, platforms, ladders):
        dx = 0
        dy = 0
        self.on_ground = False
        self.on_ladder = False

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed

        foot_rect = self.rect.copy()
        foot_rect.y += 41

        for ladder in ladders:
            if self.rect.colliderect(ladder) or foot_rect.colliderect(ladder):
                self.on_ladder = True
                break

        if self.on_ladder:
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                dy = -self.climb_speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                dy = self.climb_speed
            self.vel_y = 0
        else:
            self.vel_y += 0.5
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

        self.rect.y += dy
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.vel_y > 0:
                    self.rect.bottom = platform.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = platform.bottom
                    self.vel_y = 0

        self.rect.x += dx
        for platform in platforms:
            if self.rect.colliderect(platform):
                if dx > 0:
                    self.rect.right = platform.left
                elif dx < 0:
                    self.rect.left = platform.right

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)