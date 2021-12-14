#  globale Konfigurationsvariablen
global spalten groesse leeresFeld
set spalten 3
set groesse 400
set leeresFeld "PuzzleTeil:[ expr $spalten-1 ]:[expr $spalten-1]" 

proc BilderLesen { } {
    global BilderListe groesse
    set BilderListe {}
    cd Gif
    foreach File [ glob *.gif ] {
	set bildname [ lindex [ split $File . ] 0 ]
	catch { 
	    image create photo ${bildname}All -file $File \
	    -width $groesse -height $groesse
	    lappend BilderListe $bildname
	}
    }
    cd ..
}

proc SetzeBild { bild } {
    image create photo PuzzleAll
    PuzzleAll copy ${bild}All
}

proc SpielfeldZeichnen {} {
    global spalten groesse leeresFeld BilderListe
    catch { destroy .spielfeld .mischen .neu}
    # erzeuge das Spielfeld
    canvas .spielfeld \
        -width [ expr $groesse+10 ]  -height  [ expr $groesse+10 ] -bg grey
    wm title . "Puzzle" 
    wm geometry . +500+0
    pack .spielfeld
# hole das gesamte Bild
#    image create photo PuzzleAll -file maria.png -width $groesse -height $groesse
# Verkleinere es f?r die Vorlagenvorschau
    image create photo PuzzleSmall
    PuzzleSmall copy PuzzleAll -subsample 2
    catch { destroy .vorlage }
    toplevel .vorlage
    wm title .vorlage "Vorlage"
    canvas .vorlage.bild -width 200 -height 200
    .vorlage.bild create image 0 0 -anchor nw -image PuzzleSmall
    pack .vorlage.bild
# Zerteile das Bild in die einzelnen Kacheln
    for { set zeile 0 } { $zeile<$spalten } { incr zeile } {
	for { set spalte 0 } { $spalte<$spalten } { incr spalte } {
	    image create photo PuzzleTeil:$spalte:$zeile 
	    set upperleftx [ expr $spalte*$groesse/$spalten ]
	    set upperlefty [ expr $zeile*$groesse/$spalten  ]
	    set lowerrightx [ expr ($spalte+1)*$groesse/$spalten ] 
	    set lowerrighty [ expr ($zeile+1)*$groesse/$spalten  ]
	    PuzzleTeil:$spalte:$zeile copy PuzzleAll \
		-from $upperleftx $upperlefty $lowerrightx $lowerrighty
	    set image [ .spielfeld create image \
			    [ expr $upperleftx+$spalte*5 ] [ expr $upperlefty+$zeile*5 ] \
			    -image PuzzleTeil:$spalte:$zeile -anchor nw \
			    -tag PuzzleTeil:$spalte:$zeile ]
	    # Normaler Klick funktioniert nur neben leerem Feld
	    .spielfeld bind $image <ButtonPress-1> "geschuetzterKlick $spalte $zeile"
	    # Rechter Schummelknopf vertauscht beliebiges Feld mit leerem Feld
	    .spielfeld bind $image <ButtonPress-3> "Klick $spalte $zeile"
	}
    }
    # Jetzt noch ein Leeres Feld
    image create photo Leer -width [ expr $groesse/$spalten ] -height  [ expr $groesse/$spalten ]
    .spielfeld itemconfigure $image -image Leer
    set letztesFeld [ .spielfeld itemcget $image -tag ]
    set leeresFeld $letztesFeld
    button .mischen -text Mischen -command "Mischen 500"
    button .neu -text Neu -command SpielfeldZeichnen
    pack .mischen .neu -side left
    foreach Bild $BilderListe {
	image create photo ${Bild}XS
	${Bild}XS copy ${Bild}All -subsample 10
	catch { destroy .vorlage.bild${Bild} }
	button .vorlage.bild${Bild} \
	    -command "SetzeBild $Bild;SpielfeldZeichnen" \
	    -image ${Bild}XS
	pack .vorlage.bild${Bild} -side left
    }
}

proc Klick { spalte zeile } { 
# Klick in irgendein Feld tauscht es mit dem leeren Feld
    global leeresFeld
#    puts "Klickt in $spalte $zeile"
    tauscheFelder  PuzzleTeil:$spalte:$zeile $leeresFeld
# Das fr?here Feld ist jetzt leer
    set leeresFeld PuzzleTeil:$spalte:$zeile
}
proc geschuetzterKlick { spalte zeile } {
# Klick nur erlaubt, wenn das Feld ein Nachbarfeld des leeren Feldes ist.
    global leeresFeld
    set liste [ split $leeresFeld ":" ] ;  # Feldname hat die Form MariaTeil:$spalte:$zeile
    set leereSpalte  [ lindex $liste 1 ] ; # hol die Spalte und Zeile des leeren Feldes
    set leereZeile   [ lindex $liste 2 ]
#  ?berpr?fe, ob das Feld direkt neben dem leeren ist
    set differenz [ expr abs($spalte-$leereSpalte)+abs($zeile-$leereZeile) ]
    if { $differenz == 1 } {
	# Wenn ja vertausche die beiden
	Klick  $spalte $zeile
    }
} 

proc tauscheFelder { f1 f2 } {
    global leeresFeld
#    puts ">$f1 >$f2"
    set erstesBild  [ .spielfeld itemcget $f1 -image ]
    set zweitesBild [ .spielfeld itemcget $f2 -image ]
#    puts "-$erstesBild -$zweitesBild"
    .spielfeld itemconfigure $f1 -image $zweitesBild
    .spielfeld itemconfigure $f2 -image $erstesBild
    update
    foreach feld [list $f2 $f1] {
	if { [.spielfeld itemcget $feld -image ] eq "Leer"  } {
	    set leeresFeld $feld
	}
    }
	
}

proc Mischen { wieoft } {
    global spalten leeresFeld
    for {set i 0 } { $i<$wieoft } { incr i } {
	set x1 [expr int($spalten*rand())]
	set y1 [expr int($spalten*rand())]
	geschuetzterKlick $x1 $y1
    }
}
BilderLesen
SetzeBild maria
SpielfeldZeichnen


