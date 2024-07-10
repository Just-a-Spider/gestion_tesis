import { HttpClient } from '@angular/common/http';
import { EventEmitter, Injectable } from '@angular/core';
import { baseUrl } from '../constants';
import {
  GetUserProps,
  LoginProps,
  RegisterProps,
} from '../interfaces/auth.interface';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private _authUrl = `${baseUrl}accounts/`;
  authChange: EventEmitter<boolean> = new EventEmitter();

  constructor(private authHttp: HttpClient) {}

  private getAccessToken(): string | null {
    return localStorage.getItem('access');
  }

  private setAccessToken(token: string | null): void {
    if (token) {
      localStorage.setItem('access', token);
      this.authChange.emit(true);
    } else {
      localStorage.removeItem('access');
      this.authChange.emit(false);
    }
  }

  // Out of the box Auth functions
  register(registerProps: RegisterProps) {
    const { username, email, first_name, last_name, dni, password, password2 } =
      registerProps;

    return this.authHttp
      .post(`${this._authUrl}register/`, {
        username,
        email,
        first_name,
        last_name,
        dni,
        password,
        password2,
      })
      .subscribe((response: any) => {
        return response.detail;
      });
  }

  login(loginProps: LoginProps) {
    const { code, password } = loginProps;

    const response = this.authHttp
      .post(`${this._authUrl}login/`, {
        code,
        password,
    })
      .subscribe((response: any) => {
        if (response.access) {
          this.setAccessToken(response.access);
        }
        return response.detail;
      });

    return response;
  }

  logout() {
    this.setAccessToken(null);
  }

  // Email confirmation
  confirmEmail(key: string) {
    return this.authHttp.get(`${this._authUrl}confirm-email/${key}/`);
  }

  resendConfirmationEmail(email: string) {
    return this.authHttp.post(`${this._authUrl}send-confirmation-email/`, {
      email,
    });
  }

  // Password reset
  resetPassword(key: string, new_password: string) {
    return this.authHttp.post(`${this._authUrl}restore-password/${key}/`, {
      new_password,
    });
  }

  sendResetPasswordEmail(email: string) {
    return this.authHttp.post(`${this._authUrl}send-restore-email/`, {
      email,
    });
  }

  // Me
  me() {
    const response = this.authHttp.get<GetUserProps>(`${this._authUrl}me/`, {
      headers: {
        Authorization: `Bearer ${this.getAccessToken()}`,
      },
    });
    console.log(response);
    return response;
  }
}
