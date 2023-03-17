from argparse import ArgumentParser
from pathlib import Path

import pydicom
from pydicom.dataset import Dataset, DataElement
from rich.console import Console


def data_element_to_row(data_element: DataElement, indent: int = 0) -> list[list]:
    if isinstance(data_element, Dataset):
        output = []
        for dataset_item in data_element:
            output += data_element_to_row(data_element=dataset_item, indent=indent)

        return output

    if data_element.name == "Pixel Data":
        return []

    row = [
        [
            indent,
            f"{'>' * indent}{' ' if indent else ''}{data_element.tag}",
            data_element.VR,
            data_element.name,
            "",
            False
        ]
    ]

    if data_element.VR != "SQ":
        row[0][4] = str(data_element.value)
        return row

    row[-1][-1] = True
    for dataset_item in data_element:
        row += data_element_to_row(data_element=dataset_item, indent=indent + 1)

    return row


def get_file_content(dataset: Dataset) -> list[list]:
    file_content = []
    for data_element in dataset:
        file_content += data_element_to_row(data_element=data_element)

    return file_content


def create_html_table(table_rows: list[list[str]], title: str = None) -> str:
    html_contents: str = (
        '<!DOCTYPE html>'
        '<html>'
        '<head>'
        '<meta charset="UTF-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
        f'<title>{title + " - " if title else ""}DICOM file content</title>'
        '<style>'
        ':root {'
        '  --clr-black: #000000;'
        '  --clr-dark: #3c3f41;'
        '  --clr-darker: #313335;'
        '  --clr-darkest: #323232;'
        '  --clr-grey: #;'
        '  --clr-white: #ffffff;'
        '  --clr-green: #507e34;'
        '  --clr-blue: #5883a2;'
        '  --clr-dark-blue: #0000d0;'
        '  --clr-orange: #c57730;'
        ''
        '  --fw-regular: 500;'
        '  --fw-bold: 700;'
        ''
        '  --fs-500: 1rem;'
        '  --fs-700: 2.5rem;'
        '  --fs-900: 3rem;'
        ''
        '  --fs-header1: var(--fs-900);'
        '  --fs-table-header: var(--fs-700);'
        '  --fs-body: var(--fs-500);'
        ''
        '  --clr-background: var(--clr-white);'
        '  --clr-table-shadow: var(--clr-black);'
        '  --clr-table-background: var(--clr-darker);'
        '  --clr-table-odd-row: var(--clr-dark);'
        '  --clr-font: var(--clr-black);'
        '  --clr-font-table: var(--clr-white);'
        '}'
        '@media (prefers-color-scheme: dark) {'
        '  :root {'
        '    --clr-background: var(--clr-darkest);'
        '    --clr-table-background: var(--clr-darkest);'
        '    --clr-table-odd-row: var(--clr-dark);'
        '    --clr-font: var(--clr-white);'
        '    --clr-font-table: var(--clr-white);'
        '  }'
        '}'
        'body {'
        '  background-color: var(--clr-background);'
        '  color: var(--clr-font);'
        '  font-wieght: var(--fw-regular);'
        '  font-size: var(--fs-body);'
        '}'
        ''
        'h1 { font-size: var(--fs-header1); font-weight: var(--fw-bold); }'
        ''
        '.table-container {'
        '  padding: 15px;'
        '  display: flex;'
        '  flex-direction: column;'
        '  align-items: center;'
        '}'
        
        ''
        'table {'
        '  color: var(--clr-font-table);'
        '  margin: auto;'
        '  background: var(--clr-darker);'
        '  border-collapse: collapse;'
        '  -moz-box-shadow: 0 0 5px var(--clr-table-shadow);'
        '  -webkit-box-shadow: 0 0 5px var(--clr-table-shadow);'
        '  box-shadow: 0 0 5px var(--clr-table-shadow);'
        '  padding: 5px;'
        '}'
        ''
        'th {'
        '  font-size: var(--fs-table-header);'
        '  font-weight: var(--fw-bold);'
        '  padding: 10px;'
        '  text-align: initial;'
        '}'
        'td {'
        '  padding: 10px;'
        '}'
        'tr:nth-of-type(odd) { background-color: var(--clr-table-odd-row); }'
        ''
        'tr.italic { font-style: italic; }'
        ''
        'tr.blue { color: var(--clr-blue); }'
        'tr.green { color: var(--clr-green); }'
        'tr.orange { color: var(--clr-orange); }'
        '</style>'
        '</head>'
        f'<body><div class="table-container">{"<h1>" + title + "</h1>" if title else ""}'
        '<table><tr><th>Tag</th><th>VR</th><th>Name</th><th>Value</th></tr>'
    )

    color_classes = ["regular", "orange", "green", "blue"]

    html_contents += "".join([
        f'<tr class="{color_classes[row[0] % len(color_classes)]}{" italic" if row[-1] else ""}"><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td></tr>'
        for row in table_rows
    ])

    html_contents += '</table></div></body></html>'

    return html_contents


def get_input_arguments():
    parser = ArgumentParser(description="Convert metadata from DICOM-file to a HTML table")

    parser.add_argument(
        "files", metavar="filepath", nargs="+", help="Path/-s to the DICOM-files to convert to HTML-table/-s"
    )
    parser.add_argument(
        "-o", "--output-dir",
        required=False,
        dest="output_dir",
        type=Path,
        help=("The directory in which to place the HTML file/-s. If not given, the output will be placed in the same "
              "directory as the input file.")
    )

    return parser.parse_args()


def main():
    console = Console()

    console.print("Parsing input arguments")

    input_args = get_input_arguments()

    try:
        input_files: list[Path] = [filepath for fp in input_args.files if (filepath := Path(fp)).exists()]
    except Exception as ex:
        console.print(f"[red][bold]Failed to identify input path{'s' if len(input_args.files) > 1 else ''}[/bold][/red]")
        return

    file_count = len(input_files)
    console.print(f"Found {file_count} file{'s' if file_count > 1 else ''}")

    for fp in input_files:
        output_file = input_args.output_dir if input_args.output_dir else fp.parent
        output_file = output_file / f"{fp.stem}.html"
        console.print(f"Creating HTML file from {fp.name} as {output_file.stem}")

        if fp.suffix.casefold() == ".json".casefold():
            ds = Dataset.from_json(fp.read_text())
        else:
            ds = pydicom.dcmread(fp)

        file_data = get_file_content(dataset=ds)
        html_table = create_html_table(file_data, title=fp.stem)

        output_file.write_text(html_table)

    console.print(f"\n\n[green]DONE! {file_count} file{'s' if file_count > 1 else ''} created.[/green]")


if __name__ == "__main__":
    main()
