# NETW.FTP: FTP/SFTP/SCP

## Description

Transfers files using FTP, SFTP, or SCP protocols. Encompasses direct FTP client connections, SFTP over SSH, and SCP file copies. These protocols are purpose-built for file transfer, distinct from general HTTP uploads/downloads or raw socket data exchange.

## Detection Surface

| Method | Observable? | What You See |
|---|---|---|
| Static Source | Yes | FTP/SFTP library imports (`ftplib`, `paramiko`, `ssh2`, `scp`), FTP server addresses and ports (21, 22), file path parameters, transfer direction (put/get) |
| Static Binary | Partial | FTP library imports, protocol string constants (`USER`, `PASS`, `STOR`, `RETR`), server address literals |
| Runtime/Dynamic | Yes | FTP control connections on port 21, data connections on negotiated ports, SFTP/SCP over SSH on port 22, file transfer traffic |

## Disambiguation

- **vs NETW.HTTP**: HTTP can transfer files (uploads, downloads). `NETW.FTP` applies when FTP, SFTP, or SCP protocols are used specifically. The protocol choice is the distinguishing factor.
- **vs NETW.SOCKET**: FTP uses sockets internally, but `NETW.FTP` applies when a recognized file transfer protocol is in use. Raw socket operations that implement a custom file transfer mechanism are `NETW.SOCKET`.

## Structural Relationships

- **Often co-occurs with**: `CRED.*` (FTP/SFTP authentication credentials), `FSYS.READ` / `FSYS.WRITE` (local files being transferred), `ARTF.IP` / `ARTF.URL` (server addresses)
- **May imply**: FTP/SSH credentials exist somewhere in the artifact

## Notes

FTP (unencrypted) transmits credentials and data in cleartext. SFTP and SCP encrypt the transfer over SSH. The protocol variant is a structural property (FTP vs. SFTP vs. SCP) that affects what's observable through network analysis.
