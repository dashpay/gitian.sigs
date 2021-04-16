import os
import subprocess


def verify(version):
    global workdir

    # Checkout proper dash tag
    os.chdir('dash')

    ignore_dir = ['.git', '.github', 'dash', 'gitian-builder', 'archive', 'gitian-keys']

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
