#!/bin/sh
set -eu
force=false
case "${1-}" in
    '') ;;
    --force) force=true; shift ;;
    *) printf '%s\n' 'Usage: install-herdr-templates.sh [--force]' >&2; exit 2 ;;
esac
[ "$#" -eq 0 ] || { printf '%s\n' 'Unexpected argument' >&2; exit 2; }
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
source_file="$script_dir/../templates/agy-implementer.md"
config_dir=${XDG_CONFIG_HOME:-"${HOME:?HOME or XDG_CONFIG_HOME is required}/.config"}
directory="$config_dir/herdr-core/templates"
target="$directory/agy-implementer.md"
if [ -e "$target" ]; then
    if cmp -s "$source_file" "$target"; then
        printf 'Already installed: %s\n' "$target"
        exit 0
    fi
    if [ "$force" != true ]; then
        printf 'Template differs: %s. Use --force to replace it.\n' "$target" >&2
        exit 1
    fi
fi
mkdir -p "$directory"
cp "$source_file" "$target"
printf 'Installed: %s\n' "$target"
