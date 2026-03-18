# Resources for Experiments and Additional Material for ICAPS 2026 Submission

Paper: "A Constraint Formulation for Domain Repair with Ground or Lifted Test Plans"

## Folder / File Structure:

- `benchmarks/domrep`: The benchmark files used in the experiments. Contents:
    - `domain` folders (e.g. `satellite`). Each contains the following:
        - (Flawed) domains' files
        - Corresponding problem files (objects, initial state, goals)
        - `plans` folder (ground test plans)
        - `lifted_plans` folder (lifted versions of the ground plans, with subfolders corresponding to the proportion of lifted arguments, e.g. `033` for 0.33)

- `main`:

    - `aries`:
        - `aries`: Git submodule of Aries. Needed if you want to build it yourself using `cargo build --release`. The path to the binary to use (see `justfile`) will have to point to `[this-folder]/aries/aries/target/release/aries-plan-engine`. **Note that this binary will use the "standard" plan parser, not the "modified" one (see below)**.
        - `default-bin`: Includes default `aries` binaries that you can use if you do not want to build it yourself in the submodule.
            - `standard`: The contained binary uses the "standard" plan parser, which interprets all lifted arguments of the same name as the same variable (enforcing all occurrences of a lifted argument to be grounded identically).
            - `independent`: The contained binary uses the "modified" plan parser, which interprets each lifted argument as an independent plan variable, even if it shares its name with another one. **This is the configuration used in the experiments reported in the paper to ensure a fair comparison with the baseline, as it is this interpretation followed by it.**

    - `src/aries/justfile`: Contains both high-level and low-level commands that you can use to reproduce the experiments and/or set up your own. This includes commands to generate the `.txt` that populate `input/aries`, commands parsing the logs to produce summary `.json` files in `output/aries`, commands to plot figures based on said `.json` files, and, of course, commands to run the experiments (either all or individual instances, both locally or via `slurm`).
        - **NOTE 1**: The `aries` variable in the beginning of `justfile` corresponds to the command to execute Aries (`./[path-to-bin]`, see above).
        - **NOTE 2**: If you cannot install `just` via a package manager, you can still use the `just` command command via a pre-built binary (see [link](https://github.com/casey/just?tab=readme-ov-file#pre-built-binaries)) that you can put in a folder which you should include in the `PATH` environmental variable.

    - `src/aries/src`: Contains scripts used in the `src/aries/justfile`.

    - `input/aries`: Used to store `.txt` files specifying, on each line, the arguments to use to run one instance. See `prepare_benchmarks` command in `justfile`.

    - `output`: Used to store the output (logs and their parsing (summaries)) of experiments. Has a `aries` and `baseline` subfolder, containing the result summaries (logs themselves are git-ignored).

Do not hesitate to reach out if you have any questions.