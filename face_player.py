#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import pygame

SCRIPT_DIR          = os.path.dirname(os.path.abspath(__file__))
EXPRESSIONS_DIR     = os.path.join(SCRIPT_DIR, "expressions")
DEFAULT_EXPRESSION  = "blank"

FRAME_DELAY         = 80  # ms (12~15 FPS)

def load_expression_frames(path):
    frames = []
    for img in sorted(os.listdir(path)):
        if img.lower().endswith(".jpg"):
            full = os.path.join(path, img)
            frames.append(pygame.image.load(full).convert_alpha())
    return frames


def load_all_expressions():
    expressions = {}
    for name in sorted(os.listdir(EXPRESSIONS_DIR)):
        full_path = os.path.join(EXPRESSIONS_DIR, name)
        if os.path.isdir(full_path):
            frames = load_expression_frames(full_path)
            if frames:
                expressions[name] = frames
    return expressions


class ExpressionPlayer:
    def __init__(self, expressions, screen):
        self.expressions = expressions
        self.screen = screen

        self.current_name = DEFAULT_EXPRESSION
        self.current_frames = expressions[DEFAULT_EXPRESSION]
        self.index = 0
        self.last_change = pygame.time.get_ticks()

        self.queue = []

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_change >= FRAME_DELAY:
            self.index = (self.index + 1) % len(self.current_frames)
            self.last_change = now

        # Draw current frame
        img = self.current_frames[self.index]

        screen_rect = self.screen.get_rect()
        scaled = pygame.transform.smoothscale(
            img, 
            (screen_rect.width, screen_rect.height)
        )
        self.screen.blit(scaled, (0, 0))

        # Check queue when animation finishes
        if self.index == len(self.current_frames) - 1:
            self._check_queue()

    def _check_queue(self):
        if self.queue:
            next_expr = self.queue.pop(0)
            self.play(next_expr)
        else:
            if self.current_name != DEFAULT_EXPRESSION:
                self.play(DEFAULT_EXPRESSION)

    def play(self, name):
        if name not in self.expressions:
            print(f"[WARN] Expression '{name}' not found.")
            return

        self.current_name = name
        self.current_frames = self.expressions[name]
        self.index = 0
        self.last_change = pygame.time.get_ticks()

    def add_to_queue(self, name):
        self.queue.append(name)


def main():
    pygame.init()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()

    expressions = load_all_expressions()
    print(f"Expressions found: {list(expressions.keys())}")

    player = ExpressionPlayer(expressions, screen)

    SEQUENCE = ["blink", "happy", "angry", "sad", "sleepy", "blank"]

    for expr in SEQUENCE:
        player.add_to_queue(expr)

    running = True
    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        player.update()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
