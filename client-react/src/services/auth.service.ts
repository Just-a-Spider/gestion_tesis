/* eslint-disable no-useless-catch */
/* eslint-disable @typescript-eslint/no-explicit-any */
import { baseUrl } from "@/constants";
import { GetUserProps, LoginProps } from "@/interfaces/auth.interface";
import axios from "axios";
import { jwtDecode } from "jwt-decode";

const axiosAuth = axios.create({
  baseURL: baseUrl + "accounts/",
  headers: {
    "Content-Type": "application/json",
  },
});

class AuthService {
  // SINGLETON
  // Instance is used to keep the token in memory and to manage the token change listeners
  // Basically this is a class with only one instance
  private static instance: AuthService;

  private constructor() {}

  public static getInstance(): AuthService {
    if (!AuthService.instance) {
      AuthService.instance = new AuthService();
    }
    return AuthService.instance;
  }

  public getToken() {
    return typeof window !== "undefined" ? localStorage.getItem("token") : null;
  }

  public getCareerAndRole() {
    const token = this.getToken();
    if (token && token.split(".").length === 3) {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const decoded: any = jwtDecode(token);
      return { career: decoded.career, role: decoded.role };
    }
    return null;
  }

  // AUTHENTICATION HEADERS
  public tokenAuthHeader() {
    const token = this.getToken();
    return token
      ? {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        }
      : {};
  }

  // AUTHENTICATION METHODS
  public async login(loginProps: LoginProps): Promise<string> {
    try {
      const response = await axiosAuth.post("login/", loginProps);
      if (response.status !== 200) {
        throw new Error("Credenciales incorrectas");
      }
      return response.data.access;
    } catch (error: any) {
      if (error.response && error.response.status === 400) {
        throw new Error("Credenciales incorrectas");
      }
      throw error;
    }
  }

  // GET USER INFO
  public async getUserInfo() {
    try {
      const response = await axiosAuth.get("me/", this.tokenAuthHeader());
      return response.data as GetUserProps;
    } catch (error) {
      throw error;
    }
  }
}

export default AuthService;
