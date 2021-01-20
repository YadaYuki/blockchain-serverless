REGION := ap-northeast-1
PREFIX := blockchain
ENV := dev
PROFILE := yadayuki

s3:
	aws cloudformation --profile $(PROFILE) validate-template \
	  --template-body file://templates/s3.yml && \
	aws cloudformation --profile $(PROFILE) deploy \
		--template-file ./templates/s3.yml \
		--stack-name $(PREFIX)-$(ENV)-s3 \
		--region $(REGION) \
		--parameter-overrides \
		Prefix=$(PREFIX) \
		Environment=$(ENV)

clear:
	aws cloudformation --profile $(PROFILE) delete-stack --stack-name $(PREFIX)-$(ENV)-s3