import matplotlib
import tomllib
import argparse
import pathlib
import enum

class outputType(enum.Enum):
    HISTOGRAM = 0
    BAR = 1
    TEXT = 2

inputDataResult = tuple[list[list[str]], dict[str, int]]

def loadInputData(inputFilePath: pathlib.Path) -> inputDataResult:
    try:
        header: dict[str,int] = {}

        body: list[list[str]] = [[]]

        with open(inputFilePath.absolute(), "r") as f:
            isFirstLine = True
            for line in f:
                if isFirstLine:
                    firstLine: list[str] = line.split(",")
            
                    for i in range(0, len(firstLine)):
                        header[firstLine[i].strip()] = i
                    
                    isFirstLine = False
                else:
                    lineValues: list[str] = line.split(",")

                    body.append([x.strip() for x in lineValues])

        return ([x for x in body if x != []], header)
    except:
        print("Could not load input data!")
        exit()

def main(
    inputFilePath: pathlib.Path,
    processName: str,
    output: str,
    confidence: int,
    scope: str,
    offline: bool,
):
    print(loadInputData(inputFilePath))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Data analysis tool for FRC 957")

    parser.add_argument(
        "inputFilePath", help="file path to input data set", type=pathlib.Path
    )

    parser.add_argument(
        "processName", help="process to execute. See processesConfig.toml for options. If 'final' produces a combined display of all important data instead"
    )

    parser.add_argument(
        "-u",
        "--output",
        help="way to output calculated data. 'h' plots a histogram, 'f' prints the final values, and 'c' plots a bar graph. Default is 'histogram'",
    )

    parser.add_argument(
        "-c",
        "--confidence",
        help="confidence interval (percentage) to display. If <= 0 or >=100, does not show a confidence interval. Default is '95'",
        type=float,
    )

    parser.add_argument(
        "-s",
        "--scope",
        help="teams to analyze. 'a' analyzes all teams, '123' analyzes team 123, 'o123' analyzes opponents of team 123 in matches, and 'p123' analyzes partners of team 123 in matches. Can be repeated, e.g. '-s 123 -s 456 -s 789'. Default is 'all'",         action="append",
    )

    parser.add_argument(
        "-o", "--offline", help="runs this program in offline mode", action="store_true"
    )

    args = parser.parse_args()

    main(args.inputFilePath, args.processName, args.output, args.confidence, args.scope, args.offline)
