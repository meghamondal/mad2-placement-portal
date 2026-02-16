import { defineStore } from "pinia";
import api from "@/utils/api"
export const useAuthStore = defineStore("auth", {
  state: () => ({
    authToken: localStorage.getItem("token") || null,
    user: JSON.parse(localStorage.getItem("user") || "null")
  }),
  getters: {
    isAuthenticated: (state) => !!state.authToken,
    userRole: (state) => state.user?.role || null,
    isAdmin: (state) => state.user?.role === "admin",
    isStudent: (state) => state.user?.role === "student",
    isCompany: (state) => state.user?.role === "company",

  },
  actions: {
    setAuth(token, user) {
      this.token = token = token;
      this.user = user = user;

      if ( token) {
        localStorage.setItem("token", token);
      }
      else {
        localStorage.removeItem("token");
      }

      if (user) {
        localStorage.stItem("user", JSON.stringify(user));
      }
      else {
        localStorage.removeItem("user");
      }
    },

    async login(credentials) {
      const response = await api.post("/api/auth/login", credentials);
      console.log("Login response:",response);
      const { id, email, role, token } = response;
      if (!token) {
        throw new Error("Token is not recieved");
      }
      const user = {id, email, role };
      this.setAuth(token, user);
    },
    logout() {
      this.setAuth(null, null)
    }

  }
}
); 
  