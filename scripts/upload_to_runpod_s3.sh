#!/usr/bin/env bash
# upload_to_runpod_s3.sh
# Download a Hugging Face file (optionally using HF_TOKEN) and upload it to RunPod S3.
# Usage (example):
#   HF_TOKEN=... AWS_ACCESS_KEY_ID=... AWS_SECRET_ACCESS_KEY=... ./scripts/upload_to_runpod_s3.sh

set -euo pipefail

HF_REPO="tyecode/AnythingXL"
HF_FILE="AnythingXL_xl.safetensors"
BUCKET="r0a7imzhwk"
ENDPOINT="https://s3api-us-ca-2.runpod.io"
DEST_KEY="models/checkpoints/${HF_FILE}"
LOCAL_FILE="./${HF_FILE}"

# Optional env inputs:
# HF_TOKEN - your Hugging Face token (if needed)
# AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY - RunPod S3 API key creds

echo "Downloading ${HF_REPO}/${HF_FILE}..."
if [ -n "${HF_TOKEN:-}" ]; then
  curl -L -H "Authorization: Bearer $HF_TOKEN" \
    "https://huggingface.co/${HF_REPO}/resolve/main/${HF_FILE}" \
    -o "$LOCAL_FILE"
else
  curl -L "https://huggingface.co/${HF_REPO}/resolve/main/${HF_FILE}" -o "$LOCAL_FILE"
fi

echo "Uploading to s3://${BUCKET}/${DEST_KEY} ..."
aws s3 cp "$LOCAL_FILE" "s3://${BUCKET}/${DEST_KEY}" \
  --endpoint-url "$ENDPOINT" --only-show-errors

echo "Verifying..."
aws s3 ls --endpoint-url "$ENDPOINT" "s3://${BUCKET}/models/checkpoints/" --region us-ca-2

echo "Done. You can remove local file if desired: rm -f $LOCAL_FILE"
