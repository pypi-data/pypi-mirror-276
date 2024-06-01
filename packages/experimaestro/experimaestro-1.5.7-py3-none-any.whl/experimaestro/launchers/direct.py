from dataclasses import dataclass, field
from functools import cached_property
from typing import Dict, List, Optional
from experimaestro.launcherfinder import (
    LauncherConfiguration,
    LauncherRegistry,
    HostRequirement,
)
from experimaestro.launcherfinder.registry import CPU, GPUList, YAMLDataClass
from experimaestro.launcherfinder.specs import (
    HostSpecification,
)
from experimaestro.scriptbuilder import PythonScriptBuilder
from . import Launcher


class DirectLauncher(Launcher):
    def scriptbuilder(self):
        return PythonScriptBuilder()

    @staticmethod
    def init_registry(registry: LauncherRegistry):
        registry.register_launcher("local", DirectLauncherConfiguration)

    def __str__(self):
        return f"DirectLauncher({self.connector})"


@dataclass
class DirectLauncherConfiguration(YAMLDataClass, LauncherConfiguration):
    connector: str = "connector"
    cpu: CPU = field(default_factory=CPU)
    gpus: GPUList = field(default_factory=GPUList)
    tokens: Optional[Dict[str, int]] = None
    tags: List[str] = field(default_factory=lambda: [])
    weight: int = 0
    disable: bool = False

    @cached_property
    def spec(self) -> HostSpecification:
        return HostSpecification(cpu=self.cpu.to_spec(), cuda=self.gpus.to_spec())

    def get(
        self, registry: LauncherRegistry, requirement: "HostRequirement"
    ) -> Optional[Launcher]:
        if requirement.match(self.spec):
            launcher = DirectLauncher(connector=registry.getConnector(self.connector))
            if self.tokens:
                for token_identifier, count in self.tokens.items():
                    token = registry.getToken(token_identifier)
                    # TODO: handle the case where this is not a CounterToken
                    launcher.addListener(
                        lambda job: job.dependencies.add(token.dependency(count))
                    )
            return launcher

        return None
