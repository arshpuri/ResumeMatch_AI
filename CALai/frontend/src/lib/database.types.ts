export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export type Database = {
  public: {
    Tables: {
      applications: {
        Row: {
          applied_at: string | null
          cover_letter: string | null
          id: string
          job_id: string
          match_score: number | null
          notes: string | null
          resume_id: string | null
          status: string | null
          updated_at: string | null
          user_id: string
        }
        Insert: {
          applied_at?: string | null
          cover_letter?: string | null
          id?: string
          job_id: string
          match_score?: number | null
          notes?: string | null
          resume_id?: string | null
          status?: string | null
          updated_at?: string | null
          user_id: string
        }
        Update: {
          applied_at?: string | null
          cover_letter?: string | null
          id?: string
          job_id?: string
          match_score?: number | null
          notes?: string | null
          resume_id?: string | null
          status?: string | null
          updated_at?: string | null
          user_id?: string
        }
        Relationships: [
          {
            foreignKeyName: "applications_job_id_fkey"
            columns: ["job_id"]
            isOneToOne: false
            referencedRelation: "jobs"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "applications_resume_id_fkey"
            columns: ["resume_id"]
            isOneToOne: false
            referencedRelation: "parsed_resumes"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "applications_user_id_fkey"
            columns: ["user_id"]
            isOneToOne: false
            referencedRelation: "users"
            referencedColumns: ["id"]
          },
        ]
      }
      jobs: {
        Row: {
          application_url: string | null
          benefits: string[] | null
          company: string
          created_at: string | null
          description: string | null
          embedding: string | null
          experience_level: string | null
          expires_at: string | null
          external_id: string | null
          fts: unknown
          id: string
          is_active: boolean | null
          is_remote: boolean | null
          job_type: string | null
          location: string | null
          posted_at: string | null
          preferred_skills: string[] | null
          required_skills: string[] | null
          requirements: string[] | null
          responsibilities: string[] | null
          salary_currency: string | null
          salary_max: number | null
          salary_min: number | null
          source: string | null
          title: string
          updated_at: string | null
        }
        Insert: {
          application_url?: string | null
          benefits?: string[] | null
          company: string
          created_at?: string | null
          description?: string | null
          embedding?: string | null
          experience_level?: string | null
          expires_at?: string | null
          external_id?: string | null
          id?: string
          is_active?: boolean | null
          is_remote?: boolean | null
          job_type?: string | null
          location?: string | null
          posted_at?: string | null
          preferred_skills?: string[] | null
          required_skills?: string[] | null
          requirements?: string[] | null
          responsibilities?: string[] | null
          salary_currency?: string | null
          salary_max?: number | null
          salary_min?: number | null
          source?: string | null
          title: string
          updated_at?: string | null
        }
        Update: {
          application_url?: string | null
          benefits?: string[] | null
          company?: string
          created_at?: string | null
          description?: string | null
          embedding?: string | null
          experience_level?: string | null
          expires_at?: string | null
          external_id?: string | null
          id?: string
          is_active?: boolean | null
          is_remote?: boolean | null
          job_type?: string | null
          location?: string | null
          posted_at?: string | null
          preferred_skills?: string[] | null
          required_skills?: string[] | null
          requirements?: string[] | null
          responsibilities?: string[] | null
          salary_currency?: string | null
          salary_max?: number | null
          salary_min?: number | null
          source?: string | null
          title?: string
          updated_at?: string | null
        }
        Relationships: []
      }
      parsed_resumes: {
        Row: {
          confidence_score: number | null
          created_at: string | null
          education_level: string | null
          experience_years: number | null
          file_key: string | null
          file_name: string | null
          file_size: number | null
          id: string
          is_primary: boolean | null
          keywords: string[] | null
          mime_type: string | null
          parsed_data: Json | null
          parsing_error: string | null
          parsing_status: string | null
          raw_text: string | null
          skills: string[] | null
          updated_at: string | null
          user_id: string
          version: number | null
        }
        Insert: {
          confidence_score?: number | null
          created_at?: string | null
          education_level?: string | null
          experience_years?: number | null
          file_key?: string | null
          file_name?: string | null
          file_size?: number | null
          id?: string
          is_primary?: boolean | null
          keywords?: string[] | null
          mime_type?: string | null
          parsed_data?: Json | null
          parsing_error?: string | null
          parsing_status?: string | null
          raw_text?: string | null
          skills?: string[] | null
          updated_at?: string | null
          user_id: string
          version?: number | null
        }
        Update: {
          confidence_score?: number | null
          created_at?: string | null
          education_level?: string | null
          experience_years?: number | null
          file_key?: string | null
          file_name?: string | null
          file_size?: number | null
          id?: string
          is_primary?: boolean | null
          keywords?: string[] | null
          mime_type?: string | null
          parsed_data?: Json | null
          parsing_error?: string | null
          parsing_status?: string | null
          raw_text?: string | null
          skills?: string[] | null
          updated_at?: string | null
          user_id?: string
          version?: number | null
        }
        Relationships: [
          {
            foreignKeyName: "parsed_resumes_user_id_fkey"
            columns: ["user_id"]
            isOneToOne: false
            referencedRelation: "users"
            referencedColumns: ["id"]
          },
        ]
      }
      saved_jobs: {
        Row: {
          job_id: string
          saved_at: string
          user_id: string
        }
        Insert: {
          job_id: string
          saved_at?: string
          user_id: string
        }
        Update: {
          job_id?: string
          saved_at?: string
          user_id?: string
        }
        Relationships: [
          {
            foreignKeyName: "saved_jobs_job_id_fkey"
            columns: ["job_id"]
            isOneToOne: false
            referencedRelation: "jobs"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "saved_jobs_user_id_fkey"
            columns: ["user_id"]
            isOneToOne: false
            referencedRelation: "users"
            referencedColumns: ["id"]
          },
        ]
      }
      user_interactions: {
        Row: {
          action: string
          created_at: string
          duration_seconds: number | null
          id: string
          job_id: string
          user_id: string
        }
        Insert: {
          action: string
          created_at?: string
          duration_seconds?: number | null
          id?: string
          job_id: string
          user_id: string
        }
        Update: {
          action?: string
          created_at?: string
          duration_seconds?: number | null
          id?: string
          job_id?: string
          user_id?: string
        }
        Relationships: [
          {
            foreignKeyName: "user_interactions_job_id_fkey"
            columns: ["job_id"]
            isOneToOne: false
            referencedRelation: "jobs"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "user_interactions_user_id_fkey"
            columns: ["user_id"]
            isOneToOne: false
            referencedRelation: "users"
            referencedColumns: ["id"]
          },
        ]
      }
      users: {
        Row: {
          auth_id: string | null
          avatar_url: string | null
          created_at: string | null
          email: string
          github_url: string | null
          hashed_password: string
          headline: string | null
          id: string
          is_active: boolean | null
          linkedin_url: string | null
          location: string | null
          name: string
          phone: string | null
          portfolio_url: string | null
          preferences: Json | null
          status: string | null
          updated_at: string | null
        }
        Insert: {
          auth_id?: string | null
          avatar_url?: string | null
          created_at?: string | null
          email: string
          github_url?: string | null
          hashed_password?: string
          headline?: string | null
          id?: string
          is_active?: boolean | null
          linkedin_url?: string | null
          location?: string | null
          name?: string
          phone?: string | null
          portfolio_url?: string | null
          preferences?: Json | null
          status?: string | null
          updated_at?: string | null
        }
        Update: {
          auth_id?: string | null
          avatar_url?: string | null
          created_at?: string | null
          email?: string
          github_url?: string | null
          hashed_password?: string
          headline?: string | null
          id?: string
          is_active?: boolean | null
          linkedin_url?: string | null
          location?: string | null
          name?: string
          phone?: string | null
          portfolio_url?: string | null
          preferences?: Json | null
          status?: string | null
          updated_at?: string | null
        }
        Relationships: []
      }
    }
    Views: {
      [_ in never]: never
    }
    Functions: {
      get_skill_gap_analysis: {
        Args: { p_limit?: number; p_user_id: string }
        Returns: Json
      }
      get_user_dashboard_stats: { Args: { p_user_id: string }; Returns: Json }
      match_skills: {
        Args: { job_skills: string[]; user_skills: string[] }
        Returns: number
      }
    }
    Enums: {
      [_ in never]: never
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
}

type DefaultSchema = Database[Extract<keyof Database, "public">]

export type Tables<
  DefaultSchemaTableNameOrOptions extends
    | keyof (DefaultSchema["Tables"] & DefaultSchema["Views"])
    | { schema: keyof Database },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof Database
  }
    ? keyof (Database[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
        Database[DefaultSchemaTableNameOrOptions["schema"]]["Views"])
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof Database
}
  ? (Database[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
      Database[DefaultSchemaTableNameOrOptions["schema"]]["Views"])[TableName] extends {
      Row: infer R
    }
    ? R
    : never
  : DefaultSchemaTableNameOrOptions extends keyof (DefaultSchema["Tables"] &
        DefaultSchema["Views"])
    ? (DefaultSchema["Tables"] &
        DefaultSchema["Views"])[DefaultSchemaTableNameOrOptions] extends {
        Row: infer R
      }
      ? R
      : never
    : never

export type TablesInsert<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof Database },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof Database
  }
    ? keyof Database[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof Database
}
  ? Database[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Insert: infer I
    }
    ? I
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Insert: infer I
      }
      ? I
      : never
    : never

export type TablesUpdate<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof Database },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof Database
  }
    ? keyof Database[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof Database
}
  ? Database[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Update: infer U
    }
    ? U
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Update: infer U
      }
      ? U
      : never
    : never
