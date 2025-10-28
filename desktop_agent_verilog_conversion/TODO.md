# TODO

# Match Changes

Create some automation to use Yosys to generate the list of internal signals for each `fev_full*.eqy`. LLM provides `match_lines.txt` directly (vs. updating `fev.eqy`) (rename to `wip_match.txt`) containing default config deltas _and_ deltas for other configs (tagged as such). Apply `match_lines.txt` to all `fev*.eqy` (`fev.eqy` more directly).
