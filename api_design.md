# Upay Explore: API Design Document

## 1. Account Endpoints
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| GET | `/api/accounts/` | List all accounts owned by the logged-in user. |
| POST | `/api/accounts/` | Create a new account. |
| GET | `/api/accounts/{id}/` | Retrieve full details of an account (DetailSerializer). |
| POST | `/api/accounts/{id}/freeze/` | **Action:** Sets `is_frozen` to True. |
| GET | `/api/accounts/{id}/statement/` | **Action:** Returns all transactions for this account. |

## 2. Transaction Endpoints
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| GET | `/api/transactions/` | List all system transactions. |
| POST | `/api/transactions/` | Create a new transaction. |
| POST | `/api/transactions/{id}/reverse/` | **Action:** Reverts money and updates balances. |

## 3. Data Shapes
### Account (List)
`{"id": 1, "account_number": "ACC1", "balance": "100.00", "is_frozen": false}`

### Account (Detail)
`{"id": 1, ..., "owner_username": "zabid754"}`