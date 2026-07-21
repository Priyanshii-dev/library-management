import { z } from 'zod';

export const NAME_REGEX = /^[A-Za-z ,.'-]+$/;
export const PHONE_REGEX = /^\+?\d{1,10}$/;
export const PASSWORD_REGEX = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,13}$/;

export const loginSchema = z.object({
  email: z.string().email('Please enter a valid email address'),
  password: z.string().min(1, 'Password is required'),
});
export type LoginInput = z.infer<typeof loginSchema>;

export const registerSchema = z.object({
  first_name: z.string()
    .trim()
    .min(1, 'First name is required')
    .max(20, 'First name must be 20 characters or less')
    .regex(NAME_REGEX, 'First name can only include letters, spaces, commas, periods, apostrophes, and hyphens'),
  last_name: z.string()
    .trim()
    .min(1, 'Last name is required')
    .max(20, 'Last name must be 20 characters or less')
    .regex(NAME_REGEX, 'Last name can only include letters, spaces, commas, periods, apostrophes, and hyphens'),
  email: z.string()
    .trim()
    .min(1, 'Email is required')
    .email('Please enter a valid email address'),
  phone: z.string()
    .trim()
    .min(1, 'Phone number is required')
    .regex(PHONE_REGEX, 'Phone must be 10 digits and may start with +'),
  password: z.string()
    .min(1, 'Password is required')
    .min(8, 'Password must be at least 8 characters')
    .max(13, 'Password must be 13 characters or less')
    .regex(PASSWORD_REGEX, 'Password must include uppercase, lowercase, a number, and a special character'),
  confirm_password: z.string().min(1, 'Please confirm your password'),
}).refine((data) => data.password === data.confirm_password, {
  message: 'Passwords do not match',
  path: ['confirm_password'],
});
export type RegisterInput = z.infer<typeof registerSchema>;

export const forgotPasswordSchema = z.object({
  email: z.string().email('Please enter a valid email address'),
});
export type ForgotPasswordInput = z.infer<typeof forgotPasswordSchema>;

export const resetPasswordSchema = z.object({
  email: z.string().email('Please enter a valid email address'),
  otp_code: z.string().length(6, 'OTP must be exactly 6 characters'),
  new_password: z.string().min(8, 'Password must be at least 8 characters').max(13).regex(PASSWORD_REGEX, 'Password must be 8-13 characters and include uppercase, lowercase, a number, and a special character'),
  confirm_new_password: z.string().min(1, 'Please confirm your password'),
}).refine((data) => data.new_password === data.confirm_new_password, {
  message: 'Passwords do not match',
  path: ['confirm_new_password'],
});
export type ResetPasswordInput = z.infer<typeof resetPasswordSchema>;

export const otpSchema = z.object({
  email: z.string()
    .trim()
    .min(1, 'Email is required')
    .email('Please enter a valid email address'),
  otp_code: z.string()
    .trim()
    .min(1, 'OTP code is required')
    .length(6, 'OTP must be exactly 6 characters'),
});
export type OtpInput = z.infer<typeof otpSchema>;

export const profileUpdateSchema = z.object({
  first_name: z.string().min(1).max(100).regex(NAME_REGEX).optional(),
  last_name: z.string().min(1).max(100).regex(NAME_REGEX).optional(),
  phone: z.string().regex(PHONE_REGEX).optional(),
  email: z.string().email().optional(),
});
export type ProfileUpdateInput = z.infer<typeof profileUpdateSchema>;
