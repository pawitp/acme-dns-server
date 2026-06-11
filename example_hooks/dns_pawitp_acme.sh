#!/usr/bin/env sh

#Hook for use with acme.sh (https://github.com/acmesh-official/acme.sh) according to https://github.com/acmesh-official/acme.sh/wiki/dnsapi2#dns_myapi 
# Place in .acme.sh/dns_pawitp_acme.sh and use by specifying --dns dns_pawitp_acme when running acme.sh


#Usage: dns_pawitp_acme_add   _acme-challenge.www.domain.com   "XKrxpRBosdIKFzxW_CT3KLZNf6q0HG9i01zxXp5CPBs"
dns_pawitp_acme_add() {
    fulldomain=$1
    txtvalue=$2
    _info "Using pawitp_acme-dns"
    _debug "fulldomain $fulldomain"
    _debug "txtvalue $txtvalue"

    echo ${txtvalue} >> /opt/records/${fulldomain}
}


dns_pawitp_acme_rm() {
    fulldomain=$1
    txtvalue=$2
    _info "Using pawitp_acme-dns"
    _debug "fulldomain $fulldomain"
    _debug "txtvalue $txtvalue"

    sed -i "/${txtvalue}/d" /opt/records/${fulldomain}
}

