export type TransactionType = "personal" | "shared" | "borrowed" | "income";

export interface TransactionParticipant {
  id?: string;
  participant_name: string;
  share_amount: string;
  pending_amount: string;
  status: string;
}

export interface Transaction {
  id: string;
  transaction_type: TransactionType;
  amount: string;
  my_share: string;
  description: string;
  payment_owner: string;
  transaction_date: string;
  category_name?: string | null;
  participants: TransactionParticipant[];
}

export interface Summary {
  total_income: string;
  total_expenses: string;
  money_you_owe: string;
  money_owed_to_you: string;
  net_savings: string;
  current_balance: string;
}

export interface Friend {
  id: string;
  name: string;
  telegram_username?: string | null;
  phone?: string | null;
  notes?: string | null;
  created_at: string;
}

export interface Budget {
  id: string;
  name: string;
  amount: string;
  period: string;
  category_name?: string | null;
  is_active: boolean;
  spent_amount: string;
  remaining_amount: string;
}

export interface AuthUser {
  id: string;
  email: string;
  full_name: string;
  is_active: boolean;
  created_at: string;
}

export interface TelegramAuthPayload {
  id: number;
  first_name: string;
  last_name?: string;
  username?: string;
  photo_url?: string;
  auth_date: number;
  hash: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: AuthUser;
}
