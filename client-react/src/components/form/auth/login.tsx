import { FormFieldComponent } from "@/components/form_field";
import { Alert, AlertTitle } from "@/components/ui/alert";
import { Form, FormItem } from "@/components/ui/form";
import { useToken } from "@/providers/token.provider";
import AuthService from "@/services/auth.service";
import { zodResolver } from "@hookform/resolvers/zod";
import { AlertCircle } from "lucide-react";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { Button } from "../../ui/button";

const LoginSchema = z.object({
  code: z
    .string()
    .min(10, { message: "Escriba su código de alumno" })
    .max(12, { message: "Código de alumno muy largo" }),
  password: z.string().min(1, { message: "Escriba su contraseña" }),
});

export function LoginForm() {
  const authService = AuthService.getInstance();
  const { setKey } = useToken();
  const [showAlert, setShowAlert] = useState(false);

  const form = useForm<z.infer<typeof LoginSchema>>({
    resolver: zodResolver(LoginSchema),
    defaultValues: {
      code: "",
      password: "",
    },
  });

  async function submitLogin(data: z.infer<typeof LoginSchema>) {
    try {
      const token = await authService.login(data);
      setKey(token);
    } catch (error) {
      setShowAlert(true);
    }
  }

  return (
    <Form {...form}>
      {showAlert && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>Credenciales Incorrectas</AlertTitle>
        </Alert>
      )}
      <form
        onSubmit={form.handleSubmit(submitLogin)}
        className="sm:space-y-8 space-y-4"
      >
        <FormFieldComponent
          control={form.control}
          name="code"
          label="Código Universitario"
          placeholder="2024123456"
        />
        <FormFieldComponent
          control={form.control}
          name="password"
          label="Contraseña"
          placeholder="contraseña"
          type="password"
          togglable={true}
        />
        <FormItem className="flex justify-center">
          <Button type="submit">Ingresar</Button>
        </FormItem>
      </form>
    </Form>
  );
}
