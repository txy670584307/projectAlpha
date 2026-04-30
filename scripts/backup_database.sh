#!/bin/bash
# ============================================
# Database Backup Script for projectAlpha
# PostgreSQL 数据库定时备份脚本 (Linux)
# ============================================

BACKUP_DIR="/var/backups/projectalpha"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/projectalpha_${TIMESTAMP}.sql"
DB_NAME="projectalpha"
DB_USER="projectalpha_user"

mkdir -p "${BACKUP_DIR}"

echo "Starting database backup..."
echo "Backup file: ${BACKUP_FILE}"

pg_dump -h localhost -U "${DB_USER}" -d "${DB_NAME}" -F c -f "${BACKUP_FILE}"

if [ $? -eq 0 ]; then
    echo "Backup completed successfully."
    echo "Saved to: ${BACKUP_FILE}"
else
    echo "Backup failed with error code: $?"
fi

# Keep only last 7 backups
find "${BACKUP_DIR}" -name "projectalpha_*.sql" -mtime +7 -delete
