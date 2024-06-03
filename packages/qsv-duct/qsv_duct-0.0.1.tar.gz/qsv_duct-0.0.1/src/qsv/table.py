from duct import cmd


def table(
    file_path: str = "-",
    run: bool = False,
    read: bool = False,
    include_header_row: bool = True,
    width: int = 2,
    pad: int = 2,
    align: str | None = "left",
    condense: int | None = None,
    output: str | None = None,
    delimiter: str | None = ",",
    memcheck: bool = False,
):
    """
    # qsv table

    Outputs CSV data as a table with columns in alignment.

    This may not work well if the CSV data contains large fields.

    Note that formatting a table requires buffering all CSV data into memory.
    Therefore, you may want to use the 'sample' or 'slice' command to get a
    subsection of CSV data before formatting it with this command.

    ## Examples

    Assume we have a file `fruits.csv` with the following content:

    ```csv
    fruit,price
    apple,2.50
    banana,3.00
    carrot,1.50
    ```

    ### Run qsv table

    ```python
    qsv.table("fruits.csv", run=True)
    ```

    Output:

    ```console
    fruit    price
    apple    2.50
    carrot   1.50
    ```

    Args:
        file_path (str): The path to the CSV file to run `qsv table` on. Use a dash "-" to specify stdin as the input. Defaults to "-".
        run (bool, optional): Execute the command without returning its output. Defaults to False.
        read (bool, optional): Execute the command and return its output. Defaults to False.
        width (int, optional): The minimum width of each column. Defaults to 2.
        pad (int, optional): The minimum number of spaces between each column. Defaults to 2.
        align (str, optional): How entries should be aligned in a column.
            Options:
            - "left"
            - "right"
            - "center"
            Defaults to "left".
        condense (int | None, optional): Limits the length of each field to the value specified. If the field is UTF-8 encoded, then the passed value refers to the number of code points. Otherwise, it refers to the number of bytes.
        output (str | None, optional): Write output to a given file path instead of stdout.
        delimiter (str | None, optional): The field delimiter for reading/writing CSV data. Must be a single character. Defaults to ",".
        memcheck (bool, optional): Check if there is enough memory to load the entire CSV into memory using CONSERVATIVE heuristics.
    """

    args = []
    if width:
        args.extend(["-w", str(width)])
    if pad:
        args.extend(["-p", str(pad)])
    if align:
        args.extend(["-a", align])
    if condense:
        args.extend(["-c", condense])
    if output:
        args.extend(["-o", output])
    if delimiter:
        args.extend(["-d", delimiter])
    if memcheck:
        args.append("--memcheck")

    table_cmd = cmd("qsv", "table", file_path, *args)

    if run:
        return table_cmd.run()
    if read:
        return table_cmd.read()
    return table_cmd
