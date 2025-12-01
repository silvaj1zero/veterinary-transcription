-- ================================================
-- SCHEMA SUPABASE - VETERINARY TRANSCRIPTION SYSTEM
-- ================================================
-- Este arquivo contém o schema completo para o Supabase
-- Execute este SQL no Supabase SQL Editor após criar o projeto
-- ================================================

-- Habilitar extensões necessárias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ================================================
-- TABELA: user_profiles
-- ================================================
-- Perfis complementares aos usuários do Supabase Auth
-- Relaciona-se com auth.users via user_id
-- ================================================

CREATE TABLE IF NOT EXISTS public.user_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user' CHECK (role IN ('admin', 'user', 'viewer')),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES auth.users(id),
    metadata JSONB DEFAULT '{}'::jsonb,

    -- Constraints
    UNIQUE(user_id)
);

-- Índices para performance
CREATE INDEX idx_user_profiles_user_id ON public.user_profiles(user_id);
CREATE INDEX idx_user_profiles_role ON public.user_profiles(role);
CREATE INDEX idx_user_profiles_is_active ON public.user_profiles(is_active);

-- ================================================
-- TABELA: login_attempts
-- ================================================
-- Histórico de tentativas de login para auditoria
-- ================================================

CREATE TABLE IF NOT EXISTS public.login_attempts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    email TEXT NOT NULL,
    success BOOLEAN NOT NULL,
    ip_address TEXT,
    user_agent TEXT,
    error_message TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para consultas rápidas
CREATE INDEX idx_login_attempts_user_id ON public.login_attempts(user_id);
CREATE INDEX idx_login_attempts_email ON public.login_attempts(email);
CREATE INDEX idx_login_attempts_timestamp ON public.login_attempts(timestamp DESC);
CREATE INDEX idx_login_attempts_success ON public.login_attempts(success);

-- ================================================
-- TABELA: reports
-- ================================================
-- Metadados dos relatórios gerados
-- Os arquivos reais ficam no Supabase Storage
-- ================================================

CREATE TABLE IF NOT EXISTS public.reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_by UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    patient_name TEXT NOT NULL,
    patient_species TEXT,
    patient_breed TEXT,
    patient_age_weight TEXT,
    tutor_name TEXT,
    consultation_date DATE,
    consultation_type TEXT,
    file_path TEXT, -- Caminho no Supabase Storage
    file_size INTEGER,
    has_tutor_summary BOOLEAN DEFAULT false,
    transcription_provider TEXT, -- 'whisper' ou 'gemini'
    llm_provider TEXT, -- 'claude' ou 'gemini'
    tokens_used_input INTEGER,
    tokens_used_output INTEGER,
    cost_estimate DECIMAL(10, 4),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Índices
CREATE INDEX idx_reports_created_by ON public.reports(created_by);
CREATE INDEX idx_reports_patient_name ON public.reports(patient_name);
CREATE INDEX idx_reports_consultation_date ON public.reports(consultation_date DESC);
CREATE INDEX idx_reports_created_at ON public.reports(created_at DESC);

-- ================================================
-- TABELA: transcriptions
-- ================================================
-- Histórico de transcrições de áudio
-- ================================================

CREATE TABLE IF NOT EXISTS public.transcriptions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_by UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    audio_file_path TEXT, -- Caminho no Storage
    audio_file_size INTEGER,
    audio_duration DECIMAL(10, 2), -- em segundos
    transcription_text TEXT,
    transcription_provider TEXT, -- 'whisper' ou 'gemini'
    model_used TEXT,
    processing_time DECIMAL(10, 2), -- em segundos
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Índices
CREATE INDEX idx_transcriptions_created_by ON public.transcriptions(created_by);
CREATE INDEX idx_transcriptions_created_at ON public.transcriptions(created_at DESC);

-- ================================================
-- TRIGGERS: Updated At
-- ================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_user_profiles_updated_at
    BEFORE UPDATE ON public.user_profiles
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_reports_updated_at
    BEFORE UPDATE ON public.reports
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ================================================
-- ROW LEVEL SECURITY (RLS)
-- ================================================

-- Habilitar RLS em todas as tabelas
ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.login_attempts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.transcriptions ENABLE ROW LEVEL SECURITY;

-- ================================================
-- POLICIES: user_profiles
-- ================================================

-- Admin pode ver todos os perfis
CREATE POLICY "Admins can view all profiles"
    ON public.user_profiles
    FOR SELECT
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM public.user_profiles
            WHERE user_id = auth.uid() AND role = 'admin'
        )
    );

-- Usuários podem ver seu próprio perfil
CREATE POLICY "Users can view own profile"
    ON public.user_profiles
    FOR SELECT
    TO authenticated
    USING (user_id = auth.uid());

-- Admin pode criar perfis
CREATE POLICY "Admins can create profiles"
    ON public.user_profiles
    FOR INSERT
    TO authenticated
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.user_profiles
            WHERE user_id = auth.uid() AND role = 'admin'
        )
    );

-- Admin pode atualizar perfis
CREATE POLICY "Admins can update profiles"
    ON public.user_profiles
    FOR UPDATE
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM public.user_profiles
            WHERE user_id = auth.uid() AND role = 'admin'
        )
    );

-- Usuários podem atualizar seu próprio perfil (exceto role)
CREATE POLICY "Users can update own profile"
    ON public.user_profiles
    FOR UPDATE
    TO authenticated
    USING (user_id = auth.uid())
    WITH CHECK (user_id = auth.uid() AND role = (SELECT role FROM public.user_profiles WHERE user_id = auth.uid()));

