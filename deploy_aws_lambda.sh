#!/usr/bin/env bash
set -e

# Configuration
FUNCTION_NAME="farmingtools-subsidy-api"
REGION="${AWS_REGION:-ap-south-1}" # Default to Mumbai for lowest latency in India
RUNTIME="python3.11"
HANDLER="lambda_function.lambda_handler"
ROLE_NAME="farmingtools-subsidy-lambda-role"
ZIP_FILE="subsidy_lambda.zip"

echo "=========================================================="
echo "🚀 FarmingTools.in - AWS Lambda Deployment Assistant"
echo "   Region: $REGION (Mumbai)"
echo "   Function: $FUNCTION_NAME"
echo "=========================================================="

# 1. Package the zip file
python3 package_aws_lambda.py

if [ ! -f "$ZIP_FILE" ]; then
    echo "❌ Error: $ZIP_FILE was not created."
    exit 1
fi

# 2. Check for AWS CLI
AWS_CLI="$(which aws 2>/dev/null || echo "/Users/rajputnaresh/.local/bin/aws")"
if [ ! -x "$AWS_CLI" ]; then
    echo "⚠️ AWS CLI not found. You can upload $ZIP_FILE manually in the AWS Console:"
    echo "   1. Open https://console.aws.amazon.com/lambda"
    echo "   2. Select Region: Asia Pacific (Mumbai) ap-south-1"
    echo "   3. Create Function -> Author from scratch -> Python 3.11"
    echo "   4. Code -> Upload from -> .zip file -> Select $ZIP_FILE"
    echo "   5. Configuration -> Function URL -> Create Function URL -> Auth: NONE"
    exit 0
fi

# 3. Check AWS Credentials
if ! "$AWS_CLI" sts get-caller-identity >/dev/null 2>&1; then
    echo ""
    echo "⚠️  AWS CLI is installed, but no active credentials were found."
    echo ""
    echo "To deploy via CLI:"
    echo "  1. Run:  aws configure"
    echo "     (Enter your AWS Access Key, Secret Key, and Region: ap-south-1)"
    echo "  2. Run:  ./deploy_aws_lambda.sh"
    echo ""
    echo "Or deploy via AWS Web Console (Takes 2 minutes):"
    echo "  1. Open: https://ap-south-1.console.aws.amazon.com/lambda/home?region=ap-south-1#/create/function"
    echo "  2. Function name: $FUNCTION_NAME"
    echo "  3. Runtime: Python 3.11 or 3.12 (Architecture: arm64 or x86_64)"
    echo "  4. Click 'Create function'"
    echo "  5. Under 'Code source', click 'Upload from' -> '.zip file' and select: $(pwd)/$ZIP_FILE"
    echo "  6. Go to 'Configuration' tab -> 'Function URL' -> 'Create function URL':"
    echo "     - Auth type: NONE"
    echo "     - Enable CORS: Check the box"
    echo "     - Allow origin: *"
    echo "     - Allow methods: GET, POST, OPTIONS"
    echo "  7. Done! You will get an instant public URL like:"
    echo "     https://xxxxxxxxxxxxxxxx.lambda-url.ap-south-1.on.aws/"
    exit 0
fi

echo "✅ AWS credentials authenticated."

# 4. Check if IAM role exists
ACCOUNT_ID=$("$AWS_CLI" sts get-caller-identity --query Account --output text)
ROLE_ARN="arn:aws:iam::${ACCOUNT_ID}:role/${ROLE_NAME}"

if ! "$AWS_CLI" iam get-role --role-name "$ROLE_NAME" >/dev/null 2>&1; then
    echo "Creating IAM Role: $ROLE_NAME..."
    "$AWS_CLI" iam create-role \
        --role-name "$ROLE_NAME" \
        --assume-role-policy-document '{
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"Service": "lambda.amazonaws.com"},
                    "Action": "sts:AssumeRole"
                }
            ]
        }' >/dev/null

    "$AWS_CLI" iam attach-role-policy \
        --role-name "$ROLE_NAME" \
        --policy-arn "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
    
    echo "Waiting 10s for IAM role replication..."
    sleep 10
fi

# 5. Check if Lambda function exists
if "$AWS_CLI" lambda get-function --function-name "$FUNCTION_NAME" --region "$REGION" >/dev/null 2>&1; then
    echo "Updating existing function code for $FUNCTION_NAME..."
    "$AWS_CLI" lambda update-function-code \
        --function-name "$FUNCTION_NAME" \
        --zip-file "fileb://$ZIP_FILE" \
        --region "$REGION" >/dev/null
else
    echo "Creating new Lambda function: $FUNCTION_NAME in $REGION..."
    "$AWS_CLI" lambda create-function \
        --function-name "$FUNCTION_NAME" \
        --runtime "$RUNTIME" \
        --role "$ROLE_ARN" \
        --handler "$HANDLER" \
        --zip-file "fileb://$ZIP_FILE" \
        --timeout 10 \
        --memory-size 256 \
        --region "$REGION" >/dev/null
fi

# 6. Configure Lambda Function URL (Public HTTPS endpoint with CORS)
echo "Ensuring Function URL configuration..."
URL_CONFIG=$("$AWS_CLI" lambda get-function-url-config --function-name "$FUNCTION_NAME" --region "$REGION" 2>/dev/null || echo "")

if [ -z "$URL_CONFIG" ]; then
    echo "Creating Function URL..."
    "$AWS_CLI" lambda create-function-url-config \
        --function-name "$FUNCTION_NAME" \
        --auth-type NONE \
        --cors '{
            "AllowOrigins": ["*"],
            "AllowMethods": ["GET", "POST", "OPTIONS"],
            "AllowHeaders": ["Content-Type", "Authorization", "X-Requested-With"],
            "MaxAge": 86400
        }' \
        --region "$REGION" >/dev/null

    "$AWS_CLI" lambda add-permission \
        --function-name "$FUNCTION_NAME" \
        --statement-id FunctionURLAllowPublicAccess \
        --action lambda:InvokeFunctionUrl \
        --principal "*" \
        --function-url-auth-type NONE \
        --region "$REGION" >/dev/null || true
fi

# 7. Print Output
PUBLIC_URL=$("$AWS_CLI" lambda get-function-url-config --function-name "$FUNCTION_NAME" --region "$REGION" --query FunctionUrl --output text)

echo "=========================================================="
echo "🎉 DEPLOYMENT COMPLETE!"
echo "   Public HTTPS URL: $PUBLIC_URL"
echo "   Health Check:     ${PUBLIC_URL}health"
echo "   Widget:           ${PUBLIC_URL}subsidy_widget.html"
echo "=========================================================="
