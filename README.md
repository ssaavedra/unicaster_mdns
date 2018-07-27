Unicaster mDNS
=============

This project came to existence mainly because Android is broken. Blame Google for that.

Description
-----------

Unicaster mDNS is an application which can receive DNS queries and
depending on the suffix domain:

- intercept them and solve them statically,
- query the multicast DNS (mDNS) for the service,
- query an upstream server

The purpose is mainly allowing Android to resolve mDNS queries by
configuring this application as the network's DNS, while still
resolving outside queries by the upstream.

Limitations
-----------

The current work is not compliant with some queries, such as ANY for
the static services and no logic is implemented to handle it in mDNS.

Currently only the IPv4 multicast address is queried. Although most
parts of the code are ready to work with the IPv6 multicast address,
no logic is implemented for choosing protocol.


How it works
------------

Multicast DNS works very similarly to DNS, but the queries happen in
the `IN-mDNS` class instead of in the `IN` class. Also, queries are
sent to the Multicast IP `224.0.0.251` (`ff02::fb` in IPv6).

This service changes the returned classes so that the client will
think the answer originated in the `IN` class. Other fields are
returned unchanged.


Contributing
------------

Contributions are welcome. Please send a pull request via GitHub or
reach out directly via email using `git request-pull`.

By making a contribution to this project you certify in good faith
that you meet the Developer's Certificate of Origin 1.1 as written by
the Linux Foundation, that is also available in this repo.


License
-------

Unicaster mDNS - Copyright © 2018 Santiago Saavedra

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
