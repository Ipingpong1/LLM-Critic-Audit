#!/bin/zsh
# extra targeted queries, recency harvest, recency denominator probe, known-paper id_list check
export ARXIV_MIN_GAP=12
python3 -I scripts/arxiv_harvest.py run raw/arxiv/queries_extra.jsonl raw/arxiv --page 1000
python3 -I scripts/arxiv_harvest.py run raw/arxiv/queries_recency_harvest.jsonl raw/arxiv --page 1000
python3 -I scripts/arxiv_harvest.py probe raw/arxiv/queries_recency_probe.jsonl raw/arxiv
python3 -I scripts/arxiv_idlist.py raw/arxiv idlist_known_missing 2412.19513 2412.06559 2605.20745 2603.00539 2603.12123 2608.10729
echo EXTRA_ALL_DONE
