import random

def generate_unique_color(colors):
  while True:
    color = "#%06x"%random.randint(0, 0xFFFFFF)
    if color not in colors: return color
  
