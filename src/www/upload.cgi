#!/bin/tclsh

package require ncgi

set uploadDir "/usr/local/addons/bose_mp3/www/mp3"

puts "Content-Type: text/html"
puts ""

if {[catch {

    ::ncgi::parse

    set clientFile [::ncgi::importFile -client mp3file]

    if {$clientFile eq ""} {
        error "no file picked."
    }

    set baseName [file tail $clientFile]

    if {![string match -nocase "*.mp3" $baseName]} {
        error "only *.MP3 allowed."
    }

    set tmpFile [::ncgi::importFile -server mp3file]
    set targetFile [file join $uploadDir $baseName]

    file copy -force $tmpFile $targetFile

    puts "<html><body>"
    puts "<h2>upload ok</h2>"
    puts "<p>file saved:</p>"
    puts "<b>$baseName</b><br><br>"
    puts "<a href=\"index.html\">back</a>"
    puts "</body></html>"

} err]} {

    puts "<html><body>"
    puts "<h2>error</h2>"
    puts "<pre>$err</pre>"
    puts "<a href=\"index.html\">back</a>"
    puts "</body></html>"
}
