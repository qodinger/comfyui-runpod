#!/usr/bin/env python3
"""
Download a model file from Hugging Face to `/app/models/checkpoints` (or a custom dest).
Usage examples:
  HF_TOKEN=<token> python scripts/download_hf_model.py --model-id=repo/name --filename=AnythingXL_xl.safetensors
  HF_TOKEN=<token> python scripts/download_hf_model.py --model-id=repo/name --dest=/mnt/models
If `--filename` is omitted the script will attempt to pick the first file with
extension .safetensors, .ckpt or .pt found in the repo.
"""

import os
import shutil
import argparse
from huggingface_hub import HfApi, hf_hub_download


def choose_file(files):
    exts = ('.safetensors', '.ckpt', '.pt', '.bin')
    for ext in exts:
        for f in files:
            if f.lower().endswith(ext):
                return f
    return None


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--model-id', required=True, help='Hugging Face model repo id (e.g. owner/repo)')
    p.add_argument('--filename', help='Exact filename in the repo (optional)')
    p.add_argument('--dest', default='/app/models/checkpoints', help='Destination folder to write model file')
    p.add_argument('--overwrite', action='store_true', help='Overwrite existing file at destination')
    args = p.parse_args()

    token = os.environ.get('HF_TOKEN') or os.environ.get('HUGGINGFACE_TOKEN')
    if not token:
        raise SystemExit('Environment variable HF_TOKEN is required (Hugging Face token)')

    os.makedirs(args.dest, exist_ok=True)

    api = HfApi()
    print(f'Listing files for {args.model_id}...')
    try:
        files = api.list_repo_files(repo_id=args.model_id, token=token)
    except Exception as e:
        raise SystemExit(f'Failed to list repo files: {e}')

    filename = args.filename
    if not filename:
        filename = choose_file(files)
        if not filename:
            raise SystemExit('No candidate model file found in repo; provide --filename explicitly')
        print(f'Auto-selected filename: {filename}')

    dest_path = os.path.join(args.dest, os.path.basename(filename))
    if os.path.exists(dest_path) and not args.overwrite:
        print(f'File already exists at {dest_path}; use --overwrite to replace')
        return

    print(f'Downloading {filename} from {args.model_id}...')
    try:
        local_path = hf_hub_download(repo_id=args.model_id, filename=filename, token=token)
    except Exception as e:
        raise SystemExit(f'Failed to download file: {e}')

    print(f'Copying to {dest_path}...')
    shutil.copy2(local_path, dest_path)
    print('Done.')


if __name__ == '__main__':
    main()
