import argparse
import sys

from .autoencoder_training_main import main as autoencoder_training_main
from .gan_training_main import main as gan_training_main
from .generate_samples_main import main as generate_samples_main
from .visualize_main import main as visualize_main
from .vae_training_main import main as vae_training_main

def main():
    command = args[1]
    args = sys.argv[2:]
    print(args)
    
    if command == 'gan_training_main':
        gan_training_main(args)
    else:
        print('Unrecognized command')
        #parser.print_help()
        sys.exit(1)