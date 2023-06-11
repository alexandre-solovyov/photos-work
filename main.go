
package main

import (
	"fmt"
	"log"
	"os"
	"github.com/rwcarlsen/goexif/exif"
	"github.com/rwcarlsen/goexif/tiff"
)

type Printer struct{}

func (p Printer) Walk(name exif.FieldName, tag *tiff.Tag) error {
    fmt.Printf("%40s: %s\n", name, tag)
    return nil
}

func main() {
	input := "/home/alex/Pictures/Владимир/IMG_20210508_124707.jpg"
	fmt.Println(input)

	file, err := os.Open(input)
    if err != nil {
        log.Fatal(err)
    }

    data, err := exif.Decode(file)
    if err != nil {
        log.Fatal(err)
    }

    var p Printer
    data.Walk(p)
}
