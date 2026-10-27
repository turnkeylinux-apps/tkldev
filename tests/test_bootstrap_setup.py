#!/usr/bin/env python3
"""Exercise the bootstrap setup block with isolated downloads and a file verifier."""
import hashlib
import io
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'overlay/usr/local/sbin/tkldev-setup'


class BootstrapSetupTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.downloads = self.root / 'downloads'
        self.downloads.mkdir()
        self.name = 'bootstrap-trixie-amd64'
        self.archive = self.downloads / (self.name + '.tar.gz')
        with tarfile.open(self.archive, 'w:gz') as tar:
            entry = tarfile.TarInfo('bin/bash')
            data = b'#!/bin/sh\n'
            entry.mode, entry.size = 0o755, len(data)
            tar.addfile(entry, io.BytesIO(data))
        self.archive.with_suffix('.gz.hash').write_text(hashlib.sha512(self.archive.read_bytes()).hexdigest())
        self.bootstrap = self.root / 'bootstraps/trixie-amd64'
        self.key = self.root / 'common/keys/tkl-trixie-images.asc'
        self.key.parent.mkdir(parents=True)
        self.key.write_text('public key fixture')
        self.verifier = self.root / 'verify'
        self.verifier.write_text('''#!/usr/bin/env python3
import hashlib, pathlib, sys
assert sys.argv[1] == '--force-gpg'
payload, checksum = map(pathlib.Path, sys.argv[2:])
assert payload.is_file() and checksum.is_file()
assert hashlib.sha512(payload.read_bytes()).hexdigest() == checksum.read_text()
''')
        self.verifier.chmod(0o755)

    def run_setup(self):
        # Execute the actual production block; only network transport and verifier
        # are fixtures. Cryptographic verification belongs to signature-verify.
        block = SCRIPT.read_text().split('if [[ -d "$BOOTSTRAP_PATH" ]]; then', 1)[1]
        shell = '''set -e
fatal() { echo "$*" >&2; exit 1; }
warning() { :; }
info() { :; }
gpg() {
    test "$1" = --import && test -f "$2"
}
wget() {
    echo download >> "$TEST_ROOT/download-calls"
    cp "$DOWNLOADS/$(basename "${@: -1}")" .
}
if [[ -d "$BOOTSTRAP_PATH" ]]; then''' + block
        env = dict(os.environ, TEST_ROOT=str(self.root), DOWNLOADS=str(self.downloads),
                   BOOTSTRAP_PATH=str(self.bootstrap), BOOTSTRAP_NAME=self.name,
                   BT_VERIFY=str(self.verifier), IMAGES='https://fixture.invalid/images',
                   FAB_PATH=str(self.root), CODENAME='trixie')
        return subprocess.run(['bash', '-c', shell], env=env, capture_output=True, text=True)

    def test_downloaded_archive_is_verified_then_extracted(self):
        result = self.run_setup()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.bootstrap / 'bin/bash').read_bytes(), b'#!/bin/sh\n')
        self.assertEqual((self.root / 'download-calls').read_text().splitlines(), ['download', 'download'])

    def test_existing_bootstrap_skips_download_and_verification(self):
        (self.bootstrap / 'bin').mkdir(parents=True)
        (self.bootstrap / 'bin/bash').write_text('existing bootstrap')
        self.verifier.unlink()
        result = self.run_setup()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.root / 'download-calls').exists())
        self.assertEqual((self.bootstrap / 'bin/bash').read_text(), 'existing bootstrap')

    def test_missing_release_key_does_not_extract(self):
        self.key.unlink()
        result = self.run_setup()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.bootstrap.exists())

    def test_failed_verification_does_not_extract(self):
        self.archive.with_suffix('.gz.hash').write_text('incorrect digest')
        result = self.run_setup()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.bootstrap.exists())


if __name__ == '__main__':
    unittest.main()
