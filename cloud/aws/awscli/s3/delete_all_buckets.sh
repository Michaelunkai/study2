#!/bin/ 

# List all bucket names
buckets=$(aws s3api list-buckets --query "Buckets[].Name" --output text)

# Function to delete all versions and delete markers in a bucket
delete_all_versions() {
    bucket=$1
    versions=$(aws s3api list-object-versions --bucket $bucket --query '{Objects: Versions[].{Key:Key,VersionId:VersionId}}' --output text)
    markers=$(aws s3api list-object-versions --bucket $bucket --query '{Objects: DeleteMarkers[].{Key:Key,VersionId:VersionId}}' --output text)

    if [ ! -z "$versions" ]; then
        echo "Deleting versions in bucket: $bucket"
        echo "$versions" | while read -r key version; do
            aws s3api delete-object --bucket $bucket --key "$key" --version-id "$version"
        done
    fi

    if [ ! -z "$markers" ]; then
        echo "Deleting delete markers in bucket: $bucket"
        echo "$markers" | while read -r key version; do
            aws s3api delete-object --bucket $bucket --key "$key" --version-id "$version"
        done
    fi
}

# Iterate over each bucket
for bucket in $buckets; do
    echo "Deleting all objects in bucket: $bucket"
    
    # Delete all versions and delete markers
    delete_all_versions $bucket

    # Delete the bucket itself
    echo "Deleting bucket: $bucket"
    aws s3api delete-bucket --bucket $bucket
done

echo "All buckets deleted."
