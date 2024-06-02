"""
Base Converter Module

This module serves as a foundation for creating file conversion utilities. It facilitates the development
of file converters through abstract base classes, managing file types, and handling input and output files
efficiently. The module is designed to be extendible, supporting various file formats and conversion strategies.

Classes:

- BaseConverter: An abstract base class for creating specific file format converters, enforcing the implementation of file conversion logic.

Exceptions:

- ValueError: Raised when file paths or types are incompatible or unsupported.
- AssertionError: Ensured for internal consistency checks, confirming that file types match expected values.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Iterable, List, Optional, Tuple, Union

from .file_handler import ResolvedInputFile
from .filetypes import FileType
from .io_handler import FileReader, FileWriter, SamePathReader
from .logging_config import logger


class InvalidOutputFormatError(Exception):
    """Exception raised when the output content format check fails after conversion."""

    def __init__(self, solving_tips):
        self.solving_tips = solving_tips
        super().__init__(
            "Output content format check failed after conversion and before writing. See solving tips for help."
        )

    def __str__(self):
        return f"{super().__str__()}\n\n### Some solving tips\n{self.solving_tips}\n"


class BaseConverter(ABC):
    """
    Abstract base class for file conversion, defining the template for input to output file conversion.
    """

    file_reader: Optional[FileReader] = None
    file_writer: Optional[FileWriter] = None
    folder_as_output: Optional[bool] = None

    def __init__(
        self,
        input_files: Union[ResolvedInputFile, List[ResolvedInputFile]],
        output_file: ResolvedInputFile,
    ):
        """
        Sets up the converter with specified input and output files, ensuring compatibility.

        Args:
            input_files (Union[ResolvedInputFile, List[ResolvedInputFile]]): Either a single input file or a list of input files with resolved types.
            output_file (ResolvedInputFile): The output file where the converted data will be saved.
        """
        if isinstance(input_files, ResolvedInputFile):
            self.input_files = [input_files]
        elif isinstance(input_files, list):
            self.input_files = input_files
        else:
            raise TypeError(
                "input_files must be either a ResolvedInputFile or a list of ResolvedInputFile objects"
            )

        self.output_file = output_file
        self._check_file_types()

        # self.input_format = self.file_reader.input_format
        # self.output_format = self.file_writer.output_format
        self.check_io_handlers()

    def _check_file_types(self):
        """
        Validates that the provided files have acceptable and supported file types for conversion.
        """
        for input_file in self.input_files:
            if not isinstance(input_file, ResolvedInputFile):
                raise ValueError(
                    f"Invalid input file. Expected: {ResolvedInputFile}. Actual: {type(input_file)}"
                )
            if input_file.file_type not in self.get_supported_input_types():
                raise ValueError(
                    f"Unsupported input file type. Expected one of the followings: {self.get_supported_input_types()}, Actual: {input_file.file_type}"
                )

        if not isinstance(self.output_file, ResolvedInputFile):
            raise ValueError(
                f"Invalid output file. Expected: {ResolvedInputFile}. Actual: {type(self.output_file)}"
            )
        if self.output_file.file_type not in self.get_supported_output_types():
            raise ValueError(
                f"Unsupported output file type. Expected one of the followings: {self.get_supported_output_types()}, Actual: {self.output_file.file_type}"
            )

    def check_io_handlers(self):
        """
        Ensures that valid I/O handlers (file reader and writer) are set for the conversion.
        """

        self.custom_io_handlers_check()

        if self.file_reader is None:
            self.file_reader = SamePathReader()

        if not isinstance(self.file_reader, FileReader):
            raise ValueError("Invalid file reader")

        if self.file_writer is None:
            if self.folder_as_output is None:
                raise ValueError(
                    f"the class attribute folder_as_output should be set for your converter {self.__class__.__name__}"
                )
            return

        if not isinstance(self.file_writer, FileWriter):
            raise ValueError("Invalid file writer")

        self.folder_as_output = False

    def custom_io_handlers_check(self):
        pass

    @classmethod
    def get_input_types(cls):
        return cls.get_supported_input_types()

    @classmethod
    def get_output_types(cls):
        return cls.get_supported_output_types()

    @classmethod
    def get_supported_input_types(cls) -> Tuple[FileType, ...]:
        """
        Defines the supported input file types for this converter.

        Returns:
            Tuple[FileType]: The file types supported for input.
        """
        input_types = cls._get_supported_input_types()

        # Check if input_types is a single FileType instance
        if isinstance(input_types, FileType):
            return (input_types,)  # Convert single instance to tuple

        # Check if input_types is an iterable of FileType instances
        input_types = tuple(input_types)
        if not all(isinstance(input_type, FileType) for input_type in input_types):
            raise ValueError("Invalid supported input file type")

        return input_types

    @classmethod
    def get_supported_output_types(cls) -> Tuple[FileType, ...]:
        """
        Defines the supported output file types for this converter.

        Returns:
            Tuple[FileType]: The file types supported for output.
        """
        output_types = cls._get_supported_output_types()

        # Check if output_types is a single FileType instance
        if isinstance(output_types, FileType):
            return (output_types,)  # Convert single instance to tuple

        # Check if output_types is an iterable of FileType instances
        output_types = tuple(output_types)
        if not all(isinstance(output_type, FileType) for output_type in output_types):
            raise ValueError("Invalid supported output file type")

        return output_types

    @classmethod
    @abstractmethod
    def _get_supported_input_types(cls) -> Union[FileType, Iterable[FileType]]:
        """
        Abstract method to define the supported input file types by the converter.

        Returns:
            Iterable[FileType]: The supported input file type.
        """
        raise NotImplementedError(
            f"{cls.__name__}._get_supported_input_typess() must be implemented by subclasses."
        )

    @classmethod
    @abstractmethod
    def _get_supported_output_types(cls) -> Union[FileType, Iterable[FileType]]:
        """
        Abstract method to define the supported output file types by the converter.

        Returns:
            Iterable[FileType]: The supported output file type.
        """
        raise NotImplementedError(
            f"{cls.__name__}._get_supported_output_typess() must be implemented by subclasses."
        )

    def run_conversion(self):
        """
        Orchestrates the file conversion process, including reading, converting, and writing the file.
        """
        logger.info("Starting conversion process...")

        # log
        logger.debug(
            f"Converting {self.input_files[0].path.name} and {len(self.input_files)-1} more ({self.get_supported_input_types()}) to {self.output_file.path.name} ({self.get_supported_output_types()})..."
        )
        logger.debug(f"Input files ({len(self.input_files)}): {self.input_files}")

        # Read all input files
        logger.info("Reading input file...")
        self._input_contents = [
            self._read_content(input_file.path) for input_file in self.input_files
        ]

        # Check input content format for all files
        logger.info("Checking input content format...")
        for input_content, input_file in zip(self._input_contents, self.input_files):
            logger.debug(f"Checking input content format for {input_file.path.name}...")
            assert self._check_input_format(
                input_content
            ), f"Input content format check failed for {input_file.path.name}"
        logger.debug("Input content format check passed")

        output_path = self.convert_files()

        assert (
            output_path.exists()
        ), f"Output file {output_path.name} not found after conversion"

        logger.info(f"Output file: {output_path.resolve()}")
        logger.info("Conversion process complete.")

    def convert_files(self):
        kwargs, output_path = self._get_convertion_kwargs(self.output_file.path)

        # Convert input files to output content
        logger.info("Converting files...")
        if self.file_writer is None:
            logger.info("Writing output directly")
            self._convert(input_contents=self._input_contents, **kwargs)
            logger.debug("Conversion complete")
        else:
            logger.info("Using output content")
            self.output_content = self._convert(input_contents=self._input_contents)
            # Check output content format
            if not self._check_output_format(self.output_content):
                solving_tips = self.__get_bad_output_content_solving_tips__()
                raise InvalidOutputFormatError(solving_tips)
            logger.debug("Output content format check passed")
            # save file
            logger.info("Writing output file...")
            self._write_content(output_path, self.output_content)
            logger.debug("Write complete")
        return output_path

    def _get_convertion_kwargs(self, output_path: Path):
        kwargs = {}
        if self.folder_as_output:
            assert (
                output_path.is_dir()
            ), f"output_path {output_path} is not a dir while a folder is required for this conversion"
            kwargs["output_folder"] = output_path
        else:
            assert (
                not output_path.is_dir()
            ), f"the provided or resolved output path ('{output_path}') already exist as a dir while a file is required for this conversion"
            # if output_path.is_dir():
            #     suffix = self.get_supported_output_types().get_one_suffix()
            #     output_path = (output_path / "opencf-output").with_suffix(suffix)
            kwargs["output_file"] = output_path
        return kwargs, output_path

    @abstractmethod
    def _convert(
        self,
        input_contents: List,
        output_file: Optional[Path] = None,
        output_folder: Optional[Path] = None,
    ) -> Any:
        """
        Abstract method to be implemented by subclasses to perform the actual file conversion process.
        """
        logger.info("Conversion method not implemented")

    def __get_bad_output_content_solving_tips__(self) -> str:
        _solving_tips = (
            f"If you convertion method (`{self.__class__.__name__}._convert(self, input_content:List[])`) uses only one input, make sure you select the first element of input_contents list before procedding",
        )
        return "\n".join(f"{i+1}. {elt}" for i, elt in enumerate(_solving_tips))

    def _read_content(self, input_path: Path):
        assert self.file_reader is not None
        return self.file_reader._read_content(input_path)

    def _check_input_format(self, input_content):
        return self.file_reader._check_input_format(input_content)

    def _check_output_format(self, output_content):
        return self.file_writer._check_output_format(output_content)

    def _write_content(self, output_path: Path, output_content):
        assert self.file_writer is not None
        return self.file_writer._write_content(output_path, output_content)
