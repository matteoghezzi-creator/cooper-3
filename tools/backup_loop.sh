#!/usr/bin/env bash
# backup_loop.sh: versioned backup of /workspace/CooperAI2/loop (Cooper 3.0 stage 0).
# Creates /workspace/backups/loop/loop_YYYYmmdd-HHMM.tgz plus loop_YYYYmmdd-HHMM.manifest.sha256
# (sha256 of every file, paths relative to the parent of loop/).
# Keeps the newest 30 archives (and their manifests). Prints archive path + sha256.
# Read-only on loop/. Override dirs with SRC= / DEST= / KEEP= env vars (used by tests).
set -euo pipefail
SRC="${SRC:-/workspace/CooperAI2/loop}"
DEST="${DEST:-/workspace/backups/loop}"
KEEP="${KEEP:-30}"
[ -d "$SRC" ] || { echo "ERROR: source $SRC missing" >&2; exit 1; }
mkdir -p "$DEST"
stamp="$(date +%Y%m%d-%H%M)"
base="loop_${stamp}"
# Never overwrite an existing backup made in the same minute.
if [ -e "$DEST/$base.tgz" ]; then base="loop_$(date +%Y%m%d-%H%M%S)"; fi
[ -e "$DEST/$base.tgz" ] && { echo "ERROR: $DEST/$base.tgz exists" >&2; exit 1; }
parent="$(dirname "$SRC")"; name="$(basename "$SRC")"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
# Per-file manifest (sorted, stable).
( cd "$parent" && find "$name" -type f -print0 | LC_ALL=C sort -z | xargs -0 -r sha256sum ) > "$tmp/$base.manifest.sha256"
nfiles="$(wc -l < "$tmp/$base.manifest.sha256")"
( cd "$parent" && LC_ALL=C tar --sort=name -czf "$tmp/$base.tgz" "$name" )
# Verify: archive is readable and holds exactly the manifest's files.
narch="$(tar -tzf "$tmp/$base.tgz" | grep -v '/$' | wc -l)"
if [ "$narch" != "$nfiles" ]; then echo "ERROR: archive has $narch files, manifest $nfiles" >&2; exit 1; fi
mv "$tmp/$base.manifest.sha256" "$DEST/"
mv "$tmp/$base.tgz" "$DEST/"
# Retention: keep newest $KEEP archives; delete only older loop_*.tgz and their manifests in DEST.
ls -1 "$DEST"/loop_*.tgz 2>/dev/null | LC_ALL=C sort -r | tail -n +"$((KEEP+1))" | while read -r old; do
  rm -f -- "$old" "${old%.tgz}.manifest.sha256"
done
sum="$(sha256sum "$DEST/$base.tgz" | cut -d' ' -f1)"
echo "$DEST/$base.tgz"
echo "sha256 $sum"
echo "files $nfiles manifest $DEST/$base.manifest.sha256"
