#!/usr/bin/env python3
"""Verify every archive member; optionally extract without pickle execution."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import tarfile


def digest_stream(stream):
    h = hashlib.sha256()
    size = 0
    while block := stream.read(8 * 1024 * 1024):
        h.update(block)
        size += len(block)
    return size, h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    expected = json.loads((root / 'assets/archive_manifest.json').read_text())
    with args.archive.open('rb') as f:
        size, digest = digest_stream(f)
    if size != expected['bytes'] or digest != expected['sha256']:
        raise SystemExit('Archive size or SHA256 mismatch; extraction refused.')
    members = {m['name'].removeprefix('./'): m for m in expected['members']}
    allowed_directories = {'.'}
    for name in members:
        allowed_directories.update(str(parent) for parent in PurePosixPath(name).parents)
    observed = {}
    directory_count = 0
    with tarfile.open(args.archive, mode='r|gz') as archive:
        for item in archive:
            name = item.name.removeprefix('./')
            path = PurePosixPath(name)
            if path.is_absolute() or '..' in path.parts:
                raise SystemExit('Unsafe or unexpected archive entry; extraction refused.')
            if item.isdir() and str(path) in allowed_directories:
                directory_count += 1
                continue
            if not item.isfile():
                raise SystemExit('Unsafe or unexpected archive entry; extraction refused.')
            if name not in members or name in observed:
                raise SystemExit('Unexpected or duplicate archive member.')
            actual_size, actual_sha = digest_stream(archive.extractfile(item))
            reference = members[name]
            if actual_size != reference['size'] or actual_sha != reference['sha256']:
                raise SystemExit(f'Member checksum mismatch: {name}')
            observed[name] = {'bytes': actual_size, 'sha256': actual_sha}
            print(f'Verified {name}', flush=True)
    if set(observed) != set(members):
        raise SystemExit('Missing archive members; extraction refused.')
    if args.output:
        if args.output.exists():
            raise SystemExit('Extraction output already exists; choose a new directory.')
        unpacked_size = sum(m['size'] for m in members.values())
        probe = args.output.parent
        while not probe.exists():
            probe = probe.parent
        if shutil.disk_usage(probe).free < unpacked_size + 1024**3:
            raise SystemExit('Insufficient free space for extraction and 1 GiB reserve.')
        args.output.mkdir(parents=True)
        with tarfile.open(args.archive, mode='r|gz') as archive:
            for item in archive:
                if item.isdir():
                    continue
                name = item.name.removeprefix('./')
                destination = args.output / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                with archive.extractfile(item) as source, destination.open('xb') as target:
                    shutil.copyfileobj(source, target, length=8 * 1024 * 1024)
    report = {'status': 'PASS', 'archive': expected['filename'], 'archive_bytes': size,
              'archive_sha256': digest, 'all_members_verified': True, 'member_count': len(observed),
              'directory_count': directory_count, 'members': observed,
              'extracted': bool(args.output), 'model_execution': False}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + '\n')
    print('PASS: archive and all members verified; no model code executed.')


if __name__ == '__main__':
    main()
