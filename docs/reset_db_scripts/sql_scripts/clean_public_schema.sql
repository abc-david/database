--
-- PostgreSQL clean script for public schema with core tables
-- Cleaned version for production use
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

-- Import data for object_models table using INSERT instead of COPY
INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  'd945567f-2633-4f18-ae73-cc5a9dfb2fe3',
  'Website',
  'alpha',
  '1.0',
  '{"name": "Website", "fields": {"name": {"args": {"description": "The website name"}, "type": "str"}, "domain": {"args": {"description": "Primary domain name"}, "type": "str"}, "brand_voice": {"args": {"description": "Tone and style of content"}, "type": "str"}, "description": {"args": {"description": "Brief description of the website purpose and content"}, "type": "str"}, "target_audience": {"args": {"description": "Primary target audiences", "default_factory": "list"}, "type": "List[str]"}, "primary_language": {"args": {"default": "en-US", "description": "Primary content language"}, "type": "str"}, "content_hierarchy": {"args": {"description": "Hierarchical organization of all content", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "top_level_keywords": {"args": {"description": "Site-wide SEO keywords", "default_factory": "list"}, "type": "List[Dict[str, str]]"}}, "object_type": "alpha", "metadata_schema": {"required": ["content_type", "primary_language", "target_audience"], "recommended": ["business_vertical", "competitors"]}}',
  'Top-level container for website content with topics, categories, and settings',
  ARRAY['Content marketing websites', 'Blogs', 'Documentation sites', 'Product websites'],
  '{}',
  '2025-04-29 14:08:00.326871+02',
  '2025-04-29 14:08:00.326871+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  'ba7c1a79-0f40-4098-b766-a231b1a2cb78',
  'TopicMap',
  'alpha',
  '1.0',
  '{"name": "TopicMap", "fields": {"title": {"args": {"description": "Title of the topic map"}, "type": "str"}, "topics": {"args": {"description": "List of main topics in this topic map", "default_factory": "list"}, "type": "List[Dict[str, Any]]"}, "industry": {"args": {"description": "Industry this topic map is for"}, "type": "str"}, "metadata": {"args": {"description": "Additional metadata about this topic map", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "rationale": {"args": {"description": "Explanation of the rationale behind this topic organization"}, "type": "str"}, "conversion_goal": {"args": {"description": "Primary conversion goal for the content strategy"}, "type": "str"}, "target_audience": {"args": {"description": "Primary target audience for the content"}, "type": "str"}, "strategic_recommendations": {"args": {"description": "Strategic recommendations for implementing this content strategy", "default_factory": "list"}, "type": "List[str]"}}, "object_type": "alpha", "metadata_schema": {"required": ["content_type", "target_audience", "industry"], "recommended": ["conversion_goal", "business_vertical"]}}',
  'Top-level container for content strategy organization with topics and subtopics',
  ARRAY['Content Strategy Planning', 'SEO Content Mapping', 'Editorial Calendar Development', 'Content Gap Analysis'],
  '{TopicMapperGenericTemplate}',
  '2025-05-13 16:18:22.577616+02',
  '2025-05-15 20:12:17.034632+02'
);

