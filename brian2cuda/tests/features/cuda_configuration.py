import brian2
import os
import shutil
import sys
import socket

from brian2.tests.features import (Configuration, DefaultConfiguration,
                                   run_feature_tests, run_single_feature_test)
from brian2.core.preferences import prefs

__all__ = ['CUDAStandaloneConfiguration']

class CUDAStandaloneConfiguration(Configuration):
    name = 'CUDA standalone'
    def before_run(self):
        brian2.set_device('cuda_standalone', build_on_run=False)
        if socket.gethostname() == 'elnath':
            if prefs['devices.cpp_standalone.extra_make_args_unix'] == ['-j12']:
                prefs['devices.cpp_standalone.extra_make_args_unix'] = ['-j24']
            prefs['codegen.cuda.extra_compile_args_nvcc'].remove('-arch=sm_35')
            prefs['codegen.cuda.extra_compile_args_nvcc'].extend(['-arch=sm_20'])

    def after_run(self):
        if os.path.exists('cuda_standalone'):
            shutil.rmtree('cuda_standalone')
        brian2.device.build(directory='cuda_standalone', compile=True, run=True,
                            with_output=False)

class CUDAStandaloneConfigurationOccupancyAPINoThreadfence(Configuration):
    name = 'CUDA standalone (using cuda occupancy API and reset eventspace with cudaMemset)'
    def before_run(self):
        brian2.set_device('cuda_standalone', build_on_run=False)
        prefs['devices.cuda_standalone.threshold_threadfence'] = False
        if socket.gethostname() == 'elnath':
            if prefs['devices.cpp_standalone.extra_make_args_unix'] == ['-j12']:
                prefs['devices.cpp_standalone.extra_make_args_unix'] = ['-j24']
            prefs['codegen.cuda.extra_compile_args_nvcc'].remove('-arch=sm_35')
            prefs['codegen.cuda.extra_compile_args_nvcc'].extend(['-arch=sm_20'])

    def after_run(self):
        if os.path.exists('cuda_standalone'):
            shutil.rmtree('cuda_standalone')
        brian2.device.build(directory='cuda_standalone', compile=True, run=True,
                            with_output=False)

class CUDAStandaloneConfigurationCurandDouble(Configuration):
    name = 'CUDA standalone (curand_float_type = double)'
    def before_run(self):
        brian2.set_device('cuda_standalone', build_on_run=False)
        prefs['devices.cuda_standalone.curand_float_type'] = 'double'
        if socket.gethostname() == 'elnath':
            if prefs['devices.cpp_standalone.extra_make_args_unix'] == ['-j12']:
                prefs['devices.cpp_standalone.extra_make_args_unix'] = ['-j24']
            prefs['codegen.cuda.extra_compile_args_nvcc'].remove('-arch=sm_35')
            prefs['codegen.cuda.extra_compile_args_nvcc'].extend(['-arch=sm_20'])

    def after_run(self):
        if os.path.exists('cuda_standalone'):
            shutil.rmtree('cuda_standalone')
        brian2.device.build(directory='cuda_standalone', compile=True, run=True,
                            with_output=False)

class CUDAStandaloneConfigurationUseCudaOccupancyAPI(Configuration):
    name = 'CUDA standalone (using cuda occupancy API)'
    def before_run(self):
        brian2.set_device('cuda_standalone', build_on_run=False)
        prefs['devices.cuda_standalone.calc_occupancy'] = True
        if socket.gethostname() == 'elnath':
            if prefs['devices.cpp_standalone.extra_make_args_unix'] == ['-j12']:
                prefs['devices.cpp_standalone.extra_make_args_unix'] = ['-j24']
            prefs['codegen.cuda.extra_compile_args_nvcc'].remove('-arch=sm_35')
            prefs['codegen.cuda.extra_compile_args_nvcc'].extend(['-arch=sm_20'])

    def after_run(self):
        if os.path.exists('cuda_standalone'):
            shutil.rmtree('cuda_standalone')
        brian2.device.build(directory='cuda_standalone', compile=True, run=True,
                            with_output=False)

class CUDAStandaloneConfigurationUseCudaOccupancyAPIProfileCPU(Configuration):
    name = "CUDA standalone (using cuda occupancy API and profile='blocking')"
    def before_run(self):
        brian2.set_device('cuda_standalone', build_on_run=False, profile='blocking')
        prefs['devices.cuda_standalone.calc_occupancy'] = True
        if socket.gethostname() == 'elnath':
            if prefs['devices.cpp_standalone.extra_make_args_unix'] == ['-j12']:
                prefs['devices.cpp_standalone.extra_make_args_unix'] = ['-j24']
            prefs['codegen.cuda.extra_compile_args_nvcc'].remove('-arch=sm_35')
            prefs['codegen.cuda.extra_compile_args_nvcc'].extend(['-arch=sm_20'])

    def after_run(self):
        if os.path.exists('cuda_standalone'):
            shutil.rmtree('cuda_standalone')
        brian2.device.build(directory='cuda_standalone', compile=True, run=True,
                            with_output=False)

class CUDAStandaloneConfiguration2BlocksPerSM(Configuration):
    name = 'CUDA standalone with 2 blocks per SM'
    def before_run(self):
        brian2.set_device('cuda_standalone', build_on_run=False)
        prefs['devices.cuda_standalone.SM_multiplier'] = 2
        if socket.gethostname() == 'elnath':
            if prefs['devices.cpp_standalone.extra_make_args_unix'] == ['-j12']:
                prefs['devices.cpp_standalone.extra_make_args_unix'] = ['-j24']
            prefs['codegen.cuda.extra_compile_args_nvcc'].remove('-arch=sm_35')
            prefs['codegen.cuda.extra_compile_args_nvcc'].extend(['-arch=sm_20'])

    def after_run(self):
        if os.path.exists('cuda_standalone'):
            shutil.rmtree('cuda_standalone')
        brian2.device.build(directory='cuda_standalone', compile=True, run=True,
                            with_output=False)

