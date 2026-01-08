/*
  # Enable Vector Search with pgvector

  ## Changes
  - Enable pgvector extension
  - Add embedding column to knowledge_items
  - Create vector similarity search function
  - Add indexes for performance

  ## Security
  Vector search respects existing RLS policies
*/

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Add embedding column to knowledge_items
ALTER TABLE knowledge_items ADD COLUMN IF NOT EXISTS embedding vector(768);

-- Create index for vector similarity search
CREATE INDEX IF NOT EXISTS idx_knowledge_items_embedding ON knowledge_items 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Create similarity search function
CREATE OR REPLACE FUNCTION search_knowledge_by_embedding(
    query_embedding vector(768),
    match_threshold float DEFAULT 0.7,
    match_count int DEFAULT 10
)
RETURNS TABLE (
    id bigint,
    content text,
    knowledge_type text,
    source text,
    confidence decimal,
    similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        knowledge_items.id,
        knowledge_items.content,
        knowledge_items.knowledge_type,
        knowledge_items.source,
        knowledge_items.confidence,
        1 - (knowledge_items.embedding <=> query_embedding) as similarity
    FROM knowledge_items
    WHERE knowledge_items.embedding IS NOT NULL
    AND 1 - (knowledge_items.embedding <=> query_embedding) > match_threshold
    ORDER BY knowledge_items.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- Create hybrid search function (combines vector + keyword)
CREATE OR REPLACE FUNCTION hybrid_search_knowledge(
    query_text text,
    query_embedding vector(768),
    match_threshold float DEFAULT 0.6,
    match_count int DEFAULT 10
)
RETURNS TABLE (
    id bigint,
    content text,
    knowledge_type text,
    source text,
    confidence decimal,
    similarity float,
    keyword_match boolean
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT
        knowledge_items.id,
        knowledge_items.content,
        knowledge_items.knowledge_type,
        knowledge_items.source,
        knowledge_items.confidence,
        COALESCE(1 - (knowledge_items.embedding <=> query_embedding), 0) as similarity,
        (knowledge_items.content ILIKE '%' || query_text || '%') as keyword_match
    FROM knowledge_items
    WHERE 
        (knowledge_items.embedding IS NOT NULL AND 1 - (knowledge_items.embedding <=> query_embedding) > match_threshold)
        OR knowledge_items.content ILIKE '%' || query_text || '%'
    ORDER BY 
        (1 - (knowledge_items.embedding <=> query_embedding)) DESC NULLS LAST,
        keyword_match DESC
    LIMIT match_count;
END;
$$;

-- Add full text search column
ALTER TABLE knowledge_items ADD COLUMN IF NOT EXISTS content_search tsvector
GENERATED ALWAYS AS (to_tsvector('english', content)) STORED;

CREATE INDEX IF NOT EXISTS idx_knowledge_items_content_search ON knowledge_items USING GIN(content_search);
