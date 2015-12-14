#!/bin/bash

if [[ $(crontab -l | fgrep '/usr/local/config_agent/bin/chk_agent.sh' | wc -l) -gt 1 ]]
then
    echo yes
    # backup old crontab.
    /bin/cp -arf /var/spool/cron/root /var/spool/cron/root.20151127.1.bak
    # import old crontab as tmp-crontab, process tmp-crontab to new-crontab by awk, install new-crontab.
    crontab -l > /tmp/crontab-tmp.file && ./erase_duplicated_cron.awk /tmp/crontab-tmp.file > /tmp/crontab-new.file && crontab /tmp/crontab-new.file
    # clear tmp files.
    /bin/rm -f /tmp/crontab-tmp.file /tmp/crontab-new.file
fi

