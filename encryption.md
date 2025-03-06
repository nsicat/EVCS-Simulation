# Secure EV Charging System with Self-Signed TLS Certificates

This guide provides step-by-step instructions for setting up TLS encryption between an **EV Charging Station (EVCS)** and a **Charging Station Management System (CSMS)** using self-signed certificates.

## Prerequisites

- Two separate virtual machines (VMs) for **EVCS** and **CSMS**.
- OpenSSL installed on both VMs.
- Basic knowledge of Linux command-line operations.

---

## Step 1: Generate Self-Signed Certificates

### Generate Certificate for EVCS


Run the following command inside the **EVCS VM**:

```sh
openssl req -x509 -newkey rsa:4096 -keyout evcs_key.pem -out evcs_cert.pem -days 365 -nodes -subj "/CN=EVCS"
```
### Generate Certificate for CSMS

```sh
openssl req -x509 -newkey rsa:4096 -keyout csms_key.pem -out csms_cert.pem -days 365 -nodes -subj "/CN=CSMS"
```

## Step 2: Exchange Certificates

### Transfer the EVCS certificate to CSMS

On the EVCS VM, copy evcs_cert.pem to the CSMS VM using SCP:

```sh
scp evcs_cert.pem user@csms-vm:/path/to/store/
```

### Transfer the CSMS certificate to EVCS

On the CSMS VM, copy csms_cert.pem to the EVCS VM using SCP:

```sh
scp csms_cert.pem user@evcs-vm:/path/to/store/
```

Make sure that the TEVCS.py on line(25) is set up correctly in the line for server_host = "Certificate Name"  Certificate Name = CSMS. 