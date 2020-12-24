import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='My Git Patch Tool')
    parser.add_argument('--home', dest='home', help='home directory to save repo')
    parser.add_argument('--url', dest='url')
    parser.add_argument('--pre_tag', dest='pre_tag')
    parser.add_argument('--after_tag', dest='after_tag')
    
    args = parser.parse_args()
    print(args.home)
