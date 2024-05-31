#!/usr/bin/env bash
set -e

tmp=$(mktemp -d ourchester.XXXXX)

if [ -z "${tmp+x}" ] || [ -z "$tmp" ]; then
    echo "error: $tmp is not set or is an empty string."
    exit 1
fi

if ! command -v txtar-c >/dev/null; then
    echo go install github.com/rogpeppe/go-internal/cmd/txtar-c@latest
	exit 1
fi

declare -a files=(
	# .bumpversion.cfg # loc: 9
	# .gitignore # loc: 2
	# Makefile # loc: 3
	# README.md # loc: 17
	# index/MAIN_0pz5brdz1yntuij3.seg # loc: 337378
	# index/MAIN_6e02j8jvb29skud0.seg # loc: 359500
	# index/MAIN_WRITELOCK # loc: 0
	# index/MAIN_d2kbltu13kogygu2.seg # loc: 337378
	# index/_MAIN_3.toc # loc: 44
	# make_txtar.sh # loc: 53
	# ourchester.code-workspace # loc: 8
	# pyproject.toml # loc: 38
	# requirements-dev.lock # loc: 38
	# requirements.lock # loc: 28
	src/ourchester/__init__.py # loc: 55
	src/ourchester/cli.py # loc: 75
	src/ourchester/indexer.py # loc: 65
	src/ourchester/log.py # loc: 9
	src/ourchester/searcher.py # loc: 13
	# testdata/file1.md # loc: 14
	# testdata/file10.md # loc: 9
	# testdata/file2.md # loc: 10
	# testdata/file3.md # loc: 11
	# testdata/file4.md # loc: 5
	# testdata/file5.md # loc: 5
	# testdata/file6.md # loc: 7
	# testdata/file7.md # loc: 6
	# testdata/file8.md # loc: 5
	# testdata/file9.md # loc: 4
	
)
for file in "${files[@]}"; do
    echo $file
done | tee $tmp/filelist.txt

tar -cf $tmp/ourchester.tar -T $tmp/filelist.txt
mkdir -p $tmp/ourchester
tar xf $tmp/ourchester.tar -C $tmp/ourchester
rg --hidden --files $tmp/ourchester

mkdir -p $tmp/gpt_instructions_XXYYBB

cat >$tmp/gpt_instructions_XXYYBB/1.txt <<EOF

EOF

{
    cat $tmp/gpt_instructions_XXYYBB/1.txt
    echo txtar archive is below
    txtar-c -quote -a $tmp/ourchester
} | pbcopy

rm -rf $tmp
