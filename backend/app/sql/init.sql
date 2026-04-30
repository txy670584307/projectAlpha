-- projectAlpha 数据库初始化脚本
-- 包含触发器、索引等数据库对象

-- ============================================
-- 1. 创建自动更新时间戳的触发器函数
-- ============================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- 2. 为 tickets 表添加触发器
-- ============================================
CREATE TRIGGER update_tickets_updated_at
    BEFORE UPDATE ON tickets
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- 3. 创建索引以提升查询性能
-- ============================================
CREATE INDEX IF NOT EXISTS idx_tickets_status ON tickets(status);
CREATE INDEX IF NOT EXISTS idx_tickets_created_at ON tickets(created_at DESC);

-- 创建全文搜索索引用于标题搜索
CREATE INDEX IF NOT EXISTS idx_tickets_title_search ON tickets USING gin(to_tsvector('simple', title));

-- 创建标签索引
CREATE INDEX IF NOT EXISTS idx_tags_name ON tags(name);

-- 创建关联表索引以提升反向查询性能
CREATE INDEX IF NOT EXISTS idx_ticket_tags_tag_id ON ticket_tags(tag_id);

-- ============================================
-- 4. 创建标签统计视图
-- ============================================
CREATE OR REPLACE VIEW tag_statistics AS
SELECT 
    t.id,
    t.name,
    COUNT(tt.ticket_id) AS ticket_count,
    COUNT(CASE WHEN tk.status = 'open' THEN 1 END) AS open_ticket_count,
    COUNT(CASE WHEN tk.status = 'closed' THEN 1 END) AS closed_ticket_count
FROM tags t
LEFT JOIN ticket_tags tt ON t.id = tt.tag_id
LEFT JOIN tickets tk ON tt.ticket_id = tk.id
GROUP BY t.id, t.name;

-- ============================================
-- 5. 添加表和字段注释
-- ============================================
COMMENT ON TABLE tickets IS 'Ticket 主表，存储所有工单信息';
COMMENT ON COLUMN tickets.id IS '主键 ID';
COMMENT ON COLUMN tickets.title IS 'Ticket 标题';
COMMENT ON COLUMN tickets.description IS 'Ticket 详细描述';
COMMENT ON COLUMN tickets.status IS '状态：open-未完成, closed-已完成';
COMMENT ON COLUMN tickets.created_at IS '创建时间';
COMMENT ON COLUMN tickets.updated_at IS '最后更新时间';
COMMENT ON COLUMN tickets.completed_at IS '完成时间';

COMMENT ON TABLE tags IS '标签表，存储所有可用的标签';
COMMENT ON COLUMN tags.id IS '主键 ID';
COMMENT ON COLUMN tags.name IS '标签名称，唯一';
COMMENT ON COLUMN tags.created_at IS '创建时间';

COMMENT ON TABLE ticket_tags IS 'Ticket 和 Tag 的多对多关联表';
COMMENT ON COLUMN ticket_tags.ticket_id IS '关联的 Ticket ID';
COMMENT ON COLUMN ticket_tags.tag_id IS '关联的 Tag ID';

COMMENT ON VIEW tag_statistics IS '标签统计视图，包含每个标签的 Ticket 数量统计';
