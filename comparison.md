# Serializer Architectural Comparison


## 1. Serializer 
**Use Case:** When data does not map directly to a single database table or when performing a complex "Business Process."

*   **Project Example:** `ExchangeRequestSerializer`.
*   **Why:** Exchanging currency is an *action*, not a database row. A base `Serializer` allows us to define exactly what input we want (receiver, currencies, amount) without Django trying to save it to a specific table automatically.
*   **Verdict:** Best for complex validation and non-CRUD endpoints.

## 2. ModelSerializer 
**Use Case:** For standard CRUD (Create, Read, Update, Delete) where the API mirrors a database table.

*   **Project Example:** `WalletSerializer`, `UserSerializer`.
*   **Why:** It drastically reduces boilerplate code by automatically generating fields from the model. It also respects database constraints like `unique_together` out of the box.
*   **Verdict:** Best for 90% of standard data-entry and viewing tasks.

## 3. Nested vs. Flat Serializers
In Fintech, this is a trade-off between **Context** and **Performance**.

### **Nested Serializers **
*   **Project Example:** `TransactionSerializer` (contains `WalletSerializer`).
*   **Pros:** The frontend gets a full "tree" of data in one request. A user sees their receipt and the account details without making multiple API calls.
*   **Cons:** Larger JSON payloads and more database overhead.

### **Flat Serializers **
*   **Project Example:** `WalletListSerializer`.
*   **Pros:** Minimal bandwidth usage. Returning only `id`, `currency`, and `balance` makes the dashboard load instantly.
*   **Cons:** If the user clicks for more detail, the frontend must make another API call.

## 4. ListSerializer 
**Use Case:** When performing logic on a collection of objects rather than just one.

*   **Project Example:** `TransactionListSerializer`.
*   **Why:** It allows us to intercept the serialization process for an entire list. Useful for bulk interest payouts or end-of-day audits.



