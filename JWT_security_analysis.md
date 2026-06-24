# JWT Security Analysis & Threat Report

**Project:** Fintech Wallet Authentication System  


---

## 1. Authentication Architecture
This system utilizes **JSON Web Tokens (JWT)** to provide stateless authentication. To balance security with user experience, we have implemented a dual-token strategy:

*   **Access Token (15 min):** Short-lived tokens used for active API requests. The short duration ensures that if a token is intercepted, its utility is strictly limited.
*   **Refresh Token (24 hr):** Long-lived tokens used to obtain new access tokens without requiring user re-authentication.
*   **Token Rotation:** Enabled. Every time a refresh token is used, the old one is invalidated and a brand-new pair is issued, mitigating "token replay" risks.

---

## 2. Risk Mitigation Strategies

### A. Token Theft & Lifecycle Management
**The Risk:** Stolen access tokens can allow an attacker to impersonate a user.  
**The Implementation:** 
1.  **Short Lifetimes:** By keeping access tokens to 15 minutes, we minimize the "window of opportunity" for an attacker.
2.  **Blacklisting:** Our `LogoutView` and `RevokeSessionView` utilize the SimpleJWT Blacklist app. This ensures that while a stolen access token might work for a few minutes, the **Refresh Token** is immediately killed, preventing the attacker from maintaining long-term access.

### B. Master Key Security (`SECRET_KEY`)
**The Risk:** If the server's `SECRET_KEY` is leaked, an attacker can forge valid JWTs for any user in the system.  
**The Implementation:**  We have flagged this as a critical future upgrade. Currently, the key is in settings for development, but for production, it will be moved to a .env file to prevent source-code leaks.

---

## 3. Vulnerability Simulation & Fixes 

During the development of the `authentication` app, the following vulnerabilities were identified and resolved:

### Vulnerability 1: The "Zombie Session" (Statelessness)
*   **Scenario:** Traditionally, JWT is stateless; the server cannot "kill" a session until the token expires. If a user loses their device, an attacker has access until the 24-hour refresh token expires.
*   **The Fix:** We implemented a **Stateful Session Ledger** using the `UserSession` model. 
*   **Logic:** By storing the `refresh_token` string in our database and linking it to a user's IP and Device info, we gained the ability to **Revoke** specific sessions. When a user revokes a session, we manually blacklist the token, turning a stateless system into a controllable, secure environment.

### Vulnerability 2: IDOR (Insecure Direct Object Reference)
*   **Scenario:** A malicious user could send a `DELETE` request to `/api/auth/sessions/10/` where ID `10` belongs to a different user, effectively kicking other customers out of the system.
*   **The Fix:** We implemented **Row-Level Security** by overriding the `get_queryset` method in the session views:
    ```python
    def get_queryset(self):
        return UserSession.objects.filter(user=self.request.user)
    ```
*   **Result:** By strictly filtering queries by `self.request.user`, the database engine is physically unable to access rows belonging to other users. Any attempt to modify another user's session results in a `404 Not Found`.

---

## 4. Future Security Roadmap
To reach a higher tier of financial security, the following features are planned:
*   **Brute Force Protection:** Adding rate-limiting (`django-ratelimit`) to the login endpoint to prevent credential stuffing.
*   **XSS Mitigation:** Moving from `localStorage` to **HttpOnly Cookies** for token storage to prevent JavaScript-based theft.
*   **Token Hashing:** Storing a SHA-256 hash of the refresh token in the `UserSession` table instead of the plaintext string to protect against database leaks.

---

## 5. Conclusion
By combining the performance of stateless JWTs with a custom **Session Tracking** layer and **IDOR protection**, this implementation ensures user data privacy and session integrity. The system provides users with full transparency into their active devices and the power to revoke access instantly, fulfilling core Fintech security requirements.