-- ================================================
-- POLICIES: reports
-- ================================================

-- Usuários podem ver seus próprios relatórios
CREATE POLICY "Users can view own reports"
    ON public.reports
    FOR SELECT
    TO authenticated
    USING (created_by = auth.uid());

-- Admins podem ver todos os relatórios
CREATE POLICY "Admins can view all reports"
    ON public.reports
    FOR SELECT
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM public.user_profiles
            WHERE user_id = auth.uid() AND role = 'admin'
        )
    );

-- Usuários autenticados podem criar relatórios
CREATE POLICY "Authenticated users can create reports"
    ON public.reports
    FOR INSERT
    TO authenticated
    WITH CHECK (created_by = auth.uid());

-- Usuários podem atualizar seus próprios relatórios
CREATE POLICY "Users can update own reports"
    ON public.reports
    FOR UPDATE
    TO authenticated
    USING (created_by = auth.uid());

-- ================================================
-- POLICIES: transcriptions
-- ================================================

-- Usuários podem ver suas próprias transcrições
CREATE POLICY "Users can view own transcriptions"
    ON public.transcriptions
    FOR SELECT
    TO authenticated
    USING (created_by = auth.uid());

-- Admins podem ver todas as transcrições
CREATE POLICY "Admins can view all transcriptions"
    ON public.transcriptions
    FOR SELECT
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM public.user_profiles
            WHERE user_id = auth.uid() AND role = 'admin'
        )
    );

-- Usuários autenticados podem criar transcrições
CREATE POLICY "Authenticated users can create transcriptions"
    ON public.transcriptions
    FOR INSERT
    TO authenticated
    WITH CHECK (created_by = auth.uid());

-- ================================================
-- POLICIES: login_attempts
-- ================================================

-- Apenas admins podem ver tentativas de login
CREATE POLICY "Admins can view login attempts"
    ON public.login_attempts
    FOR SELECT
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM public.user_profiles
            WHERE user_id = auth.uid() AND role = 'admin'
        )
    );

-- Sistema pode inserir tentativas de login (via service_role)
CREATE POLICY "System can insert login attempts"
    ON public.login_attempts
    FOR INSERT
    TO authenticated
    WITH CHECK (true);

-- ================================================
-- FUNÇÃO: Criar perfil automaticamente após signup
-- ================================================

CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.user_profiles (user_id, full_name, role, created_by)
    VALUES (
        NEW.id,
        COALESCE(NEW.raw_user_meta_data->>'full_name', NEW.email),
        COALESCE(NEW.raw_user_meta_data->>'role', 'user'),
        NEW.id
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger para criar perfil automaticamente
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW
    EXECUTE FUNCTION public.handle_new_user();

-- ================================================
-- DADOS INICIAIS: Criar admin padrão
-- ================================================
-- ATENÇÃO: Execute este bloco MANUALMENTE após criar o primeiro usuário admin via Supabase Dashboard
-- Substitua 'USER_ID_DO_ADMIN_AQUI' pelo ID real do usuário admin
-- ================================================

/*
-- Atualizar perfil do admin
UPDATE public.user_profiles
SET role = 'admin', full_name = 'Administrador'
WHERE user_id = 'USER_ID_DO_ADMIN_AQUI';
*/

-- ================================================
-- VIEWS ÚTEIS
-- ================================================

-- View: Estatísticas de usuários
CREATE OR REPLACE VIEW public.user_stats AS
SELECT
    COUNT(*) as total_users,
    COUNT(*) FILTER (WHERE role = 'admin') as total_admins,
    COUNT(*) FILTER (WHERE role = 'user') as total_users_regular,
    COUNT(*) FILTER (WHERE is_active = true) as active_users,
    COUNT(*) FILTER (WHERE is_active = false) as inactive_users
FROM public.user_profiles;

-- View: Estatísticas de relatórios
CREATE OR REPLACE VIEW public.report_stats AS
SELECT
    COUNT(*) as total_reports,
    COUNT(*) FILTER (WHERE DATE(created_at) = CURRENT_DATE) as reports_today,
    COUNT(*) FILTER (WHERE DATE(created_at) >= CURRENT_DATE - INTERVAL '7 days') as reports_this_week,
    COUNT(*) FILTER (WHERE DATE(created_at) >= CURRENT_DATE - INTERVAL '30 days') as reports_this_month,
    SUM(cost_estimate) as total_cost,
    SUM(cost_estimate) FILTER (WHERE DATE(created_at) = CURRENT_DATE) as cost_today,
    AVG(tokens_used_input) as avg_tokens_input,
    AVG(tokens_used_output) as avg_tokens_output
FROM public.reports;

-- ================================================
-- GRANTS: Permissões para authenticated users
-- ================================================

GRANT USAGE ON SCHEMA public TO authenticated;
GRANT ALL ON public.user_profiles TO authenticated;
GRANT ALL ON public.login_attempts TO authenticated;
GRANT ALL ON public.reports TO authenticated;
GRANT ALL ON public.transcriptions TO authenticated;
GRANT SELECT ON public.user_stats TO authenticated;
GRANT SELECT ON public.report_stats TO authenticated;

-- ================================================
-- FIM DO SCHEMA
-- ================================================
-- Próximos passos:
-- 1. Criar projeto no Supabase
-- 2. Executar este SQL no SQL Editor
-- 3. Criar bucket de storage para áudios e relatórios
-- 4. Configurar variáveis de ambiente no .env
-- ================================================
