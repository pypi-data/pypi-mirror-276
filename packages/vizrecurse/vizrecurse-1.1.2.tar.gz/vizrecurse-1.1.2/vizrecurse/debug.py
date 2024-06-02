"""Convenience tools for development"""
import inspect

def dump_frame_info(frame) -> None:
    print('\n\n')
    print(f"frame_addr: {hex(id(frame))}")
    print(f"frame: {repr(frame)}")
    print(f"frame.f_locals {frame.f_locals}", end='\n')
    print(f"dir(frame) {dir(frame)}", end='\n')
    print(f"frame.f_code.co_name {frame.f_code.co_name}", end='\n')
    print(f"inspect.getframeinfo(frame): {inspect.getframeinfo(frame)}")
