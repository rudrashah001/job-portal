import React, { createContext, useState, useEffect } from "react";
import jwtDecode from "jwt-decode";
import { useNavigate } from "react-router-dom";

export const AuthContext = createContext();

export function AuthProvider({ children }) {
const [user, setUser] = useState(null);
const nav = useNavigate();

// Load token on refresh
useEffect(() => {
const token = localStorage.getItem("token");
if (!token) return;

```
try {
  const decoded = jwtDecode(token);
  setUser({ id: decoded.sub, role: decoded.role });
} catch (err) {
  console.error("Invalid token:", err);
  localStorage.removeItem("token");
}
```

}, []);

// Handle login
const login = (token) => {
localStorage.setItem("token", token);

```
const decoded = jwtDecode(token);
setUser({ id: decoded.sub, role: decoded.role });

if (decoded.role === "recruiter") {
  nav("/recruiter/dashboard");
} else {
  nav("/student/dashboard");
}
```

};

// Handle logout
const logout = () => {
localStorage.removeItem("token");
setUser(null);
nav("/");
};

return (
<AuthContext.Provider value={{ user, login, logout }}>
{children}
</AuthContext.Provider>
);
}
