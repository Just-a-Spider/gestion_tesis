import { ThemeProvider } from "@/providers/theme.provider";
import "./App.css";
import { LoginForm } from "./components/form/auth/login";
import Navbar from "./components/ui/navbar";
import { useToken } from "./providers/token.provider";

function App() {
  const { key } = useToken();

  return (
    <ThemeProvider defaultTheme="system" storageKey="vite-ui-theme">
        <Navbar />
        {key ? (
          <div>
            <h1>Usuario autenticado</h1>
          </div>
        ) : (
          <LoginForm />
        )}
    </ThemeProvider>
  );
}

export default App;
