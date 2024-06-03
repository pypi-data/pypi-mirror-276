from duct import cmd


def slice(
    file_path: str = "-",
    run: bool = False,
    read: bool = False,
    start: int | None = None,
    end: int | None = None,
    length: int | None = None,
    index: int | None = None,
    json: bool = False,
    output: str | None = None,
    include_header_row: bool = True,
    delimiter: str | None = ",",
):
    """
    # qsv slice

    Returns the rows in the range specified (starting at 0, `[start, end)`).
    The range does not include headers.

    If the end of the range isn't specified, then the slice continues to the
    last record in the CSV data.

    ## Examples

    Assume we have a file `fruits.csv` with the following content:

    ```csv
    fruit,price
    apple,2.50
    banana,3.00
    carrot,1.50
    ```

    ### Get first two rows including header row

    ```python
    qsv.slice("fruits.csv", end=2, run=True)
    # or
    qsv.slice("fruits.csv", start=0, end=2, run=True)
    # or
    qsv.slice("fruits.csv", length=2, run=True)
    ```

    Output:

    ```console
    fruit,price
    apple,2.50
    banana,3.00
    ```

    Args:
        file_path (str): The file to run `qsv slice` on.
        run (bool, optional): Execute the command without returning its output. Defaults to False.
        read (bool, optional): Execute the command and return its output. Defaults to False.
        start (int | None, optional): The index of the record to slice from. If negative, starts from the last record.
        end (int | None, optional): The index of the record to slice to.
        length (int | None, optional): The length of the slice (can be used instead of `end`).
        index (int | None, optional): Slice a single record (shortcut for `start=N, len=1`). If negative, starts from the last record.
        json (bool, optional): Output the result as JSON. Fields are written as key-value pairs. The key is the column name. The value is the field value. The output is a JSON array. If --no-headers is set, then the keys are the column indices (zero-based).
        output (str | None, optional): Write output to a given file path instead of stdout.
        include_header_row (bool, optional): When set to True, the first row will be interpreted as headers. Otherwise, the first row will not appear in the output as the header row. Defaults to True.
        delimiter (bool, optional): The field delimiter for reading CSV data. Must be a single character. Defaults to `,`.
    """

    args = []
    if start:
        args.extend(["-s", str(start)])
    if end:
        args.extend(["-e", str(end)])
    if length:
        args.extend(["-l", str(length)])
    if index:
        args.extend(["-i", str(index)])
    if json:
        args.append("--json")
    if output:
        args.extend(["-o", output])
    if not include_header_row:
        args.append("-n")
    if delimiter:
        args.extend(["-d", delimiter])

    slice_cmd = cmd("qsv", "slice", file_path, *args)

    if run:
        return slice_cmd.run()
    if read:
        return slice_cmd.read()
    return slice_cmd
