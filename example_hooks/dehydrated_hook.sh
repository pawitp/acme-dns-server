#!/usr/bin/env bash
# Please note that this example script requires HOOK_CHAIN=no (default behavior)

deploy_challenge() {
    local DOMAIN="${1}" TOKEN_FILENAME="${2}" TOKEN_VALUE="${3}"

    echo $TOKEN_VALUE >> /opt/records/_acme-challenge.$DOMAIN
}

exit_hook() {
    rm -f /opt/records/*
}

HANDLER="$1"; shift
if [[ "${HANDLER}" =~ ^(deploy_challenge|exit_hook)$ ]]; then
    "$HANDLER" "$@"
fi
