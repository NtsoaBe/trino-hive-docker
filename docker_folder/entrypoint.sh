#!/bin/bash
set -e

# Default DB Variables
export DB_HOST=${DB_HOST:-postgres}
export DB_PORT=${DB_PORT:-5432}
export DB_NAME=${DB_NAME:-metastore}
export DB_USER=${DB_USER:-hive}
export DB_PASSWORD=${DB_PASSWORD:-hive}
export WAREHOUSE_DIR=${WAREHOUSE_DIR:-s3a://warehouse/}

# Default S3 (MinIO) Variables
export S3_ENDPOINT=${S3_ENDPOINT:-http://minio:9000}
export S3_ACCESS_KEY=${S3_ACCESS_KEY:-minioadmin}
export S3_SECRET_KEY=${S3_SECRET_KEY:-minioadmin}

# # Render XML configuration
# envsubst < ${HIVE_HOME}/conf/metastore-site.xml.template > ${HIVE_HOME}/conf/metastore-site.xml

# Render XML files from templates
envsubst < ${HIVE_HOME}/conf/hive-site.xml.template > ${HIVE_HOME}/conf/hive-site.xml
envsubst < ${HIVE_HOME}/conf/core-site.xml.template > ${HIVE_HOME}/conf/core-site.xml

# Ensure Hadoop configuration dir also has core-site.xml
mkdir -p ${HADOOP_HOME}/etc/hadoop
cp ${HIVE_HOME}/conf/core-site.xml ${HADOOP_HOME}/etc/hadoop/core-site.xml

# Wait for DB
echo "Waiting for PostgreSQL at ${DB_HOST}:${DB_PORT}..."
while ! nc -z ${DB_HOST} ${DB_PORT}; do
  sleep 2
done

# Initialize Metastore Schema
if ! ${HIVE_HOME}/bin/schematool -dbType postgres -info > /dev/null 2>&1; then
    echo "Initializing database schema..."
    ${HIVE_HOME}/bin/schematool -dbType postgres -initSchema
fi

echo "Starting Hive Metastore..."
exec ${HIVE_HOME}/bin/hive --service metastore