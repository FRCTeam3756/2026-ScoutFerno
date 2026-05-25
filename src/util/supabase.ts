import { createClient } from '@supabase/supabase-js';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseKey = import.meta.env.VITE_SUPABASE_PUBLISHABLE_KEY;

if (!supabaseUrl) {
  throw new Error(
    "Missing VITE_SUPABASE_URL. Add it to your environment before starting the app.",
  );
}

if (!supabaseKey) {
  throw new Error(
    "Missing VITE_SUPABASE_PUBLISHABLE_KEY. Add it to your environment before starting the app.",
  );
}

export const supabase = createClient(supabaseUrl, supabaseKey);
