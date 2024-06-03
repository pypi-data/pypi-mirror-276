import time
from csv import writer
from multiprocessing import Process
from typing import List, Tuple

import typer
from rich.console import Console
from rich.status import Status
from tabulate import tabulate

from polyharmonics.associated_legendre_functions import (
    ass_legendre_store,
    associated_legendre_def,
    associated_legendre_rec,
    associated_legendre_rec_alt,
)

SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
SUP = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
console = Console()


def associated_legendre_bench_command(
    nm: str = typer.Argument(
        ...,
        help="""Calculate the associated Legendre functions from 0:0 to the given subscripts and superscripts.
        Either a pair of integers separated by ':' or a comma-separated list of such pairs.""",  # noqa: E501
        metavar="SUB:SUP",
    ),
    eval: float = typer.Option(
        None,
        "--eval",
        case_sensitive=False,
        help="Evaluate the functions on the given number.",
    ),
    max_time: float = typer.Option(
        60.0,
        "--max-time",
        case_sensitive=False,
        help="Maximum execution time in seconds for each calculation. Default is 60 seconds.",  # noqa: E501
    ),
    csv: str = typer.Option(
        None,
        "--csv",
        case_sensitive=False,
        help="""Save the results in a CSV file with the given name.
        File extension must not be specified.""",
    ),
) -> None:
    """Benchmark the calculation of associated Legendre functions and display the time taken."""  # noqa: E501

    try:
        nm_values: List[Tuple[int, int]] = []
        for value in nm.split(","):
            n, m = value.split(":")
            if n is None or m is None or n == "" or m == "":
                raise typer.BadParameter(
                    "Between each ',' must be a pair of integers separated by ':'."  # noqa: E501
                )
            else:
                nm_values.append((int(n), int(m)))

        nm_values.sort(key=lambda x: (x[0], x[1]))
        if any(n < 0 for n, m in nm_values):
            raise typer.BadParameter(
                "All subscripts must be greater or equal to 0."  # noqa: E501
            )
    except ValueError:
        raise typer.BadParameter(
            "nm must either be a pair of integers separated by ':' or a list of such pairs separated by commas."  # noqa: E501
        )

    with console.status(status="", spinner="dots") as status:
        status: Status
        table = []
        n_tests = 5
        headers = [
            "N:M",
            "Definition w storage",
            "Definition w/o storage",
            "Recursion w storage",
            "Recursion w/o storage",
            "Alternative recursion",
        ]

        timed_out = [False for _ in range(n_tests)]
        for n, m in nm_values:
            # List of tests to run for each n, m of nm_values
            tests = [
                {
                    "fun": calculate_associated_legendre,
                    "args": (n, m, eval, True, False, True),
                    "text": (
                        "Calculating all associated Legendre functions from "
                        f"P{str(0).translate(SUB)}{str(0).translate(SUP)}(x) to "
                        f"P{str(n).translate(SUB)}{str(m).translate(SUP)}(x) with the "
                        "definition and storage."
                    ),
                },
                {
                    "fun": calculate_associated_legendre,
                    "args": (n, m, eval, True, False, False),
                    "text": (
                        "Calculating all associated Legendre functions from "
                        f"P{str(0).translate(SUB)}{str(0).translate(SUP)}(x) to "
                        f"P{str(n).translate(SUB)}{str(m).translate(SUP)}(x) with the "
                        "definition but no storage."
                    ),
                },
                {
                    "fun": calculate_associated_legendre,
                    "args": (n, m, eval, False, False, True),
                    "text": (
                        "Calculating all associated Legendre functions from "
                        f"P{str(0).translate(SUB)}{str(0).translate(SUP)}(x) to "
                        f"P{str(n).translate(SUB)}{str(m).translate(SUP)}(x) with the "
                        "recursion and storage."
                    ),
                },
                {
                    "fun": calculate_associated_legendre,
                    "args": (n, m, eval, False, False, False),
                    "text": (
                        "Calculating all associated Legendre functions from "
                        f"P{str(0).translate(SUB)}{str(0).translate(SUP)}(x) to "
                        f"P{str(n).translate(SUB)}{str(m).translate(SUP)}(x) with the "
                        "recursion but no storage."
                    ),
                },
                {
                    "fun": calculate_associated_legendre,
                    "args": (n, m, eval, False, True, False),
                    "text": (
                        "Calculating all associated Legendre functions from "
                        f"P{str(0).translate(SUB)}{str(0).translate(SUP)}(x) to "
                        f"P{str(n).translate(SUB)}{str(m).translate(SUP)}(x) with the "
                        "alternative recursion."
                    ),
                },
            ]
            assert len(tests) == n_tests
            row = [f"{n}:{m}"]
            for n_test, test in enumerate(tests):
                status.update(f"[bold yellow1]{test['text']}[/]")
                if timed_out[n_test]:
                    row.append("TIMEOUT")
                else:
                    legendre_calc = Process(target=test["fun"], args=test["args"])
                    t_start = time.time()
                    legendre_calc.start()
                    while legendre_calc.is_alive():
                        if time.time() - t_start > max_time:
                            legendre_calc.terminate()
                            row.append("TIMEOUT")
                            timed_out[n_test] = True
                            break

                    if len(row) == n_test + 1:
                        row.append(round(time.time() - t_start, 6))

            table.append(row)

    if csv is None:
        console.print("[bold green]ASSOCIATED LEGENDRE FUNCTIONS UP TO N:M[/]")
        console.print(
            tabulate(
                table,
                headers,
                tablefmt="fancy_grid",
                maxheadercolwidths=[None] + [12 for _ in range(n_tests)],
            )
        )
    else:
        with open(csv + ".csv", "w") as f:
            csv_writer = writer(f)
            csv_writer.writerow(headers)
            for row in table:
                csv_writer.writerow(row)

    raise typer.Exit()


def calculate_associated_legendre(
    n: int,
    m: int,
    eval: float | None,
    use_def: bool,
    use_alt_rec: bool,
    store: bool,
):
    if store:
        # Reset the stores to avoid following calculations to be faster than expected
        ass_legendre_store.reset(
            definition=use_def,
            recursion=not use_def,
        )
    n_values = range(n + 1)
    for i in n_values:
        m_values = range(m + 1 if n >= m else n + 1)
        for j in m_values:
            if use_alt_rec:
                associated_legendre_rec_alt(i, j, eval=eval)
            else:
                if use_def:
                    associated_legendre_def(i, j, eval=eval, store=store)
                else:
                    associated_legendre_rec(i, j, eval=eval, store=store)
