import dpack
from pydantic import BaseModel
from ethpm_types.contract_type import ContractType
from ape.contracts.base import ContractInstance  # NOTE: different from ethpm


class ApeDpack(BaseModel):
    dpack: dpack.Dpack

    @property
    def contract_types(self) -> dict[str, ContractType]:
        return {name: data.contract_type for name, data in self.dpack.types.items()}

    @property
    def contract_instances(self) -> dict[str, ContractInstance]:
        return {
            name: ContractInstance(
                address=data.address, contract_type=self.contract_types[data.typename]
            )
            for name, data in self.dpack.objects.items()
        }

    def __getattr__(self, name):
        return self.contract_instances.get(name)

    def __dir__(self):
        return super().__dir__() + sorted(self.contract_instances.keys())

    def __repr__(self):
        return f"<ApeDpack contract_types={list(self.contract_types)} contract_instances={list(self.contract_instances)}>"


def load(path):
    return ApeDpack(dpack=dpack.load(path))
