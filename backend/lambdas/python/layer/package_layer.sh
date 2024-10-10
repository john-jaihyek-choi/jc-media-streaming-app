#!/bin/bash

# Step 1: Generate requirements.txt for boto3_helper and utils
echo "Generating requirements for boto3_helper/ and utils/..."
pipreqs ../. --force

# Step 2: Temporarily create directory for zip
echo "Creating temporary directory for layer"
rsync -av --exclude='package_layer.sh' --exclude='*.zip' --exclude='python' ./ python/

# Step 3: Install dependencies from the generated requirements.txt files
echo "Installing dependencies from requirements.txt files into python/lib/python3.12/site-packages/..."
pip install -r ../requirements.txt -t python/lib/python3.12/site-packages/
echo "Dependency installation completed!"

# Step 4: Zip content for Lambda Layer
echo "Zipping the packages for Lambda Layer..."
zip -r layer_package.zip python/

# Step 5 Cleaning up temporary directory
echo "Cleaning up temporary directory python/..."
rm -r python/
rm utils/requirements.txt
rm boto3_helper/requirements.txt

echo "layer.zip creation successful!"