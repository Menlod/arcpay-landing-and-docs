---
title: Using SDK
---

# Connecting via the SDK

Welcome to ArcPay, a payment processing solution on the TON network. This guide will help you quickly start integrating ArcPay into your project.

## Merchant Registration

To start accepting payments using ArcPay, you need to register as a merchant through our Telegram bot.

## Connecting the SDK

The full SDK source code and sample application are available on GitHub: [ArcPay SDK on GitHub](https://github.com/Architec-Ton/arcpay-sdk)

### Creating an order

To create a payment order, send an API request with the order data and your `ArcKey` received from the bot:

```HTML
[HEADER] ArcKey=<you-key>
[POST] https://arcpay.online/api/v1/arcpay/order
[BODY] order details
```

Make sure that the ArcKey is specified in the request header.

<details>
<summary>
Python example
</summary>

```python
url = "https://arcpay.online/api/v1/arcpay/order"
headers = {"Content-Type": "application/json", "ArcKey": ARC_KEY}
data = {
    "title": "Premium Subscription Box",
    "orderId": f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}",
    "currency": "TON",
    "items": [
        {
            "title": "Exclusive Travel Package",
            "description": "A luxurious 5-day trip to Bali with first-class accommodation.",
            "imageUrl": "https://www.luxurytravelmagazine.com/files/610/1/2901/Kayon-Jungle-aerial_reg.jpg",
            "price": 0.500,
            "count": 1,
            "itemId": "id-987654",
        },
        {
            "title": "Gourmet Dinner Experience",
            "description": "A 7-course gourmet dinner at a Michelin-starred restaurant.",
            "imageUrl": "https://www.luxurytravelmagazine.com/files/610/2/2572/Samabe-restaurant_big_reg.jpg",
            "price": 0.150,
            "count": 2,
            "itemId": "id-654321",
        },
    ],
    "meta": {
    "telegram_id": (request_data["telegram_id"] if "telegram_id" in request_data else None)
    },
    "captured": False,
}
result = None
async with ClientSession() as session:
  async with session.post(url, json=data, headers=headers) as response:
    if response.status == 200:
        result = await response.json()
        print(f"Order created successfully: {result}") # Process the response # Add your logic here to handle the received data
      else:
        print(f"Failed to create order. Status: {response.status}, Error: {await response.text()}")
```

</details>

After successfully creating an order, you will receive an `OrderID'. It must be transferred to the frontend to initiate the payment process or use `paymentUrl`.

For more detailed information about the API, you can read the [Swagger documentation](https://arcpay.online/api/v1/arcpay/docs).

### Installing the SDK

Install the SDK for React:

```bash
npm i @arcpay/react-sdk
```

### Configuring the provider in the React application

To get started, add ArcPayProvider to the root file of the application so that the SDK is available to the entire project:

```typescript
import { createRoot } from 'react-dom/client';
import App from './App.tsx';
import { ArcPayProvider } from '@arcpay/react-sdk';

createRoot(document.getElementById('root')!).render(
  <ArcPayProvider>
    <App />
  </ArcPayProvider>
);
```

### Integration of the payment component

To track the order status, add a callback function that will track status changes by order ID (OrderID):

```typescript
useEffect(() => {
  arcPay.onOrderChange(orderId, (updatedOrder) => {
    console.log(updatedOrder);
  });
}, [orderId]);
```

When the order status changes, as well as immediately after installation, the function passed to onOrderChange will be called automatically. This allows you to always be aware of the current status of the order.

### Payment initialization

To start the payment, use the `paymentUrl` link. If the link is available, you can initiate the payment by opening it in a new tab:

```typescript
<button onClick={() => window.open(order.paymentUrl, '_blank')}>
  Pay ({order.amount} {order.currency})
</button>
```

:::note
If there is no paymentUrl, it means that payment for this order is currently impossible.

For TMA-based applications, it is recommended to use the OpenLink from the TMA package
:::

## Getting order information via webhook

When the payment is completed successfully, the order status has changed to `received` or `captured'.

To process order status changes on the backend side, use a Webhook.
Below is an example of processing a request from ArcPay in Python:

```python
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
ARC_KEY = os.getenv("ARC_KEY")

async def handle_webhook(request):
    try:
        # Read the request body
        raw_body_bytes = await request.read()
        raw_body = raw_body_bytes.decode("utf-8")
        data = json.loads(raw_body)

        # Get the signature from the request headers
        signature = request.headers.get("X-Signature")
        if not signature:
            return web.Response(status=400, text="Missing signature header")

        # Calculate the expected signature
        expected_signature = hmac.new(
            PRIVATE_KEY.encode("utf-8"), raw_body_bytes, hashlib.sha256
        ).hexdigest()

        # Validate the signature
        if not hmac.compare_digest(signature, expected_signature):
            return web.Response(status=403, text="Invalid signature")

        # Process the request
        # Add your logic here to handle the received data
        print(f"Received data: {data}")

        if data["event"] == "order.status.changed":
            if data["data"]["status"] == "received":
                print("Order received successfully, we capture it!")

        return web.Response(status=200, text="Webhook received successfully")

    except json.JSONDecodeError:
        return web.Response(status=400, text="Invalid JSON format")
    except Exception as e:
        return web.Response(status=500, text=f"Unexpected error: {str(e)}")
```
