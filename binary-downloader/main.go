package main

import (
	"archive/zip"
	"bytes"
	"errors"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"path"

	"github.com/urfave/cli/v2"
)

const BinaryPath = "/usr/local/bin"

type Installer interface {
	Install(binaryName string, content []byte)
}

type ZipInstaller struct {
}

func (i ZipInstaller) Install(binaryName string, content []byte) {
	fmt.Println("Zip installer: ")

	zipReader, err := zip.NewReader(bytes.NewReader(content), int64(len(content)))
	if err != nil {
		log.Fatal(err)
	}

	for _, zipFile := range zipReader.File {
		fmt.Println("Reading file:", zipFile.Name)
		if zipFile.Name != binaryName {
			continue
		}

		unzippedFileBytes, err := readZipFile(zipFile)
		if err != nil {
			log.Println(err)
		}
		BinaryInstaller{}.Install(binaryName, unzippedFileBytes)
	}
}

func readZipFile(zf *zip.File) ([]byte, error) {
	f, err := zf.Open()
	if err != nil {
		return nil, err
	}
	defer f.Close()
	return io.ReadAll(f)
}

type BinaryInstaller struct {
}

func (i BinaryInstaller) Install(binaryName string, content []byte) {
	fmt.Println("Binary installer")

	path := path.Join(BinaryPath, binaryName)
	fmt.Println(path)
	if err := os.WriteFile(path, content, 0755); err != nil {
		log.Fatal(err)
	}
}

func downloadFromURL(url string) ([]byte, error) {
	resp, err := http.Get(url)
	if err != nil {
		return []byte{}, err
	}
	defer resp.Body.Close()
	return io.ReadAll(resp.Body)
}

func mimeTypeToInstaller(mimeType string) (Installer, error) {
	switch mimeType {
	case "application/octet-stream":
		return BinaryInstaller{}, nil
	case "application/zip":
		return ZipInstaller{}, nil
	}
	return nil, errors.New("could not determine content type")
}

func installAction(cCtx *cli.Context) error {
	url := cCtx.String("url")
	name := cCtx.String("name")
	version := cCtx.String("version")
	content, err := downloadFromURL(url)
	if err != nil {
		log.Println(err)
	}
	mimeType := http.DetectContentType(content)
	installer, err := mimeTypeToInstaller(mimeType)
	if err != nil {
		log.Println(err)
	}

	installer.Install(name, content)
	fmt.Println("Content: ", mimeType)
	return nil
}

func main() {
	app := &cli.App{
		Commands: []*cli.Command{
			{
				Name:  "install",
				Usage: "Install binary from given URL",
				Flags: []cli.Flag{
					&cli.StringFlag{
						Name:     "url",
						Usage:    "URL to binary",
						Required: true,
					},
					&cli.StringFlag{
						Name:     "name",
						Usage:    "Binary name that will be installed at /usr/local/bin",
						Required: true,
					},
                    &cli.StringFlag{
						Name:     "version",
						Usage:    "Version of binary",
						Required: true,
					},
				},
				Action: installAction,
			},
		},
	}

	if err := app.Run(os.Args); err != nil {
		log.Fatal(err)
	}
}
