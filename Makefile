ZIP_FILE_NAME := lambda_package.zip
SOURCE_DIRECTORY := ./src
TMP_DIRECTORY := ./tmp_package

package:
	@ cp -r $(SOURCE_DIRECTORY) $(TMP_DIRECTORY)
	@ cd $(TMP_DIRECTORY); pip install `pipenv lock -r` -t ./
	@ cd $(TMP_DIRECTORY); zip -r ./$(ZIP_FILE_NAME) .
	@ mv $(TMP_DIRECTORY)/$(ZIP_FILE_NAME) ./
	@ rm -f $(TMP_DIRECTORY)

.PHONY: clean
clean:
	@ rm $(ZIP_FILE_NAME)

