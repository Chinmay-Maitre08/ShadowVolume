# ShadowVolume
Ransomware Resilience Script:
The provided Python script is designed to enhance resilience against ransomware attacks by continuously monitoring and securing a specified file. It creates encrypted backups, tracks changes, and utilizes Volume Shadow Copy Service (VSS) for snapshot creation.

Backup and Encryption Logic:

When the monitored file is modified, the script triggers the creation of an encrypted backup in a designated backup directory.
Additionally, the original content of the file is saved in a separate directory for reference and recovery purposes.
The script employs the cryptography library to encrypt and decrypt file content using the Fernet symmetric encryption scheme, enhancing the security of the backup process.
Password Protection and Cache Mechanism:

The script requires a password for accessing and creating backups. It incorporates a password cache mechanism to avoid frequent password prompts within a specified duration.
The encryption key used for securing the backups is dynamically generated upon successful password verification, providing an additional layer of security against unauthorized access.





