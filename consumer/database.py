
import logging
import re

import pyodbc

from consumer.config import SQL_CONNECTION_STRING


logger = logging.getLogger(__name__)


INSERT_SQL = """
INSERT INTO dbo.system_metrics
(
    event_id,
    host_id,
    hostname,
    platform,
    event_timestamp,

    cpu_usage_percent,
    cpu_user_percent,
    cpu_system_percent,
    cpu_idle_percent,

    logical_cores,
    physical_cores,

    cpu_context_switches,
    cpu_interrupts,
    cpu_software_interrupts,

    memory_total_bytes,
    memory_available_bytes,
    memory_used_bytes,
    memory_free_bytes,
    memory_usage_percent,

    disk_total_bytes,
    disk_used_bytes,
    disk_free_bytes,
    disk_usage_percent,

    disk_read_count,
    disk_write_count,
    disk_read_bytes,
    disk_write_bytes,

    network_bytes_sent,
    network_bytes_received,

    network_packets_sent,
    network_packets_received,

    network_errors_in,
    network_errors_out,

    network_dropped_in,
    network_dropped_out
)
VALUES
(
    ?, ?, ?, ?, ?,
    ?, ?, ?, ?,
    ?, ?,
    ?, ?, ?,
    ?, ?, ?, ?, ?,
    ?, ?, ?, ?,
    ?, ?, ?, ?,
    ?, ?,
    ?, ?,
    ?, ?,
    ?, ?
)
"""


def create_connection():
    if not SQL_CONNECTION_STRING:
        raise RuntimeError(
            "SQL_CONNECTION_STRING is missing"
        )

    return pyodbc.connect(
        SQL_CONNECTION_STRING,
        autocommit=False,
    )


def is_duplicate_key_error(exc):
    # SQL Server error 2601: duplicate unique index.
    # SQL Server error 2627: unique constraint violation.
    # pyodbc often reports SQLSTATE 23000 for both,
    # but that SQLSTATE covers other integrity errors too.
    message = " ".join(str(arg) for arg in exc.args)

    return bool(
        re.search(r"\((2601|2627)\)", message)
    )


def insert_batch(connection, records):
    if not records:
        return

    cursor = connection.cursor()

    try:
        cursor.fast_executemany = True

        try:
            cursor.executemany(
                INSERT_SQL,
                records,
            )

            connection.commit()

        except pyodbc.IntegrityError as exc:
            connection.rollback()

            if not is_duplicate_key_error(exc):
                raise

            logger.warning(
                "Batch contains duplicate keys; "
                "retrying records individually"
            )

            cursor.fast_executemany = False

            for record in records:
                try:
                    cursor.execute(
                        INSERT_SQL,
                        record,
                    )

                    connection.commit()

                except pyodbc.IntegrityError as row_exc:
                    connection.rollback()

                    if not is_duplicate_key_error(row_exc):
                        raise

                    logger.warning(
                        "Duplicate event skipped: %s",
                        record[0],
                    )

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
