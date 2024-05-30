import argparse

##########################################################################################################
## Bucket
def bucket_args():
    """
    Initializes the arguments needed to excecute operations on a given S3 bucket.

    Example
    -------
    a_bucket_function(bucket_args())
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket", required=True, help="Name of the bucket")
    parser.add_argument("--aws_region", required=True, help="aws region where to look for the bucket")
    parser.add_argument("--prefix", required=True, help="Buckets Prefix")
    args = parser.parse_args()
    return args

bucket_args_call = bucket_args()
##########################################################################################################

if __name__ == "__main__":
    print(bucket_args())
