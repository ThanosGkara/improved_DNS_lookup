#!/usr/bin/python

"""
Author: Athanasios Gkaraliakos
email: a.gkaraliakos@gmail.com

The script is written on python >=2.6

Script to resolve hostnames and ips from DNS

Depends on python-dns " yum install python-dns "

"""

import sys
import argparse
from pprint import pprint
try:
    import dns.resolver
    import dns.reversename
except ImportError:
    print "Plase install python-dns rpm: 'yum install python-dns' "
    sys.exit(1)

# create a new instance named 'my_resolver'
hostname_resolver = dns.resolver.Resolver()


def aliases(hostname):
    cnames = []
    try:
        cname = hostname_resolver.query(hostname, "CNAME")
        # for attr in dir(cnames):
        #     print "obj.%s = %s" % (attr, getattr(cnames, attr))
        # # pprint(vars(cnames))
        # # print ' query qname:', cnames.qname, ' num ans.', len(cnames)
        for rdata in cname:
            # print ' cname target address:', rdata.target
            tmp_name = rdata.target
            cnames.append(str(tmp_name)[:-1])
    except:
        pass

    return cnames


# def hostname_dns_resolver(hostname, iptype):
def hostname_dns_resolver(hostname, v=False):
    """
    This function receives a host name and tries to resolve it via DNS and get the IPv4/IPv6 address/es

    :param hostname: Hostname
    :param v: verbose
    :return: IP addresses found ( IPv4 or IPv6 or both )
    """
    # if iptype not in ['ipv4', 'ipv6', 'ip']:
    #     sys.stderr("Not given ip type ", ' ipv4', ' ipv6', ' ip')
    #     sys.exit(1)

    iplist = []

    hostname = hostname.lower()
    if v:
        alias = aliases(hostname)
        if len(alias) > 0:
            hostname_tmp = hostname + ' ( ' + ' '.join(alias) + ' )'
        else:
            hostname_tmp = hostname
        iplist.append(str(hostname_tmp))
    else:
        iplist.append(str(hostname))

    try:
        ipv4 = hostname_resolver.query(hostname, "A")
        for ip in ipv4:
            iplist.append(str(ip))
    except dns.resolver.NoAnswer:
        iplist.append("IPv4NOTFOUND")
    except dns.resolver.NXDOMAIN:
        iplist.append("IPv4NOTFOUND")
    try:
        ipv6 = hostname_resolver.query(hostname, "AAAA")
        for ip in ipv6:
            iplist.append(str(ip))
    except dns.resolver.NoAnswer:
        iplist.append("IPv6NOTFOUND")
    except dns.resolver.NXDOMAIN:
        iplist.append("IPv6NOTFOUND")
    return iplist


def ip_dns_resolver(ip):

    ip_rev = dns.reversename.from_address(ip)
    try:
        hostname = str(hostname_resolver.query(ip_rev, "PTR")[0])
    except:
        hostname = "NO_HOSTNAME"

    hostname = hostname[:-1]
    return hostname


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('--hostname', nargs='+', help='Define the hostnames you want to resolve ')
    parser.add_argument('--ips', nargs='+', help='Define the ips you want to resolve ')
    parser.add_argument('-v', action='store_true', help='More rich output regarding each machine')

    args = parser.parse_args()

    if args.hostname:
        hostname = args.hostname[0]
        if args.v:
            # del _ips_[0]
            _ips_ = hostname_dns_resolver(hostname, args.v)
            tmp = []
            for i in xrange(1, len(_ips_)):
                if 'NOTFOUND' not in _ips_[i]:
                    tmp.append(ip_dns_resolver(_ips_[i]))
            for i in xrange(len(tmp)):
                _ips_[i+1] = _ips_[i+1] + ' ---> ' + tmp[i]
            del tmp
        else:
            _ips_ = hostname_dns_resolver(hostname)
        print '\n'.join(map(str, _ips_))

    elif args.ips:
        print ip_dns_resolver(args.ips[0])
    else:
        print parser.print_usage()
        sys.exit(1)

if __name__ == '__main__':
    main()
