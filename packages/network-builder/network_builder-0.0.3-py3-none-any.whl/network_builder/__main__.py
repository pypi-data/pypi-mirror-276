from .network_builder import main
import argparse

if __name__ == '__main__':
    argparse = argparse.ArgumentParser()
    argparse.add_argument('--config_file', help='Path to the config file', required=True)
    args = argparse.parse_args()

    main(args.config_file)