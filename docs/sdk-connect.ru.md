---
title: Подключение через SDK
---

# Подключение через SDK

Добро пожаловать в ArcPay — решение для обработки платежей в сети TON. Это руководство поможет вам быстро начать интеграцию ArcPay в ваш проект.

## Регистрация продавца

Чтобы начать принимать платежи с помощью ArcPay, вам необходимо зарегистрироваться в качестве продавца через нашего Telegram-бота.

## Подключение SDK

Полный исходный код SDK и примеры приложений доступны на GitHub: [ArcPay SDK on GitHub](https://github.com/Architec-Ton/arcpay-sdk)

### Создание заказа

Для создания заказа на оплату отправьте запрос на API с данными заказа и вашим `ArcKey`, полученным из бота::

```HTML
[HEADER] ArcKey=<you-key>
[POST] https://arcpay.online/api/v1/arcpay/order
[BODY] order details
```

Убедитесь, что в заголовке запроса указан ArcKey.

<details>
<summary>
Пример на python  
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

После успешного создания заказа вы получите `orderId`. Его необходимо передать на фронтенд для инициации процесса оплаты или передать платежную ссылку: `paymentUrl`.

Для получения более детальной информации об API вы можете ознакомиться с [документацией Swagger](https://arcpay.online/api/v1/arcpay/docs).

### Установка SDK

Установите SDK для React:

```bash
npm i @arcpay/react-sdk
```

### Настройка провайдера в приложении React

Для начала работы добавьте ArcPayProvider в корневой файл приложения, чтобы SDK был доступен всему проекту:

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

### Интеграция платежного компонента

Для отслеживания статуса заказа добавьте callback функцию, который будет отслеживать изменения статуса по идентификатору заказа (orderId):

```typescript
useEffect(() => {
  arcPay.onOrderChange(orderId, (updatedOrder) => {
    console.log(updatedOrder);
  });
}, [orderId]);
```

При изменении статуса заказа, а также сразу после установки функция переданная в onOrderChange, будет вызвана автоматически. Это позволяет всегда быть в курсе текущего состояния заказа.

### Инициализация платежа

Для запуска оплаты используйте ссылку `paymentUrl`. Если ссылка доступна, вы можете инициировать оплату, открыв её в новой вкладке:

```typescript
<button onClick={() => window.open(order.paymentUrl, '_blank')}>
  Pay ({order.amount} {order.currency})
</button>
```

:::note
Если paymentUrl отсутствует, значит, оплата для данного заказа в данный момент невозможна.

Для приложений на основе TMA рекомендуется использовать openLink из пакета TMA
:::

## Получение информации о заказе через webhook

Когда платеж будет успешно проведён, статус заказа изменится на `received` или `captured`.

Для обработки изменений статуса заказа на стороне бэкенда используйте Webhook.
Ниже приведён пример обработки запроса от ArcPay на Python:

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
