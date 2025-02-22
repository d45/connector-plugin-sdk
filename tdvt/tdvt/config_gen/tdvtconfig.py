""" Test result and configuration related classes. """

import json
import re

from ..resources import *
from .test_config import TestConfig, RunTimeTestConfig

class TdvtInvocation(object):
    """Track how items were tested. This captures how tdvt was invoked."""
    def __init__(self, from_args=None, from_json=None, test_config: TestConfig=None):
        self.tested_sql = False
        self.tested_tuples = True
        self.log_dir = ''
        self.output_dir = ''
        self.timeout_seconds = 60 * 60
        self.logical = False
        self.config_file = ''
        self.suite_name = ''
        self.d_override = ''
        self.verbose = False
        self.command_line = ''
        self.noheader = False
        self.thread_count = 6
        self.leave_temp_dir = False
        self.run_as_perf = False
        self.thread_id = -1
        self.tds = ''
        self.tested_run_time_config = None

        if from_args:
            self.init_from_args(from_args)
        if from_json:
            self.init_from_json(from_json)
        if test_config:
            self.set_run_time_test_config(test_config.run_time_config)
            self.suite_name = test_config.dsname

    def set_run_time_test_config(self, rtt: RunTimeTestConfig):
            self.timeout_seconds = rtt.timeout_seconds
            self.d_override = rtt.d_override
            self.run_as_perf = rtt.run_as_perf
            self.tested_run_time_config = rtt

    def init_from_args(self, args):
        if args.compare_sql: 
            self.tested_sql = args.compare_sql 
        if args.nocompare_tuples:
            self.tested_tuples = False
        if args.noclean:
            self.leave_temp_dir = True
        if args.verbose:
            self.verbose = args.verbose

    def init_from_json(self, json):
        self.tested_sql = json['tested_sql']
        self.tested_tuples = json['tested_tuples']
        self.output_dir = json['output_dir']
        self.logical = json['logical']
        self.config_file = json['config_file']
        self.suite_name = json['suite_name']
        self.d_override = json['d_override']
        self.verbose = json['verbose']
        self.tds = json['tds']
        self.noheader = json['noheader']
        self.thread_count = json['thread_count']

    def __str__(self):
        return "suite [{}]: tested sql [{}]: tested tuples [{}]: output dir [{}]: logical [{}]: config file [{}]: override [{}]: tds [{}]: thread [{}]".format(self.suite_name, self.tested_sql, self.tested_tuples, self.output_dir, self.logical, self.config_file, self.d_override, self.tds, self.thread_count)

    def __json__(self):
        return {
        'tested_sql' : self.tested_sql, 
        'tested_tuples' : self.tested_tuples, 
        'output_dir' : self.output_dir, 
        'logical' : self.logical, 
        'config_file' : self.config_file, 
        'suite_name' : self.suite_name, 
        'd_override' : self.d_override, 
        'verbose' : self.verbose, 
        'tds' : self.tds, 
        'noheader' : self.noheader, 
        'thread_count' : self.thread_count }

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