-- Import data for projects table using INSERT
INSERT INTO public.projects (id, name, schema_name, description, created_by, created_at, updated_at, primary_language, status, project_type, vector_collection_id, parent_project_id, is_template)
VALUES (
  '608f473d-fb5c-473c-960d-7b4dede729c2',
  'B2B_SaaS',
  'b2b_saas',
  '{"seo": {"default_meta_title": "B2B SaaS Tools for Enhanced Productivity | AI-Powered Solutions", "default_meta_keywords": "B2B SaaS, productivity tools, AI business tools, project management, automation, business analytics, CRM, document management", "default_meta_description": "Discover the best B2B SaaS tools to boost your team''s productivity. Expert reviews, comparisons, and implementation guides for AI-powered business solutions."}, "text": "A comprehensive resource for B2B SaaS tools that enhance business productivity and efficiency, with a focus on AI-powered solutions.", "topics": {"products": ["Asana", "Monday.com", "ClickUp", "Slack", "Microsoft Teams", "Zoom", "Zapier", "Make", "n8n", "Tableau", "Power BI", "Looker", "ChatGPT for Business", "Jasper", "Grammarly Business", "Salesforce", "HubSpot", "Pipedrive", "Notion", "Confluence", "SharePoint"], "categories": ["Project Management", "Communication", "Automation", "Analytics", "AI Tools", "CRM", "Document Management"], "main_topic": "B2B SaaS Tools to Improve Productivity (Leveraging AI)", "description": "A comprehensive guide to B2B SaaS tools that enhance business productivity, with special focus on AI-powered solutions. Covering tools for project management, communication, automation, analytics, and more.", "max_pillars": 7, "min_pillars": 5}, "content": {"types": ["guides", "reviews", "comparisons", "case_studies", "tutorials"], "audience": ["ctos", "it_directors", "operations_managers", "business_process_owners", "department_heads"], "industry": "business_software", "brand_voice": ["professional", "authoritative", "practical", "clear", "technical"], "format_options": ["websites", "ebooks", "email_sequences", "webinars"], "preferred_length": "comprehensive", "update_frequency": "weekly"}, "business": {"intention": "To become the go-to reference for B2B decision-makers seeking productivity-enhancing SaaS tools.", "competitors": ["G2", "Capterra", "Software Advice"], "differentiation": ["Focus on productivity metrics and ROI", "Detailed integration guides", "Real-world use cases", "AI-specific tool analysis", "Regular updates on new features"], "for_b2b_audience": true, "for_b2c_audience": false, "unique_selling_points": ["ROI-focused tool analysis", "Integration compatibility guides", "Productivity metrics comparison", "AI implementation strategies", "Regular industry updates", "Expert-curated recommendations"], "for_affiliate_marketing": true}, "metadata": {"tags": ["productivity", "b2b", "saas", "ai", "business", "software"], "creation": {"creator_name": "Admin", "creation_date": "2023-08-15"}, "languages": {"primary": "en", "secondary": []}}, "extensions": {"seo": {"enabled": true, "seed_topics": ["b2b saas productivity", "ai for business productivity", "project management tools"]}, "analytics": {"enabled": true, "google_analytics_id": null, "google_search_console_verified": false}}, "objectives": {"goals": ["establish_authority_in_b2b_saas", "drive_qualified_traffic", "generate_affiliate_revenue", "build_email_list", "create_resource_library"], "success_metrics": {"conversion_rate": 3.5, "monthly_visitors": 10000, "affiliate_revenue": 5000, "email_subscribers": 2000}}, "localization": {"locale": "en_US", "timezone": "UTC", "date_format": "%Y-%m-%d", "time_format": "%H:%M:%S"}}',
  NULL,
  '2025-05-19 17:31:21.069595+02',
  '2025-05-19 17:31:21.069595+02',
  'en',
  'active',
  'content',
  NULL,
  NULL,
  false
);

