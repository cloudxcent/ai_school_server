# Azure Setup Guide for AI School

## Prerequisites
- Azure account with active subscription
- Azure CLI installed (optional but recommended)

## Step 1: Create Azure Storage Account

### Using Azure Portal:
1. Go to [Azure Portal](https://portal.azure.com)
2. Click "Create a resource"
3. Search for "Storage account"
4. Click "Create"

### Storage Account Configuration:
- **Subscription**: Select your subscription
- **Resource Group**: Create new or use existing
- **Storage Account Name**: Choose a unique name (e.g., `aischoolstorage123`)
- **Region**: Choose region closest to your users
- **Performance**: Standard
- **Redundancy**: LRS (Locally Redundant Storage) for development

### Review and Create:
1. Review your settings
2. Click "Create"
3. Wait for deployment to complete

## Step 2: Get Connection String

1. Navigate to your storage account
2. Go to "Security + networking" → "Access keys"
3. Copy the "Connection string" from Key1

## Step 3: Configure Environment Variables

Create a `.env` file in the backend directory:

```bash
# Copy .env.example to .env
cp .env.example .env
```

Edit the `.env` file with your actual values:

```
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=your_account_name;AccountKey=your_account_key;EndpointSuffix=core.windows.net
SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000
```

## Step 4: Table Storage Schema

The application will automatically create a `users` table with the following schema:

| Column | Type | Description |
|--------|------|-------------|
| PartitionKey | String | User email (for efficient querying) |
| RowKey | String | User ID (UUID) |
| email | String | User email address |
| password_hash | String | Bcrypt hashed password |
| full_name | String | User's full name |
| phone_number | String | User's phone number (optional) |
| created_at | String | ISO timestamp of account creation |
| last_login | String | ISO timestamp of last login |
| is_active | Boolean | Account active status |

## Step 5: Security Considerations

### Production Environment:
1. **Use Azure Key Vault** for storing sensitive configuration
2. **Enable Azure Storage encryption** at rest
3. **Configure firewall rules** to restrict access
4. **Use Managed Identity** instead of connection strings
5. **Enable logging and monitoring**

### JWT Security:
1. Use a strong, random secret key (at least 32 characters)
2. Consider shorter token expiration times for production
3. Implement token refresh mechanism
4. Store tokens securely on client side

## Step 6: Cost Optimization

### Development:
- Use LRS (Locally Redundant Storage)
- Monitor usage in Azure Cost Management
- Delete test data regularly

### Production:
- Choose appropriate redundancy level
- Implement data retention policies
- Use Azure Storage lifecycle management

## Step 7: Monitoring and Logging

### Enable diagnostics:
1. Go to your storage account
2. Navigate to "Monitoring" → "Diagnostic settings"
3. Add diagnostic setting
4. Enable logs for Table service
5. Send to Log Analytics workspace

### Monitor performance:
- Use Azure Monitor for storage metrics
- Set up alerts for high usage or errors
- Monitor request latency and availability

## Troubleshooting

### Common Issues:

1. **Connection String Format Error**
   - Ensure no extra spaces or line breaks
   - Verify account name and key are correct

2. **Table Creation Fails**
   - Check storage account permissions
   - Verify connection string is valid

3. **Authentication Errors**
   - Verify JWT secret key is set
   - Check token expiration settings

### Debug Steps:
1. Test connection string with Azure Storage Explorer
2. Enable Flask debug mode
3. Check Azure Storage logs
4. Verify firewall and network settings
