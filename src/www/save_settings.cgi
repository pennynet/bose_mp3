#!/bin/tclsh
package require ncgi

set cfgFile "/usr/local/addons/bose_mp3/etc/bose_mp3-settings.conf"

::ncgi::parse

set fh [open $cfgFile w]

for {set i 1} {$i <= 100} {incr i} {
    set name [string trim [::ncgi::value speaker_name_$i]]
    set ip [string trim [::ncgi::value speaker_ip_$i]]

    if {$name ne "" && $ip ne ""} {
        puts $fh "$name=$ip"
    }
}

puts $fh ""
puts $fh "ANNOUNCE_VOLUME=[::ncgi::value ANNOUNCE_VOLUME]"
puts $fh "WAIT=[::ncgi::value WAIT]"

close $fh

::ncgi::redirect "index.cgi"
