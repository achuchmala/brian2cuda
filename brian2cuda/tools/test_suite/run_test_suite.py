"""
Run brian2 test suite on standalone architectures
"""

import argparse
import utils

parser = argparse.ArgumentParser(description='Run the brian2 testsuite on GPU.')

parser.add_argument('--no-long-tests', action='store_false',
                    help="Set to not run long tests. By default they are run.")

parser.add_argument('--skip-not-implemented', action='store_true',
                    help="Weather to reset prefs between tests or not.")

parser.add_argument('--test-parallel', nargs='?', const=None, default=[],
                    help="Weather to use multiple cores for testing. Optionally the "
                         "targets for which mpi should be used, can be passed as "
                         "arguments. If none are passed, all are run in parallel.")

parser.add_argument('--notify-slack', action='store_true',
                    help="Send progress reports through Slack via ClusterBot "
                          "(if installed)")

parser.add_argument('-v', '--verbosity', action='count', default=None,
                    help="Increase pytest verbosity.")

args = utils.parse_arguments(parser)

bot = None
if args.notify_slack:
    try:
        from clusterbot import ClusterBot
        bot = ClusterBot()
    except ImportError:
        print("WARNING: clusterbot not installed. Can't notify slack.")
        pass

buffer = utils.PrintBuffer(clusterbot=bot)

import os, sys
from StringIO import StringIO

import brian2
from brian2 import test, prefs
import brian2cuda

all_prefs_combinations, print_lines = utils.set_preferences(args, prefs,
                                                            return_lines=True)
buffer.add(print_lines)
buffer.print_all()

extra_test_dirs = os.path.join(os.path.abspath(os.path.dirname(brian2cuda.__file__)), 'tests')

if args.test_parallel is None:
    args.test_parallel = args.targets

stored_prefs = prefs.as_file

# Only the conftest.py located in the `rootdir` of a pytest run is loaded and used for
# all tests (else each conftest.py applies only to the tests in its own directory).
# To use brian2's conftest.py also for our brian2cuda tests, we set `rootdir` to the
# `brian2` directory, where `brian2/conftest.py` is located.
# XXX: If we ever want to have an own conftest.py, we need to pass `--confcutdir` here
# (which overwrites the `--confcutdir` default option in `make_argv`), such that the
# search of conftest.py files does not stop at `brian2` but at a higher directory, which
# should include the conftest.py we want to load.
additional_args = ['--rootdir={}'.format(os.path.dirname(brian2.__file__))]

if args.verbosity is not None:
   additional_args += ['-{}'.format(args.verbosity * 'v')]

all_successes = []
for target in args.targets:

    test_in_parallel = []
    if target in args.test_parallel:
        test_in_parallel = [target]

    if target == 'cuda_standalone':
        preference_dictionaries = all_prefs_combinations
    else:
        preference_dictionaries = [None]

    successes = []
    for n, prefs_dict in enumerate(preference_dictionaries):

        # reset prefs to stored prefs
        prefs.read_preference_file(StringIO(stored_prefs))

        if prefs_dict is not None:
            buffer.add("{}. RUN: test suite on CUDA_STANDALONE with prefs: "
                       "".format(n + 1))
            # print and set preferences
            print_lines = utils.print_single_prefs(prefs_dict, set_prefs=prefs,
                                                   return_lines=True)
            buffer.add(print_lines)
            buffer.print_all()

        success = test(codegen_targets=[],
                       long_tests=args.no_long_tests,
                       test_codegen_independent=False,
                       test_standalone=target,
                       reset_preferences=False,
                       fail_for_not_implemented=not args.skip_not_implemented,
                       test_in_parallel=test_in_parallel,
                       extra_test_dirs=extra_test_dirs,
                       float_dtype=None,
                       additional_args=additional_args)

        successes.append(success)

    buffer.add("\nTARGET: {}".format(target.upper()))
    all_success, print_lines = utils.check_success(successes,
                                                   all_prefs_combinations,
                                                   return_lines=True)
    all_successes.append(all_success)
    buffer.add(print_lines)
    buffer.print_all()

if len(args.targets) > 1:
    buffer.add("\nFINISHED ALL TARGETS")

    if all(all_successes):
        buffer.add("\nALL TARGETS PASSED")
        buffer.print_all()
    else:
        buffer.add("\n{}/{} TARGETS FAILED:".format(
            sum(all_successes) - len(all_successes), len(all_successes)))
        for n, target in enumerate(args.targets):
            if not all_successes[n]:
                buffer.add("\t{} failed.".format(target))
        buffer.print_all()
        sys.exit(1)

elif not all_successes[0]:
    sys.exit(1)
