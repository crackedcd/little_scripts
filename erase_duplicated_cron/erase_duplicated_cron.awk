#!/bin/awk -f

BEGIN{
    new_arr[0] = "value"
    n = 1
}

{
    cron_content = $0
    #print cron_content
    if (! cron_content in new_arr) {
        new_arr[cron_content] += 1
        if (new_arr[cron_content] <= 1) {
            if (cron_content ~ /\#/) {
                printf "\n"
            }
            printf cron_content"\n"
        }
    }
}

END {
    #    for (i in new_arr) {
    #        print i, new_arr[i]
    #    }
}