-- Import data for prompts table using INSERT
INSERT INTO public.prompts (id, name, description, engine_type, template_type, template, version, is_active, created_at, updated_at, use_cases)
VALUES (
  'af45a91c-6e16-4d12-8d8a-65fc248efadc',
  'TopicMapperGenericTemplate',
  'Creates a conceptual topic map for a project''s knowledge space, which can be later merged with SEO data to form the website structure',
  'gpt-4',
  'topic_mapping',
  '{"name": "TopicMapperGenericTemplate", "user_input": {"focused_question": {"mandatory": true, "generation": {"placeholders": {"optional": ["project_description.topics.main_topics"], "mandatory": ["project_description.name", "project_description.content.industry", "project_description.content.audience", "project_description.business.intention"]}, "prompt_template": "Based on the following request details, create a single focused question that will retrieve the most relevant context for creating a topic map:\\\\n\\\\nProject Name: {project_description.name}\\\\nIndustry: {project_description.content.industry}\\\\nTarget Audience: {project_description.content.audience}\\\\nBusiness Intention: {project_description.business.intention}\\\\nMain Topics: {project_description.topics.main_topics}\\\\n\\\\nRespond with ONLY the focused question, using natural language that will match semantically similar content in our vector database."}, "resolution_time": "runtime", "resolution_method": "llm_predict"}}, "description": "Creates a conceptual topic map for a project''s knowledge space, which can be later merged with SEO data to form the website structure", "human_message": {"output_format": {"object_models": ["TopicMap"]}}, "template_type": "topic_mapping", "system_message": {"agent_goal": {"example": "Your goal is to identify 5-8 major topic areas and 3-6 subtopics for each, creating a foundational knowledge structure that will later be merged with SEO data to form the final website architecture.", "mandatory": true, "placeholders": {"optional": [], "mandatory": []}, "resolution_time": "adaptation", "resolution_method": "llm_adaptation", "plain_text_example": "Your goal is to identify 5-8 major topic areas and 3-6 subtopics for each, creating a foundational knowledge structure that will later be merged with SEO data to form the final website architecture."}, "agent_role": {"example": "You are a {template.agent_role} specializing in {template.agent_experience} for {project_description.content.industry} projects.", "mandatory": true, "placeholders": {"optional": [], "mandatory": ["project_description.content.industry", "template.agent_role", "template.agent_experience"]}, "resolution_time": "adaptation", "resolution_method": "llm_adaptation", "plain_text_example": "You are a topic mapping strategist specializing in information architecture and knowledge organization for technology education projects."}, "agent_task": {"example": "Using the provided context, {template.primary_task} that captures the essential knowledge domains of {project_description.name} and aligns with {project_description.business.intention}.", "mandatory": true, "placeholders": {"optional": [], "mandatory": ["project_description.name", "project_description.business.intention", "template.primary_task"]}, "resolution_time": "adaptation", "resolution_method": "llm_adaptation", "plain_text_example": "Using the provided context, create a conceptual topic map that captures the essential knowledge domains of AI Learning Hub and aligns with establishing thought leadership in AI education."}, "agent_tools": {"example": "AVAILABLE TOOLS:\\\\n{tools_list}", "mandatory": false, "placeholders": {"optional": [], "mandatory": ["tools_list"]}, "resolution_time": "runtime", "resolution_method": "langchain_injection"}, "output_format": {"example": "The output must be a valid JSON object with this structure:\\\\n\\\\n{object_model.output_schema}", "mandatory": true, "placeholders": {"optional": [], "mandatory": ["object_model.output_schema"]}, "resolution_time": "runtime", "resolution_method": "pydantic_mirroring"}, "agent_response": {"example": "Your response must include:\\\\n1. A conceptual topic map with 5-8 major topic areas\\\\n2. 3-6 subtopics for each major topic area\\\\n3. A brief explanation of the rationale behind your topic organization\\\\n4. Suggestions for potential content types within each topic area\\\\n\\\\nFocus on creating a logical knowledge structure rather than SEO optimization, as this will be merged with SEO data later.", "mandatory": true, "placeholders": {"optional": [], "mandatory": []}, "resolution_time": "runtime", "resolution_method": "langchain_injection"}, "key_information": {"example": "Positioning Statement: {positioning_sentence}\\\\nProject Name: {project_description.name}\\\\nIndustry: {project_description.content.industry}\\\\nBusiness Context: {project_description.business.intention}\\\\nTarget Audience: {project_description.content.audience}\\\\nProject Description: {project_description.text}\\\\nMain Topics: {project_description.topics.main_topics}", "mandatory": true, "placeholders": {"optional": ["positioning_sentence", "project_description.text", "project_description.topics.main_topics"], "mandatory": ["project_description.name", "project_description.content.industry", "project_description.content.audience", "project_description.business.intention"]}, "resolution_time": "runtime", "resolution_method": "langchain_injection"}, "context_placeholder": {"example": "{context_placeholder}", "mandatory": true, "placeholders": {"optional": [], "mandatory": ["context_placeholder"]}, "resolution_time": "runtime", "resolution_method": "langchain_injection"}, "closing_instructions": {"example": "Balance breadth and depth in your topic map. Include evergreen topics that will remain relevant over time, while allowing space for trending or emerging topics in {project_description.content.industry}.", "mandatory": false, "placeholders": {"optional": ["project_description.content.industry"], "mandatory": []}, "resolution_time": "adaptation", "resolution_method": "llm_adaptation", "plain_text_example": "Balance breadth and depth in your topic map. Include evergreen topics that will remain relevant over time, while allowing space for trending or emerging topics in artificial intelligence."}, "positioning_sentence": {"example": "A concise statement capturing the core identity and strategic intent of this {project_description.content.industry} project''s knowledge organization.", "mandatory": false, "placeholders": {"optional": [], "mandatory": ["project_description.content.industry"]}, "resolution_time": "adaptation", "resolution_method": "llm_adaptation", "plain_text_example": "Organizing complex {project_description.content.industry} knowledge into an intuitive structure that aligns with both user mental models and business objectives."}, "additional_instructions": {"example": "Consider both the hierarchy and potential interconnections between topics. Focus on {project_description.topics.main_topic} as a central organizing principle, ensuring all content serves {project_description.content.audience} in their journey.", "mandatory": false, "placeholders": {"optional": ["project_description.topics.main_topic", "project_description.content.audience"], "mandatory": []}, "resolution_time": "adaptation", "resolution_method": "llm_adaptation", "plain_text_example": "Consider both the hierarchy and potential interconnections between topics. Focus on artificial intelligence as a central organizing principle, ensuring all content serves software developers in their learning journey."}}, "template_defaults": {"agent_role": "topic mapping strategist", "tone_style": "analytical and practical", "primary_task": "create a conceptual topic map", "expertise_areas": ["information architecture", "content strategy", "knowledge organization", "topic clustering"], "agent_experience": "information architecture and knowledge organization"}}',
  '1.0',
  true,
  '2025-05-07 21:29:40.900216+02',
  '2025-05-13 16:18:27.029175+02',
  ARRAY['Topic Mapping', 'Information Architecture', 'Content Strategy']
);

-- Revoke and grant public schema privileges
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO david; 