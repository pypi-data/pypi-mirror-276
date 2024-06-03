"""Build tools for bertrand-enabled C++ extensions."""
import re
import shutil
import subprocess
import sys
import sysconfig
from pathlib import Path
from typing import Any

import numpy
import pybind11
from pybind11.setup_helpers import Pybind11Extension
from pybind11.setup_helpers import build_ext as pybind11_build_ext
import setuptools


# TODO: list cpptrace, pcre2, googletest version #s explicitly here?

ROOT: Path = Path(__file__).absolute().parent.parent
DEPS: Path = ROOT / "third_party"


def get_include() -> str:
    """Get the path to the include directory for this package, which is necessary to
    make C++ headers available to the compiler.

    Returns
    -------
    str
        The path to the include directory for this package.
    """
    return str(ROOT)


def quick_include() -> list[str]:
    """Return the complete include and link flags necessary to build a pure-C++ project
    with bertrand as a dependency.

    Returns
    -------
    list
        A list of strings containing the various include and link libraries needed to
        build a bertrand-enabled project from the command line, as a single unit.
    """
    cpptrace = DEPS / "cpptrace-0.5.2"
    gtest = DEPS / "googletest-1.14.0"
    pcre2 = DEPS / "pcre2-10.43"
    return [
        f"-I{sysconfig.get_path('include')}",
        f"-I{get_include()}",
        f"-I{pybind11.get_include()}",
        f"-I{numpy.get_include()}",
        f"-I{str(cpptrace / 'include')}",
        f"-I{str(gtest / 'googletest' / 'include')}",
        f"-I{str(pcre2 / 'src')}",
        f"-L{str(cpptrace / 'build')}",
        f"-L{str(cpptrace / 'build' / '_deps' / 'libdwarf-build' / 'src' / 'lib' / 'libdwarf')}",
        f"-L{str(cpptrace / 'build' / '_deps' / 'zstd-build' / 'lib')}",
        f"-L{str(gtest / 'build' / 'lib')}",
        f"-L{str(pcre2 / '.libs')}",
        f"-lpython{sysconfig.get_python_version()}",
        "-lcpptrace",
        "-ldwarf",
        "-lz",
        "-lzstd",
        "-ldl",
        "-lgtest",
    ]


