FROM eclipse-temurin:8-jre-jammy

ENV HADOOP_VERSION=3.3.6
ENV HIVE_VERSION=3.1.3
ENV POSTGRES_JDBC_VERSION=42.6.0

ENV HADOOP_HOME=/opt/hadoop
ENV HIVE_HOME=/opt/hive
ENV PATH="${HADOOP_HOME}/bin:${HIVE_HOME}/bin:${PATH}"

RUN apt-get update && apt-get install -y wget netcat-openbsd gettext-base \
    && rm -rf /var/lib/apt/lists/*

RUN wget -q https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz \
    && tar -xf hadoop-${HADOOP_VERSION}.tar.gz -C /opt/ \
    && mv /opt/hadoop-${HADOOP_VERSION} ${HADOOP_HOME} \
    && rm hadoop-${HADOOP_VERSION}.tar.gz

RUN wget -q https://archive.apache.org/dist/hive/hive-${HIVE_VERSION}/apache-hive-${HIVE_VERSION}-bin.tar.gz \
    && tar -xf apache-hive-${HIVE_VERSION}-bin.tar.gz -C /opt/ \
    && mv /opt/apache-hive-${HIVE_VERSION}-bin ${HIVE_HOME} \
    && rm apache-hive-${HIVE_VERSION}-bin.tar.gz

# FIX: Comment out ALL Postgres "SET" statements that cause schematool parser errors
RUN sed -i 's/^SET /-- SET /g' \
    ${HIVE_HOME}/scripts/metastore/upgrade/postgres/hive-schema-3.1.0.postgres.sql

RUN wget -q https://jdbc.postgresql.org/download/postgresql-${POSTGRES_JDBC_VERSION}.jar -O ${HIVE_HOME}/lib/postgresql-${POSTGRES_JDBC_VERSION}.jar

# Fix Guava version conflict
RUN rm ${HIVE_HOME}/lib/guava-*.jar \
    && cp ${HADOOP_HOME}/share/hadoop/hdfs/lib/guava-*.jar ${HIVE_HOME}/lib/

# Add AWS and S3 support to Hive Metastore for Delta/Iceberg on MinIO
RUN cp ${HADOOP_HOME}/share/hadoop/tools/lib/hadoop-aws-*.jar ${HIVE_HOME}/lib/ \
    && cp ${HADOOP_HOME}/share/hadoop/tools/lib/aws-java-sdk-bundle-*.jar ${HIVE_HOME}/lib/

# COPY metastore-site.xml.template ${HIVE_HOME}/conf/metastore-site.xml.template
COPY hive-site.xml.template ${HIVE_HOME}/conf/hive-site.xml.template
COPY core-site.xml.template ${HIVE_HOME}/conf/core-site.xml.template
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 9083

ENTRYPOINT ["/entrypoint.sh"]
