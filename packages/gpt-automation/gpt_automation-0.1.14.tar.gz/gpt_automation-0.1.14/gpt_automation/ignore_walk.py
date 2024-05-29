import logging
import os
import pathlib

from gpt_automation.ignore_file_parser import collect_patterns_from_ignore_files ,generate_pattern_pairs
from gpt_automation.utils.git_tools import find_git_root
from gpt_automation.filters import (
    should_ignore_by_ignore_files,
    filter_with_white_list,
    should_ignore_by_black_list,
    should_include_by_include_only_list,
)
from gpt_automation.utils.pattern_utils import compile_patterns



def traverse_with_filters(path, blacklist, whitelist, profile_names=None, ignore_filenames=['.gitignore', ".gptignore"],
                          include_only_filenames=[".gptincludeonly"]):
    blacklist_patterns = compile_patterns(blacklist)
    whitelist_patterns = compile_patterns(whitelist) if whitelist else None
    include_only_patterns = compile_patterns(include_only_filenames) if include_only_filenames else None

    visited_dirs = set()
    ignore_patterns_stack = initialize_ignore_patterns_stack(path, ignore_filenames, profile_names)
    include_only_patterns_stack = initialize_ignore_patterns_stack(path, include_only_filenames, profile_names)

    def walk(directory_path, current_depth):
        if directory_path in visited_dirs:
            return
        visited_dirs.add(directory_path)

        local_ignore_patterns = collect_patterns_from_ignore_files(directory_path, ignore_filenames, profile_names)
        ignore_patterns_stack.append(local_ignore_patterns if local_ignore_patterns else None)

        local_include_only_patterns = collect_patterns_from_ignore_files(directory_path, include_only_filenames,
                                                                         profile_names)
        include_only_patterns_stack.append(local_include_only_patterns if local_include_only_patterns
                                           else generate_pattern_pairs(directory_path, ["*"]))

        entries = list(os.scandir(directory_path))
        subdirectories, file_names = [], []
        for entry in entries:
            if entry.is_dir(follow_symlinks=False):
                subdirectories.append(entry.name)
            elif entry.is_file():
                file_names.append(entry.name)

        filtered_filenames = [filename for filename in file_names if
                              not should_ignore_by_ignore_files(os.path.join(directory_path, filename),
                                                                ignore_patterns_stack) and
                              not should_ignore_by_black_list(os.path.join(directory_path, filename),
                                                              blacklist_patterns)]

        filtered_filenames = filter_with_white_list(filtered_filenames, whitelist_patterns)

        filtered_filenames = [filename for filename in filtered_filenames if
                              should_include_by_include_only_list(os.path.join(directory_path, filename),
                                                                  include_only_patterns_stack)]

        filtered_subdirectories = [subdir for subdir in subdirectories if
                                   not should_ignore_by_ignore_files(os.path.join(directory_path, subdir + "/"),
                                                                     ignore_patterns_stack) and
                                   not should_ignore_by_black_list(os.path.join(directory_path, subdir + "/"),
                                                                   blacklist_patterns)]

        filtered_subdirectories_yield = [subdir for subdir in filtered_subdirectories if
                                         should_include_by_include_only_list(os.path.join(directory_path, subdir + "/"),
                                                                             include_only_patterns_stack)]

        yield directory_path, filtered_subdirectories_yield[:], filtered_filenames[:]

        for subdir in filtered_subdirectories_yield:
            full_subdir_path = os.path.join(directory_path, subdir)
            if not should_ignore_by_ignore_files(full_subdir_path, ignore_patterns_stack) and \
                    not should_ignore_by_black_list(full_subdir_path, blacklist_patterns):
                yield from walk(full_subdir_path, current_depth + 1)

        ignore_patterns_stack.pop()
        include_only_patterns_stack.pop()

    return walk(path, 0)


def initialize_ignore_patterns_stack(start_path, ignore_filenames, profile_names):
    git_root_path = find_git_root(start_path)
    patterns_stack = []
    if git_root_path:
        relative_path = os.path.relpath(start_path, git_root_path)
        current_path = git_root_path
        for part in pathlib.Path(relative_path).parts:
            current_path = os.path.join(current_path, part)
            pattern_pairs = collect_patterns_from_ignore_files(current_path, ignore_filenames, profile_names)
            patterns_stack.append(pattern_pairs if pattern_pairs else [])
    else:
        patterns_stack.append([])
    return patterns_stack