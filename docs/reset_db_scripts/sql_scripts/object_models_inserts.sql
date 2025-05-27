-- Generated INSERT statements for object_models

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  'd945567f-2633-4f18-ae73-cc5a9dfb2fe3',
  'Website',
  'alpha',
  '1.0',
  '{"name": "Website", "fields": {"name": {"args": {"description": "The website name"}, "type": "str"}, "domain": {"args": {"description": "Primary domain name"}, "type": "str"}, "brand_voice": {"args": {"description": "Tone and style of content"}, "type": "str"}, "description": {"args": {"description": "Brief description of the website purpose and content"}, "type": "str"}, "target_audience": {"args": {"description": "Primary target audiences", "default_factory": "list"}, "type": "List[str]"}, "primary_language": {"args": {"default": "en-US", "description": "Primary content language"}, "type": "str"}, "content_hierarchy": {"args": {"description": "Hierarchical organization of all content", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "top_level_keywords": {"args": {"description": "Site-wide SEO keywords", "default_factory": "list"}, "type": "List[Dict[str, str]]"}}, "object_type": "alpha", "metadata_schema": {"required": ["content_type", "primary_language", "target_audience"], "recommended": ["business_vertical", "competitors"]}}',
  'Top-level container for website content with topics, categories, and settings',
  ARRAY["Content marketing websites",Blogs,"Documentation sites","Product websites"],
  '{}',
  '2025-04-29 14:08:00.326871+02',
  '2025-04-29 14:08:00.326871+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '1c0b74eb-8b2f-4e00-a52a-336a905bceea',
  'Book',
  'alpha',
  '1.0',
  '{"name": "Book", "fields": {"isbn": {"args": {"default": "", "description": "International Standard Book Number"}, "type": "str"}, "title": {"args": {"description": "The book title"}, "type": "str"}, "authors": {"args": {"description": "Book authors with details", "default_factory": "list"}, "type": "List[Dict[str, Any]]"}, "subtitle": {"args": {"default": "", "description": "Book subtitle"}, "type": "str"}, "back_matter": {"args": {"description": "Appendices, glossary, index, etc.", "default_factory": "dict"}, "type": "Dict[str, str]"}, "description": {"args": {"description": "Book description or summary"}, "type": "str"}, "front_matter": {"args": {"description": "Title page, copyright, dedication, etc.", "default_factory": "dict"}, "type": "Dict[str, str]"}, "target_audience": {"args": {"description": "Intended readership", "default_factory": "list"}, "type": "List[str]"}, "publication_date": {"args": {"default": "", "description": "Date of publication"}, "type": "str"}, "content_hierarchy": {"args": {"description": "Chapters, sections, appendices structure", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "top_level_keywords": {"args": {"description": "Book-wide keywords", "default_factory": "list"}, "type": "List[Dict[str, str]]"}}, "object_type": "alpha", "metadata_schema": {"required": ["content_type", "primary_language", "target_audience"], "recommended": ["genre", "page_count", "publisher"]}}',
  'Top-level container for book content with chapters, front matter, and back matter',
  ARRAY["Book publishing","Technical manuals","Educational resources","Fiction works"],
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
  ARRAY["Digital publishing","Lead magnets","Online courses","Digital products"],
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
  ARRAY["API documentation","Technical guides","Developer documentation","Product documentation"],
  '{}',
  '2025-04-29 14:08:00.331518+02',
  '2025-04-29 14:08:00.331518+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '8c3efa1e-2144-4341-930f-14ed9a7118db',
  'KnowledgeBase',
  'alpha',
  '1.0',
  '{"name": "KnowledgeBase", "fields": {"name": {"args": {"description": "The knowledge base name"}, "type": "str"}, "description": {"args": {"description": "Brief description of the knowledge base purpose"}, "type": "str"}, "target_audience": {"args": {"description": "Intended knowledge base users", "default_factory": "list"}, "type": "List[str]"}, "primary_language": {"args": {"default": "en-US", "description": "Primary knowledge base language"}, "type": "str"}, "content_hierarchy": {"args": {"description": "Knowledge base structure with categories and articles", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "top_level_keywords": {"args": {"description": "Knowledge base-wide keywords", "default_factory": "list"}, "type": "List[Dict[str, str]]"}}, "object_type": "alpha", "metadata_schema": {"required": ["content_type", "primary_language", "target_audience"], "recommended": ["knowledge_base_type", "support_level"]}}',
  'Top-level container for knowledge base content with articles, FAQs, and guides',
  ARRAY["Customer support","Internal knowledge bases","Help centers","Community documentation"],
  '{}',
  '2025-04-29 14:08:00.332612+02',
  '2025-04-29 14:08:00.332612+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  'd49c4731-9726-4169-80f3-874a9970751d',
  'LearningManagementSystem',
  'alpha',
  '1.0',
  '{"name": "LearningManagementSystem", "fields": {"name": {"args": {"description": "The LMS name"}, "type": "str"}, "description": {"args": {"description": "Brief description of the LMS purpose"}, "type": "str"}, "target_audience": {"args": {"description": "Intended learners", "default_factory": "list"}, "type": "List[str]"}, "primary_language": {"args": {"default": "en-US", "description": "Primary content language"}, "type": "str"}, "content_hierarchy": {"args": {"description": "Course and module structure", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "top_level_keywords": {"args": {"description": "LMS-wide keywords", "default_factory": "list"}, "type": "List[Dict[str, str]]"}}, "object_type": "alpha", "metadata_schema": {"required": ["content_type", "primary_language", "target_audience"], "recommended": ["education_level", "subject_area"]}}',
  'Top-level container for educational content with courses, modules, and assessments',
  ARRAY["Online education","Corporate training","Skill development","Academic courses"],
  '{}',
  '2025-04-29 14:08:00.333826+02',
  '2025-04-29 14:08:00.333826+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '6558cf18-f1c8-46c9-982a-7312cb5208c8',
  'EmailCampaign',
  'alpha',
  '1.0',
  '{"name": "EmailCampaign", "fields": {"name": {"args": {"description": "The campaign name"}, "type": "str"}, "description": {"args": {"description": "Brief description of the campaign purpose"}, "type": "str"}, "target_audience": {"args": {"description": "Intended email recipients", "default_factory": "list"}, "type": "List[str]"}, "primary_language": {"args": {"default": "en-US", "description": "Primary email language"}, "type": "str"}, "content_hierarchy": {"args": {"description": "Email sequence structure", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "top_level_keywords": {"args": {"description": "Campaign-wide keywords", "default_factory": "list"}, "type": "List[Dict[str, str]]"}}, "object_type": "alpha", "metadata_schema": {"required": ["content_type", "primary_language", "target_audience"], "recommended": ["campaign_type", "email_frequency"]}}',
  'Top-level container for email marketing campaigns with messages and sequences',
  ARRAY["Email marketing","Newsletter campaigns","Lead nurturing","Customer engagement"],
  '{}',
  '2025-04-29 14:08:00.335125+02',
  '2025-04-29 14:08:00.335125+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '3a860d74-8b6c-4ad1-b138-3d8db4ccb2f1',
  'SocialMediaCampaign',
  'alpha',
  '1.0',
  '{"name": "SocialMediaCampaign", "fields": {"name": {"args": {"description": "The campaign name"}, "type": "str"}, "description": {"args": {"description": "Brief description of the campaign purpose"}, "type": "str"}, "target_audience": {"args": {"description": "Intended social media audience", "default_factory": "list"}, "type": "List[str]"}, "primary_language": {"args": {"default": "en-US", "description": "Primary content language"}, "type": "str"}, "content_hierarchy": {"args": {"description": "Social media content structure", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "top_level_keywords": {"args": {"description": "Campaign-wide keywords", "default_factory": "list"}, "type": "List[Dict[str, str]]"}}, "object_type": "alpha", "metadata_schema": {"required": ["content_type", "primary_language", "target_audience"], "recommended": ["campaign_type", "social_platforms"]}}',
  'Top-level container for social media content with posts and engagement strategies',
  ARRAY["Social media marketing","Brand awareness","Community engagement","Content distribution"],
  '{}',
  '2025-04-29 14:08:00.336169+02',
  '2025-04-29 14:08:00.336169+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '21352024-9fdc-4b40-ab06-43d04d148b76',
  'PodcastSeries',
  'alpha',
  '1.0',
  '{"name": "PodcastSeries", "fields": {"name": {"args": {"description": "The podcast series name"}, "type": "str"}, "description": {"args": {"description": "Brief description of the podcast purpose"}, "type": "str"}, "target_audience": {"args": {"description": "Intended podcast listeners", "default_factory": "list"}, "type": "List[str]"}, "primary_language": {"args": {"default": "en-US", "description": "Primary podcast language"}, "type": "str"}, "content_hierarchy": {"args": {"description": "Episode structure and organization", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "top_level_keywords": {"args": {"description": "Podcast-wide keywords", "default_factory": "list"}, "type": "List[Dict[str, str]]"}}, "object_type": "alpha", "metadata_schema": {"required": ["content_type", "primary_language", "target_audience"], "recommended": ["podcast_category", "episode_frequency"]}}',
  'Top-level container for podcast content with episodes and show notes',
  ARRAY["Audio content","Podcast shows","Audio storytelling","Educational podcasts"],
  '{}',
  '2025-04-29 14:08:00.337192+02',
  '2025-04-29 14:08:00.337192+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '1468a149-29c1-4f16-975b-df4b80f7c854',
  'VideoCourse',
  'alpha',
  '1.0',
  '{"name": "VideoCourse", "fields": {"name": {"args": {"description": "The video course name"}, "type": "str"}, "description": {"args": {"description": "Brief description of the course purpose"}, "type": "str"}, "target_audience": {"args": {"description": "Intended course students", "default_factory": "list"}, "type": "List[str]"}, "primary_language": {"args": {"default": "en-US", "description": "Primary course language"}, "type": "str"}, "content_hierarchy": {"args": {"description": "Course structure with lessons and modules", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "top_level_keywords": {"args": {"description": "Course-wide keywords", "default_factory": "list"}, "type": "List[Dict[str, str]]"}}, "object_type": "alpha", "metadata_schema": {"required": ["content_type", "primary_language", "target_audience"], "recommended": ["course_level", "subject_area"]}}',
  'Top-level container for video-based educational content with lessons and resources',
  ARRAY["Online courses","Video tutorials","Skill development","Educational content"],
  '{}',
  '2025-04-29 14:08:00.338231+02',
  '2025-04-29 14:08:00.338231+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  'a3245394-6584-4b08-8fef-9f1cbb692185',
  'Newsletter',
  'alpha',
  '1.0',
  '{"name": "Newsletter", "fields": {"name": {"args": {"description": "The newsletter name"}, "type": "str"}, "description": {"args": {"description": "Brief description of the newsletter purpose"}, "type": "str"}, "target_audience": {"args": {"description": "Intended newsletter subscribers", "default_factory": "list"}, "type": "List[str]"}, "primary_language": {"args": {"default": "en-US", "description": "Primary newsletter language"}, "type": "str"}, "content_hierarchy": {"args": {"description": "Newsletter structure with sections", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "top_level_keywords": {"args": {"description": "Newsletter-wide keywords", "default_factory": "list"}, "type": "List[Dict[str, str]]"}}, "object_type": "alpha", "metadata_schema": {"required": ["content_type", "primary_language", "target_audience"], "recommended": ["newsletter_type", "frequency"]}}',
  'Top-level container for newsletter content with issues and sections',
  ARRAY["Email newsletters","Content distribution","Community updates","Industry news"],
  '{}',
  '2025-04-29 14:08:00.33938+02',
  '2025-04-29 14:08:00.33938+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '189d8f00-e336-4a97-b94b-f3e06ecb0547',
  'BlogPost',
  'beta',
  '1.0',
  '{"name": "BlogPost", "fields": {"slug": {"args": {"description": "URL-friendly version of the title"}, "type": "str"}, "tags": {"args": {"description": "Content classification tags", "default_factory": "list"}, "type": "List[str]"}, "title": {"args": {"description": "The blog post title"}, "type": "str"}, "author": {"args": {"description": "Author information", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "content": {"args": {"description": "Complete markdown content"}, "type": "str"}, "excerpt": {"args": {"default": "", "description": "Brief summary or excerpt"}, "type": "str"}, "keywords": {"args": {"description": "SEO keywords with priority", "default_factory": "list"}, "type": "List[Dict[str, str]]"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "publish_date": {"args": {"default": "", "description": "Publication date"}, "type": "str"}, "extracted_components": {"args": {"description": "Components extracted from markdown content", "default_factory": "dict"}, "type": "Dict[str, List]"}}, "object_type": "beta", "metadata_schema": {"required": ["content_type", "word_count", "tags"], "recommended": ["reading_time", "author_bio"]}}',
  'Standalone blog post with title, content, and metadata',
  ARRAY["Blog content",Articles,"Opinion pieces","News updates"],
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
  ARRAY["Marketing pages","Lead generation","Product launches","Campaign landing pages"],
  '{}',
  '2025-04-29 14:08:00.342039+02',
  '2025-04-29 14:08:00.342039+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  'd384da83-c7bd-40ca-a6d2-4d7478e08f92',
  'ProductPage',
  'beta',
  '1.0',
  '{"name": "ProductPage", "fields": {"slug": {"args": {"description": "URL-friendly version of the title"}, "type": "str"}, "tags": {"args": {"description": "Content classification tags", "default_factory": "list"}, "type": "List[str]"}, "title": {"args": {"description": "The product page title"}, "type": "str"}, "content": {"args": {"description": "Complete markdown content"}, "type": "str"}, "benefits": {"args": {"description": "Product benefits", "default_factory": "list"}, "type": "List[str]"}, "features": {"args": {"description": "Key product features", "default_factory": "list"}, "type": "List[str]"}, "keywords": {"args": {"description": "SEO keywords with priority", "default_factory": "list"}, "type": "List[Dict[str, str]]"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "product_name": {"args": {"description": "Name of the product"}, "type": "str"}, "product_description": {"args": {"description": "Brief product description"}, "type": "str"}, "extracted_components": {"args": {"description": "Components extracted from markdown content", "default_factory": "dict"}, "type": "Dict[str, List]"}}, "object_type": "beta", "metadata_schema": {"required": ["content_type", "word_count", "tags"], "recommended": ["product_category", "target_audience"]}}',
  'Detailed product information page with features and benefits',
  ARRAY[E-commerce,"Product marketing","SaaS products","Digital products"],
  '{}',
  '2025-04-29 14:08:00.343079+02',
  '2025-04-29 14:08:00.343079+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  'f119cc99-1dff-4204-ac2e-fc175b123bd2',
  'ProductReview',
  'beta',
  '1.0',
  '{"name": "ProductReview", "fields": {"cons": {"args": {"description": "Product disadvantages", "default_factory": "list"}, "type": "List[str]"}, "pros": {"args": {"description": "Product advantages", "default_factory": "list"}, "type": "List[str]"}, "slug": {"args": {"description": "URL-friendly version of the title"}, "type": "str"}, "tags": {"args": {"description": "Content classification tags", "default_factory": "list"}, "type": "List[str]"}, "title": {"args": {"description": "The review title"}, "type": "str"}, "rating": {"args": {"ge": 0.0, "le": 5.0, "description": "Overall product rating"}, "type": "float"}, "content": {"args": {"description": "Complete markdown content"}, "type": "str"}, "keywords": {"args": {"description": "SEO keywords with priority", "default_factory": "list"}, "type": "List[Dict[str, str]]"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "product_name": {"args": {"description": "Name of the reviewed product"}, "type": "str"}, "product_category": {"args": {"description": "Category of the product"}, "type": "str"}, "extracted_components": {"args": {"description": "Components extracted from markdown content", "default_factory": "dict"}, "type": "Dict[str, List]"}}, "object_type": "beta", "metadata_schema": {"required": ["content_type", "word_count", "tags"], "recommended": ["review_type", "target_audience"]}}',
  'Detailed product evaluation with pros, cons, and recommendations',
  ARRAY["Product reviews","Buying guides","Consumer research","Product comparisons"],
  '{}',
  '2025-04-29 14:08:00.344191+02',
  '2025-04-29 14:08:00.344191+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  'ac93cd6b-1bfb-49a2-a1bb-170e1499eb26',
  'AudioPlayer',
  'gamma',
  '1.0',
  '{"name": "AudioPlayer", "fields": {"tags": {"args": {"description": "Classification tags", "default_factory": "list"}, "type": "List[str]"}, "title": {"args": {"description": "Audio title"}, "type": "str"}, "duration": {"args": {"default": "", "description": "Audio duration"}, "type": "str"}, "position": {"args": {"default": 0, "description": "Character position in the parent document"}, "type": "int"}, "audio_url": {"args": {"description": "URL to the audio file"}, "type": "str"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "description": {"args": {"default": "", "description": "Brief description of the audio"}, "type": "str"}}, "object_type": "gamma", "metadata_schema": {"required": ["content_type", "tags"], "recommended": ["audio_type", "target_audience"]}}',
  'Embedded audio content',
  ARRAY["Podcast episodes","Audio content","Music players","Audio tutorials"],
  '{}',
  '2025-04-29 14:08:00.363355+02',
  '2025-04-29 14:08:00.363355+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  'bb0318fc-ea08-4188-a6d7-1bd4ca26daa4',
  'ProductComparison',
  'beta',
  '1.0',
  '{"name": "ProductComparison", "fields": {"slug": {"args": {"description": "URL-friendly version of the title"}, "type": "str"}, "tags": {"args": {"description": "Content classification tags", "default_factory": "list"}, "type": "List[str]"}, "title": {"args": {"description": "The comparison title"}, "type": "str"}, "winner": {"args": {"default": "", "description": "Best product in the comparison"}, "type": "str"}, "content": {"args": {"description": "Complete markdown content"}, "type": "str"}, "keywords": {"args": {"description": "SEO keywords with priority", "default_factory": "list"}, "type": "List[Dict[str, str]]"}, "products": {"args": {"description": "List of products being compared", "default_factory": "list"}, "type": "List[Dict[str, Any]]"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "comparison_criteria": {"args": {"description": "Criteria used for comparison", "default_factory": "list"}, "type": "List[str]"}, "extracted_components": {"args": {"description": "Components extracted from markdown content", "default_factory": "dict"}, "type": "Dict[str, List]"}}, "object_type": "beta", "metadata_schema": {"required": ["content_type", "word_count", "tags"], "recommended": ["comparison_type", "target_audience"]}}',
  'Side-by-side comparison of multiple products',
  ARRAY["Product comparisons","Buying guides","Market research","Consumer education"],
  '{}',
  '2025-04-29 14:08:00.34552+02',
  '2025-04-29 14:08:00.34552+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '8fa7b7f2-a969-461e-ac1d-381d2f331921',
  'Listicle',
  'beta',
  '1.0',
  '{"name": "Listicle", "fields": {"slug": {"args": {"description": "URL-friendly version of the title"}, "type": "str"}, "tags": {"args": {"description": "Content classification tags", "default_factory": "list"}, "type": "List[str]"}, "title": {"args": {"description": "The listicle title"}, "type": "str"}, "content": {"args": {"description": "Complete markdown content"}, "type": "str"}, "keywords": {"args": {"description": "SEO keywords with priority", "default_factory": "list"}, "type": "List[Dict[str, str]]"}, "list_type": {"args": {"default": "numbered", "description": "Type of list (numbered, bulleted, etc.)"}, "type": "str"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "list_items": {"args": {"description": "Items in the list", "default_factory": "list"}, "type": "List[Dict[str, Any]]"}, "extracted_components": {"args": {"description": "Components extracted from markdown content", "default_factory": "dict"}, "type": "Dict[str, List]"}}, "object_type": "beta", "metadata_schema": {"required": ["content_type", "word_count", "tags"], "recommended": ["list_category", "target_audience"]}}',
  'List-based article with numbered or bulleted items',
  ARRAY["List articles","Top 10 lists",Roundups,"Curated content"],
  '{}',
  '2025-04-29 14:08:00.346765+02',
  '2025-04-29 14:08:00.346765+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '86f5dc95-a6bc-4f5a-a374-fd8db7470a56',
  'HowToGuide',
  'beta',
  '1.0',
  '{"name": "HowToGuide", "fields": {"slug": {"args": {"description": "URL-friendly version of the title"}, "type": "str"}, "tags": {"args": {"description": "Content classification tags", "default_factory": "list"}, "type": "List[str]"}, "steps": {"args": {"description": "Step-by-step instructions", "default_factory": "list"}, "type": "List[Dict[str, Any]]"}, "title": {"args": {"description": "The guide title"}, "type": "str"}, "content": {"args": {"description": "Complete markdown content"}, "type": "str"}, "keywords": {"args": {"description": "SEO keywords with priority", "default_factory": "list"}, "type": "List[Dict[str, str]]"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "prerequisites": {"args": {"description": "Required knowledge or materials", "default_factory": "list"}, "type": "List[str]"}, "estimated_time": {"args": {"default": "", "description": "Estimated completion time"}, "type": "str"}, "difficulty_level": {"args": {"default": "intermediate", "description": "Guide difficulty level"}, "type": "str"}, "extracted_components": {"args": {"description": "Components extracted from markdown content", "default_factory": "dict"}, "type": "Dict[str, List]"}}, "object_type": "beta", "metadata_schema": {"required": ["content_type", "word_count", "tags"], "recommended": ["skill_level", "target_audience"]}}',
  'Step-by-step instructional content',
  ARRAY[Tutorials,Instructions,"DIY guides","Educational content"],
  '{}',
  '2025-04-29 14:08:00.347888+02',
  '2025-04-29 14:08:00.347888+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  'c8e974d1-9de1-4021-a23b-b1f6c73ece51',
  'CaseStudy',
  'beta',
  '1.0',
  '{"name": "CaseStudy", "fields": {"slug": {"args": {"description": "URL-friendly version of the title"}, "type": "str"}, "tags": {"args": {"description": "Content classification tags", "default_factory": "list"}, "type": "List[str]"}, "title": {"args": {"description": "The case study title"}, "type": "str"}, "content": {"args": {"description": "Complete markdown content"}, "type": "str"}, "results": {"args": {"description": "Key results and outcomes", "default_factory": "list"}, "type": "List[str]"}, "industry": {"args": {"description": "Industry of the client"}, "type": "str"}, "keywords": {"args": {"description": "SEO keywords with priority", "default_factory": "list"}, "type": "List[Dict[str, str]]"}, "solution": {"args": {"description": "Solution implemented"}, "type": "str"}, "challenge": {"args": {"description": "Problem or challenge faced"}, "type": "str"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "client_name": {"args": {"description": "Name of the client or company"}, "type": "str"}, "extracted_components": {"args": {"description": "Components extracted from markdown content", "default_factory": "dict"}, "type": "Dict[str, List]"}}, "object_type": "beta", "metadata_schema": {"required": ["content_type", "word_count", "tags"], "recommended": ["case_study_type", "target_audience"]}}',
  'Detailed analysis of a specific implementation or success story',
  ARRAY["Business case studies","Success stories","Implementation examples","Industry analysis"],
  '{}',
  '2025-04-29 14:08:00.349196+02',
  '2025-04-29 14:08:00.349196+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '0ce84ba4-0f84-4f44-a90c-ee1c94224152',
  'KeyTakeaway',
  'gamma',
  '1.0',
  '{"name": "KeyTakeaway", "fields": {"tags": {"args": {"description": "Classification tags", "default_factory": "list"}, "type": "List[str]"}, "text": {"args": {"description": "The key takeaway text"}, "type": "str"}, "position": {"args": {"default": 0, "description": "Character position in the parent document"}, "type": "int"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "importance": {"args": {"default": "high", "description": "Level of importance"}, "type": "str"}}, "object_type": "gamma", "metadata_schema": {"required": ["content_type", "tags"], "recommended": ["takeaway_type", "context"]}}',
  'Important conclusion or learning',
  ARRAY["Educational content",Summaries,"Learning points","Content highlights"],
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
  ARRAY["Industry reports","Research papers","Technical documentation","Thought leadership"],
  '{}',
  '2025-04-29 14:08:00.350454+02',
  '2025-04-29 14:08:00.350454+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '217c3a36-f0ca-4c97-943c-f5c32128ad93',
  'EbookChapter',
  'beta',
  '1.0',
  '{"name": "EbookChapter", "fields": {"slug": {"args": {"description": "URL-friendly version of the title"}, "type": "str"}, "tags": {"args": {"description": "Content classification tags", "default_factory": "list"}, "type": "List[str]"}, "title": {"args": {"description": "The chapter title"}, "type": "str"}, "content": {"args": {"description": "Complete markdown content"}, "type": "str"}, "summary": {"args": {"default": "", "description": "Chapter summary"}, "type": "str"}, "keywords": {"args": {"description": "SEO keywords with priority", "default_factory": "list"}, "type": "List[Dict[str, str]]"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "key_points": {"args": {"description": "Key points in the chapter", "default_factory": "list"}, "type": "List[str]"}, "ebook_title": {"args": {"description": "Title of the parent ebook"}, "type": "str"}, "chapter_number": {"args": {"description": "Chapter number in sequence"}, "type": "int"}, "extracted_components": {"args": {"description": "Components extracted from markdown content", "default_factory": "dict"}, "type": "Dict[str, List]"}}, "object_type": "beta", "metadata_schema": {"required": ["content_type", "word_count", "tags"], "recommended": ["chapter_type", "target_audience"]}}',
  'Chapter of an ebook with content and structure',
  ARRAY["Ebook content","Digital books","Online courses","Educational content"],
  '{}',
  '2025-04-29 14:08:00.351724+02',
  '2025-04-29 14:08:00.351724+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  'bce7da40-d9b1-417c-98ac-f92b0297807e',
  'BookChapter',
  'beta',
  '1.0',
  '{"name": "BookChapter", "fields": {"slug": {"args": {"description": "URL-friendly version of the title"}, "type": "str"}, "tags": {"args": {"description": "Content classification tags", "default_factory": "list"}, "type": "List[str]"}, "title": {"args": {"description": "The chapter title"}, "type": "str"}, "content": {"args": {"description": "Complete markdown content"}, "type": "str"}, "summary": {"args": {"default": "", "description": "Chapter summary"}, "type": "str"}, "keywords": {"args": {"description": "SEO keywords with priority", "default_factory": "list"}, "type": "List[Dict[str, str]]"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "book_title": {"args": {"description": "Title of the parent book"}, "type": "str"}, "key_points": {"args": {"description": "Key points in the chapter", "default_factory": "list"}, "type": "List[str]"}, "chapter_number": {"args": {"description": "Chapter number in sequence"}, "type": "int"}, "extracted_components": {"args": {"description": "Components extracted from markdown content", "default_factory": "dict"}, "type": "Dict[str, List]"}}, "object_type": "beta", "metadata_schema": {"required": ["content_type", "word_count", "tags"], "recommended": ["chapter_type", "target_audience"]}}',
  'Chapter of a book with content and structure',
  ARRAY["Book content","Print books","Educational resources","Fiction works"],
  '{}',
  '2025-04-29 14:08:00.352812+02',
  '2025-04-29 14:08:00.352812+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  'ceaa82da-c0b5-4862-a95f-365dbd217394',
  'FAQPage',
  'beta',
  '1.0',
  '{"name": "FAQPage", "fields": {"slug": {"args": {"description": "URL-friendly version of the title"}, "type": "str"}, "tags": {"args": {"description": "Content classification tags", "default_factory": "list"}, "type": "List[str]"}, "title": {"args": {"description": "The FAQ page title"}, "type": "str"}, "content": {"args": {"description": "Complete markdown content"}, "type": "str"}, "keywords": {"args": {"description": "SEO keywords with priority", "default_factory": "list"}, "type": "List[Dict[str, str]]"}, "questions": {"args": {"description": "List of questions and answers", "default_factory": "list"}, "type": "List[Dict[str, Any]]"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "categories": {"args": {"description": "FAQ categories", "default_factory": "list"}, "type": "List[str]"}, "extracted_components": {"args": {"description": "Components extracted from markdown content", "default_factory": "dict"}, "type": "Dict[str, List]"}}, "object_type": "beta", "metadata_schema": {"required": ["content_type", "word_count", "tags"], "recommended": ["faq_category", "target_audience"]}}',
  'Collection of frequently asked questions and answers',
  ARRAY["Customer support","Product documentation","Knowledge bases","Help centers"],
  '{}',
  '2025-04-29 14:08:00.353859+02',
  '2025-04-29 14:08:00.353859+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '38c3d0b0-99df-4b35-93a0-01c131b5448b',
  'VideoEmbed',
  'gamma',
  '1.0',
  '{"name": "VideoEmbed", "fields": {"tags": {"args": {"description": "Classification tags", "default_factory": "list"}, "type": "List[str]"}, "title": {"args": {"description": "Video title"}, "type": "str"}, "platform": {"args": {"default": "youtube", "description": "Video platform (YouTube, Vimeo, etc.)"}, "type": "str"}, "position": {"args": {"default": 0, "description": "Character position in the parent document"}, "type": "int"}, "video_url": {"args": {"description": "URL to the video"}, "type": "str"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "description": {"args": {"default": "", "description": "Brief description of the video"}, "type": "str"}}, "object_type": "gamma", "metadata_schema": {"required": ["content_type", "tags"], "recommended": ["video_type", "target_audience"]}}',
  'Embedded video content',
  ARRAY["Video content",Tutorials,"Product demos","Educational content"],
  '{}',
  '2025-04-29 14:08:00.362283+02',
  '2025-04-29 14:08:00.362283+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '8ff622ad-a21e-4215-9513-8f240784baba',
  'CallToAction',
  'gamma',
  '1.0',
  '{"name": "CallToAction", "fields": {"tags": {"args": {"description": "Classification tags", "default_factory": "list"}, "type": "List[str]"}, "text": {"args": {"description": "The CTA button or link text"}, "type": "str"}, "type": {"args": {"default": "button", "description": "Type of CTA (button, link, banner, etc.)"}, "type": "str"}, "placement": {"args": {"default": "inline", "description": "Where the CTA appears (inline, bottom, popup, etc.)"}, "type": "str"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "target_url": {"args": {"description": "Destination URL"}, "type": "str"}, "action_type": {"args": {"default": "learn_more", "description": "Type of action (signup, download, learn_more, etc.)"}, "type": "str"}}, "object_type": "gamma", "metadata_schema": {"required": ["content_type", "tags"], "recommended": ["conversion_rate", "target_audience"]}}',
  'Interactive element prompting user action',
  ARRAY["Marketing pages","Lead generation","Conversion optimization","Email marketing"],
  '{}',
  '2025-04-29 14:08:00.354916+02',
  '2025-04-29 14:08:00.354916+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '1d7a224d-562f-4f8b-9edf-45a1d89bf088',
  'Table',
  'gamma',
  '1.0',
  '{"name": "Table", "fields": {"rows": {"args": {"description": "Table data rows", "default_factory": "list"}, "type": "List[List[str]]"}, "tags": {"args": {"description": "Classification tags", "default_factory": "list"}, "type": "List[str]"}, "title": {"args": {"default": "", "description": "Table title or caption"}, "type": "str"}, "headers": {"args": {"description": "Column headers", "default_factory": "list"}, "type": "List[str]"}, "markdown": {"args": {"description": "Complete markdown for the table"}, "type": "str"}, "position": {"args": {"default": 0, "description": "Character position in the parent document"}, "type": "int"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}}, "object_type": "gamma", "metadata_schema": {"required": ["content_type", "tags"], "recommended": ["data_source", "last_updated"]}}',
  'Structured data presentation',
  ARRAY["Data presentation",Comparisons,"Information organization","Technical documentation"],
  '{}',
  '2025-04-29 14:08:00.356134+02',
  '2025-04-29 14:08:00.356134+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  'd8f274e4-ae31-4e37-903e-3ac5b93ce7d3',
  'Blockquote',
  'gamma',
  '1.0',
  '{"name": "Blockquote", "fields": {"tags": {"args": {"description": "Classification tags", "default_factory": "list"}, "type": "List[str]"}, "text": {"args": {"description": "The quoted text"}, "type": "str"}, "author": {"args": {"default": "", "description": "Quote author"}, "type": "str"}, "source": {"args": {"default": "", "description": "Source of the quote"}, "type": "str"}, "position": {"args": {"default": 0, "description": "Character position in the parent document"}, "type": "int"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}}, "object_type": "gamma", "metadata_schema": {"required": ["content_type", "tags"], "recommended": ["quote_type", "context"]}}',
  'Featured quote or excerpt',
  ARRAY["Content highlights",Testimonials,"Expert quotes","Content emphasis"],
  '{}',
  '2025-04-29 14:08:00.357444+02',
  '2025-04-29 14:08:00.357444+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '1af27dfc-df37-4814-bf4f-756ae6123c51',
  'ImageWithCaption',
  'gamma',
  '1.0',
  '{"name": "ImageWithCaption", "fields": {"tags": {"args": {"description": "Classification tags", "default_factory": "list"}, "type": "List[str]"}, "caption": {"args": {"description": "Image caption or description"}, "type": "str"}, "alt_text": {"args": {"default": "", "description": "Alternative text for accessibility"}, "type": "str"}, "position": {"args": {"default": 0, "description": "Character position in the parent document"}, "type": "int"}, "image_url": {"args": {"description": "URL or path to the image"}, "type": "str"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}}, "object_type": "gamma", "metadata_schema": {"required": ["content_type", "tags"], "recommended": ["image_type", "context"]}}',
  'Visual element with descriptive text',
  ARRAY["Content illustration","Visual storytelling","Product images","Educational content"],
  '{}',
  '2025-04-29 14:08:00.358693+02',
  '2025-04-29 14:08:00.358693+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '5303ce42-1ae3-49f5-a2a1-9c290b6f5a8f',
  'CodeSnippet',
  'gamma',
  '1.0',
  '{"name": "CodeSnippet", "fields": {"code": {"args": {"description": "The code snippet"}, "type": "str"}, "tags": {"args": {"description": "Classification tags", "default_factory": "list"}, "type": "List[str]"}, "language": {"args": {"default": "python", "description": "Programming language"}, "type": "str"}, "position": {"args": {"default": 0, "description": "Character position in the parent document"}, "type": "int"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "description": {"args": {"default": "", "description": "Brief description of the code"}, "type": "str"}}, "object_type": "gamma", "metadata_schema": {"required": ["content_type", "tags"], "recommended": ["code_type", "context"]}}',
  'Programming code example',
  ARRAY["Technical documentation","Programming tutorials","API examples","Code sharing"],
  '{}',
  '2025-04-29 14:08:00.359858+02',
  '2025-04-29 14:08:00.359858+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '00611c33-8097-42f5-b748-28ff4af2bf9d',
  'InteractiveDemo',
  'gamma',
  '1.0',
  '{"name": "InteractiveDemo", "fields": {"tags": {"args": {"description": "Classification tags", "default_factory": "list"}, "type": "List[str]"}, "title": {"args": {"description": "Demo title"}, "type": "str"}, "demo_url": {"args": {"description": "URL to the interactive demo"}, "type": "str"}, "position": {"args": {"default": 0, "description": "Character position in the parent document"}, "type": "int"}, "demo_type": {"args": {"default": "product", "description": "Type of interactive demo"}, "type": "str"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "description": {"args": {"description": "Brief description of the demo"}, "type": "str"}}, "object_type": "gamma", "metadata_schema": {"required": ["content_type", "tags"], "recommended": ["demo_category", "target_audience"]}}',
  'Interactive element for user engagement',
  ARRAY["Product demos","Interactive tutorials","User engagement","Feature showcases"],
  '{}',
  '2025-04-29 14:08:00.361109+02',
  '2025-04-29 14:08:00.361109+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '25e954e2-9371-436f-ae6d-9ca8bba1136e',
  'ReadingTime',
  'qualifier',
  '1.0',
  '{"name": "ReadingTime", "fields": {"minutes": {"args": {"description": "Estimated reading time in minutes"}, "type": "int"}, "word_count": {"args": {"default": 0, "description": "Total word count"}, "type": "int"}, "reading_speed": {"args": {"default": 200, "description": "Words per minute for calculation"}, "type": "int"}}, "object_type": "qualifier", "metadata_schema": {"required": ["content_type"], "recommended": ["content_type", "target_audience"]}}',
  'Estimated consumption duration',
  ARRAY["Content metrics","User experience","Content planning","Engagement metrics"],
  '{}',
  '2025-04-29 14:08:00.397215+02',
  '2025-04-29 14:08:00.397215+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  'c68efd7a-c22c-4d1d-8092-887e1c3cc88d',
  'FAQItem',
  'gamma',
  '1.0',
  '{"name": "FAQItem", "fields": {"tags": {"args": {"description": "Classification tags", "default_factory": "list"}, "type": "List[str]"}, "answer": {"args": {"description": "The FAQ answer"}, "type": "str"}, "category": {"args": {"default": "", "description": "FAQ category"}, "type": "str"}, "position": {"args": {"default": 0, "description": "Character position in the parent document"}, "type": "int"}, "question": {"args": {"description": "The FAQ question"}, "type": "str"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}}, "object_type": "gamma", "metadata_schema": {"required": ["content_type", "tags"], "recommended": ["faq_type", "context"]}}',
  'Single question and answer pair',
  ARRAY[FAQs,"Help content","Customer support","Educational content"],
  '{}',
  '2025-04-29 14:08:00.365533+02',
  '2025-04-29 14:08:00.365533+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '79ff4f75-355a-4bbb-8e48-47df96ff3846',
  'Testimonial',
  'gamma',
  '1.0',
  '{"name": "Testimonial", "fields": {"tags": {"args": {"description": "Classification tags", "default_factory": "list"}, "type": "List[str]"}, "text": {"args": {"description": "The testimonial text"}, "type": "str"}, "author": {"args": {"description": "Testimonial author information", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "rating": {"args": {"ge": 0.0, "le": 5.0, "default": null, "description": "Rating (if applicable)"}, "type": "float"}, "position": {"args": {"default": 0, "description": "Character position in the parent document"}, "type": "int"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}}, "object_type": "gamma", "metadata_schema": {"required": ["content_type", "tags"], "recommended": ["testimonial_type", "context"]}}',
  'Customer or user quote',
  ARRAY["Social proof","Customer reviews","Case studies","Marketing content"],
  '{}',
  '2025-04-29 14:08:00.366997+02',
  '2025-04-29 14:08:00.366997+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '36754287-709c-4737-8479-7554bedaedae',
  'StepInstructions',
  'gamma',
  '1.0',
  '{"name": "StepInstructions", "fields": {"tags": {"args": {"description": "Classification tags", "default_factory": "list"}, "type": "List[str]"}, "notes": {"args": {"default": "", "description": "Additional notes or tips"}, "type": "str"}, "position": {"args": {"default": 0, "description": "Character position in the parent document"}, "type": "int"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "instruction": {"args": {"description": "The step instruction"}, "type": "str"}, "step_number": {"args": {"description": "Step number in sequence"}, "type": "int"}}, "object_type": "gamma", "metadata_schema": {"required": ["content_type", "tags"], "recommended": ["step_type", "context"]}}',
  'Individual step in a process',
  ARRAY["How-to guides",Tutorials,"Process documentation","Educational content"],
  '{}',
  '2025-04-29 14:08:00.368126+02',
  '2025-04-29 14:08:00.368126+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '097cb0a5-42ea-440a-b30b-f9dfcf34ed25',
  'Definition',
  'gamma',
  '1.0',
  '{"name": "Definition", "fields": {"tags": {"args": {"description": "Classification tags", "default_factory": "list"}, "type": "List[str]"}, "term": {"args": {"description": "The term being defined"}, "type": "str"}, "category": {"args": {"default": "", "description": "Definition category"}, "type": "str"}, "position": {"args": {"default": 0, "description": "Character position in the parent document"}, "type": "int"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "definition": {"args": {"description": "The term definition"}, "type": "str"}}, "object_type": "gamma", "metadata_schema": {"required": ["content_type", "tags"], "recommended": ["definition_type", "context"]}}',
  'Term explanation',
  ARRAY[Glossaries,"Technical documentation","Educational content","Reference materials"],
  '{}',
  '2025-04-29 14:08:00.369157+02',
  '2025-04-29 14:08:00.369157+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '0cff1fbc-b633-42c2-adb3-6d314afc66b8',
  'SidebarContent',
  'gamma',
  '1.0',
  '{"name": "SidebarContent", "fields": {"tags": {"args": {"description": "Classification tags", "default_factory": "list"}, "type": "List[str]"}, "title": {"args": {"description": "Sidebar title"}, "type": "str"}, "content": {"args": {"description": "Sidebar content"}, "type": "str"}, "position": {"args": {"default": "right", "description": "Sidebar position (left, right)"}, "type": "str"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}}, "object_type": "gamma", "metadata_schema": {"required": ["content_type", "tags"], "recommended": ["sidebar_type", "context"]}}',
  'Supplementary information',
  ARRAY["Content sidebars","Additional information","Related content","Contextual help"],
  '{}',
  '2025-04-29 14:08:00.370195+02',
  '2025-04-29 14:08:00.370195+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '3aa577e2-7ded-4160-aa8f-d9a38ebf5ea7',
  'PullQuote',
  'gamma',
  '1.0',
  '{"name": "PullQuote", "fields": {"tags": {"args": {"description": "Classification tags", "default_factory": "list"}, "type": "List[str]"}, "text": {"args": {"description": "The quoted text"}, "type": "str"}, "author": {"args": {"default": "", "description": "Quote author"}, "type": "str"}, "position": {"args": {"default": 0, "description": "Character position in the parent document"}, "type": "int"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}}, "object_type": "gamma", "metadata_schema": {"required": ["content_type", "tags"], "recommended": ["quote_type", "context"]}}',
  'Highlighted quote from text',
  ARRAY["Content highlights","Article emphasis","Key points","Content design"],
  '{}',
  '2025-04-29 14:08:00.371222+02',
  '2025-04-29 14:08:00.371222+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  'a13e491b-a528-4a96-ab63-25d0b4ba744d',
  'Infographic',
  'gamma',
  '1.0',
  '{"name": "Infographic", "fields": {"tags": {"args": {"description": "Classification tags", "default_factory": "list"}, "type": "List[str]"}, "title": {"args": {"description": "Infographic title"}, "type": "str"}, "position": {"args": {"default": 0, "description": "Character position in the parent document"}, "type": "int"}, "image_url": {"args": {"description": "URL or path to the infographic"}, "type": "str"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "data_source": {"args": {"default": "", "description": "Source of the data"}, "type": "str"}, "description": {"args": {"description": "Brief description of the infographic"}, "type": "str"}}, "object_type": "gamma", "metadata_schema": {"required": ["content_type", "tags"], "recommended": ["infographic_type", "target_audience"]}}',
  'Visual representation of information',
  ARRAY["Data visualization","Information design","Educational content","Content marketing"],
  '{}',
  '2025-04-29 14:08:00.372423+02',
  '2025-04-29 14:08:00.372423+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  'dcfd3488-890a-425b-b350-27bec97ec6ed',
  'DataVisualization',
  'gamma',
  '1.0',
  '{"name": "DataVisualization", "fields": {"tags": {"args": {"description": "Classification tags", "default_factory": "list"}, "type": "List[str]"}, "title": {"args": {"description": "Visualization title"}, "type": "str"}, "position": {"args": {"default": 0, "description": "Character position in the parent document"}, "type": "int"}, "image_url": {"args": {"description": "URL or path to the visualization"}, "type": "str"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "data_source": {"args": {"default": "", "description": "Source of the data"}, "type": "str"}, "description": {"args": {"description": "Brief description of the visualization"}, "type": "str"}, "visualization_type": {"args": {"default": "chart", "description": "Type of visualization (chart, graph, etc.)"}, "type": "str"}}, "object_type": "gamma", "metadata_schema": {"required": ["content_type", "tags"], "recommended": ["visualization_category", "target_audience"]}}',
  'Chart, graph, or data display',
  ARRAY["Data analysis",Statistics,"Research reports","Business intelligence"],
  '{}',
  '2025-04-29 14:08:00.373701+02',
  '2025-04-29 14:08:00.373701+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '816869d8-b8f5-4a8f-bfe1-424e12a1a06d',
  'ProductFeature',
  'gamma',
  '1.0',
  '{"name": "ProductFeature", "fields": {"tags": {"args": {"description": "Classification tags", "default_factory": "list"}, "type": "List[str]"}, "title": {"args": {"description": "Feature title"}, "type": "str"}, "benefits": {"args": {"description": "Feature benefits", "default_factory": "list"}, "type": "List[str]"}, "position": {"args": {"default": 0, "description": "Character position in the parent document"}, "type": "int"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "description": {"args": {"description": "Feature description"}, "type": "str"}}, "object_type": "gamma", "metadata_schema": {"required": ["content_type", "tags"], "recommended": ["feature_category", "target_audience"]}}',
  'Specific product capability',
  ARRAY["Product marketing","Feature lists","Product documentation","Sales content"],
  '{}',
  '2025-04-29 14:08:00.375157+02',
  '2025-04-29 14:08:00.375157+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  'f68bf45c-b15d-415f-874d-ce40c95824a9',
  'ProsAndConsList',
  'gamma',
  '1.0',
  '{"name": "ProsAndConsList", "fields": {"cons": {"args": {"description": "List of disadvantages", "default_factory": "list"}, "type": "List[str]"}, "pros": {"args": {"description": "List of advantages", "default_factory": "list"}, "type": "List[str]"}, "tags": {"args": {"description": "Classification tags", "default_factory": "list"}, "type": "List[str]"}, "title": {"args": {"description": "List title"}, "type": "str"}, "position": {"args": {"default": 0, "description": "Character position in the parent document"}, "type": "int"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}}, "object_type": "gamma", "metadata_schema": {"required": ["content_type", "tags"], "recommended": ["list_category", "context"]}}',
  'Advantages and disadvantages',
  ARRAY["Product reviews","Comparison content","Decision guides","Analysis content"],
  '{}',
  '2025-04-29 14:08:00.376357+02',
  '2025-04-29 14:08:00.376357+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '911bbe0d-37e7-4141-b394-b9777ea027fb',
  'Checklist',
  'gamma',
  '1.0',
  '{"name": "Checklist", "fields": {"tags": {"args": {"description": "Classification tags", "default_factory": "list"}, "type": "List[str]"}, "items": {"args": {"description": "Checklist items", "default_factory": "list"}, "type": "List[Dict[str, Any]]"}, "title": {"args": {"description": "Checklist title"}, "type": "str"}, "position": {"args": {"default": 0, "description": "Character position in the parent document"}, "type": "int"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}}, "object_type": "gamma", "metadata_schema": {"required": ["content_type", "tags"], "recommended": ["checklist_type", "context"]}}',
  'Action item list',
  ARRAY["Task lists","Process guides","Implementation checklists","Planning tools"],
  '{}',
  '2025-04-29 14:08:00.377482+02',
  '2025-04-29 14:08:00.377482+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '129e14e0-9eb7-4378-935a-9879fbe76753',
  'Topic',
  'organizer',
  '1.0',
  '{"name": "Topic", "fields": {"icon": {"args": {"default": "", "description": "Icon identifier or URL"}, "type": "str"}, "name": {"args": {"description": "The topic name"}, "type": "str"}, "slug": {"args": {"description": "URL-friendly version of the name"}, "type": "str"}, "tags": {"args": {"description": "Classification tags", "default_factory": "list"}, "type": "List[str]"}, "keywords": {"args": {"description": "SEO keywords with priority", "default_factory": "list"}, "type": "List[Dict[str, str]]"}, "parent_id": {"args": {"default": null, "description": "ID of parent topic (if any)"}, "type": "str"}, "subtopics": {"args": {"description": "List of subtopics", "default_factory": "list"}, "type": "List[Dict[str, Any]]"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "description": {"args": {"description": "Brief description of the topic scope"}, "type": "str"}}, "object_type": "organizer", "metadata_schema": {"required": ["content_type", "tags"], "recommended": ["importance_level", "audience_focus"]}}',
  'Primary subject area',
  ARRAY["Content hierarchies",Taxonomies,"Site architecture","Information organization"],
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
  ARRAY["Content hierarchies",Taxonomies,"Site architecture","Information organization"],
  '{}',
  '2025-04-29 14:08:00.379739+02',
  '2025-04-29 14:08:00.379739+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '81b523f1-1a03-48ee-816d-3f2002c9822b',
  'Category',
  'organizer',
  '1.0',
  '{"name": "Category", "fields": {"icon": {"args": {"default": "", "description": "Icon identifier or URL"}, "type": "str"}, "name": {"args": {"description": "The category name"}, "type": "str"}, "slug": {"args": {"description": "URL-friendly version of the name"}, "type": "str"}, "tags": {"args": {"description": "Classification tags", "default_factory": "list"}, "type": "List[str]"}, "keywords": {"args": {"description": "SEO keywords with priority", "default_factory": "list"}, "type": "List[Dict[str, str]]"}, "parent_id": {"args": {"default": null, "description": "ID of parent category (if any)"}, "type": "str"}, "thumbnail": {"args": {"default": "", "description": "URL or path to category thumbnail image"}, "type": "str"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "description": {"args": {"description": "Brief description of the category"}, "type": "str"}, "display_order": {"args": {"default": 0, "description": "Order for display"}, "type": "int"}}, "object_type": "organizer", "metadata_schema": {"required": ["content_type", "tags"], "recommended": ["content_count", "featured_content"]}}',
  'Content classification grouping',
  ARRAY["Content categorization","Blog categories","Product grouping","Content organization"],
  '{}',
  '2025-04-29 14:08:00.380854+02',
  '2025-04-29 14:08:00.380854+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '177c4906-f214-43d0-b2a2-91640cdddec3',
  'Subcategory',
  'organizer',
  '1.0',
  '{"name": "Subcategory", "fields": {"icon": {"args": {"default": "", "description": "Icon identifier or URL"}, "type": "str"}, "name": {"args": {"description": "The subcategory name"}, "type": "str"}, "slug": {"args": {"description": "URL-friendly version of the name"}, "type": "str"}, "tags": {"args": {"description": "Classification tags", "default_factory": "list"}, "type": "List[str]"}, "order": {"args": {"default": 0, "description": "Display order within parent category"}, "type": "int"}, "keywords": {"args": {"description": "SEO keywords with priority", "default_factory": "list"}, "type": "List[Dict[str, str]]"}, "parent_id": {"args": {"default": null, "description": "ID of parent category"}, "type": "str"}, "thumbnail": {"args": {"default": "", "description": "URL or path to subcategory thumbnail image"}, "type": "str"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "description": {"args": {"description": "Brief description of the subcategory"}, "type": "str"}}, "object_type": "organizer", "metadata_schema": {"required": ["content_type", "tags"], "recommended": ["category_relation", "content_count"]}}',
  'Nested classification within a category',
  ARRAY["Content categorization","Product subcategories","Content organization","Hierarchical classification"],
  '{}',
  '2025-04-29 14:08:00.382178+02',
  '2025-04-29 14:08:00.382178+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '9807e2ce-902d-4847-8957-be641834a6b1',
  'TableOfContents',
  'organizer',
  '1.0',
  '{"name": "TableOfContents", "fields": {"tags": {"args": {"description": "Classification tags", "default_factory": "list"}, "type": "List[str]"}, "items": {"args": {"description": "TOC entries with hierarchical structure", "default_factory": "list"}, "type": "List[Dict[str, Any]]"}, "title": {"args": {"default": "Table of Contents", "description": "TOC title"}, "type": "str"}, "max_depth": {"args": {"default": 3, "description": "Maximum depth of TOC hierarchy"}, "type": "int"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "show_page_numbers": {"args": {"default": true, "description": "Whether to display page numbers"}, "type": "bool"}}, "object_type": "organizer", "metadata_schema": {"required": ["content_type", "tags"], "recommended": ["document_type", "entry_count"]}}',
  'Content organization listing with hierarchical structure',
  ARRAY[Books,Ebooks,Documentation,"Long-form content"],
  '{}',
  '2025-04-29 14:08:00.383287+02',
  '2025-04-29 14:08:00.383287+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '8a708e20-3ba2-49f9-9d79-d6e7342d2424',
  'Index',
  'organizer',
  '1.0',
  '{"name": "Index", "fields": {"tags": {"args": {"description": "Classification tags", "default_factory": "list"}, "type": "List[str]"}, "title": {"args": {"default": "Index", "description": "Index title"}, "type": "str"}, "entries": {"args": {"description": "Index entries with page references", "default_factory": "list"}, "type": "List[Dict[str, Any]]"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}}, "object_type": "organizer", "metadata_schema": {"required": ["content_type", "tags"], "recommended": ["document_type", "entry_count"]}}',
  'Alphabetical topic listing',
  ARRAY[Books,Ebooks,Documentation,"Reference materials"],
  '{}',
  '2025-04-29 14:08:00.384451+02',
  '2025-04-29 14:08:00.384451+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '1d9f1d02-e67e-47b4-ad15-559ec26bad61',
  'Sitemap',
  'organizer',
  '1.0',
  '{"name": "Sitemap", "fields": {"tags": {"args": {"description": "Classification tags", "default_factory": "list"}, "type": "List[str]"}, "title": {"args": {"default": "Sitemap", "description": "Sitemap title"}, "type": "str"}, "structure": {"args": {"description": "Website structure with pages and hierarchy", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "last_updated": {"args": {"default": "", "description": "Last update date"}, "type": "str"}}, "object_type": "organizer", "metadata_schema": {"required": ["content_type", "tags"], "recommended": ["sitemap_type", "page_count"]}}',
  'Website structure',
  ARRAY["Website organization","Navigation planning","SEO optimization","Content architecture"],
  '{}',
  '2025-04-29 14:08:00.385521+02',
  '2025-04-29 14:08:00.385521+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '3bca8aaa-c981-4a91-b677-a04ff12b26b6',
  'CourseModule',
  'organizer',
  '1.0',
  '{"name": "CourseModule", "fields": {"tags": {"args": {"description": "Classification tags", "default_factory": "list"}, "type": "List[str]"}, "order": {"args": {"default": 0, "description": "Display order in course"}, "type": "int"}, "title": {"args": {"description": "Module title"}, "type": "str"}, "lessons": {"args": {"description": "List of lessons in the module", "default_factory": "list"}, "type": "List[Dict[str, Any]]"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "description": {"args": {"description": "Module description"}, "type": "str"}, "prerequisites": {"args": {"description": "Required modules or lessons", "default_factory": "list"}, "type": "List[str]"}}, "object_type": "organizer", "metadata_schema": {"required": ["content_type", "tags"], "recommended": ["lesson_count", "estimated_duration"]}}',
  'Group of related lessons in a course',
  ARRAY["Online courses","Educational content","Training programs","Learning paths"],
  '{}',
  '2025-04-29 14:08:00.386592+02',
  '2025-04-29 14:08:00.386592+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '0a16253a-33d9-475b-a6b5-d646ea817702',
  'TaxonomyTerm',
  'organizer',
  '1.0',
  '{"name": "TaxonomyTerm", "fields": {"name": {"args": {"description": "The term name"}, "type": "str"}, "slug": {"args": {"description": "URL-friendly version of the name"}, "type": "str"}, "tags": {"args": {"description": "Classification tags", "default_factory": "list"}, "type": "List[str]"}, "parent_id": {"args": {"default": null, "description": "ID of parent term (if any)"}, "type": "str"}, "belongs_to": {"args": {"description": "References to container objects", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "vocabulary": {"args": {"description": "Vocabulary this term belongs to"}, "type": "str"}, "description": {"args": {"description": "Brief description of the term"}, "type": "str"}}, "object_type": "organizer", "metadata_schema": {"required": ["content_type", "tags"], "recommended": ["term_relation", "usage_count"]}}',
  'Hierarchical classification term',
  ARRAY["Content classification",Taxonomies,"Metadata organization","Content tagging"],
  '{}',
  '2025-04-29 14:08:00.387716+02',
  '2025-04-29 14:08:00.387716+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '0ff71310-f707-4601-9fad-6bcd57073442',
  'ContentHub',
  'organizer',
  '1.0',
  '{"name": "ContentHub", "fields": {"title": {"args": {"description": "Hub title"}, "type": "str"}, "description": {"args": {"description": "Hub description"}, "type": "str"}, "content_items": {"args": {"description": "List of content items in the hub", "default_factory": "list"}, "type": "List[Dict[str, Any]]"}}, "object_type": "organizer", "metadata_schema": {"required": ["content_type"], "recommended": ["content_count", "featured_content"]}}',
  'Centralized topic collection',
  ARRAY["Content organization","Topic hubs","Content clusters","Information architecture"],
  '{}',
  '2025-04-29 14:08:00.388914+02',
  '2025-04-29 14:08:00.388914+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '0329af5f-c8b0-4ea3-b3dd-c06a46267320',
  'Tag',
  'qualifier',
  '1.0',
  '{"name": "Tag", "fields": {"name": {"args": {"description": "The tag name"}, "type": "str"}, "slug": {"args": {"description": "URL-friendly version of the name"}, "type": "str"}, "parent_id": {"args": {"default": null, "description": "ID of parent tag (for hierarchical tagging)"}, "type": "str"}, "tag_group": {"args": {"default": "", "description": "Optional group this tag belongs to"}, "type": "str"}, "description": {"args": {"default": "", "description": "Brief description of what the tag represents"}, "type": "str"}, "usage_count": {"args": {"default": 0, "description": "Number of content items using this tag"}, "type": "int"}}, "object_type": "qualifier", "metadata_schema": {"required": ["content_type"], "recommended": ["tag_importance"]}}',
  'Content classification label',
  ARRAY["Content tagging",Classification,"Content organization",Metadata],
  '{}',
  '2025-04-29 14:08:00.390214+02',
  '2025-04-29 14:08:00.390214+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  'e58c7de0-c63d-48e2-91fc-46de2a73bf70',
  'Keyword',
  'qualifier',
  '1.0',
  '{"name": "Keyword", "fields": {"cpc": {"args": {"default": 0.0, "description": "Cost per click"}, "type": "float"}, "keyword": {"args": {"description": "The keyword term"}, "type": "str"}, "difficulty": {"args": {"ge": 0.0, "le": 100.0, "default": 0.0, "description": "Keyword difficulty score"}, "type": "float"}, "competition": {"args": {"ge": 0.0, "le": 1.0, "default": 0.0, "description": "Competition level"}, "type": "float"}, "search_intent": {"args": {"default": "informational", "description": "Search intent type"}, "type": "str"}, "search_volume": {"args": {"default": 0, "description": "Monthly search volume"}, "type": "int"}}, "object_type": "qualifier", "metadata_schema": {"required": ["content_type"], "recommended": ["keyword_type", "target_audience"]}}',
  'SEO search term',
  ARRAY["SEO optimization","Content targeting","Search marketing","Content strategy"],
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
  ARRAY["Content targeting","Audience segmentation","Content strategy",Marketing],
  '{}',
  '2025-04-29 14:08:00.392676+02',
  '2025-04-29 14:08:00.392676+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '4c8b7cb0-dbdf-4cd6-94e5-6fbe2ebfea4d',
  'DifficultyLevel',
  'qualifier',
  '1.0',
  '{"name": "DifficultyLevel", "fields": {"level": {"args": {"description": "Difficulty level (beginner, intermediate, advanced, etc.)"}, "type": "str"}, "description": {"args": {"description": "Brief description of the level"}, "type": "str"}, "prerequisites": {"args": {"description": "Required knowledge or skills", "default_factory": "list"}, "type": "List[str]"}}, "object_type": "qualifier", "metadata_schema": {"required": ["content_type"], "recommended": ["target_audience", "skill_requirements"]}}',
  'Content complexity indicator',
  ARRAY["Content difficulty","Educational content","Technical documentation","Content targeting"],
  '{}',
  '2025-04-29 14:08:00.393791+02',
  '2025-04-29 14:08:00.393791+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  'a4fe0fb4-e2f6-4001-a04e-b559dbbc177c',
  'Author',
  'qualifier',
  '1.0',
  '{"name": "Author", "fields": {"bio": {"args": {"default": "", "description": "Author biography"}, "type": "str"}, "name": {"args": {"description": "Author name"}, "type": "str"}, "expertise": {"args": {"description": "Areas of expertise", "default_factory": "list"}, "type": "List[str]"}, "contact_info": {"args": {"description": "Contact information", "default_factory": "dict"}, "type": "Dict[str, Any]"}}, "object_type": "qualifier", "metadata_schema": {"required": ["content_type"], "recommended": ["author_role", "publication_count"]}}',
  'Content creator',
  ARRAY["Content attribution","Author profiles","Content management",Credits],
  '{}',
  '2025-04-29 14:08:00.39487+02',
  '2025-04-29 14:08:00.39487+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '1a21b7f9-5171-4f63-a836-bd2718736830',
  'ContentStatus',
  'qualifier',
  '1.0',
  '{"name": "ContentStatus", "fields": {"status": {"args": {"description": "Current status (draft, review, published, etc.)"}, "type": "str"}, "assigned_to": {"args": {"default": "", "description": "Person assigned to next action"}, "type": "str"}, "next_action": {"args": {"default": "", "description": "Next required action"}, "type": "str"}, "last_updated": {"args": {"default": "", "description": "Last status update date"}, "type": "str"}}, "object_type": "qualifier", "metadata_schema": {"required": ["content_type"], "recommended": ["workflow_stage", "due_date"]}}',
  'Publication workflow state',
  ARRAY["Content workflow","Publication management","Content lifecycle","Editorial process"],
  '{}',
  '2025-04-29 14:08:00.395984+02',
  '2025-04-29 14:08:00.395984+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  'da09dbd9-59f6-4e2b-a007-272000155cdd',
  'SEOMetadata',
  'qualifier',
  '1.0',
  '{"name": "SEOMetadata", "fields": {"title": {"args": {"description": "SEO title"}, "type": "str"}, "robots": {"args": {"default": "index, follow", "description": "Robots meta tag"}, "type": "str"}, "keywords": {"args": {"description": "Meta keywords", "default_factory": "list"}, "type": "List[str]"}, "description": {"args": {"description": "Meta description"}, "type": "str"}, "canonical_url": {"args": {"default": "", "description": "Canonical URL"}, "type": "str"}}, "object_type": "qualifier", "metadata_schema": {"required": ["content_type"], "recommended": ["seo_priority", "target_keywords"]}}',
  'Search optimization information',
  ARRAY["SEO optimization","Search marketing","Content strategy","Technical SEO"],
  '{}',
  '2025-04-29 14:08:00.398305+02',
  '2025-04-29 14:08:00.398305+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '24298555-8c00-45bd-92f5-7fc05b4df6e6',
  'Language',
  'qualifier',
  '1.0',
  '{"name": "Language", "fields": {"code": {"args": {"description": "Language code (e.g., en-US)"}, "type": "str"}, "name": {"args": {"description": "Language name"}, "type": "str"}, "direction": {"args": {"default": "ltr", "description": "Text direction (ltr, rtl)"}, "type": "str"}}, "object_type": "qualifier", "metadata_schema": {"required": ["content_type"], "recommended": ["target_region", "translation_status"]}}',
  'Content language identifier',
  ARRAY["Multilingual content",Localization,"Content targeting","International SEO"],
  '{}',
  '2025-04-29 14:08:00.399472+02',
  '2025-04-29 14:08:00.399472+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '982877ad-a1f6-4c8e-bf6e-cd704a0c2d52',
  'GeographicTarget',
  'qualifier',
  '1.0',
  '{"name": "GeographicTarget", "fields": {"city": {"args": {"default": "", "description": "Target city"}, "type": "str"}, "region": {"args": {"default": "", "description": "Target region/state"}, "type": "str"}, "country": {"args": {"description": "Target country"}, "type": "str"}, "coordinates": {"args": {"description": "Geographic coordinates", "default_factory": "dict"}, "type": "Dict[str, float]"}}, "object_type": "qualifier", "metadata_schema": {"required": ["content_type"], "recommended": ["target_radius", "local_keywords"]}}',
  'Location specificity',
  ARRAY["Local SEO","Geographic targeting","Content localization","Regional marketing"],
  '{}',
  '2025-04-29 14:08:00.40068+02',
  '2025-04-29 14:08:00.40068+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '4881ecf8-c587-4649-9bb8-b600f4db9b1f',
  'ContentLicense',
  'qualifier',
  '1.0',
  '{"name": "ContentLicense", "fields": {"type": {"args": {"description": "License type (e.g., CC BY, All Rights Reserved)"}, "type": "str"}, "description": {"args": {"description": "License description"}, "type": "str"}, "restrictions": {"args": {"description": "Usage restrictions", "default_factory": "list"}, "type": "List[str]"}, "attribution_required": {"args": {"default": true, "description": "Whether attribution is required"}, "type": "bool"}}, "object_type": "qualifier", "metadata_schema": {"required": ["content_type"], "recommended": ["license_url", "attribution_text"]}}',
  'Usage permissions',
  ARRAY["Content licensing","Copyright management","Content sharing","Legal compliance"],
  '{}',
  '2025-04-29 14:08:00.401827+02',
  '2025-04-29 14:08:00.401827+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  'd724e375-6562-4cf4-84ae-49e5b8acacfd',
  'Version',
  'qualifier',
  '1.0',
  '{"name": "Version", "fields": {"date": {"args": {"description": "Version date"}, "type": "str"}, "author": {"args": {"default": "", "description": "Version author"}, "type": "str"}, "number": {"args": {"description": "Version number"}, "type": "str"}, "changes": {"args": {"description": "List of changes", "default_factory": "list"}, "type": "List[str]"}}, "object_type": "qualifier", "metadata_schema": {"required": ["content_type"], "recommended": ["change_type", "review_status"]}}',
  'Content iteration identifier',
  ARRAY["Version control","Content updates","Change tracking",Documentation],
  '{}',
  '2025-04-29 14:08:00.402938+02',
  '2025-04-29 14:08:00.402938+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '8954e722-d855-499e-8b94-b899362722ab',
  'Revision',
  'qualifier',
  '1.0',
  '{"name": "Revision", "fields": {"date": {"args": {"description": "Revision date"}, "type": "str"}, "author": {"args": {"default": "", "description": "Revision author"}, "type": "str"}, "number": {"args": {"description": "Revision number"}, "type": "int"}, "changes": {"args": {"description": "List of changes", "default_factory": "list"}, "type": "List[str]"}}, "object_type": "qualifier", "metadata_schema": {"required": ["content_type"], "recommended": ["change_type", "review_status"]}}',
  'Tracked content change',
  ARRAY["Content revisions","Change history","Content tracking","Editorial process"],
  '{}',
  '2025-04-29 14:08:00.403996+02',
  '2025-04-29 14:08:00.403996+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '0aeeee3c-a6a2-485f-acb8-e8ad461b0c64',
  'LifecycleStage',
  'qualifier',
  '1.0',
  '{"name": "LifecycleStage", "fields": {"goals": {"args": {"description": "Stage goals", "default_factory": "list"}, "type": "List[str]"}, "stage": {"args": {"description": "Lifecycle stage (awareness, consideration, decision, etc.)"}, "type": "str"}, "metrics": {"args": {"description": "Stage success metrics", "default_factory": "list"}, "type": "List[str]"}, "description": {"args": {"description": "Stage description"}, "type": "str"}}, "object_type": "qualifier", "metadata_schema": {"required": ["content_type"], "recommended": ["target_audience", "conversion_goal"]}}',
  'Content stage in buyer journey',
  ARRAY["Content strategy","Buyer journey","Marketing funnel","Content planning"],
  '{}',
  '2025-04-29 14:08:00.405012+02',
  '2025-04-29 14:08:00.405012+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  'ff52c623-653b-4915-a522-67370dc8ec9f',
  'Sentiment',
  'qualifier',
  '1.0',
  '{"name": "Sentiment", "fields": {"tone": {"args": {"description": "Content tone (positive, negative, neutral)"}, "type": "str"}, "emotions": {"args": {"description": "Detected emotions", "default_factory": "list"}, "type": "List[str]"}, "intensity": {"args": {"ge": 0.0, "le": 1.0, "default": 0.5, "description": "Tone intensity"}, "type": "float"}}, "object_type": "qualifier", "metadata_schema": {"required": ["content_type"], "recommended": ["brand_voice", "target_audience"]}}',
  'Emotional tone indicator',
  ARRAY["Content tone","Brand voice","Emotional analysis","Content strategy"],
  '{}',
  '2025-04-29 14:08:00.406061+02',
  '2025-04-29 14:08:00.406061+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '9cd22fcf-4f4b-4886-9f93-4a28a1ae1961',
  'KeywordTrend',
  'qualifier',
  '1.0',
  '{"name": "KeywordTrend", "fields": {"keyword": {"args": {"description": "The keyword"}, "type": "str"}, "forecast": {"args": {"description": "Future trend forecast", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "trend_data": {"args": {"description": "Historical trend data", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "growth_rate": {"args": {"default": 0.0, "description": "Growth rate over time"}, "type": "float"}, "related_events": {"args": {"description": "Events affecting the trend", "default_factory": "list"}, "type": "List[str]"}, "seasonal_patterns": {"args": {"description": "Seasonal patterns", "default_factory": "dict"}, "type": "Dict[str, Any]"}}, "object_type": "qualifier", "metadata_schema": {"required": ["content_type"], "recommended": ["trend_confidence", "forecast_period"]}}',
  'Keyword performance and trends over time',
  ARRAY["Trend analysis","Keyword research","Content planning","SEO strategy"],
  '{}',
  '2025-04-29 14:08:00.412988+02',
  '2025-04-29 14:08:00.412988+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '85d68da0-c666-4640-b389-f58f20425c20',
  'LongTailKeyword',
  'qualifier',
  '1.0',
  '{"name": "LongTailKeyword", "fields": {"cpc": {"args": {"default": 0.0, "description": "Cost per click"}, "type": "float"}, "keyword": {"args": {"description": "The long-tail keyword"}, "type": "str"}, "content_gaps": {"args": {"description": "Identified content gaps", "default_factory": "list"}, "type": "List[str]"}, "search_intent": {"args": {"default": "informational", "description": "Search intent type"}, "type": "str"}, "search_volume": {"args": {"default": 0, "description": "Monthly search volume"}, "type": "int"}, "seasonal_trends": {"args": {"description": "Seasonal search patterns", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "difficulty_score": {"args": {"ge": 0.0, "le": 100.0, "default": 0.0, "description": "Keyword difficulty score"}, "type": "float"}, "competition_level": {"args": {"ge": 0.0, "le": 1.0, "default": 0.0, "description": "Competition level"}, "type": "float"}, "related_questions": {"args": {"description": "Related question-based queries", "default_factory": "list"}, "type": "List[str]"}, "ranking_difficulty": {"args": {"ge": 0.0, "le": 1.0, "default": 0.0, "description": "Estimated ranking difficulty"}, "type": "float"}}, "object_type": "qualifier", "metadata_schema": {"required": ["content_type"], "recommended": ["content_opportunity", "target_audience"]}}',
  'Long-tail keyword with search metrics and content opportunities',
  ARRAY["SEO optimization","Content targeting","Keyword research","Content strategy"],
  '{}',
  '2025-04-29 14:08:00.40723+02',
  '2025-04-29 14:08:00.40723+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  'efbb83e5-278b-46d3-aeaa-cf864b05ed8e',
  'SEOKeyword',
  'qualifier',
  '1.0',
  '{"name": "SEOKeyword", "fields": {"cpc": {"args": {"default": 0.0, "description": "Cost per click"}, "type": "float"}, "keyword": {"args": {"description": "The primary keyword"}, "type": "str"}, "search_intent": {"args": {"default": "informational", "description": "Search intent type"}, "type": "str"}, "search_volume": {"args": {"default": 0, "description": "Monthly search volume"}, "type": "int"}, "seasonal_trends": {"args": {"description": "Seasonal search patterns", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "difficulty_score": {"args": {"ge": 0.0, "le": 100.0, "default": 0.0, "description": "Keyword difficulty score"}, "type": "float"}, "related_keywords": {"args": {"description": "Related keywords", "default_factory": "list"}, "type": "List[str]"}, "competition_level": {"args": {"ge": 0.0, "le": 1.0, "default": 0.0, "description": "Competition level"}, "type": "float"}, "ranking_difficulty": {"args": {"ge": 0.0, "le": 1.0, "default": 0.0, "description": "Estimated ranking difficulty"}, "type": "float"}, "content_opportunities": {"args": {"description": "Content opportunities", "default_factory": "list"}, "type": "List[str]"}}, "object_type": "qualifier", "metadata_schema": {"required": ["content_type"], "recommended": ["content_priority", "target_audience"]}}',
  'Primary keyword with search metrics and optimization data',
  ARRAY["SEO optimization","Content targeting","Keyword research","Content strategy"],
  '{}',
  '2025-04-29 14:08:00.408524+02',
  '2025-04-29 14:08:00.408524+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '0930f5e3-5ff2-4c59-b0fa-492c1e88514c',
  'KeywordCluster',
  'qualifier',
  '1.0',
  '{"name": "KeywordCluster", "fields": {"keywords": {"args": {"description": "Keywords in the cluster", "default_factory": "list"}, "type": "List[Dict[str, Any]]"}, "cluster_name": {"args": {"description": "Name of the keyword cluster"}, "type": "str"}, "cluster_metrics": {"args": {"description": "Aggregate metrics for the cluster", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "ranking_potential": {"args": {"ge": 0.0, "le": 1.0, "default": 0.0, "description": "Overall ranking potential"}, "type": "float"}, "cluster_difficulty": {"args": {"ge": 0.0, "le": 100.0, "default": 0.0, "description": "Overall cluster difficulty"}, "type": "float"}, "content_opportunities": {"args": {"description": "Content opportunities for the cluster", "default_factory": "list"}, "type": "List[str]"}}, "object_type": "qualifier", "metadata_schema": {"required": ["content_type"], "recommended": ["cluster_priority", "target_audience"]}}',
  'Group of related keywords for content planning',
  ARRAY["Content planning","Topic clusters","Keyword research","Content strategy"],
  '{}',
  '2025-04-29 14:08:00.409708+02',
  '2025-04-29 14:08:00.409708+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  'd97c9f11-65e2-4088-a272-ff99a2b61547',
  'ContentGap',
  'qualifier',
  '1.0',
  '{"name": "ContentGap", "fields": {"content_type": {"args": {"default": "article", "description": "Recommended content type"}, "type": "str"}, "search_volume": {"args": {"default": 0, "description": "Total search volume"}, "type": "int"}, "priority_score": {"args": {"ge": 0.0, "le": 1.0, "default": 0.0, "description": "Priority score for addressing"}, "type": "float"}, "gap_description": {"args": {"description": "Description of the content gap"}, "type": "str"}, "target_audience": {"args": {"description": "Target audience for content", "default_factory": "list"}, "type": "List[str]"}, "difficulty_score": {"args": {"ge": 0.0, "le": 100.0, "default": 0.0, "description": "Content difficulty score"}, "type": "float"}, "related_keywords": {"args": {"description": "Related keywords", "default_factory": "list"}, "type": "List[str]"}}, "object_type": "qualifier", "metadata_schema": {"required": ["content_type"], "recommended": ["implementation_priority", "resource_requirements"]}}',
  'Content opportunity based on keyword analysis',
  ARRAY["Content planning","Gap analysis","Content strategy","SEO optimization"],
  '{}',
  '2025-04-29 14:08:00.41079+02',
  '2025-04-29 14:08:00.41079+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '3d7dc5dd-a0a0-4383-9114-766dc72d3017',
  'SearchIntent',
  'qualifier',
  '1.0',
  '{"name": "SearchIntent", "fields": {"intent_type": {"args": {"description": "Type of intent (informational, navigational, transactional, commercial)"}, "type": "str"}, "related_keywords": {"args": {"description": "Keywords with this intent", "default_factory": "list"}, "type": "List[str]"}, "intent_description": {"args": {"description": "Description of the intent"}, "type": "str"}, "user_journey_stage": {"args": {"default": "awareness", "description": "Stage in user journey"}, "type": "str"}, "content_requirements": {"args": {"description": "Content requirements for this intent", "default_factory": "list"}, "type": "List[str]"}}, "object_type": "qualifier", "metadata_schema": {"required": ["content_type"], "recommended": ["content_format", "target_audience"]}}',
  'Search intent categorization and analysis',
  ARRAY["Content targeting","User intent","Content strategy","SEO optimization"],
  '{}',
  '2025-04-29 14:08:00.411873+02',
  '2025-04-29 14:08:00.411873+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  'e84439f1-b57a-4e1e-8f49-71cea1e47609',
  'CompetitorKeyword',
  'qualifier',
  '1.0',
  '{"name": "CompetitorKeyword", "fields": {"keyword": {"args": {"description": "The keyword"}, "type": "str"}, "content_type": {"args": {"default": "", "description": "Type of ranking content"}, "type": "str"}, "ranking_history": {"args": {"description": "Historical ranking data", "default_factory": "list"}, "type": "List[Dict[str, Any]]"}, "backlink_profile": {"args": {"description": "Backlink information", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "content_strategy": {"args": {"description": "Observed content strategy", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "ranking_position": {"args": {"default": 0, "description": "Current ranking position"}, "type": "int"}, "competitor_domain": {"args": {"description": "Competitor domain"}, "type": "str"}}, "object_type": "qualifier", "metadata_schema": {"required": ["content_type"], "recommended": ["competitor_analysis", "strategy_insights"]}}',
  'Competitor keyword rankings and strategies',
  ARRAY["Competitive analysis","Keyword research","Content strategy","SEO optimization"],
  '{}',
  '2025-04-29 14:08:00.414124+02',
  '2025-04-29 14:08:00.414124+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  'ea66ec66-6d76-4de0-9dfc-00193488518a',
  'KeywordOpportunity',
  'qualifier',
  '1.0',
  '{"name": "KeywordOpportunity", "fields": {"keyword": {"args": {"description": "The keyword"}, "type": "str"}, "content_gaps": {"args": {"description": "Identified content gaps", "default_factory": "list"}, "type": "List[str]"}, "search_volume": {"args": {"default": 0, "description": "Monthly search volume"}, "type": "int"}, "difficulty_score": {"args": {"ge": 0.0, "le": 100.0, "default": 0.0, "description": "Keyword difficulty score"}, "type": "float"}, "opportunity_score": {"args": {"ge": 0.0, "le": 1.0, "default": 0.0, "description": "Opportunity score"}, "type": "float"}, "ranking_potential": {"args": {"ge": 1.0, "le": 100.0, "default": 0.0, "description": "Potential ranking position"}, "type": "float"}, "revenue_potential": {"args": {"default": 0.0, "description": "Estimated revenue potential"}, "type": "float"}, "implementation_priority": {"args": {"default": "medium", "description": "Implementation priority level"}, "type": "str"}}, "object_type": "qualifier", "metadata_schema": {"required": ["content_type"], "recommended": ["content_requirements", "resource_needs"]}}',
  'High-potential keyword opportunity',
  ARRAY["Content planning","Keyword research","Content strategy","SEO optimization"],
  '{}',
  '2025-04-29 14:08:00.415315+02',
  '2025-04-29 14:08:00.415315+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  'c501e249-5454-4ef5-aeaa-bb902faf21e9',
  'KeywordResearch',
  'qualifier',
  '1.0',
  '{"name": "KeywordResearch", "fields": {"findings": {"args": {"description": "Research findings", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "industry": {"args": {"description": "Industry focus"}, "type": "str"}, "research_date": {"args": {"description": "Date of research"}, "type": "str"}, "recommendations": {"args": {"description": "Strategic recommendations", "default_factory": "list"}, "type": "List[str]"}, "success_metrics": {"args": {"description": "Success metrics", "default_factory": "list"}, "type": "List[str]"}, "target_audience": {"args": {"description": "Target audience segments", "default_factory": "list"}, "type": "List[str]"}, "implementation_plan": {"args": {"description": "Implementation plan", "default_factory": "dict"}, "type": "Dict[str, Any]"}}, "object_type": "qualifier", "metadata_schema": {"required": ["content_type"], "recommended": ["research_scope", "implementation_timeline"]}}',
  'Comprehensive keyword research findings',
  ARRAY["Keyword research","Content strategy","SEO planning","Market research"],
  '{}',
  '2025-04-29 14:08:00.416554+02',
  '2025-04-29 14:08:00.416554+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '8a8a7e6e-576d-46d4-bc14-17fd14799652',
  'KeywordStrategy',
  'qualifier',
  '1.0',
  '{"name": "KeywordStrategy", "fields": {"timeline": {"args": {"description": "Implementation timeline", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "content_plan": {"args": {"description": "Content development plan", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "ranking_goals": {"args": {"description": "Ranking objectives", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "strategy_name": {"args": {"description": "Strategy name"}, "type": "str"}, "success_metrics": {"args": {"description": "Success metrics", "default_factory": "list"}, "type": "List[str]"}, "target_keywords": {"args": {"description": "Target keywords with priorities", "default_factory": "list"}, "type": "List[Dict[str, Any]]"}, "implementation_steps": {"args": {"description": "Implementation steps", "default_factory": "list"}, "type": "List[str]"}}, "object_type": "qualifier", "metadata_schema": {"required": ["content_type"], "recommended": ["strategy_priority", "resource_allocation"]}}',
  'Strategic planning for keyword targeting',
  ARRAY["Content strategy","SEO planning","Keyword targeting","Content optimization"],
  '{}',
  '2025-04-29 14:08:00.417845+02',
  '2025-04-29 14:08:00.417845+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '5cfdb63f-2c83-40bf-818e-8ca8d3bb2016',
  'SerpSnapshot',
  'qualifier',
  '1.0',
  '{"name": "SerpSnapshot", "fields": {"keyword": {"args": {"description": "Target keyword"}, "type": "str"}, "timestamp": {"args": {"description": "When snapshot was taken"}, "type": "str"}, "top_domains": {"args": {"description": "Top ranking domains with counts", "default_factory": "list"}, "type": "List[Dict[str, Any]]"}, "content_types": {"args": {"description": "Content type distribution", "default_factory": "dict"}, "type": "Dict[str, int]"}, "serp_features": {"args": {"description": "SERP features present", "default_factory": "list"}, "type": "List[str]"}, "snippet_types": {"args": {"description": "Snippet type distribution", "default_factory": "dict"}, "type": "Dict[str, int]"}, "organic_results": {"args": {"description": "List of organic search results", "default_factory": "list"}, "type": "List[Dict[str, Any]]"}}, "object_type": "qualifier", "metadata_schema": {"required": ["content_type"], "recommended": ["serp_analysis", "competition_level"]}}',
  'SerpSnapshot',
  ARRAY[SerpSnapshot],
  '{}',
  '2025-05-03 08:13:12.957329+02',
  '2025-05-03 08:13:12.957329+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '5008cc26-e98c-4ae7-b9f8-81d5dff0709a',
  'ContentOpportunity',
  'qualifier',
  '1.0',
  '{"name": "ContentOpportunity", "fields": {"topic": {"args": {"description": "The main topic of the content opportunity"}, "type": "str"}, "questions": {"args": {"description": "Related questions to address in the content", "default_factory": "list"}, "type": "List[str]"}, "primary_keyword": {"args": {"description": "The main keyword for this opportunity"}, "type": "Dict[str, Any]"}, "difficulty_score": {"args": {"ge": 0.0, "le": 100.0, "default": 50.0, "description": "Content creation difficulty score"}, "type": "float"}, "competing_content": {"args": {"description": "List of competing content pieces", "default_factory": "list"}, "type": "List[Dict[str, Any]]"}, "opportunity_score": {"args": {"ge": 0.0, "le": 1.0, "default": 0.0, "description": "Overall opportunity score"}, "type": "float"}, "secondary_keywords": {"args": {"description": "Related keywords for this opportunity", "default_factory": "list"}, "type": "List[Dict[str, Any]]"}, "suggested_content_type": {"args": {"description": "Recommended content type (guide, blog_post, comparison, etc.)"}, "type": "str"}}, "object_type": "qualifier", "metadata_schema": {"required": ["content_type"], "recommended": ["content_priority", "target_audience"]}}',
  'Content opportunity based on keyword and topic analysis',
  ARRAY["Content planning","Topic research","Content strategy","SEO optimization"],
  '{}',
  '2025-05-03 08:47:27.971378+02',
  '2025-05-03 08:47:27.971378+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  'ba7c1a79-0f40-4098-b766-a231b1a2cb78',
  'TopicMap',
  'alpha',
  '1.0',
  '{"name": "TopicMap", "fields": {"title": {"args": {"description": "Title of the topic map"}, "type": "str"}, "topics": {"args": {"description": "List of main topics in this topic map", "default_factory": "list"}, "type": "List[Dict[str, Any]]"}, "industry": {"args": {"description": "Industry this topic map is for"}, "type": "str"}, "metadata": {"args": {"description": "Additional metadata about this topic map", "default_factory": "dict"}, "type": "Dict[str, Any]"}, "rationale": {"args": {"description": "Explanation of the rationale behind this topic organization"}, "type": "str"}, "conversion_goal": {"args": {"description": "Primary conversion goal for the content strategy"}, "type": "str"}, "target_audience": {"args": {"description": "Primary target audience for the content"}, "type": "str"}, "strategic_recommendations": {"args": {"description": "Strategic recommendations for implementing this content strategy", "default_factory": "list"}, "type": "List[str]"}}, "object_type": "alpha", "metadata_schema": {"required": ["content_type", "target_audience", "industry"], "recommended": ["conversion_goal", "business_vertical"]}}',
  'Top-level container for content strategy organization with topics and subtopics',
  ARRAY["Content Strategy Planning","SEO Content Mapping","Editorial Calendar Development","Content Gap Analysis"],
  '{TopicMapperGenericTemplate}',
  '2025-05-13 16:18:22.577616+02',
  '2025-05-15 20:12:17.034632+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  'ba548675-c31d-4fe0-b847-943737d181ae',
  'PromptTemplate',
  'prompt_template',
  '1.0',
  '{"name": "PromptTemplate", "fields": {"name": {"args": {"description": "Unique name for the prompt template"}, "type": "str"}, "tags": {"args": {"description": "List of tags for categorization", "default_factory": "list"}, "type": "List[str]"}, "version": {"args": {"default": "1.0", "description": "Version of the prompt template"}, "type": "str"}, "created_at": {"args": {"description": "Creation timestamp"}, "type": "datetime"}, "updated_at": {"args": {"description": "Last update timestamp"}, "type": "datetime"}, "description": {"args": {"description": "Description of what this prompt template is used for"}, "type": "str"}, "human_message": {"args": {"description": "Human message components for the prompt"}, "type": "dict"}, "system_message": {"args": {"description": "System message components for the prompt"}, "type": "dict"}}, "validators": [{"pre": true, "code": "def name_not_empty(cls, v):\\n    if not v.strip():\\n        raise ValueError(''Template name cannot be empty'')\\n    return v", "name": "name_not_empty", "fields": ["name"]}, {"pre": false, "code": "def system_message_validation(cls, v):\\n    if not isinstance(v, dict):\\n        raise ValueError(''system_message must be a dictionary'')\\n    required_keys = [''agent_role'', ''agent_task'', ''agent_goal'', ''key_information'', ''context_placeholder'', ''agent_response'', ''output_format'']\\n    missing = [key for key in required_keys if key not in v]\\n    if missing:\\n        raise ValueError(f''Missing required system_message components: {missing}'')\\n    return v", "name": "system_message_validation", "fields": ["system_message"]}], "description": "Definition for structured prompt templates to be used in LLM interactions", "metadata_schema": {"required": ["name", "system_message"], "recommended": ["description", "version"], "human_message_schema": {"required": ["focused_question"], "components": ["focused_question"]}, "system_message_schema": {"required": ["agent_role", "agent_task", "agent_goal", "key_information", "context_placeholder", "agent_response", "output_format"], "components": ["positioning_sentence", "agent_role", "agent_task", "agent_goal", "agent_tools", "key_information", "context_placeholder", "agent_response", "additional_instructions", "closing_instructions", "output_format"]}}}',
  'Definition for structured prompt templates to be used in LLM interactions',
  ARRAY[],
  '{}',
  '2025-05-17 17:10:01.539281+02',
  '2025-05-17 17:10:01.539281+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  'dd517472-5a48-4583-bd42-4d163b602fab',
  'MasterPromptTemplate',
  'prompt_template',
  '1.0',
  '{"name": "MasterPromptTemplate", "fields": {"name": {"args": {"description": "Unique name for the prompt template"}, "type": "str"}, "tags": {"args": {"description": "List of tags for categorization", "default_factory": "list"}, "type": "List[str]"}, "version": {"args": {"default": "1.0", "description": "Version of the prompt template"}, "type": "str"}, "created_at": {"args": {"description": "Creation timestamp"}, "type": "datetime"}, "updated_at": {"args": {"description": "Last update timestamp"}, "type": "datetime"}, "description": {"args": {"description": "Description of what this prompt accomplishes"}, "type": "str"}, "human_message": {"args": {"components": {"focused_question": {"args": {"example": "Please analyze this article about neural networks and suggest how I can improve it for better search visibility while keeping it accessible to beginners.", "purpose": "Provides the specific prompt or question from the user", "description": "The specific question or instruction from the human"}, "type": "str"}}, "description": "Human message components"}, "type": "Dict"}, "system_message": {"args": {"components": {"agent_goal": {"args": {"example": "Your goal is to help the user increase the article''s search visibility while maintaining its educational value.", "purpose": "Provides broader context for why the task matters", "description": "The overall goal or objective of the task"}, "type": "str"}, "agent_role": {"args": {"example": "Your role is that of an expert content strategist with deep knowledge of SEO principles and content marketing.", "purpose": "Defines the specific perspective and expertise the LLM should adopt", "description": "Role the LLM should assume"}, "type": "str"}, "agent_task": {"args": {"example": "Analyze the provided article to identify key topics, determine search intent, and suggest content improvements.", "purpose": "Clearly defines the action the LLM should take", "description": "The specific task the LLM is being asked to perform"}, "type": "str"}, "agent_tools": {"args": {"example": ["SEO keyword research", "Topic clustering", "Readability analysis", "Content gap identification"], "purpose": "Describes resources or methods available to the LLM", "description": "Tools or capabilities the LLM can use"}, "type": "List[str]"}, "output_format": {"args": {"example": "Format your recommendations as a JSON object with the following structure: { \\"topics\\": [], \\"intent\\": \\"\\", \\"recommendations\\": [] }", "purpose": "Specifies exact formatting requirements for parsing", "description": "Technical format for the output"}, "type": "str"}, "agent_response": {"args": {"example": "Provide your analysis in these sections: 1) Key Topics Identified, 2) Search Intent Analysis, 3) Content Improvement Recommendations.", "purpose": "Structures how the LLM should present its output", "description": "Format for the LLM''s response"}, "type": "str"}, "key_information": {"args": {"example": "The article is targeting beginners in machine learning who have programming experience but limited mathematical background.", "purpose": "Provides essential background knowledge or constraints", "description": "Critical information the LLM needs to know"}, "type": "str"}, "context_placeholder": {"args": {"example": "[CONTEXT: The following is the article to analyze: {context}]", "purpose": "Marks where retrieved or dynamically generated context should be inserted", "description": "Placeholder for dynamic context to be injected"}, "type": "str"}, "closing_instructions": {"args": {"example": "Remember to keep suggestions practical and aligned with the user''s goals rather than generic SEO advice.", "purpose": "Offers final guidance or reinforces key aspects of the task", "description": "Final instructions before the human message"}, "type": "str"}, "positioning_sentence": {"args": {"example": "You are using Claude, a helpful AI assistant created by Anthropic.", "purpose": "Sets the foundation for the LLM''s understanding of its role", "description": "Initial sentence positioning the LLM"}, "type": "str"}, "additional_instructions": {"args": {"example": "Ensure your recommendations are actionable and suitable for implementation by someone with the user''s stated expertise level.", "purpose": "Provides supplementary guidance or constraints", "description": "Any additional instructions for the LLM"}, "type": "str"}, "controlled_context_placeholder": {"args": {"example": "[CONTROLLED CONTEXT: Specific guidelines for this article: {controlled_context}]", "purpose": "Enables fine-grained control over context inserted by the application", "description": "Placeholder for manually controlled context injection"}, "type": "str"}}, "description": "System message components"}, "type": "Dict"}}, "validators": [{"pre": false, "code": "def components_validation(cls, values):\\n    if not values.get(\\"system_message\\") and not values.get(\\"human_message\\"):\\n        raise ValueError(\\"At least one of system_message or human_message must be provided\\")\\n    return values", "name": "components_validation", "fields": ["system_message", "human_message"]}], "description": "Definition for a comprehensive prompt template with system and human message components", "metadata_schema": {"required": ["name", "description", "version"], "resolution": {"system_message.agent_tools": "py_vectorbase_injection", "system_message.context_placeholder": "dynamic_context_injection", "system_message.controlled_context_placeholder": "controlled_context_injection"}, "recommended": ["system_message.positioning_sentence", "system_message.agent_role", "system_message.agent_task", "human_message.focused_question"], "assembly_orders": {"agent": ["system_message.positioning_sentence", "system_message.agent_role", "system_message.agent_task", "system_message.agent_tools", "system_message.additional_instructions", "system_message.agent_response", "human_message.focused_question"], "chatbot": ["system_message.positioning_sentence", "system_message.agent_role", "system_message.agent_task", "system_message.agent_goal", "human_message.focused_question", "system_message.agent_tools", "system_message.key_information", "system_message.context_placeholder", "system_message.controlled_context_placeholder", "system_message.additional_instructions", "system_message.agent_response", "system_message.output_format", "system_message.closing_instructions"], "standard": ["system_message.positioning_sentence", "system_message.agent_role", "system_message.agent_task", "system_message.agent_goal", "system_message.agent_tools", "system_message.key_information", "system_message.context_placeholder", "system_message.controlled_context_placeholder", "system_message.additional_instructions", "system_message.agent_response", "system_message.output_format", "system_message.closing_instructions", "human_message.focused_question"]}}}',
  'Definition for a comprehensive prompt template with system and human message components',
  ARRAY[],
  '{}',
  '2025-05-18 08:23:53.895752+02',
  '2025-05-18 08:23:53.895752+02'
);

