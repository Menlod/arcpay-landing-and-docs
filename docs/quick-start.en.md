---
title: Quick Start
---

# Quick Start

Welcome to ArcPay — a payment processing solution on the TON network. This guide will help you quickly start integrating ArcPay into your project.

## Table of Contents

1. [Merchant Registration](#merchant-registration)
2. [Creating a Payment](#creating-a-payment)
3. [Processing a Payment](#processing-a-payment)
   - [Payment Link](#payment-link)
   - [Integrations](#integration)
4. [Order Confirmation and Status](#order-confirmation-and-status)

---

## Merchant Registration

To start accepting payments using ArcPay, you need to register as a merchant via our [Telegram Bot](https://t.me/ArcPayBot).

#### Steps:

1. **Start the Bot**: Open Telegram and initiate a conversation with the [ArcPay Bot](https://t.me/ArcPayBot).
2. **Fill in Project Details**: Provide information about your project, including the project name and description.
3. **Set Return and Webhook URLs**:
   - **Return URL**: The URL where users will be redirected after a successful payment (optional).
   - **Webhook URL**: An endpoint on your server that will receive updates about payment statuses (optional).
4. **Configure Accepted Tokens**: Choose the cryptocurrencies you want to accept for payments.
5. **Get Credentials**:
   - **ArcKey**: Your unique key used to authenticate API requests.
   - **Private Key**: Keep this secure; it is used for signing requests.

---

## Creating a Payment

After registration, you can create a new payment order using the ArcPay [API](https://arcpay.online/api/v1/arcpay/docs).

You will need to make a POST request, including your ArcKey in the header.

- `ArcKey`: string : Access key obtained from the bot.

```html
[POST] /order
```

### Request Parameters

- `title` (string): The title of the order.
- `orderId` (string) (optional | default = `INV-{now}`): Your internal order identifier for accounting purposes. 
- `currency` (string): Currency code (e.g., `TON`).
- `feeFromMerchant` (boolean) (optional | default = false): A flag that allows you to withdraw the commission for the order from the seller, and not from the buyer.
- `items` (array): List of items in the order.
  - Each item includes:
    - `title` (string): Item name.
    - `description` (string) (optional): Item description.
    - `imageUrl` (string) (optional): URL of the item's image.
    - `price` (number): Price per unit of the item.
    - `count` (number): Quantity.
    - `itemId` (string) (optional | default = `id-{now}`): Item identifier.
- `meta` (object) (optional): Additional metadata (e.g., customer ID).
- `captured` (boolean) (optional | default = true): Payment capture status. If `true`, the payment will be captured automatically.

#### Example Request:

```bash
curl -X POST 'https://arcpay.online/api/v1/arcpay/order' \
     -H 'Content-Type: application/json' \
     -H 'ArcKey: YOUR_ARC_KEY' \
     -d '{
       "title": "Sample box",
       "orderId": "INV-202401001",
       "currency": "ARC",
       "feeFromMerchant": true,
       "items": [
         {
           "title": "Travel trip",
           "description": "Sample description here",
           "imageUrl": "https://www.gstatic.com/webp/gallery/1.webp",
           "price": 1.025,
           "count": 1,
           "itemId": "id-123456"
         }
       ],
       "meta": {
         "customer_id": "user-1234567"
       }
     }'
```

### Response Parameters

After successfully creating the order, the API will return a response with the order details. Below are the response parameters:

- `uuid` (string): Unique order identifier in the ArcPay system.
- `title` (string): The order title specified in the request.
- `orderId` (string): Your internal order identifier provided in the request.
- `currency` (string): The order currency.
- `feeFromMerchant` (boolean): A flag that allows you to withdraw the commission for the order from the seller, and not from the buyer.
- `items` (array): List of items in the order.
  - Each item includes:
    - `title` (string): Item name.
    - `description` (string): Item description.
    - `imageUrl` (string): URL of the item image.
    - `price` (number): Price of the item.
    - `count` (number): Item quantity.
    - `itemId` (string): Item identifier.
- `meta` (object): Additional metadata provided in the request.
- `status` (string): The current order status (e.g., `created`).
  - Possible values:
    - `created`: The order has been created and is awaiting payment.
    - `received`: The order has been paid.
    - `captured`: The order has been captured automatically or by the merchant.
    - `cancelled`: The order has been canceled.
    - `failed`: Payment failed.
- `createdAt` (string): The date and time the order was created in ISO 8601 format.
- `paymentUrl` (string): URL for order payment. You can redirect the client to this link to complete the payment.
- `testnet` (boolean): Indicates whether the order is executed on the test network.

#### Example Response:

```json
{
  "uuid": "3d933202-5256-432d-8b5c-d4f6612a467e",
  "title": "Sample box",
  "orderId": "INV-202401001",
  "currency": "ARC",
  "feeFromMerchant": true,
  "items": [
    {
      "title": "Travel trip",
      "description": "Sample description here",
      "imageUrl": "https://www.gstatic.com/webp/gallery/1.webp",
      "price": 1.025,
      "count": 1,
      "itemId": "id-123456"
    }
  ],
  "meta": {
    "customer_id": "user-1234567"
  },
  "status": "created",
  "createdAt": "2024-09-16T07:38:29.094367Z",
  "paymentUrl": "https://arcpay.online/pay/3FA85F6457174562B3FC2C963F66AFA6",
  "testnet": false
}
```

#### Notes:

- **Order Tracking**: Using the order’s `uuid` obtained during its creation, you can check its status through relevant API endpoints or receive updates via webhooks.
- **Order Payment**: The link in `paymentUrl` directs the client to the ArcPay payment page. You can use this link to redirect the client or integrate it into your application.
- **Webhook URL**: Ensure your Webhook URL is set correctly to receive notifications about order status changes.
- **Security**: Store the received data securely and do not share the order’s `uuid` with third parties unless necessary.

## Processing a Payment

ArcPay offers two methods for processing payments:

### Payment Link

After creating an order, you can use the payment link to direct your customers to the ArcPay payment page.

### Integration

Integrate the ArcPay payment interface directly into your website or application. A ReactJS version is currently available.
Also, for more fast integration you may use our [SDK](https://github.com/Architec-Ton/arcpay-sdk)

## Order Confirmation and Status

### Checking Order Status

You can retrieve the current status and detailed information about the order using its unique identifier (`uuid`) via the API.

```http
GET /order/{uuid}
```

#### Example Request

```bash
curl -X GET 'https://arcpay.online/api/v1/arcpay/order/3d933202-5256-432d-8b5c-d4f6612a467e'
```

#### Example Response

```json
{
  "uuid": "3d933202-5256-432d-8b5c-d4f6612a467e",
  "title": "Sample box",
  "orderId": "INV-202401001",
  "currency": "ARC",
  "feeFromMerchant": true,
  "captured": true,
  "items": [
    {
      "title": "Travel trip",
      "description": "Sample description here",
      "imageUrl": "https://www.gstatic.com/webp/gallery/1.webp",
      "price": 1.025,
      "count": 1,
      "itemId": "id-123456"
    }
  ],
  "meta": {
    "customer_id": "user-1234567"
  },
  "status": "received",
  "createdAt": "2024-09-16T07:38:29.094367Z",
  "updatedAt": "2024-09-16T08:00:00.000000Z",
  "paymentUrl": "https://arcpay.online/pay/3d933202-5256-432d-8b5c-d4f6612a467e",
  "testnet": false
}
```

### Webhook Notifications for Order Status Changes

The ArcPay system can send notifications to your server about order-related events, such as order status changes. These notifications are sent via webhook and signed using HMAC with your private key to ensure security and authenticity.

#### Webhook URL Setup

During registration via the Telegram bot, you specify the `Webhook URL` — the URL where ArcPay will send event notifications.

#### Notification Format

Each webhook is an HTTP `POST` request with a JSON body containing information about the order and event, as well as the signature of this data encrypted with a private key issued to you via hmac in the 'X-Signature' header.
##### Example Request Body:

```json
{
  "event": "order.status.changed",
  "data": {
    "uuid": "3d933202-5256-432d-8b5c-d4f6612a467e",
    "orderId": "INV-202401001",

    "status": "captured",
    "currency": "ARC",
    "feeFromMerchant": true,
    "amount": 1.025,
    "captured": true,
    "createdAt": "2024-09-16T07:38:29.094367Z",
    "testnet": false,
    "meta": {
      "customer_id": "user-1234567"
    },
    "txn": {
      "hash": "3FA85F6457174562B3FC2C963F66AFA6",
      "lt": 34698129839
    },
    "customer": {
      "wallet": "EQBXRdZTk5P49mL0nOYfDR1VR33N3sPUgB7PNQMaj6DhxOJH"
    }
  }
}
```
