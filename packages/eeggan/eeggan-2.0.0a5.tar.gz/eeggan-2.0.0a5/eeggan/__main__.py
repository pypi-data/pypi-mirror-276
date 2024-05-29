import argparse
import sys

from .autoencoder_training_main import main as autoencoder_training_main
from .gan_training_main import main as gan_training_main
from .generate_samples_main import main as generate_samples_main
from .visualize_main import main as visualize_main
from .vae_training_main import main as vae_training_main

def main():
    parser = argparse.ArgumentParser(description='EEG-GAN')
    parser.add_argument('command', help='Subcommand to run')
    args = parser.parse_args(sys.argv[1:2])

    if args.command == 'gan_training_main':
        gan_training_main(sys.argv[2:])
    else:
        print('Unrecognized command')
        #parser.print_help()
        sys.exit(1)