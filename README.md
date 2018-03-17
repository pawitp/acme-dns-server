# ACME DNS Server
This is a very simple DNS server written in Python for serving DNS TXT records
for the purpose of ACME (Let's Encrypt) DNS-01 validation, which is required
for generating wildcard certificates.

The server requires Python 3 and has no additional dependency. It can only
serve TXT record and ignores everything in the query except the domain name.

## Why?
Current solutions for DNS-01 validation generally involves using hook scripts
to allow the ACME client to modify DNS records for the domain using some API
available. However, this is not always feasible or desirable for the
following reasons:

 - **Security**: You may not want your ACME client to be able to modify all
   DNS records.
 - **Speed**: Production DNS servers are often focused on reliability where
   as record update speed is not usually a concern and it may take time for
   record updates to replicate over several server. However, for ACME
   verification, reliability is not a concern (in the off chance that it
   failed, it can be retried without affecting users) but slow update can
   be frustrating to server administrators trying to generate certificates.

## How?
The problem can be fixed by delegating the `_acme-challenge` sub-domain to
ACME DNS server. All this DNS server does is load records from a text
file and serve it as a reply with one line being one TXT records. No caching
or replication is performed, allowing all updates to be reflected right away.

## Usage

 1. First, add NS record to your domain names to delegate it to the server
    running ACME DNS server. You will need to add one record for every domain
    or subdomain you wish to generate certificates for.

    For example:

    | Certificate Name | Sub-domain where NS record is needed |
    | ---------------- | ------------------------------------ |
    | example.com      | _acme-challenge.example.com          |
    | *.example.com    | _acme-challenge.example.com          |
    | www.example.com  | _acme-challenge.www.example.com      |

 2. Run the ACME DNS server. You will need to run it as root or use other
    methods to allow it to bind on port 53.

    `./acme-dns-server.py 53 /opt/records`

    Where `53` is the port to listen on (usually 53) and `/opt/records` is
    the where the script will load DNS records from.

 3. Write a hook for the ACME client you are using to update the DNS record as
    desired. The hook should write to the `/opt/record/$NAME` with one TXT
    record per line. For example, the hook for generating certificates for
    `example.com` should write to `/opt/records/_acme-challenge.example.com`.

    An example hook for the [dehydrated](https://github.com/lukas2511/dehydrated)
    client is provided in the `example_hooks` directory.

 4. Run your ACME client to generate the certificate.
