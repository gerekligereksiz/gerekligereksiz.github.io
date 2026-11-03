#!/usr/bin/env python3
import argparse
import os
from PIL import Image

def main():
    parser = argparse.ArgumentParser(description='Crop image from edges')
    parser.add_argument('input', help='Input image path')
    parser.add_argument('--top', type=int, default=0, help='Crop from top')
    parser.add_argument('--bottom', type=int, default=0, help='Crop from bottom')
    parser.add_argument('--left', type=int, default=0, help='Crop from left')
    parser.add_argument('--right', type=int, default=0, help='Crop from right')
    parser.add_argument('--output', '-o', help='Output image path (default: overwrite input)')
    
    args = parser.parse_args()
    
    if args.top == 0 and args.bottom == 0 and args.left == 0 and args.right == 0:
        parser.error('At least one of --top, --bottom, --left, --right must be specified')
    
    if not os.path.exists(args.input):
        print(f'Error: {args.input} does not exist')
        exit(1)
    
    im = Image.open(args.input)
    w, h = im.size
    
    left = args.left
    top = args.top
    right = w - args.right
    bottom = h - args.bottom
    
    if left < 0 or top < 0 or right > w or bottom > h or left >= right or top >= bottom:
        print('Error: Invalid crop values')
        exit(1)
    
    out = im.crop((left, top, right, bottom))
    output_path = args.output if args.output else args.input
    out.save(output_path)
    print(f'{out.size[0]}x{out.size[1]}')

if __name__ == '__main__':
    main()
