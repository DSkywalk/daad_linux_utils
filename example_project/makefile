TARGET_NAME := example
TARGET := $(TARGET_NAME).dsk

PLATFORM := CPC
TERP := DCPCIE.Z80
GFX := BLANK.GRA

SOURCEDIR := src
BASEDIR := $(shell pwd)
SOURCES := $(shell find $(SOURCEDIR)/ -name '*.dsf')

all: $(TARGET)

build/$(TARGET_NAME).dsf: $(SOURCES)
	echo $(SOURCES)
	@mkdir -p build
	predrf.py $(SOURCEDIR)/$(TARGET_NAME).dsf -o build/_$(TARGET_NAME).dsf
	@cp build/_$(TARGET_NAME).dsf build/$(TARGET_NAME).dsf

build/$(TARGET_NAME).json: build/$(TARGET_NAME).dsf
	drf cpc build/$(TARGET_NAME).dsf build/$(TARGET_NAME).json

build/$(TARGET_NAME).DDB: build/$(TARGET_NAME).json
	php ${DAAD_LIB_PATH}/drb.php cpc es build/$(TARGET_NAME).json

build/DAAD.BIN: build/$(TARGET_NAME).DDB
	mcrf build/DAAD.BIN ${DAAD_LIB_PATH}/$(PLATFORM)/$(TERP) build/$(TARGET_NAME).DDB ${DAAD_LIB_PATH}/$(PLATFORM)/$(GFX)

build/DAAD.DSK: build/DAAD.BIN
	@cp -f ${DAAD_LIB_PATH}/CPC/empty.dsk build/_tmp.dsk
	@iDSK build/_tmp.dsk -i build/DAAD.BIN -t 1 | grep 'Ko'
	@cp build/_tmp.dsk build/DAAD.DSK
	@cp -v build/DAAD.DSK $(TARGET_NAME).dsk

build_DSK: build/DAAD.DSK

$(TARGET): build_DSK
	@echo "Done!"

clean:
	rm build/* $(TARGET)

run: build_DSK
	@echo "Running $(TARGET)..."
	@retroarch -L ${HOME}/.config/retroarch/cores/cap32_libretro.so "$(BASEDIR)/$(TARGET)" > /dev/null 2>&1

