#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT_DIR=$(cd "${SCRIPT_DIR}/.." && pwd)
echo "Script is located at: $SCRIPT_DIR"
echo "PROJECT ROOT is located at: $PROJECT_ROOT_DIR"

read -p "Do you confirm? (y/n): " choice
case "$choice" in
  [yY]) echo "Process starting...";;
  [nN]) echo "Please verify package_layer.sh for correct path to root and the script"; exit 1;;
  *) echo "Invalid choice. Process starting...";;
esac

# Step 1: Generate requirements.txt for boto3_helper and utils
echo "Generating project requirements..."
poetry export -f requirements.txt --output "${PROJECT_ROOT_DIR}/requirements.txt"

# Step 2: Temporarily create directory for zip
echo "Creating temporary directory for layer"
rsync -av --exclude="package_layer.sh" --exclude="*.zip" --exclude="${SCRIPT_DIR}/python" "${SCRIPT_DIR}/" "${SCRIPT_DIR}/python/"

# Step 3: Install dependencies from the generated requirements.txt files
echo "Installing dependencies from requirements.txt files into python/lib/python3.12/site-packages/..."
pip install --platform manylinux2014_x86_64 --target=package --implementation cp --python-version 3.12 --only-binary=:all: --upgrade -r "${PROJECT_ROOT_DIR}/requirements.txt" -t "${SCRIPT_DIR}/python/lib/python3.12/site-packages/"
echo "Dependency installation completed!"

# Step 4: Zip content for Lambda Layer
echo "Zipping the packages for Lambda Layer..."
# find ./ -type d -name "__pycache__" -exec rm -rf {} + &&
(cd "${SCRIPT_DIR}" && zip -r -o "layer_package.zip" python/ -x "__pycache__")

# Step 5 Cleaning up temporary directory
echo "Cleaning up temporary directories..."
rm -r "${SCRIPT_DIR}/python/"

echo "layer.zip creation successful!"