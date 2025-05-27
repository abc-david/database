--
-- PostgreSQL clean script part 1: Create tables and constraints
--

-- Drop tables if they exist (in reverse order of dependencies)
DROP TABLE IF EXISTS public.prompts CASCADE;
DROP TABLE IF EXISTS public.projects CASCADE;
DROP TABLE IF EXISTS public.object_models CASCADE;

-- Create tables
CREATE TABLE IF NOT EXISTS public.object_models (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying(100) NOT NULL,
    object_type character varying(50) NOT NULL,
    version character varying(20) DEFAULT '1.0'::character varying NOT NULL,
    definition jsonb NOT NULL,
    description text NOT NULL,
    use_cases text[] NOT NULL,
    related_templates text[] DEFAULT '{}'::text[] NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.projects (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying(255) NOT NULL,
    schema_name character varying(100) NOT NULL,
    description jsonb DEFAULT '{}'::jsonb NOT NULL,
    created_by uuid,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    primary_language character varying(50) DEFAULT 'en'::character varying NOT NULL,
    status character varying(50) DEFAULT 'draft'::character varying NOT NULL,
    project_type character varying(50) DEFAULT 'content'::character varying NOT NULL,
    vector_collection_id character varying(255),
    parent_project_id uuid,
    is_template boolean DEFAULT false,
    CONSTRAINT valid_description CHECK ((jsonb_typeof(description) = 'object'::text)),
    CONSTRAINT valid_project_type CHECK (((project_type)::text = ANY (ARRAY[('content'::character varying)::text, ('seo'::character varying)::text, ('chatbot'::character varying)::text])))
);

CREATE TABLE IF NOT EXISTS public.prompts (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying(100) NOT NULL,
    description text,
    engine_type character varying(50) NOT NULL,
    template_type character varying(50) NOT NULL,
    template jsonb NOT NULL,
    version character varying(20) DEFAULT '1.0'::character varying NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    use_cases text[] DEFAULT '{}'::text[] NOT NULL
);

-- Add constraints
ALTER TABLE ONLY public.object_models
    ADD CONSTRAINT object_model_templates_name_key UNIQUE (name);

ALTER TABLE ONLY public.object_models
    ADD CONSTRAINT object_model_templates_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_schema_name_key UNIQUE (schema_name);

ALTER TABLE ONLY public.prompts
    ADD CONSTRAINT prompt_templates_pkey PRIMARY KEY (id);

-- Add foreign keys
ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_parent_project_id_fkey FOREIGN KEY (parent_project_id) REFERENCES public.projects(id);

-- Create useful indexes
CREATE INDEX object_model_templates_name_idx ON public.object_models USING btree (name);
CREATE INDEX object_model_templates_object_type_idx ON public.object_models USING btree (object_type);
CREATE INDEX projects_created_at_idx ON public.projects USING btree (created_at);
CREATE INDEX projects_description_idx ON public.projects USING gin (description jsonb_path_ops);
CREATE INDEX projects_name_idx ON public.projects USING btree (name);
CREATE INDEX projects_primary_language_idx ON public.projects USING btree (primary_language);
CREATE INDEX projects_project_type_idx ON public.projects USING btree (project_type);
CREATE INDEX projects_status_idx ON public.projects USING btree (status);
CREATE INDEX idx_prompt_templates_active ON public.prompts USING btree (is_active);
CREATE INDEX idx_prompt_templates_engine_type ON public.prompts USING btree (engine_type);
CREATE INDEX prompt_templates_engine_type_idx ON public.prompts USING btree (engine_type);
CREATE INDEX prompt_templates_template_type_idx ON public.prompts USING btree (template_type); 