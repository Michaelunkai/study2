# List all EKS clusters
eks_clusters=$(aws eks list-clusters --query 'clusters[*]' --output text)

# Delete each EKS cluster
for cluster in $eks_clusters; do
    aws eks delete-cluster --name $cluster
done

# Check if EKS clusters are deleted
aws eks list-clusters --query 'clusters[*]' --output text
