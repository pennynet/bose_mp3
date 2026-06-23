#!/bin/tclsh
package require ncgi

set uploadDir "/usr/local/addons/bose_mp3/www/mp3"

::ncgi::parse

set file [::ncgi::value file]

set file [file tail $file]

if {$file ne ""} {
    set target [file join $uploadDir $file]
    if {[file exists $target]} {
        file delete -force $target
    }
}

::ncgi::redirect "index.cgi"
