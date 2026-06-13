#!/usr/bin/env sh

#Hook for use with acme.sh (https://github.com/acmesh-official/acme.sh) according to https://github.com/acmesh-official/acme.sh/wiki/dnsapi2#dns_myapi 
# Place in .acme.sh/dns_pawitp_acme.sh and use by specifying --dns dns_pawitp_acme when running acme.sh

basedir="/opt/records/"


#Usage: dns_pawitp_acme_add   _acme-challenge.www.domain.com   "XKrxpRBosdIKFzxW_CT3KLZNf6q0HG9i01zxXp5CPBs"
dns_pawitp_acme_add() {
    fulldomain=$1
    txtvalue=$2
    _info "Using pawitp_acme-dns"
    _debug "fulldomain $fulldomain"
    _debug "txtvalue $txtvalue"

    echo ${txtvalue} >> ${basedir}${fulldomain}
}


dns_pawitp_acme_rm() {
    fulldomain=$1
    txtvalue=$2
    _info "Using pawitp_acme-dns"
    _debug "fulldomain $fulldomain"
    _debug "txtvalue $txtvalue"

    # Delete file if it exists and only has one/zero lines
    if [ -f ${basedir}${fulldomain} ]; then
        if [[ $(wc -l < ${basedir}${fulldomain}) -ge 1 ]]; then
            sed -i "/${txtvalue}/d" ${basedir}${fulldomain}
        fi
	if [[ $(wc -l < ${basedir}${fulldomain}) -lt 1 ]]; then
            rm ${basedir}${fulldir}
        fi
    fi
}

