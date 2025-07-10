# Azure Speech Services Credentials Template

Copy this file to `credentials.md` and fill in your actual Azure Speech Services credentials.

## Primary Key
key1 
[YOUR_AZURE_SPEECH_KEY_1_HERE]

## Secondary Key  
key2
[YOUR_AZURE_SPEECH_KEY_2_HERE]

## Location/Region
location 
[YOUR_AZURE_REGION_HERE]

## Endpoint
endpoint
https://[YOUR_REGION].api.cognitive.microsoft.com/

## Setup Instructions

1. Go to Azure Portal (https://portal.azure.com)
2. Create a Speech Services resource
3. Copy the keys and endpoint from the resource
4. Create a `credentials.md` file in this directory
5. Fill in your actual credentials in the format above

## Security Note

- **NEVER commit credentials.md to version control**
- The credentials.md file is excluded in .gitignore for security
- Keep your Azure keys secure and rotate them regularly 