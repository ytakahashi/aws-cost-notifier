ZIP_FILE_NAME := lambda_package.zip
SOURCE_DIRECTORY := ./src
TMP_DIRECTORY := ./tmp_package

.DEFAULT_GOAL := package

package:
	@ cp -r $(SOURCE_DIRECTORY) $(TMP_DIRECTORY)
	# @ cd $(TMP_DIRECTORY); pip install `pipenv lock -r` -t ./
	@ cd $(TMP_DIRECTORY); zip -r ./$(ZIP_FILE_NAME) .
	@ mv $(TMP_DIRECTORY)/$(ZIP_FILE_NAME) ./
	@ rm -fr $(TMP_DIRECTORY)
	@ printf "%0.s\033[96;1m-\033[m" {1..70}
	@ printf "\n\033[33;1mCreated $(ZIP_FILE_NAME)\033[m\n"

.PHONY: clean
clean:
	@ rm $(ZIP_FILE_NAME)