INSERT INTO public.object_models (id, name, object_type, version, definition, description, use_cases, related_templates, created_at, updated_at)
VALUES (
  '8cf46032-124b-4e8f-a337-bc284c6520e1',
  'PromptChain',
  'prompt_chain',
  '1.0',
  '{"name": "PromptChain", "fields": {"name": {"args": {"description": "Unique name for the prompt chain"}, "type": "str"}, "tags": {"args": {"description": "List of tags for categorization", "default_factory": "list"}, "type": "List[str]"}, "version": {"args": {"default": "1.0.0", "description": "Version of the prompt chain"}, "type": "str"}, "created_at": {"args": {"description": "Creation timestamp"}, "type": "datetime"}, "updated_at": {"args": {"description": "Last update timestamp"}, "type": "datetime"}, "chain_steps": {"args": {"example": [{"output_key": "extracted_context", "prompt_name": "ContextExtractor", "input_mapping": {}, "assembly_order": "standard", "version_requirement": ">=1.0.0"}, {"output_key": "topics", "prompt_name": "TopicGenerator", "input_mapping": {"context": "$outputs.extracted_context"}, "assembly_order": "agent", "version_requirement": ">=1.0.0"}], "description": "Ordered list of prompt steps in the chain"}, "type": "List[Dict]"}, "description": {"args": {"description": "Description of what this prompt chain accomplishes"}, "type": "str"}, "input_schema": {"args": {"example": {"query": "string", "max_topics": "integer", "context_source": "string"}, "description": "Schema defining expected input fields for the chain"}, "type": "Dict"}, "output_schema": {"args": {"example": {"topics": "List[string]", "reasoning": "string", "context_used": "string"}, "description": "Schema defining the expected output structure"}, "type": "Dict"}, "execution_pattern": {"args": {"default": "sequential", "description": "Pattern for executing the chain steps", "allowed_values": ["sequential", "branching", "parallel"]}, "type": "str"}, "version_resolution": {"args": {"example": {"fallback": "use_latest", "strategy": "minimum"}, "description": "Strategy for resolving prompt template versions"}, "type": "Dict"}}, "validators": [{"pre": false, "code": "def chain_steps_validation(cls, v):\\n    if not isinstance(v, list) or len(v) == 0:\\n        raise ValueError(''chain_steps must be a non-empty list'')\\n    for step in v:\\n        if not isinstance(step, dict):\\n            raise ValueError(''Each chain step must be a dictionary'')\\n        if ''prompt_name'' not in step:\\n            raise ValueError(''Each chain step must include prompt_name'')\\n    return v", "name": "chain_steps_validation", "fields": ["chain_steps"]}, {"pre": false, "code": "def input_mapping_validation(cls, v):\\n    if not isinstance(v, list) or len(v) == 0:\\n        return v\\n    for i, step in enumerate(v):\\n        if i > 0 and ''input_mapping'' in step:\\n            for key, value in step[''input_mapping''].items():\\n                if isinstance(value, str) and value.startswith(''$outputs.'') and value[9:] not in [s[''output_key''] for s in v[:i]]:\\n                    raise ValueError(f''Input mapping refers to non-existent output key: {value[9:]}'')\\n    return v", "name": "input_mapping_validation", "fields": ["chain_steps"]}], "description": "Definition for a chain of prompt templates to be executed sequentially", "metadata_schema": {"required": ["name", "description", "chain_steps", "version"], "recommended": ["input_schema", "output_schema", "version_resolution"], "chain_execution_patterns": {"parallel": {"behavior": "Define parallel steps that don''t depend on each other''s outputs", "description": "Multiple prompts execute simultaneously with the same input"}, "branching": {"behavior": "Define conditions in input_mapping to determine which branch to take", "description": "Chain can split based on conditions from previous outputs"}, "sequential": {"behavior": "Each step must complete before the next begins", "description": "Execute prompts one after another, passing outputs as inputs to the next step"}}}}',
  'Definition for a chain of prompt templates to be executed sequentially',
  ARRAY[],
  '{}',
  '2025-05-18 08:24:55.986502+02',
  '2025-05-18 08:24:55.986502+02'
);

