# Launcher registry

from dataclasses import dataclass
import itertools
from types import new_class
from typing import ClassVar, Dict, List, Optional, Set, Type, Union
from experimaestro import Annotated
from pathlib import Path
import typing
import pkg_resources
import humanfriendly
import yaml
from yaml import Loader, Dumper
from experimaestro.utils import logger
from experimaestro.utils.yaml import (
    Initialize,
    YAMLDataClass,
    YAMLException,
    YAMLList,
    add_path_resolvers,
)

from .base import LauncherConfiguration, ConnectorConfiguration, TokenConfiguration
from .specs import CPUSpecification, CudaSpecification, HostRequirement

if typing.TYPE_CHECKING:
    from experimaestro.launchers import Launcher
    from experimaestro.tokens import Token


class LauncherNotFoundError(Exception):
    pass


@dataclass
class GPU(YAMLDataClass):
    """Represents a GPU"""

    model: str
    count: int
    memory: Annotated[int, Initialize(humanfriendly.parse_size)]

    def to_spec(self):
        return [CudaSpecification(self.memory, self.model) for _ in range(self.count)]


class GPUList(YAMLList[GPU]):
    """Represents a list of GPUs"""

    def __repr__(self):
        return f"GPUs({super().__repr__()})"

    def to_spec(self) -> List[CudaSpecification]:
        return list(itertools.chain(*[gpu.to_spec() for gpu in self]))


@dataclass
class CPU(YAMLDataClass):
    """Represents a CPU"""

    memory: Annotated[int, Initialize(humanfriendly.parse_size)] = 0
    cores: int = 1

    def to_spec(self):
        return CPUSpecification(self.memory, self.cores)


@dataclass
class Host(YAMLDataClass):
    name: str
    gpus: List[GPU]
    launchers: List[str]


Launchers = Dict[str, List[LauncherConfiguration]]
Connectors = Dict[str, Dict[str, ConnectorConfiguration]]
Tokens = Dict[str, Dict[str, TokenConfiguration]]


def new_loader(name: str) -> Type[Loader]:
    return new_class("LauncherLoader", (yaml.FullLoader,))  # type: ignore


def load_yaml(loader_cls: Type[Loader], path: Path):
    if not path.is_file():
        return None

    logger.warning(
        "Using YAML file to configure launchers is deprecated. Please remove %s using launchers.py",
        path,
    )
    logger.debug("Loading %s", path)
    with path.open("rt") as fp:
        loader = loader_cls(fp)
        try:
            return loader.get_single_data()
        finally:
            loader.dispose()


def unknown_error(loader: Loader, node):
    raise YAMLException(
        "",
        node.start_mark.name,
        node.start_mark.line,
        node.start_mark.column,
        f"No handler defined for key {node}",
    )


