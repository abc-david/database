--
-- PostgreSQL clean script part 3: Insert data for object_models (top 15 records)
--

-- Import data for object_models table using INSERT
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

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '1c0b74eb-8b2f-4e00-a52a-336a905bceea',
  'Book',
  'alpha',
  '1.0',
  '{"name": "Book", "fields": {"isbn": {"args": {"default": "", "description": "International Standard Book Number"}, "type": "str"}, "title": {"args": {"description": "The book title"}, "type": "str"}, "authors": {"args": {"description": "Book authors with details", "default_factory": "list"}, "type": "List[Dict[str, Any]]"}, "subtitle": {"args": {"default": "", "description": "Book subtitle"}, "type": "str"}, "back_matter": {"args": {"description": "Appendices, glossary, index, etc.", "default_factory": "dict"}, "type": "Dict[str, str]"}, "description": {"args": {"description": "Book description or summary"}, "type": "str"}, "front_matter": {"args": {"description": "Title page, copyright, dedication, etc.", "default_factory": "dict"}, "type": "Dict[str, str]"}, "target_audience": {"args": {"description": "Intended readership", "default_factory": "list"}, "type": "List[str]"}, "publication_date": {"args": {"default": "", "description": "Date of publication"}, "type": "str"}, "content_hierarchy": {"args": {"description": "Chapters, sections, appendices structure", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "top_level_keywords": {"args": {"description": "Book-wide keywords", "default_factory": "list"}, "type": "List[Dict[str, str]]"}}, "object_type": "alpha", "metadata_schema": {"required": ["content_type", "primary_language", "target_audience"], "recommended": ["genre", "page_count", "publisher"]}}',
  'Top-level container for book content with chapters, front matter, and back matter',
  ARRAY['Book publishing', 'Technical manuals', 'Educational resources', 'Fiction works'],
  '{}',
  '2025-04-29 14:08:00.329269+02',
  '2025-04-29 14:08:00.329269+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  'd6064135-867c-435d-bedb-5307ebafd236',
  'Ebook',
  'alpha',
  '1.0',
  '{"name": "Ebook", "fields": {"title": {"args": {"description": "The ebook title"}, "type": "str"}, "authors": {"args": {"description": "Ebook authors with details", "default_factory": "list"}, "type": "List[Dict[str, Any]]"}, "subtitle": {"args": {"default": "", "description": "Ebook subtitle"}, "type": "str"}, "back_matter": {"args": {"description": "Appendices, glossary, index, etc.", "default_factory": "dict"}, "type": "Dict[str, str]"}, "description": {"args": {"description": "Ebook description or summary"}, "type": "str"}, "front_matter": {"args": {"description": "Title page, copyright, dedication, etc.", "default_factory": "dict"}, "type": "Dict[str, str]"}, "target_audience": {"args": {"description": "Intended readership", "default_factory": "list"}, "type": "List[str]"}, "digital_features": {"args": {"description": "Digital-specific features like hyperlinks, multimedia, etc.", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "content_hierarchy": {"args": {"description": "Chapters, sections, appendices structure", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "top_level_keywords": {"args": {"description": "Ebook-wide keywords", "default_factory": "list"}, "type": "List[Dict[str, str]]"}}, "object_type": "alpha", "metadata_schema": {"required": ["content_type", "primary_language", "target_audience"], "recommended": ["genre", "page_count", "publisher", "digital_format"]}}',
  'Top-level container for digital book content with specialized digital publishing fields',
  ARRAY['Digital publishing', 'Lead magnets', 'Online courses', 'Digital products'],
  '{Book,EbookChapter}',
  '2025-04-29 14:08:00.330375+02',
  '2025-04-29 14:08:00.330375+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '69cc8c34-29b5-4949-9960-de67c5f84a76',
  'DocumentationSite',
  'alpha',
  '1.0',
  '{"name": "DocumentationSite", "fields": {"name": {"args": {"description": "The documentation site name"}, "type": "str"}, "api_version": {"args": {"default": "", "description": "API version being documented"}, "type": "str"}, "description": {"args": {"description": "Brief description of the documentation purpose"}, "type": "str"}, "target_audience": {"args": {"description": "Intended documentation users", "default_factory": "list"}, "type": "List[str]"}, "primary_language": {"args": {"default": "en-US", "description": "Primary documentation language"}, "type": "str"}, "content_hierarchy": {"args": {"description": "Documentation structure with sections and subsections", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "top_level_keywords": {"args": {"description": "Documentation-wide keywords", "default_factory": "list"}, "type": "List[Dict[str, str]]"}}, "object_type": "alpha", "metadata_schema": {"required": ["content_type", "primary_language", "target_audience"], "recommended": ["api_version", "documentation_type"]}}',
  'Top-level container for technical documentation with sections, API references, and tutorials',
  ARRAY['API documentation', 'Technical guides', 'Developer documentation', 'Product documentation'],
  '{}',
  '2025-04-29 14:08:00.331518+02',
  '2025-04-29 14:08:00.331518+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '189d8f00-e336-4a97-b94b-f3e06ecb0547',
  'BlogPost',
  'beta',
  '1.0',
  '{"name": "BlogPost", "fields": {"slug": {"args": {"description": "URL-friendly version of the title"}, "type": "str"}, "tags": {"args": {"description": "Content classification tags", "default_factory": "list"}, "type": "List[str]"}, "title": {"args": {"description": "The blog post title"}, "type": "str"}, "author": {"args": {"description": "Author information", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "content": {"args": {"description": "Complete markdown content"}, "type": "str"}, "excerpt": {"args": {"default": "", "description": "Brief summary or excerpt"}, "type": "str"}, "keywords": {"args": {"description": "SEO keywords with priority", "default_factory": "list"}, "type": "List[Dict[str, str]]"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "publish_date": {"args": {"default": "", "description": "Publication date"}, "type": "str"}, "extracted_components": {"args": {"description": "Components extracted from markdown content", "default_factory": "dict"}, "type": "Dict[str, List]"}}, "object_type": "beta", "metadata_schema": {"required": ["content_type", "word_count", "tags"], "recommended": ["reading_time", "author_bio"]}}',
  'Standalone blog post with title, content, and metadata',
  ARRAY['Blog content', 'Articles', 'Opinion pieces', 'News updates'],
  '{}',
  '2025-04-29 14:08:00.340693+02',
  '2025-04-29 14:08:00.340693+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '79546481-60b7-40fa-9cb5-2cbc067d9708',
  'LandingPage',
  'beta',
  '1.0',
  '{"name": "LandingPage", "fields": {"slug": {"args": {"description": "URL-friendly version of the title"}, "type": "str"}, "tags": {"args": {"description": "Content classification tags", "default_factory": "list"}, "type": "List[str]"}, "title": {"args": {"description": "The landing page title"}, "type": "str"}, "content": {"args": {"description": "Complete markdown content"}, "type": "str"}, "headline": {"args": {"description": "Main headline or value proposition"}, "type": "str"}, "keywords": {"args": {"description": "SEO keywords with priority", "default_factory": "list"}, "type": "List[Dict[str, str]]"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "subheadline": {"args": {"default": "", "description": "Supporting headline"}, "type": "str"}, "extracted_components": {"args": {"description": "Components extracted from markdown content", "default_factory": "dict"}, "type": "Dict[str, List]"}}, "object_type": "beta", "metadata_schema": {"required": ["content_type", "word_count", "tags"], "recommended": ["conversion_goal", "target_audience"]}}',
  'Conversion-focused page with clear call-to-action',
  ARRAY['Marketing pages', 'Lead generation', 'Product launches', 'Campaign landing pages'],
  '{}',
  '2025-04-29 14:08:00.342039+02',
  '2025-04-29 14:08:00.342039+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  'c68efd7a-c22c-4d1d-8092-887e1c3cc88d',
  'FAQItem',
  'gamma',
  '1.0',
  '{"name": "FAQItem", "fields": {"tags": {"args": {"description": "Classification tags", "default_factory": "list"}, "type": "List[str]"}, "answer": {"args": {"description": "The FAQ answer"}, "type": "str"}, "category": {"args": {"default": "", "description": "FAQ category"}, "type": "str"}, "position": {"args": {"default": 0, "description": "Character position in the parent document"}, "type": "int"}, "question": {"args": {"description": "The FAQ question"}, "type": "str"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}}, "object_type": "gamma", "metadata_schema": {"required": ["content_type", "tags"], "recommended": ["faq_type", "context"]}}',
  'Single question and answer pair',
  ARRAY['FAQs', 'Help content', 'Customer support', 'Educational content'],
  '{}',
  '2025-04-29 14:08:00.365533+02',
  '2025-04-29 14:08:00.365533+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '129e14e0-9eb7-4378-935a-9879fbe76753',
  'Topic',
  'organizer',
  '1.0',
  '{"name": "Topic", "fields": {"icon": {"args": {"default": "", "description": "Icon identifier or URL"}, "type": "str"}, "name": {"args": {"description": "The topic name"}, "type": "str"}, "slug": {"args": {"description": "URL-friendly version of the name"}, "type": "str"}, "tags": {"args": {"description": "Classification tags", "default_factory": "list"}, "type": "List[str]"}, "keywords": {"args": {"description": "SEO keywords with priority", "default_factory": "list"}, "type": "List[Dict[str, str]]"}, "parent_id": {"args": {"default": null, "description": "ID of parent topic (if any)"}, "type": "str"}, "subtopics": {"args": {"description": "List of subtopics", "default_factory": "list"}, "type": "List[Dict[str, Any]]"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "description": {"args": {"description": "Brief description of the topic scope"}, "type": "str"}}, "object_type": "organizer", "metadata_schema": {"required": ["content_type", "tags"], "recommended": ["importance_level", "audience_focus"]}}',
  'Primary subject area',
  ARRAY['Content hierarchies', 'Taxonomies', 'Site architecture', 'Information organization'],
  '{}',
  '2025-04-29 14:08:00.378686+02',
  '2025-04-29 14:08:00.378686+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  'd3141350-820c-4953-a944-16686ab61949',
  'Subtopic',
  'organizer',
  '1.0',
  '{"name": "Subtopic", "fields": {"icon": {"args": {"default": "", "description": "Icon identifier or URL"}, "type": "str"}, "name": {"args": {"description": "The subtopic name"}, "type": "str"}, "slug": {"args": {"description": "URL-friendly version of the name"}, "type": "str"}, "tags": {"args": {"description": "Classification tags", "default_factory": "list"}, "type": "List[str]"}, "order": {"args": {"default": 0, "description": "Display order within parent topic"}, "type": "int"}, "keywords": {"args": {"description": "SEO keywords with priority", "default_factory": "list"}, "type": "List[Dict[str, str]]"}, "parent_id": {"args": {"default": null, "description": "ID of parent topic"}, "type": "str"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "description": {"args": {"description": "Brief description of the subtopic scope"}, "type": "str"}}, "object_type": "organizer", "metadata_schema": {"required": ["content_type", "tags"], "recommended": ["topic_relation", "content_count"]}}',
  'Secondary subject area within a primary topic',
  ARRAY['Content hierarchies', 'Taxonomies', 'Site architecture', 'Information organization'],
  '{}',
  '2025-04-29 14:08:00.379739+02',
  '2025-04-29 14:08:00.379739+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '25e954e2-9371-436f-ae6d-9ca8bba1136e',
  'ReadingTime',
  'qualifier',
  '1.0',
  '{"name": "ReadingTime", "fields": {"minutes": {"args": {"description": "Estimated reading time in minutes"}, "type": "int"}, "word_count": {"args": {"default": 0, "description": "Total word count"}, "type": "int"}, "reading_speed": {"args": {"default": 200, "description": "Words per minute for calculation"}, "type": "int"}}, "object_type": "qualifier", "metadata_schema": {"required": ["content_type"], "recommended": ["content_type", "target_audience"]}}',
  'Estimated consumption duration',
  ARRAY['Content metrics', 'User experience', 'Content planning', 'Engagement metrics'],
  '{}',
  '2025-04-29 14:08:00.397215+02',
  '2025-04-29 14:08:00.397215+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  'e58c7de0-c63d-48e2-91fc-46de2a73bf70',
  'Keyword',
  'qualifier',
  '1.0',
  '{"name": "Keyword", "fields": {"cpc": {"args": {"default": 0.0, "description": "Cost per click"}, "type": "float"}, "keyword": {"args": {"description": "The keyword term"}, "type": "str"}, "difficulty": {"args": {"ge": 0.0, "le": 100.0, "default": 0.0, "description": "Keyword difficulty score"}, "type": "float"}, "competition": {"args": {"ge": 0.0, "le": 1.0, "default": 0.0, "description": "Competition level"}, "type": "float"}, "search_intent": {"args": {"default": "informational", "description": "Search intent type"}, "type": "str"}, "search_volume": {"args": {"default": 0, "description": "Monthly search volume"}, "type": "int"}}, "object_type": "qualifier", "metadata_schema": {"required": ["content_type"], "recommended": ["keyword_type", "target_audience"]}}',
  'SEO search term',
  ARRAY['SEO optimization', 'Content targeting', 'Search marketing', 'Content strategy'],
  '{}',
  '2025-04-29 14:08:00.391497+02',
  '2025-04-29 14:08:00.391497+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '323a0930-1458-4320-a92d-d9e2c47f7503',
  'Audience',
  'qualifier',
  '1.0',
  '{"name": "Audience", "fields": {"name": {"args": {"description": "The audience name"}, "type": "str"}, "interests": {"args": {"description": "Audience interests", "default_factory": "list"}, "type": "List[str]"}, "description": {"args": {"description": "Brief description of the audience"}, "type": "str"}, "pain_points": {"args": {"description": "Audience pain points", "default_factory": "list"}, "type": "List[str]"}, "demographics": {"args": {"description": "Demographic information", "default_factory": "dict"}, "type": "Dict[str, Any]"}}, "object_type": "qualifier", "metadata_schema": {"required": ["content_type"], "recommended": ["audience_size", "engagement_level"]}}',
  'Target reader/user group',
  ARRAY['Content targeting', 'Audience segmentation', 'Content strategy', 'Marketing'],
  '{}',
  '2025-04-29 14:08:00.392676+02',
  '2025-04-29 14:08:00.392676+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '0ce84ba4-0f84-4f44-a90c-ee1c94224152',
  'KeyTakeaway',
  'gamma',
  '1.0',
  '{"name": "KeyTakeaway", "fields": {"tags": {"args": {"description": "Classification tags", "default_factory": "list"}, "type": "List[str]"}, "text": {"args": {"description": "The key takeaway text"}, "type": "str"}, "position": {"args": {"default": 0, "description": "Character position in the parent document"}, "type": "int"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "importance": {"args": {"default": "high", "description": "Level of importance"}, "type": "str"}}, "object_type": "gamma", "metadata_schema": {"required": ["content_type", "tags"], "recommended": ["takeaway_type", "context"]}}',
  'Important conclusion or learning',
  ARRAY['Educational content', 'Summaries', 'Learning points', 'Content highlights'],
  '{}',
  '2025-04-29 14:08:00.364369+02',
  '2025-04-29 14:08:00.364369+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  'c1781e08-0764-4512-b463-7d6c1cc3dcca',
  'Whitepaper',
  'beta',
  '1.0',
  '{"name": "Whitepaper", "fields": {"slug": {"args": {"description": "URL-friendly version of the title"}, "type": "str"}, "tags": {"args": {"description": "Content classification tags", "default_factory": "list"}, "type": "List[str]"}, "title": {"args": {"description": "The whitepaper title"}, "type": "str"}, "authors": {"args": {"description": "Authors of the whitepaper", "default_factory": "list"}, "type": "List[Dict[str, Any]]"}, "content": {"args": {"description": "Complete markdown content"}, "type": "str"}, "abstract": {"args": {"description": "Brief summary of the whitepaper"}, "type": "str"}, "industry": {"args": {"default": "", "description": "Industry focus"}, "type": "str"}, "keywords": {"args": {"description": "SEO keywords with priority", "default_factory": "list"}, "type": "List[Dict[str, str]]"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "publication_date": {"args": {"default": "", "description": "Date of publication"}, "type": "str"}, "extracted_components": {"args": {"description": "Components extracted from markdown content", "default_factory": "dict"}, "type": "Dict[str, List]"}}, "object_type": "beta", "metadata_schema": {"required": ["content_type", "word_count", "tags"], "recommended": ["research_type", "target_audience"]}}',
  'In-depth report on a specific topic or industry',
  ARRAY['Industry reports', 'Research papers', 'Technical documentation', 'Thought leadership'],
  '{}',
  '2025-04-29 14:08:00.350454+02',
  '2025-04-29 14:08:00.350454+02'
);

-- Revoke and grant schema privileges
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO david; 