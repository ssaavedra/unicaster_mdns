from dnslib import CLASS, RR, QTYPE, A, AAAA

mdns_domain = '.local.'

forward_dns_host = '1.1.1.1'
forward_dns_port = 53
forward_dns_tcp = False


static_entries = {
    'my.server.example.': [
        RR("my.server.example.", QTYPE.A, CLASS.IN, ttl=0, rdata=A('127.0.0.1')),
        RR("my.server.example.", QTYPE.AAAA, CLASS.IN, ttl=0, rdata=AAAA('fe80::1')),
    ]
}
