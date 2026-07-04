# NETW.DECENTRAL: Decentralized / Blockchain Communication

## Description

Communicates via decentralized networks: blockchain networks (Bitcoin, Ethereum, Solana), decentralized storage (IPFS), smart contracts, or decentralized compute platforms (Internet Computer Protocol canisters, Ethereum contracts, Solana programs). The defining structural property is that the infrastructure is distributed across independent nodes with no single controlling entity. There is no single operator, registrar, or hosting provider that controls the communication channel.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | Blockchain client library imports (`web3.js`, `ethers.js`, `@dfinity/agent`), smart contract addresses, IPFS CIDs, canister IDs, RPC endpoint URLs for blockchain nodes, wallet/signing operations |
| Static Binary | Partial | Blockchain library imports, contract addresses in data sections, IPFS hash patterns, ICP canister ID patterns |
| Runtime/Dynamic | Yes | Connections to blockchain RPC endpoints, IPFS gateway requests, smart contract call transactions, canister query/update calls |

## Disambiguation

- **vs NETW.HTTP**: Blockchain interactions often use HTTP/JSON-RPC as transport. `NETW.DECENTRAL` applies when the destination is a decentralized network, even if the transport is HTTP. A JSON-RPC call to an Ethereum node is `NETW.DECENTRAL` (and `NETW.HTTP` for the transport).
- **vs CRPT.WALLET / CRPT.***: Cryptographic operations related to blockchain (signing transactions, key management) fall under `CRPT.*`. The network communication with the blockchain itself is `NETW.DECENTRAL`. A wallet signing a transaction is `CRPT.*`. Submitting that signed transaction to the network is `NETW.DECENTRAL`.

## Structural Relationships

- **Often co-occurs with**: `CRPT.*` (transaction signing, key management), `ARTF.URL` (RPC endpoint URLs), `XFRM.ENCODE` (data encoded for blockchain storage, limited block/transaction sizes require compact encoding)
- **May imply**: The code interacts with infrastructure that persists data or state beyond any single operator's control

## Notes

Key structural identifiers to capture: smart contract addresses (Ethereum: 0x-prefixed 40-hex-char), canister IDs (ICP: text-encoded principal), IPFS CIDs (Qm... or bafy...), blockchain RPC endpoints. These identifiers are the decentralized equivalent of domain names. They point to specific resources on the decentralized network. Content published to decentralized networks persists as long as the network operates and is replicated across independent nodes.