class Extension(Pybind11Extension):
    """A setuptools.Extension class that builds using CMake and supports C++20 modules.

    Parameters
    ----------
    *args, **kwargs : Any
        Arbitrary arguments passed to the Pybind11Extension constructor.
    cxx_std : int, default 20
        The C++ standard to use when compiling the extension.  Values less than 20 will
        raise a ValueError.
    traceback : bool, default True
        If set to false, add `BERTRAND_NO_TRACEBACK` to the compile definitions, which
        will disable cross-language tracebacks for the extension.
    cmake_args : dict[str, Any], optional
        Additional arguments to pass to the Extension's CMake configuration.  These are
        emitted as key-value pairs into a `set_target_properties()` block in the
        generated CMakeLists.txt file.  Some options are filled in by default,
        including `PREFIX`, `LIBRARY_OUTPUT_DIRECTORY`, `LIBRARY_OUTPUT_NAME`,
        `SUFFIX`, `CXX_STANDARD`, and `CXX_STANDARD_REQUIRED`.
    """

    MODULE_REGEX = re.compile(r"\s*export\s+module\s+(\w+).*;", re.MULTILINE)

    def __init__(
        self,
        *args: Any,
        executable: bool = False,
        cxx_std: int = 23,
        traceback: bool = True,
        cmake_args: dict[str, Any] | None = None,
        **kwargs: Any
    ) -> None:
        if cxx_std < 23:
            raise ValueError(
                "C++ standard must be at least C++23 to enable bertrand features"
            )

        super().__init__(*args, **kwargs)
        self.executable = executable
        self.cxx_std = cxx_std
        self.traceback = traceback
        self.cmake_args = cmake_args or {}

        self.include_dirs.append(get_include())
        self.include_dirs.append(numpy.get_include())
        if self.traceback:
            self.extra_compile_args.append("-g")
            self.extra_link_args.append("-g")
        else:
            self.define_macros.append("BERTRAND_NO_TRACEBACK")

    def add_to_cmakelists(
        self,
        cmakelists: Path,
        build_dir: Path,
        module_cache: dict[str, bool]
    ) -> None:
        """Generate a temporary CMakeLists.txt that configures the extension for
        building with CMake.

        Parameters
        ----------
        cmakelists : Path
            The (current) path to the generated CMakeLists.txt file.
        build_dir : Path
            The path to the build directory for the extension.
        module_cache : dict[str, bool]
            A dictionary that caches whether each source file exports a module.  If the
            same source is used across multiple extensions, this will prevent duplicate
            scans.
        """
        with cmakelists.open("a") as f:
            if self.executable:
                f.write(f"add_executable({self.name}\n")
            else:
                f.write(f"add_library({self.name} MODULE\n")
            # TODO: add sources related to built-in bertrand modules
            for source in self.sources:
                f.write(f"    {ROOT / source}\n")
            f.write(")\n")

            f.write(f"set_target_properties({self.name} PROPERTIES\n")
            f.write( "    PREFIX \"\"\n")
            f.write(f"    OUTPUT_NAME {self.name}\n")
            if not self.executable:
                f.write(f"    LIBRARY_OUTPUT_DIRECTORY {build_dir}")
                f.write(f"    SUFFIX {sysconfig.get_config_var('EXT_SUFFIX')}\n")
            f.write(f"    CXX_STANDARD {self.cxx_std}\n")
            f.write( "    CXX_STANDARD_REQUIRED ON\n")
            for key, value in self.cmake_args.items():
                f.write(f"    {key} {value}\n")
            f.write(")\n")

            modules = []
            for source in self.sources:
                if source not in module_cache:
                    with Path(ROOT / source).open("r", encoding="utf_8") as s:
                        module_cache[source] = bool(self.MODULE_REGEX.search(s.read()))
                if module_cache[source]:
                    modules.append(source)

            if modules:
                f.write(f"target_sources({self.name} PRIVATE\n")
                f.write( "    FILE_SET CXX_MODULES\n")
                f.write(f"    BASE_DIRS {ROOT}\n")
                f.write( "    FILES\n")
                for source in modules:
                    f.write(f"        {ROOT / source}\n")
                f.write(")\n")

            if self.include_dirs:
                f.write(f"target_include_directories({self.name} PRIVATE\n")
                for include in self.include_dirs:
                    f.write(f"    {include}\n")
                f.write(")\n")

            if self.library_dirs:
                f.write(f"target_link_directories({self.name} PRIVATE\n")
                for lib_dir in self.library_dirs:
                    f.write(f"    {lib_dir}\n")
                f.write(")\n")

            if self.libraries:
                f.write(f"target_link_libraries({self.name} PRIVATE\n")
                for lib in self.libraries:
                    f.write(f"    {lib}\n")
                f.write(")\n")

            if self.extra_compile_args:
                f.write(f"target_compile_options({self.name} PRIVATE\n")
                for flag in self.extra_compile_args:
                    f.write(f"    {flag}\n")
                f.write(")\n")

            _link_options = [sysconfig.get_config_var("LDFLAGS")] + self.extra_link_args
            if _link_options:
                f.write(f"target_link_options({self.name} PRIVATE\n")
                for flag in _link_options:
                    f.write(f"    {flag}\n")
                f.write(")\n")

            if self.define_macros:
                f.write(f"target_compile_definitions({self.name} PRIVATE\n")
                for define in self.define_macros:
                    if isinstance(define, tuple):
                        f.write(f"    {define[0]}={define[1]}\n")
                    else:
                        f.write(f"    {define}\n")
                f.write(")\n")


