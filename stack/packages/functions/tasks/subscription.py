# demo by safelyup.net
import boto3

def aws(regToken):
    marketplaceClient = boto3.client('meteringmarketplace')
    customerData = marketplaceClient.resolve_customer(RegistrationToken=regToken)
    return {
        'ProductCode': customerData['ProductCode'],
        'CustomerIdentifier': customerData['CustomerIdentifier'],
        'CustomerAWSAccountId': customerData['CustomerAWSAccountId'],
    }
