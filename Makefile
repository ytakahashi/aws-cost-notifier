ZIP_FILE_NAME := lambda_package.zip
SOURCE_DIRECTORY := ./src
TMP_DIRECTORY := ./tmp_package

S3_BUCKET_NAME = cost-check-lambda

.DEFAULT_GOAL := deploy-file

.PHONY: deploy-file
deploy-file: zip yml

zip:
	@ cp -r $(SOURCE_DIRECTORY) $(TMP_DIRECTORY)
	@ cd $(TMP_DIRECTORY); pip install `pipenv lock -r` -t ./
	@ cd $(TMP_DIRECTORY); zip -r ./$(ZIP_FILE_NAME) .
	@ mv $(TMP_DIRECTORY)/$(ZIP_FILE_NAME) ./
	@ rm -fr $(TMP_DIRECTORY)

yml:
	@ aws cloudformation package --template-file deploy.yml \
	--s3-bucket $(S3_BUCKET_NAME) \
	--output-template-file deploy-output.yml

.PHONY: clean
clean:
	@ rm $(ZIP_FILE_NAME)

