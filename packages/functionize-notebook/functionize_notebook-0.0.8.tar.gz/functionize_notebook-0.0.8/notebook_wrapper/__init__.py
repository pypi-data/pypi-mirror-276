import dill as pickle
import tempfile
from datetime import datetime
from pathlib import Path
from time import sleep
from typing import Any, List

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbformat.v4 import nbbase


class NotebookWrapper:
    def __init__(
        self,
        notebookFile: str | Path,
        inputVariable: str | List[str] | None,
        outputVariable: str | List[str] | None,
        inputTag: str = "input",
        allowError: bool = False,
    ):
        self.notebook = Path(notebookFile)

        if inputVariable is None:
            inputVariable = []
        elif isinstance(inputVariable, str):
            inputVariable = [inputVariable]
        self.inputVariable = inputVariable

        self.outputVariable = outputVariable

        self.inputTag = inputTag
        
        self.allowError = allowError

        pass

    def __call__(self, *args, **kwargs):
        return self.run(*args, *kwargs)

    def run(self, *args, **kwargs) -> Any | List[Any]:
        return self.export(None, *args, **kwargs)

    def export(self, _outputNotebook: str | Path | None, *args, **kwargs):
        if isinstance(_outputNotebook, str):
            _outputNotebook = Path(_outputNotebook)

        # map input
        variableMapping = dict(zip(self.inputVariable, args))
        variableMapping.update(kwargs)

        nb = nbformat.read(self.notebook, as_version=nbformat.NO_CONVERT)

        inputIndex = -1
        if len(variableMapping) > 0:
            # add saving path for input
            inputPath = Path(
                tempfile.gettempdir(),
                "BHTuNbWrapper",
                self.notebook.stem,
                "input",
                datetime.now().__str__() + ".pkl",
            )
            inputPath.parent.mkdir(parents=True, exist_ok=True)

            # add input values
            inputPath.write_bytes(pickle.dumps(variableMapping))
            # wait for nb input file
            for _ in range(50):
                if inputPath.exists():
                    break
                else:
                    sleep(0.2)
            else:
                raise IOError(inputPath.__str__() + " took too much time to write.")

            inputIndex = self._insertInputCell(nb, inputPath)

        outputIndex = -1
        if self.outputVariable is not None:
            # add saving path for output
            outputPath = Path(
                tempfile.gettempdir(),
                "BHTuNbWrapper",
                self.notebook.stem,
                "output",
                datetime.now().__str__() + ".pkl",
            )
            outputPath.parent.mkdir(parents=True, exist_ok=True)

            outputIndex = self._insertOutputCell(nb, outputPath)
            pass

        ep = ExecutePreprocessor(timeout=None, allow_errors=self.allowError)
        resultNb, _ = ep.preprocess(nb, {"metadata": {"path": self.notebook.parent}})

        if _outputNotebook is not None:
            if inputIndex >= 0:
                resultNb.cells.pop(inputIndex)

                # Add markdown cell noting injected variables
                mdText = "`functionize-notebook` has modified this notebook during execution. The following variables have been injected:\n\n"
                for variable, varValue in variableMapping.items():
                    try:
                        varStr = str(varValue)
                    except Exception:
                        varStr = "This variable could not be represent in text."
                    mdText += f"- {variable}: {varStr}\n"

                mdCell = nbbase.new_markdown_cell(source=mdText)
                resultNb.cells.insert(inputIndex, mdCell)

            if outputIndex >= 0:
                resultNb.cells.pop(outputIndex)

            with open(_outputNotebook, "w") as f:
                nbformat.write(resultNb, f)
                pass

        if self.outputVariable is not None:
            # wait for nb output
            for _ in range(50):
                if outputPath.exists():
                    break
                else:
                    sleep(0.2)
            else:
                raise IOError(outputPath.__str__() + " took too much time to write.")

            res = pickle.loads(outputPath.read_bytes())

            return res
        else:
            return None

    def _insertInputCell(self, nb, inputPath: Path):
        # identify input cell
        inputIndex = 0
        for i, cell in enumerate(nb.cells):
            if "tags" in cell.metadata and self.inputTag in cell.metadata["tags"]:
                inputIndex = i
                break
            pass

        newCell = nbbase.new_code_cell(
            source="""
                from pathlib import Path
                import dill as pickle
                
                inputVariables = pickle.loads(Path("%s").read_bytes())
                for key, value in inputVariables.items():
                    globals()[key] = value
                    pass
            """
            % inputPath
        )

        nb.cells.insert(inputIndex + 1, newCell)

        return inputIndex + 1

    def _insertOutputCell(self, nb, outputPath: Path):
        if isinstance(self.outputVariable, List):
            requestVars = "[" + ",".join(self.outputVariable) + "]"
        else:
            requestVars = self.outputVariable
        newCell = nbbase.new_code_cell(
            source="""
                from pathlib import Path
                import dill as pickle
                
                outputVariable = %s
                Path("%s").write_bytes(pickle.dumps(outputVariable))
            """
            % (requestVars, outputPath)
        )

        nb.cells.append(newCell)

        return len(nb.cells) - 1
