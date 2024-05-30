from dataclasses import dataclass
from typing import Any, Dict

from eulith_web3.eip712_types import Eip712Data, Eip712Domain, Eip712Field


@dataclass
class LightSimulationProposal:
    proposal_id: int
    to_enable: bool
    safe_address: str
    network_id: int
    proposer_sub: str
    safe_owner_sub: str
    status: str

    @classmethod
    def from_json(cls, j: Dict[str, Any]) -> "LightSimulationProposal":
        return cls(**j)


@dataclass
class LightSimulationSubmitResponse:
    proposal: LightSimulationProposal
    approved: bool

    @classmethod
    def from_json(cls, j: Dict[str, Any]) -> "LightSimulationSubmitResponse":
        proposal = LightSimulationProposal.from_json(j["proposal"])
        approved = j["approved"]
        return cls(proposal=proposal, approved=approved)


@dataclass
class LightSimulationHashInput:
    safe_address: str
    chain_id: int
    proposer_id: int
    safe_owner_id: int
    to_enable: bool
    proposal_id: int

    @classmethod
    def from_json(cls, j: Dict[str, Any]) -> "LightSimulationHashInput":
        return cls(**j)

    def typed_data(self) -> Eip712Data:
        types = {
            "EIP712Domain": [
                Eip712Field(name="name", type="string"),
                Eip712Field(name="version", type="string"),
            ],
            "LightSimulationProposalHashInput": [
                Eip712Field(name="safeAddress", type="string"),
                Eip712Field(name="chainId", type="int32"),
                Eip712Field(name="proposerId", type="int32"),
                Eip712Field(name="safeOwnerId", type="int32"),
                Eip712Field(name="toEnable", type="bool"),
                Eip712Field(name="proposalId", type="int32"),
            ],
        }

        payload = Eip712Data(
            types=types,
            primaryType="LightSimulationProposalHashInput",
            domain=Eip712Domain(name="EulithLightSimulationProposal", version="1"),
            message={
                "safeAddress": self.safe_address,
                "chainId": self.chain_id,
                "proposerId": self.proposer_id,
                "safeOwnerId": self.safe_owner_id,
                "toEnable": self.to_enable,
                "proposalId": self.proposal_id,
            },
        )

        return payload