class LauncherRegistry:
    INSTANCES: ClassVar[Dict[Path, "LauncherRegistry"]] = {}
    CURRENT_CONFIG_DIR: ClassVar[Optional[Path]] = None

    @staticmethod
    def instance():
        """Returns an instance for the current configuration directory"""
        if LauncherRegistry.CURRENT_CONFIG_DIR is None:
            LauncherRegistry.CURRENT_CONFIG_DIR = Path(
                "~/.config/experimaestro"
            ).expanduser()

        if LauncherRegistry.CURRENT_CONFIG_DIR not in LauncherRegistry.INSTANCES:
            LauncherRegistry.INSTANCES[
                LauncherRegistry.CURRENT_CONFIG_DIR
            ] = LauncherRegistry(LauncherRegistry.CURRENT_CONFIG_DIR)

        return LauncherRegistry.INSTANCES[LauncherRegistry.CURRENT_CONFIG_DIR]

    @staticmethod
    def set_config_dir(config_dir: Path):
        LauncherRegistry.CURRENT_CONFIG_DIR = config_dir

    def __init__(self, basepath: Path):
        self.LauncherLoader: Type[Loader] = new_loader("LauncherLoader")
        self.ConnectorLoader: Type[Loader] = new_loader("ConnectorLoader")
        self.TokenLoader: Type[Loader] = new_loader("TokenLoader")
        self.Dumper: Type[Dumper] = new_class("CustomDumper", (Dumper,), {})
        self.find_launcher_fn = None

        # Add safeguards
        add_path_resolvers(
            self.LauncherLoader,
            [],
            Dict[str, LauncherConfiguration],
            dumper=self.Dumper,
        )

        # Use entry points for connectors and launchers
        for entry_point in pkg_resources.iter_entry_points("experimaestro.connectors"):
            entry_point.load().init_registry(self)

        for entry_point in pkg_resources.iter_entry_points("experimaestro.launchers"):
            entry_point.load().init_registry(self)

        for entry_point in pkg_resources.iter_entry_points("experimaestro.tokens"):
            entry_point.load().init_registry(self)

        # Register the find launcher function if it exists
        launchers_py = basepath / "launchers.py"
        if launchers_py.is_file():
            logger.info("Loading %s", launchers_py)

            from importlib import util

            spec = util.spec_from_file_location("xpm_launchers_conf", launchers_py)
            module = util.module_from_spec(spec)
            spec.loader.exec_module(module)

            self.find_launcher_fn = getattr(module, "find_launcher", None)
            if self.find_launcher_fn is None:
                logger.warn("No find_launcher() function was found in %s", launchers_py)

        # Read the configuration file
        launchers: Launchers = (
            load_yaml(self.LauncherLoader, basepath / "launchers.yaml") or {}
        )
        self.launchers = sorted(
            itertools.chain(*launchers.values()), key=lambda launcher: -launcher.weight
        )

        self.connectors: Connectors = (
            load_yaml(self.ConnectorLoader, basepath / "connectors.yaml") or {}
        )
        self.tokens: Tokens = (
            load_yaml(self.TokenLoader, basepath / "tokens.yaml") or {}
        )

    def register_launcher(self, identifier: str, cls: Type[YAMLDataClass]):
        add_path_resolvers(
            self.LauncherLoader, [identifier, None], cls, dumper=self.Dumper
        )

    def register_connector(self, identifier: str, cls: Type[YAMLDataClass]):
        add_path_resolvers(
            self.ConnectorLoader, [identifier, None], cls, dumper=self.Dumper
        )

    def register_token(self, identifier: str, cls: Type[YAMLDataClass]):
        add_path_resolvers(self.TokenLoader, [identifier], cls, dumper=self.Dumper)

    def getToken(self, identifier: str) -> "Token":
        for tokens in self.tokens.values():
            if identifier in tokens:
                return tokens[identifier].create(self, identifier)
        raise AssertionError(f"No token with identifier {identifier}")

    def getConnector(self, identifier: str):
        for connectors in self.connectors.values():
            if identifier in connectors:
                return connectors[identifier].create(self)

        # Default local connector
        if identifier == "local":
            from experimaestro.connectors.local import LocalConnector

            return LocalConnector.instance()

        raise AssertionError(f"No connector with identifier {identifier}")

    def find(
        self, *input_specs: Union[HostRequirement, str], tags: Set[str] = set()
    ) -> Optional["Launcher"]:
        """ "
        Arguments:
            spec: The processing requirements
            tags: Restrict the launchers to those containing one of the specified tags
        """

        if len(self.launchers) == 0 and self.find_launcher_fn is None:
            logger.info("No launchers.yaml file: using local host ")
            from experimaestro.launchers.direct import DirectLauncher
            from experimaestro.connectors.local import LocalConnector

            return DirectLauncher(LocalConnector.instance())

        # Parse specs
        from .parser import parse

        specs = []
        for spec in input_specs:
            if isinstance(spec, str):
                specs.extend(parse(spec))
            else:
                specs.append(spec)

        # Use launcher function
        if self.find_launcher_fn is not None:
            for spec in specs:
                if launcher := self.find_launcher_fn(spec, tags):
                    return launcher

        # We have registered launchers
        for spec in specs:
            for handler in self.launchers:
                if (not tags) or any((tag in tags) for tag in handler.tags):
                    if launcher := handler.get(self, spec):
                        return launcher
        return None


def find_launcher(
    *specs: Union[HostRequirement, str], tags: Set[str] = set()
) -> "Launcher":
    """Find a launcher matching a given specification"""
    launcher = LauncherRegistry.instance().find(*specs, tags=tags)
    if not launcher:
        raise LauncherNotFoundError(
            f"No launcher with specification: {specs}."
            "Please refer to the documentation at the following URL: "
            "https://experimaestro-python.readthedocs.io/en/latest/launchers/"
        )
    return launcher