class CUDAStandaloneConfiguration2BlocksPerSMLaunchBounds(Configuration):
    name = 'CUDA standalone with 2 blocks per SM and __launch_bounds__'
    def before_run(self):
        brian2.set_device('cuda_standalone', build_on_run=False)
        prefs['devices.cuda_standalone.SM_multiplier'] = 2
        prefs['devices.cuda_standalone.launch_bounds'] = True
        if socket.gethostname() == 'elnath':
            if prefs['devices.cpp_standalone.extra_make_args_unix'] == ['-j12']:
                prefs['devices.cpp_standalone.extra_make_args_unix'] = ['-j24']
            prefs['codegen.cuda.extra_compile_args_nvcc'].remove('-arch=sm_35')
            prefs['codegen.cuda.extra_compile_args_nvcc'].extend(['-arch=sm_20'])

    def after_run(self):
        if os.path.exists('cuda_standalone'):
            shutil.rmtree('cuda_standalone')
        brian2.device.build(directory='cuda_standalone', compile=True, run=True,
                            with_output=False)

class CUDAStandaloneConfigurationSynLaunchBoundsOccup(Configuration):
    name = 'CUDA standalone (SYN __launch_bounds__, occup)'
    def before_run(self):
        brian2.set_device('cuda_standalone', build_on_run=False)
        prefs['devices.cuda_standalone.syn_launch_bounds'] = True
        prefs['devices.cuda_standalone.calc_occupancy'] = True
        if socket.gethostname() == 'elnath':
            if prefs['devices.cpp_standalone.extra_make_args_unix'] == ['-j12']:
                prefs['devices.cpp_standalone.extra_make_args_unix'] = ['-j24']
            prefs['codegen.cuda.extra_compile_args_nvcc'].remove('-arch=sm_35')
            prefs['codegen.cuda.extra_compile_args_nvcc'].extend(['-arch=sm_20'])

    def after_run(self):
        if os.path.exists('cuda_standalone'):
            shutil.rmtree('cuda_standalone')
        brian2.device.build(directory='cuda_standalone', compile=True, run=True,
                            with_output=False)

class CUDAStandaloneConfiguration2BlocksPerSMSynLaunchBoundsOccup(Configuration):
    name = 'CUDA standalone (2 bl/SM, SYN __launch_bounds__, occup)'
    def before_run(self):
        brian2.set_device('cuda_standalone', build_on_run=False)
        prefs['devices.cuda_standalone.SM_multiplier'] = 2
        prefs['devices.cuda_standalone.syn_launch_bounds'] = True
        prefs['devices.cuda_standalone.calc_occupancy'] = True
        if socket.gethostname() == 'elnath':
            if prefs['devices.cpp_standalone.extra_make_args_unix'] == ['-j12']:
                prefs['devices.cpp_standalone.extra_make_args_unix'] = ['-j24']
            prefs['codegen.cuda.extra_compile_args_nvcc'].remove('-arch=sm_35')
            prefs['codegen.cuda.extra_compile_args_nvcc'].extend(['-arch=sm_20'])

    def after_run(self):
        if os.path.exists('cuda_standalone'):
            shutil.rmtree('cuda_standalone')
        brian2.device.build(directory='cuda_standalone', compile=True, run=True,
                            with_output=False)

class CUDAStandaloneConfigurationProfileGPU(Configuration):
    name = 'CUDA standalone (profile=True)'
    def before_run(self):
        brian2.set_device('cuda_standalone', build_on_run=False, profile=True)
        prefs['devices.cuda_standalone.profile'] = True
        if socket.gethostname() == 'elnath':
            if prefs['devices.cpp_standalone.extra_make_args_unix'] == ['-j12']:
                prefs['devices.cpp_standalone.extra_make_args_unix'] = ['-j24']
            prefs['codegen.cuda.extra_compile_args_nvcc'].remove('-arch=sm_35')
            prefs['codegen.cuda.extra_compile_args_nvcc'].extend(['-arch=sm_20'])

    def after_run(self):
        if os.path.exists('cuda_standalone'):
            shutil.rmtree('cuda_standalone')
        brian2.device.build(directory='cuda_standalone', compile=True, run=True,
                            with_output=False)

class CUDAStandaloneConfigurationProfileCPU(Configuration):
    name = "CUDA standalone (profile='blocking')"
    def before_run(self):
        brian2.set_device('cuda_standalone', build_on_run=False, profile='blocking')
        if socket.gethostname() == 'elnath':
            if prefs['devices.cpp_standalone.extra_make_args_unix'] == ['-j12']:
                prefs['devices.cpp_standalone.extra_make_args_unix'] = ['-j24']
            prefs['codegen.cuda.extra_compile_args_nvcc'].remove('-arch=sm_35')
            prefs['codegen.cuda.extra_compile_args_nvcc'].extend(['-arch=sm_20'])

    def after_run(self):
        if os.path.exists('cuda_standalone'):
            shutil.rmtree('cuda_standalone')
        brian2.device.build(directory='cuda_standalone', compile=True, run=True,
                            with_output=False)

