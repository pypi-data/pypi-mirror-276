from duct import cmd, Expression


def count(
    file_path: str = "-",
    run: bool = False,
    read: bool = False,
    include_header_row: bool = False,
    human_readable: bool = False,
    width: bool = False,
):
    """
    # qsv count

    Returns a count of the number of records in the CSV data.

    Note that the count will not include the header row
    unless the `include_header_row` parameter/method is used.


    ## Examples

    Assume we have a file `fruits.csv` with the following content:

    ```csv
    fruit,price
    apple,2.50
    banana,3.00
    carrot,1.50
    ```

    ### Get non-header row count and print to stdout

    ```python
    qsv.count("fruits.csv").run()
    # or
    qsv.count("fruits.csv", run=True)
    ```

    Output:

    ```console
    3
    ```

    ### Get non-header row count and read to variable

    ```python
    row_count = qsv.count("fruits.csv").read()
    # or
    row_count = qsv.count("fruits.csv", read=True)
    ```

    ### Get row count including header row and print to stdout

    ```python
    qsv.count("fruits.csv").include_header_row().run()
    # or
    qsv.count("fruits.csv", include_header_row=True, run=True)
    ```

    Output:

    ```console
    4
    ```

    Args:
        file_path (str): The file to run `qsv count` on.
        run (bool, optional): Execute the command without returning its output. Defaults to False.
        read (bool, optional): Execute the command and return its output. Defaults to False.
        include_header_row (bool, optional): Include the header row (first row) in the row count. Defaults to False.
        human_readable (bool, optional): Comma separate row count. Defaults to False.
        width (bool, optional): Also return the estimated length of the longest record. Defaults to False.
    """

    args = []
    if include_header_row:
        args.append("-n")
    if human_readable:
        args.append("-H")
    if width:
        args.append("--width")

    count_cmd = cmd("qsv", "count", file_path, *args)

    if run:
        return count_cmd.run()
    if read:
        return count_cmd.read()
    return count_cmd


class CountBuilder(Expression):
    def __init__(self):
        self.file_path: str | None = None
        self.args = []

    def file(self, file_path: str):
        """
        The file to run `qsv count` on.
        """
        self.file_path = file_path
        return self

    def include_header_row(self):
        """
        Include the header row (first row) in the row count.
        """
        self.args.append("-n")
        return self

    def human_readable(self):
        """
        Comma separate row count.
        """
        self.args.append("-H")
        return self

    def width(self):
        """
        Also return the estimated length of the longest record.
        """
        self.args.append("--width")
        return self

    def run(self):
        """
        Execute the command without returning its output.
        """
        if not self.file_path:
            return None
        return cmd("qsv", "count", self.file_path, *self.args).run()

    def read(self):
        """
        Execute the command and return its output.
        """
        return cmd("qsv", "count", self.file_path, *self.args).read()
