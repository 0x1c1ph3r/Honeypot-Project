# **Honeypot for Attack Detection and Deception**

## **Overview**

This lightweight and customizable honeypot service emulates realistic services on random ports to confuse attackers, detect unauthorized access, and empower defenders. The honeypot provides a simple setup with advanced logging features, making it suitable for integration into SIEMs or IPS solutions. It can be customized to fulfill various use cases, such as creating complex obfuscation strategies and logging IP addresses for further analysis.

## **Installation**

### **Requirements**
- Python 3.6+  
- `socket` module (comes pre-installed with Python)  
- A server or local machine for running the honeypot.

### **Setup**

1. Clone the repository:
    ```bash
    git clone https://github.com/0x1c1ph3r/Honeypot-Project.git
    cd Honeypot-Project
    ```
2. Run the honeypot script:
    ```bash
    python honeypot.py
    ```

## **Customizing the Honeypot**

The honeypot is highly customizable, and you can modify the following:

- **Service List**: Add more services to the `services` dictionary, defining the name, banner, and port range.
- **Port Range**: Adjust the random port range for each service in the configuration.
- **Logging**: Set up custom logging options in the `log_ip()` function to integrate with your SIEM or IPS solutions.
  
Example:
```python
services = {
    'FTP': {'banner': '220 Welcome to FTP Server', 'ports': range(21, 30)},
    'HTTP': {'banner': 'HTTP/1.1 200 OK', 'ports': range(80, 90)},
    # Add more services as needed
}
```

## **Practical Use Cases**

- **Obfuscating Real Services**: Deploy fake services on standard ports like 21 for FTP and 80 for HTTP, while running real services on random ports.
- **Windows Service Simulation on Linux**: Use Windows-based service banners on Linux machines to mislead attackers scanning for OS-specific vulnerabilities.
- **Logging for Threat Detection**: Integrate the logging features with your SIEM tool to trigger alerts based on suspicious activities, such as repeated connection attempts on fake services.
