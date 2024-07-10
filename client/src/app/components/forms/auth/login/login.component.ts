import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { LoginProps } from '@interfaces/auth.interface';
import { AuthService } from '@services/auth.service';
import { InputTextModule } from 'primeng/inputtext';
import { PasswordModule } from 'primeng/password';

@Component({
  selector: 'form-login',
  standalone: true,
  imports: [FormsModule, InputTextModule, PasswordModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css',
})
export class LoginComponent {
  loginProps: LoginProps = {
    code: '',
    password: '',
  };

  constructor(private authService: AuthService) {}

  login() {
    this.authService.login(this.loginProps);
    // Reload the page to update the navbar
    window.location.reload();
  }
}
