# template_autofill 
A web service that fills PPTX template with Excel data. \
Output is one filled joint presentation. \
[Not working, domain name expired] http://www.pptautofill.ru

# Technical details
Application based on event-driven architecture and can be deployed on AWS (uses services: Lambda, S3, API Gateway). \
To work with PowerPoint files it uses python-pptx library.

# Useful AWS Lambda developement links
Upload file from AWS Lambda to S3: https://www.youtube.com/watch?v=vXiZO1c5Sk0 \
Lambda+S3+DynamoDB+IAM https://aws.amazon.com/ru/getting-started/hands-on/build-web-app-s3-lambda-api-gateway-dynamodb/ \
Build lambda layers for Python dependencies https://docs.aws.amazon.com/lambda/latest/dg/python-package.html
