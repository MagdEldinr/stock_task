
## Tech Stack

**Language:** Python\
**FrameWork:** DRF\
**Messaging:** vernemq\
**DB:** sqlite




## Installation

- run `docker-compose up --build -d`
- make sure you are in the this folder `$path/thndr/`
- run vernemq consumer `python stock/consumers/stock_consumer.py`
- There will be 3 user created on the first time you run the server
  - User with id `1` with 100 funds
  - User with id `2` with 1000 funds
  - User with id `3` with 10000 funds
## API Reference

#### Retrieve stock

```http
  GET /api/stock/${stock_id}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `stock_id` | `string` | **Required**. Id of stock to fetch |

#### Retrieve user

```http
  GET /api/users/${id}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `id` | `int` | **Required**. Id of user to fetch |

```http
  POST /api/users/deposit
```

| Body parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `user_id` | `int` | **Required**. Id of user |
| `amount` | `int` | **Required**. Amount of funds to be deposited |

```http
  POST /api/users/withdraw
```

| Body parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `user_id` | `int` | **Required**. Id of user |
| `amount` | `int` | **Required**. Amount of funds to be deposited |

```http
  POST /api/transactions/sell
```

| Body parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `user_id` | `int` | **Required**. Id of user |
| `stock_id` | `string` | **Required**. Id of stock to be sold |
| `total` | `int` | **Required**. Count of stock to be sold |
| `upper_bound` | `int` | **Required**. Max value stock can be sold with |
| `lower_bound` | `int` | **Required**. Min value stock can be sold with |

```http
  POST /api/transactions/buy
```

| Body parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `user_id` | `int` | **Required**. Id of user |
| `stock_id` | `string` | **Required**. Id of stock to be bought |
| `total` | `int` | **Required**. Count of stock to be bought |
| `upper_bound` | `int` | **Required**. Max value stock can be bought with |
| `lower_bound` | `int` | **Required**. Min value stock can be bought with |