class BuildExt(pybind11_build_ext):
    """A custom build_ext command that uses CMake to build extensions with support for
    C++20 modules, parallel builds, clangd, executable targets, and bertrand's core
    dependencies without any extra configuration.
    """

    CMAKE_MIN_VERSION = "3.28" # CMake 3.28+ is necessary for C++20 module support
    user_options = pybind11_build_ext.user_options + [
        (
            "workers=",
            "j",
            "The number of parallel workers to use when building CMake extensions"
        )
    ]

    def __init__(self, *args: Any, workers: int | None = None, **kwargs: Any) -> None:
        """Initialize the build extensions command.

        Parameters
        ----------
        *args : Any
            Arbitrary positional arguments passed to the parent class.
        workers : int, default 0
            The number of parallel workers to use when building the extensions.  If set
            to 0, then the build will be single-threaded.
        **kwargs : Any
            Arbitrary keyword arguments passed to the parent class.
        """
        super().__init__(*args, **kwargs)
        self.workers = workers

    def finalize_options(self) -> None:
        """Extract the number of parallel workers from the setup() call.

        Raises
        ------
        ValueError
            If the workers option is not set to a positive integer.
        """
        super().finalize_options()
        if self.workers is not None:
            try:
                self.workers = int(self.workers)
            except ValueError as e:
                raise ValueError("workers must be set to an integer") from e

            if self.workers < 1:
                raise ValueError("workers must be set to a positive integer")

    def init_cmakelists(self) -> Path:
        """Create and initialize a CMakeLists.txt file for the entire project.

        Returns
        -------
        Path
            The path to the generated CMakeLists.txt file, for further processing.
        """
        file = Path(self.build_lib).absolute() / "CMakeLists.txt"
        file.parent.mkdir(parents=True, exist_ok=True)
        file.touch(exist_ok=True)

        with file.open("w") as f:
            f.write(f"cmake_minimum_required(VERSION {self.CMAKE_MIN_VERSION})\n")
            f.write(f"project({self.distribution.get_name()} LANGUAGES CXX)\n")
            f.write(f"set(CMAKE_BUILD_TYPE {'Debug' if self.debug else 'Release'})\n")
            f.write(f"set(PYTHON_EXECUTABLE {sys.executable})\n")
            f.write("set(CMAKE_COLOR_DIAGNOSTICS ON)\n")
            f.write("set(CMAKE_CXX_SCAN_FOR_MODULES ON)\n")
            f.write("set(CMAKE_EXPORT_COMPILE_COMMANDS ON)\n")

            if self.compiler.include_dirs:
                f.write("include_directories(\n")
                for include in self.compiler.include_dirs:
                    f.write(f"    {include}\n")
                f.write(")\n")

            if self.compiler.library_dirs:
                f.write("link_directories(\n")
                for lib_dir in self.compiler.library_dirs:
                    f.write(f"    {lib_dir}\n")
                f.write(")\n")

            if self.compiler.libraries:
                f.write("link_libraries(\n")
                f.write(f"    python{sysconfig.get_python_version()}\n")
                for lib in self.compiler.libraries:
                    f.write(f"    {lib}\n")
                f.write(")\n")

        return file

    def build_extensions(self) -> None:
        """Build all extensions in the project."""
        self.check_extensions_list(self.extensions)

        call_cmake = False
        cmakelists = self.init_cmakelists()
        module_cache: dict[str, bool] = {}
        for ext in self.extensions:
            if isinstance(ext, Extension):
                call_cmake = True
                build_dir = Path(ROOT / self.get_ext_fullpath(ext.name)).parent
                ext.add_to_cmakelists(cmakelists, build_dir, module_cache)
            else:
                super().build_extension(ext)

        config_args = [
            "cmake",
            "-G",
            "Ninja",
            str(cmakelists.parent)
        ]
        build_args = [
            "cmake",
            "--build",
            ".",
            "--config",
            "Debug" if self.debug else "Release"
        ]
        if self.workers:
            build_args += ["--parallel", str(self.workers)]

        print(self.workers)

        if call_cmake:
            try:
                subprocess.check_call(config_args, cwd=cmakelists.parent)
                subprocess.check_call(build_args, cwd=cmakelists.parent)
            except subprocess.CalledProcessError as e:
                if e.stderr:
                    print(e.stderr)

            shutil.move(
                cmakelists.parent / "compile_commands.json",
                ROOT / "compile_commands.json"
            )

    def get_ext_filename(self, fullname: str) -> str:
        """Format the filename of the extension module.

        Parameters
        ----------
        fullname : str
            The name of the extension module.

        Returns
        -------
        str
            The formatted filename of the build product (either a shared library or an
            executable).  If the extension is an executable, the name is returned
            directly.  Otherwise, it will be decorated with a shared library extension
            based on the platform, like normal.

        Notes
        -----
        Overriding this method is required to allow setuptools to correctly copy the
        build products out of the build directory without errors.
        """
        ext = self.ext_map[fullname]
        if getattr(ext, "executable", False):
            return ext.name
        return super().get_ext_filename(fullname)


def setup(
    *args: Any,
    cmdclass: dict[str, Any] | None = None,
    workers: int | None = None,
    **kwargs: Any
) -> None:
    """A custom setup() function that automatically appends the BuildExt command to the
    setup commands.

    Parameters
    ----------
    *args : Any
        Arbitrary positional arguments passed to the setuptools.setup() function.
    cmdclass : dict[str, Any] | None, default None
        A dictionary of command classes to override the default setuptools commands.
        If no setting is given for "build_ext", then it will be set to
        bertrand.setuptools.BuildExt.
    workers : int | None, default None
        The number of parallel workers to use when building extensions.  If set to
        None, then the build will be single-threaded.  This can also be set through
        the command line by supplying either `--workers=NUM` or `-j NUM`.
    **kwargs : Any
        Arbitrary keyword arguments passed to the setuptools.setup() function.
    """
    class BuildExtensions(BuildExt):
        """A private subclass of BuildExt that captures the number of workers to use
        from the setup() call.
        """
        def __init__(self, *a: Any, **kw: Any):
            super().__init__(*a, workers=workers, **kw)

    if cmdclass is None:
        cmdclass = {"build_ext": BuildExtensions}
    elif "build_ext" not in cmdclass:
        cmdclass["build_ext"] = BuildExtensions

    setuptools.setup(*args, cmdclass=cmdclass, **kwargs)
