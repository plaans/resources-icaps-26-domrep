## Folder Structure:

- `aries`: Git submodule of Aries. Needed if you want to build it yourself using (`cargo build --release`). The path to the executable to use (see `justfile`) will have to point to `[this-folder]/aries/target/release/aries-plan-engine`. Note that this executable will use the "standard" plan parser (see below).

- `default-bin`: Includes default `aries` executables that you can use if you do not want to build it yourself in the submodule.
    - `standard`: The contained executable uses the "standard" plan parser, which interprets all lifted arguments of the same name as the same variable (enforcing all occurrences of a lifted argument to be grounded identically).
    - `independent`: The contained executable uses the "modified" plan parser, which interprets each lifted argument as an independent plan variable, even if it shares its name with another one. **This is the configuration used in the experiments reported in the paper to ensure a fair comparison with the baseline, as it is this interpretation that they followed.**