#!/bin/python3

import sys

pptt = {}
struct = {}


def print_struct():
    if struct['type']   == 'socket':
        struct['show'] = 'socket:       '
    elif struct['type'] == 'cluster':
        struct['show'] = '  cluster:    '
    elif struct['type'] == 'core':
        struct['show'] = '    core:     '
    elif struct['type'] == 'cache':
        struct['show'] = '      cache:  '
    elif struct['type'] == 'thread':
        struct['show'] = '      thread: '

    print(f"{struct['show']} offset: {struct['address']}", end='')

    if 'parent' in struct:
        print(f" parent: {struct['parent']}", end='')

    if 'cpuid' in struct and struct['type'] in ['core', 'thread']:
        print(f" cpuId: {struct['cpuid']}", end='')

    if 'l1i' in struct:
        print(f" L1i: {struct['l1i']}", end='')
        print(f" L1d: {struct['l1d']}", end='')

    if struct['type'] == 'cache':
        if 'cacheid' in struct:
            print(f" cacheId: {struct['cacheid']}", end='')
        print(f" size: {struct['size']}", end='')
        if struct['nextcache'] != '0x0':
            print(f" next: {struct['nextcache']}", end='')

    print(' ')


with open(sys.argv[1], encoding='utf-8') as log:

    start_parsing = False

    while True:
        line = log.readline()

        if line.startswith('PPTT'):
            start_parsing = True
        elif line.startswith('-smp'):
            print(line.strip())
        elif line.startswith('Table Statistics'):
            break
        # empty
        elif line.strip() == "":
            continue
        if not start_parsing:
            continue;

        # parsing starts

        try:
            value = line.split(':')[1].strip()
        except IndexError:
            break

        if '* Structure Offset *' in line:
            if 'type' in struct:
                print_struct()
            struct = {}
            struct['address'] = value
        elif 'Flags' in line:
            struct['flags'] = value
            if struct['flags'] == '0x11':
                struct['type'] = 'socket'
            elif struct['flags'] == '0x10':
                struct['type'] = 'cluster'
            elif struct['flags'] == '0x1E':
                struct['type'] = 'thread'
            elif struct['flags'] == '0x7F':
                struct['type'] = 'cache'
            elif struct['flags'] == '0xFF':
                struct['type'] = 'cache'
        elif 'Parent' in line:
            struct['parent'] = value
        elif 'Parent' in line:
            struct['parent'] = value
        elif 'Private resources [0]' in line:
            struct['l1i'] = value
            struct['type'] = 'core'
        elif 'Private resources [1]' in line:
            struct['l1d'] = value
        elif 'Next Level of Cache' in line:
            struct['nextcache'] = value
        elif 'Cache ID' in line:
            struct['cacheid'] = value
        elif 'Size' in line:
            struct['size'] = value
        elif 'ACPI Processor ID' in line:
            struct['cpuid'] = value

print_struct()
