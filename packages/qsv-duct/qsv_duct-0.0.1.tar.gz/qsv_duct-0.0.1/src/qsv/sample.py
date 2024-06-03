from duct import cmd


def sample(
    sample_size: int,
    file_path: str = "-",
    run: bool = False,
    read: bool = False,
    seed: int | None = None,
    rng: str = "standard",
    user_agent: str | None = None,
    timeout: int | None = None,
    output: str | None = None,
    include_header_row: bool = True,
    delimiter: str | None = ",",
):
    """
    # qsv sample

    Randomly samples CSV data uniformly using memory proportional to the size of
    the sample if no index is present, or constant memory if an index is present.

    When an index is present, this command will use random indexing.
    This allows for efficient sampling such that the entire CSV file is not parsed.

    Otherwise, if no index is present, it will visit every CSV record exactly once,
    which is necessary to provide a uniform random sample (reservoir sampling).
    If you wish to limit the number of records visited, use the 'qsv slice' command
    to pipe into 'qsv sample'.

    This command is intended to provide a means to sample from a CSV data set that
    is too big to fit into memory (for example, for use with commands like
    'qsv stats' with the '--everything' option).

    ## Examples

    Assume we have a file `fruits.csv` with the following content:

    ```csv
    fruit,price
    apple,2.50
    banana,3.00
    carrot,1.50
    ```

    ### Get two random rows

    ```python
    qsv.sample("fruits.csv", sample_size=2, run=True)
    ```

    Output:

    ```console
    fruit,price
    apple,2.50
    carrot,1.50
    ```

    Args:
        file_path (str): The CSV file to sample. This can be a local file, stdin, or a URL (http and https schemes supported).
        run (bool, optional): Execute the command without returning its output. Defaults to False.
        read (bool, optional): Execute the command and return its output. Defaults to False.
        seed (int | None, optional): Random Number Generator (RNG) seed.
        rng (str | None, optional): The RNG algorithm to use.
            Three RNGs are supported:
            - standard: Use the standard RNG.
                1.5 GB/s throughput.
            - faster: Use faster RNG using the Xoshiro256Plus algorithm.
                8 GB/s throughput.
            - cryptosecure: Use cryptographically secure HC128 algorithm.
                Recommended by eSTREAM (https://www.ecrypt.eu.org/stream/).
                2.1 GB/s throughput though slow initialization.
            Defaults to "standard".
        user_agent (str | None, optional): Specify custom user agent to use when the input is a URL.
            It supports the following variables: $QSV_VERSION, $QSV_TARGET, $QSV_BIN_NAME, $QSV_KIND and $QSV_COMMAND.
            Try to follow the syntax here: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent
        timeout (int | None, optional): Timeout for downloading URLs in seconds. Defaults to 30.
        output (str | None, optional): Write output to a given file path instead of stdout.
        include_header_row (bool, optional): When set, the first row will be considered as part of the population to sample from. (When not set, the first row is the header row and will always appear in the output.)
        delimiter (str | None, optional): The field delimiter for reading/writing CSV data. Must be a single character. Defaults to ",".
    """

    args = []
    if seed:
        args.extend(["--seed", str(seed)])
    if rng:
        args.extend(["--rng", rng])
    if user_agent:
        args.extend(["--user-agent", user_agent])
    if timeout:
        args.extend(["--timeout", str(timeout)])
    if output:
        args.extend(["-o", output])
    if not include_header_row:
        args.append("-n")
    if delimiter:
        args.extend(["-d", delimiter])

    sample_cmd = cmd("qsv", "sample", str(sample_size), file_path, *args)

    if run:
        return sample_cmd.run()
    if read:
        return sample_cmd.read()
    return sample_cmd
