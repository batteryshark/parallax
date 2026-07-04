# ARTF.CRYPTO_ADDR: Embedded Cryptocurrency Address

## Description

Bitcoin, Ethereum, Monero, or other cryptocurrency wallet addresses present as string literals in source or binary. Identifiable by format-specific patterns: Bitcoin uses base58check encoding (starting with `1`, `3`, or `bc1` for bech32), Ethereum uses `0x`-prefixed 40-character hex strings, Monero uses long base58 strings (starting with `4` or `8`, 95 characters). Other chains have their own format conventions (Litecoin `L`/`M`/`ltc1`, Dogecoin `D`, Solana base58 32-byte keys, etc.). The artifact is the wallet address itself, a payment destination identifier.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | String literals matching cryptocurrency address formats, address validation function calls, constants named `wallet`, `address`, `payout_address`, or similar |
| Static Binary | Yes | Base58-encoded strings of characteristic length in data sections, `0x`-prefixed 40-char hex strings, address-format constants |
| Runtime/Dynamic | Yes | Addresses used in transaction construction, passed to blockchain API calls, written to configuration, or displayed to users |

## Disambiguation

- **vs ARTF.HASH**: Cryptocurrency addresses and hash digests can both appear as hex or base58 strings. The distinction is format: Ethereum addresses are 20 bytes (40 hex chars) with `0x` prefix and optional checksum encoding; SHA-256 digests are 32 bytes (64 hex chars). Bitcoin addresses include a checksum and version byte. Context (variable naming, surrounding API calls) further disambiguates.
- **vs CRPT.***: `ARTF.CRYPTO_ADDR` is the static presence of a wallet address. Cryptographic operations on blockchain data (signing transactions, hashing blocks) are `CRPT.*` atoms. The address is an artifact; the operations are behaviors.

## Structural Relationships

- **Often co-occurs with**: `NETW.HTTP` (address used in blockchain API calls), `XFRM.ENCODE` (address encoded to avoid detection), `XFRM.STRCON` (address assembled from fragments), `FSYS.WRITE` (address written to configuration or clipboard)
- **May imply**: The code interacts with cryptocurrency payment infrastructure, either as a payment receiver, a miner payout target, or a ransom destination

## Notes

Address format identifies the blockchain. A `bc1`-prefixed bech32 string is Bitcoin SegWit. A `0x`-prefixed 40-hex-char string is Ethereum. A 95-character base58 string starting with `4` is Monero. Some formats overlap with other data types, Ethereum addresses resemble truncated hex hashes, and Bitcoin addresses use the same base58 encoding found in IPFS hashes (though with different version bytes). Checksum validation can confirm whether a candidate string is a valid address.
