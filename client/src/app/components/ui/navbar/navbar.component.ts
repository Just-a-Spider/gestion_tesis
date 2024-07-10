import { Component } from '@angular/core';
import { GetUserProps } from '@app/interfaces/auth.interface';
import { LoginComponent } from '@components/forms/auth/login/login.component';
import { AuthService } from '@services/auth.service';
import { ButtonModule } from 'primeng/button';
import { SidebarModule } from 'primeng/sidebar';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [LoginComponent, SidebarModule, ButtonModule],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css',
})
export class NavbarComponent {
  sidebarVisible = false;
  isAuthenticated = false;
  showLogin = false;

  // User data
  user: GetUserProps | undefined;

  constructor(private authService: AuthService) {}

  ngOnInit() {
    // Safely check for 'localStorage' by first checking if 'window' is defined
    if (typeof window !== 'undefined') {
      const accessExists = !!localStorage.getItem('access');
      this.isAuthenticated = accessExists;

      if (accessExists) {
        this.authService.me().subscribe((user: GetUserProps) => {
          console.log(user);
          this.user = user;
        });
      }
    }

    this.authService.authChange.subscribe((authState) => {
      this.isAuthenticated = authState;
    });
  }

  toggleLogin() {
    this.showLogin = !this.showLogin;
  }

  logout() {
    this.authService.logout();
  }
}
