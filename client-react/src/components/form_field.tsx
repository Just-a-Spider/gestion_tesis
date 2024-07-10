/* eslint-disable @typescript-eslint/no-explicit-any */
import {
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { ToggleInput } from './toggable_field';

export function FormFieldComponent({
  control,
  name,
  placeholder,
  label,
  type = 'text',
  togglable = false,
  className,
}: {
  control: any;
  name: any;
  placeholder?: string;
  label?: string;
  type?: string;
  togglable?: boolean;
  className?: string;
}) {
  return (
    <FormField
      control={control}
      name={name}
      render={({ field: { value, ...field } }) => (
        <FormItem>
          {label && <FormLabel>{label}</FormLabel>}
          <FormControl>
            {togglable ? (
              <ToggleInput field={field} name={placeholder || ''} />
            ) : type === 'file' ? (
              <Input
                type="file"
                className={
                  className ||
                  ''
                }
                {...field}
                onChange={(e) => {
                  if (e.target.files) {
                    field.onChange(e.target.files[0]);
                  }
                }}
              />
            ) : (
              <Input
                type={type}
                className={
                  className ||
                  ''
                }
                placeholder={placeholder}
                value={value || ''}
                {...field}
              />
            )}
          </FormControl>
          <FormMessage />
        </FormItem>
      )}
    />
  );
}
