import boto3

def s3_client(args):
    """
    Initialize the S3 bucket client for the Python AWS SDK.
    """
    s3 = boto3.client('s3', region_name=args.aws_region)
    return s3
