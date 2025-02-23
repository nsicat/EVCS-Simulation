# MITM Attack on EVCS Systems

## Step 1: Set Up Virtual Machines

Choose two Virtual Machines (VMs):

- **VM 1**: Runs the `EVCS.py` script (Electric Vehicle Charging Station).
- **VM 2**: Runs the `CSMS.py` script (Charging Station Management System).

---

## Step 2: Modify EVCS and CSMS Scripts

### **EVCS Script (`EVCS.py`)
1. Open the `EVCS.py` script.
2. Locate the `__init__` function.
3. Modify the `self.host` attribute to point to the CSMS VM's IP address:

   ```python
   self.host = "<CSMS_VM_IP_ADDRESS>"
   ```

### **CSMS Script (`CSMS.py`)
1. Open the `CSMS.py` script.
2. Locate the `__init__` function.
3. Modify the `self.host` attribute to bind to all network interfaces:

   ```python
   self.host = "0.0.0.0"
   ```

This allows it to accept connections from any IP address.

---

## Step 3: Set Up Kali Linux for MITM Attack

### **Enable IP Forwarding**
Open a terminal in Kali Linux and run the following command to enable IP forwarding:

```bash
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward
```

Verify that IP forwarding is enabled:

```bash
cat /proc/sys/net/ipv4/ip_forward
```

If enabled, the output should be `1`.

### **Configure Ettercap for ARP Poisoning**
1. Open Ettercap GUI in Kali Linux.
2. Scan the network to identify the IP addresses of the **EVCS VM** and **CSMS VM**.
3. Assign:
   - **EVCS VM IP** → Target 1
   - **CSMS VM IP** → Target 2
4. Start **ARP Poisoning** on the targets.
5. Begin capturing and analyzing the communication between the two VMs.

---

## Conclusion
By following these steps, you can intercept and analyze the communication between an Electric Vehicle Charging Station and its Management System. This allows you to study potential vulnerabilities and explore security improvements.
