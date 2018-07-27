#!/usr/bin/env python3
# -*- coding: utf-8 -*-


##############################################################################
# Unicaster mDNS - Copyright © 2018 Santiago Saavedra
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
##############################################################################

from dnslib import CLASS, RR, RDMAP, QTYPE, A, AAAA, DNSRecord, DNSHeader, DNSQuestion
from dnslib.server import DNSServer
from dnslib.intercept import InterceptResolver

import signal, socket, struct, sys, os

from config import mdns_domain, forward_dns_host, forward_dns_port, forward_dns_tcp, static_entries

# Include IN_mDNS class to the dnslib
CLASS.forward[0x8001] = 'IN_mDNS'
CLASS.reverse['IN_mDNS'] = 0x8001


nameserver4 = '224.0.0.251'
nameserver6 = 'ff02::fb'


def get_mdns_socket(family=socket.AF_INET):
    sock = socket.socket(family, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if sys.platform == 'darwin':
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.bind(('', 5353))

    if family is socket.AF_INET:
        mreq4 = struct.pack('4sl', socket.inet_pton(socket.AF_INET, nameserver4), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq4)

    elif family is socket.AF_INET6:
        mreq6 = struct.pack('4sl', socket.inet_pton(socket.AF_INET6, nameserver6), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq6)

    return sock


class Resolver(object):
    def resolve(self, request, handler):
        reply = request.reply()
        qname = request.q.qname

        if static_entries.get(str(qname)):
            # print("Got from static entries")
            for response in static_entries[str(qname)]:
                if request.q.qtype == response.rtype:
                    reply.add_answer(response)
            return reply

        if str(qname).endswith(mdns_domain):
            # print("Querying mDNS")
            return self.resolve_mdns(request, handler)
        else:
            # print("Querying upstream DNS")
            return self.resolve_fwd(request, handler)

    def resolve_fwd(self, request, handler):
        r = InterceptResolver(
            forward_dns_host, forward_dns_port, "1s", [], [], [], timeout=1)
        return r.resolve(request, handler)

    def resolve_mdns(self, request, handler):
        reply = request.reply()
        qname = request.q.qname

        sock = get_mdns_socket()
        d = DNSRecord(DNSHeader(id = 0, bitmap = 0), q = request.q)
        sock.sendto(d.pack(), (nameserver4, 5353))
        # sock.sendto(d.pack(), (nameserver6, 5353))

        while True:
            buf, remote = sock.recvfrom(8192)
            d = DNSRecord.parse(buf)
            success = False
            if (d.header.aa == 1) and (d.header.a > 0):
                for response in d.rr:
                    if str(response.rname) == qname:
                        success = True
                        response.rclass = CLASS.IN
                        reply.add_answer(response)
                        # print(reply)
            if success:
                break
        return reply
            

class TimeoutException(Exception):
    pass

if __name__ == '__main__':
    print("""Unicaster mDNS - Copyright © 2018 Santiago Saavedra
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions; you can see the full license
at https://www.gnu.org/licenses/gpl.html
""".encode('utf-8'))
    resolver = Resolver()
    s = DNSServer(resolver,
                  os.environ.get('DNS_HOST', ''),
                  int(os.environ.get('DNS_PORT', 5053)))
    s.start()
