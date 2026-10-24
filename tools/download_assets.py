#!/usr/bin/env python3
"""Download fixed Release parts and reconstruct the unchanged archive."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import urllib.request


def file_sha(path):
    digest = hashlib.sha256()
    with path.open('rb') as source:
        while block := source.read(4 * 1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('downloads/onedc-assets.tar.gz'))
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / 'assets/release_manifest.json').read_text())
    if manifest.get('status') != 'complete':
        raise SystemExit('Release transfer is not yet marked complete. Read verification/DELIVERY_STATUS.json.')
    expected = json.loads((root / 'assets/archive_manifest.json').read_text())
    output = args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        digest = file_sha(output)
        if output.stat().st_size == expected['bytes'] and digest == expected['sha256']:
            print('Existing archive verified.')
            return
        raise SystemExit('Output exists with a different hash; choose a new output path.')
    partial = output.with_name(output.name + '.partial')
    checkpoint = partial.with_name(partial.name + '.json')
    completed = 0
    if partial.exists() and checkpoint.exists():
        state = json.loads(checkpoint.read_text())
        if state['archive_sha256'] != expected['sha256']:
            raise SystemExit('Resume checkpoint belongs to another archive.')
        completed = state['completed_parts']
        expected_offset = sum(p['bytes'] for p in manifest['parts'][:completed])
        if partial.stat().st_size < expected_offset:
            raise SystemExit('Partial file is shorter than its checkpoint.')
        with partial.open('r+b') as f:
            f.truncate(expected_offset)
            offset = 0
            for part in manifest['parts'][:completed]:
                h = hashlib.sha256()
                remaining = part['bytes']
                while remaining:
                    block = f.read(min(4 * 1024 * 1024, remaining))
                    if not block:
                        raise SystemExit('Truncated completed part.')
                    h.update(block)
                    remaining -= len(block)
                if h.hexdigest() != part['sha256']:
                    raise SystemExit('A completed part no longer matches its hash.')
                offset += part['bytes']
    elif partial.exists() or checkpoint.exists():
        raise SystemExit('Incomplete resume state; choose a new output path or inspect the partial file.')
    else:
        checkpoint.write_text(json.dumps({'archive_sha256': expected['sha256'], 'completed_parts': 0}))
    with partial.open('ab') as dest:
        for index, part in enumerate(manifest['parts'][completed:], start=completed):
            start = dest.tell()
            h = hashlib.sha256()
            total = 0
            try:
                request = urllib.request.Request(part['url'], headers={'User-Agent': 'OneDC-asset-recovery'})
                with urllib.request.urlopen(request, timeout=60) as response:
                    while block := response.read(4 * 1024 * 1024):
                        total += len(block)
                        if total > part['bytes']:
                            raise ValueError('Response exceeds the fixed part size.')
                        h.update(block)
                        dest.write(block)
                if total != part['bytes'] or h.hexdigest() != part['sha256']:
                    raise ValueError('Part size or SHA256 mismatch.')
            except BaseException:
                dest.truncate(start)
                raise
            dest.flush()
            os.fsync(dest.fileno())
            temporary = checkpoint.with_name(checkpoint.name + '.tmp')
            temporary.write_text(json.dumps({'archive_sha256': expected['sha256'], 'completed_parts': index + 1}))
            temporary.replace(checkpoint)
            print(f"Verified part {index + 1}/{len(manifest['parts'])}", flush=True)
    digest = file_sha(partial)
    if partial.stat().st_size != expected['bytes'] or digest != expected['sha256']:
        raise SystemExit('Full archive SHA256 mismatch.')
    partial.replace(output)
    checkpoint.unlink()
    print(f'Archive verified: {output}')


if __name__ == '__main__':
    main()
