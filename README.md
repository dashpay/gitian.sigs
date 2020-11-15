# gitian.sigs
This repository is for deterministic build results for Dash releases.

See the [release process](https://github.com/dashpay/dash/blob/master/doc/release-process.md)
in the Dash repository for how to
deterministically build binaries and then pgp-sign them.

[Instructions for setting up a virtual machine](https://github.com/dashpay/dash/blob/master/doc/gitian-building.md) in which you can
gitian build as well as [public keys of developers and active contributors](https://github.com/dashpay/dash/tree/master/contrib/gitian-keys) can also be found there.

You can verify PGP signatures produced by a specific author (e.g. with a nickname `some_food`)
for a specific version (e.g. 0.9.9.9) via a simple bash script like this:
``` bash
export VERSION=0.9.9.9 && export PR_AUTHOR=some_food \
  && gpg --status-fd 1 --verify-files $VERSION-{osx-*,win-*,linux}/$PR_AUTHOR/*.sig 2>/dev/null | grep -e GOODSIG \
  && gpg --status-fd 1 --verify-files $VERSION-{osx-*,win-*,linux}/$PR_AUTHOR/*.sig 2>/dev/null | grep -e BADSIG -B4 | grep -e BADSIG -e FILE_START
```

This should produce a few lines like
```
[GNUPG:] GOODSIG 9999999999999999 some_food <some_food@some_plate.org>
```
or something like
```
[GNUPG:] FILE_START 1 0.9.9.9-win-signed/some_food/dash-win-signer-build.assert.sig
[GNUPG:] BADSIG 9999999999999999 some_food <some_food@some_plate.org>
```
if there is a bad signature.
