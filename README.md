# improved_DNS_lookup
**Python script for DNS**

#Usage

**Hostname lookup**

```bash
./improved_DNS_lookup.py --hostname www.google.gr                                                                                                                                       1 ↵  1383  14:53:56 
www.google.gr
172.217.23.67
2a00:1450:4002:800::2003
```

**Enhanced Hostname look**

Resolves the actual hosts corresponding to each ip address 

```bash
./improved_DNS_lookup.py -v --hostname www.google.gr                                                                                                                                      ✓  1384  14:54:15 
www.google.gr
172.217.23.67 ---> mil04s22-in-f67.1e100.net
2a00:1450:4002:800::2003 ---> mil04s22-in-x03.1e100.net
```

**Resolve ip address back to host name**

```bash
./improved_DNS_lookup.py -v --ips 2a00:1450:4002:800::2003                                                                                                                                ✓  1385  14:58:06 
mil04s22-in-x03.1e100.net
```

```bash
./improved_DNS_lookup.py --ips 172.217.23.67                                                                                                                                              ✓  1387  14:59:31 
mil04s22-in-f67.1e100.net
```



