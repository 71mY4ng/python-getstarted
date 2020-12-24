#!/usr/bin/env python

# [about foobar](https://stackoverflow.com/questions/1523427/what-is-the-common-header-format-of-python-files)

import os, sys, argparse
from git import Repo


repo_url = "https://github.com/71mY4ng/articles.git"
rw_dir = "/home/timyang/Downloads/git-download/"
repository_name = "articles"
to_path = os.path.join(rw_dir, repository_name)

repo = Repo(to_path)

if repo.bare:
    assert not repo_url is None
    repo.clone(url=repo_url, to_path=to_path)

assert not repo.bare

# tar repository file
def tar_repo():
    with open(os.path.join(rw_dir, 'repo.tar'), 'wb') as fp:
        repo.archive(fp)


def get_diff_list(pre_tag_name, after_tag_name):
    pre_tag = repo.tags[pre_tag_name].commit
    after_tag = repo.tags[after_tag_name].commit

    tag_diffs = after_tag.diff(pre_tag)

    for diff in tag_diffs:
        print(diff.change_type, ": ", diff.a_path)

def get_tree(commit):
    tree = repo.tree(repo.commit(commit))

    for entry in tree:
        print(entry)

def ptree(args):
    get_tree(args.ref_commit)

def dl(args):
    get_diff_list(args.pre_tag, args.after_tag)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='My Git Patch Tool')

    parser.add_argument('--home', dest='home', help='home directory to save repo')
    parser.add_argument('--url', dest='url')

    subparsers = parser.add_subparsers(help='sub-command help')
    parser_diff_list = subparsers.add_parser('diff_list', aliases=['dl'],
            help='print diff file list')

    parser_diff_list.add_argument('--pre_tag', dest='pre_tag', required=True)
    parser_diff_list.add_argument('--after_tag', dest='after_tag', required=True)
    parser_diff_list.set_defaults(func=dl)

    parser_print_tree = subparsers.add_parser('print_tree', aliases=['ptree'],
            help='print commit file tree')
    parser_print_tree.add_argument('--ref', dest='ref_commit')
    parser_print_tree.set_defaults(func=ptree)
    
    args = parser.parse_args()
    args.func(args)
