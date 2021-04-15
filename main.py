# coding=utf-8
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os
import subprocess


def verify(version):
    global workdir

    # Checkout proper dash tag
    os.chdir('dash')

    ignore_dir = ['.git', '0.12.3.1', '0.12.0.56', '0.12.3', '.github', 'dash', 'gitian-builder']

    for d in ignore_dir:
        if d in version:
            return


    suffices = ['-linux', '-osx-unsigned', '-win-unsigned', '-win-signed', '-osx-signed']

    tag = version
    for s in suffices:
        if not s in tag: continue
        tag = 'v' + tag.replace(s, '')
    print('tag', tag)

    result = subprocess.call(['git', 'checkout', tag])
    assert result == 0

    os.chdir('../gitian-builder')

    print('\nVerifying v' + version + '\n')

    gitian_yml = ''

    if 'linux' in version:
        gitian_yml = "gitian-linux.yml"
    elif 'win-unsigned' in version:
        gitian_yml = "gitian-win.yml"
    elif 'osx-unsigned' in version:
        gitian_yml = "gitian-osx.yml"
    elif 'win-signed' in version:
        gitian_yml = 'gitian-win-signer.yml'
    elif 'osx-signed' in version:
        gitian_yml = 'gitian-osx-signer.yml'
    else:
        assert False

    result = subprocess.call(
        ['bin/gverify', '-v', '-d', '../', '-r', version, '../dash/contrib/gitian-descriptors/' + gitian_yml])
    assert result == 0
    # print('\nVerifying v'+args.version+' Windows\n')
    # subprocess.call(['bin/gverify', '-v', '-d', '../gitian.sigs/', '-r', args.version+'-win-unsigned', '../dash/contrib/gitian-descriptors/gitian-win.yml'])
    # print('\nVerifying v'+args.version+' MacOS\n')
    # subprocess.call(['bin/gverify', '-v', '-d', '../gitian.sigs/', '-r', args.version+'-osx-unsigned', '../dash/contrib/gitian-descriptors/gitian-osx.yml'])
    # print('\nVerifying v'+args.version+' Signed Windows\n')
    # subprocess.call(['bin/gverify', '-v', '-d', '../gitian.sigs/', '-r', args.version+'-win-signed', '../dash/contrib/gitian-descriptors/gitian-win-signer.yml'])
    # print('\nVerifying v'+args.version+' Signed MacOS\n')
    # subprocess.call(['bin/gverify', '-v', '-d', '../gitian.sigs/', '-r', args.version+'-osx-signed', '../dash/contrib/gitian-descriptors/gitian-osx-signer.yml'])


def main():
    list_subfolders_with_paths = [f.path for f in os.scandir(os.getcwd()) if f.is_dir()]

    versions = [x.split("/") for x in list_subfolders_with_paths]

    for version in versions:
        version.reverse()

    versions = [x[0] for x in versions]

    for version in versions:
        verify(version)
        os.chdir('../')


if __name__ == '__main__':
    main()

