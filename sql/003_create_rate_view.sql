CREATE VIEW dbo.v_system_metrics_rates
AS

WITH previous_values AS
(
    SELECT
        *,

        LAG(event_timestamp)
        OVER
        (
            PARTITION BY host_id
            ORDER BY event_timestamp
        )
        AS previous_timestamp,

        LAG(network_bytes_received)
        OVER
        (
            PARTITION BY host_id
            ORDER BY event_timestamp
        )
        AS previous_received,

        LAG(network_bytes_sent)
        OVER
        (
            PARTITION BY host_id
            ORDER BY event_timestamp
        )
        AS previous_sent,

        LAG(cpu_interrupts)
        OVER
        (
            PARTITION BY host_id
            ORDER BY event_timestamp
        )
        AS previous_interrupts

    FROM dbo.system_metrics
)

SELECT
    *,

    CASE
        WHEN
            previous_timestamp IS NOT NULL

            AND network_bytes_received
                >= previous_received

            AND DATEDIFF_BIG(
                MILLISECOND,
                previous_timestamp,
                event_timestamp
            ) > 0

        THEN
            (
                network_bytes_received
                - previous_received
            )
            /
            (
                DATEDIFF_BIG(
                    MILLISECOND,
                    previous_timestamp,
                    event_timestamp
                )
                / 1000.0
            )
    END
    AS bytes_received_per_second,

    CASE
        WHEN
            previous_timestamp IS NOT NULL

            AND network_bytes_sent
                >= previous_sent

        THEN
            (
                network_bytes_sent
                - previous_sent
            )
            /
            NULLIF(
                DATEDIFF_BIG(
                    MILLISECOND,
                    previous_timestamp,
                    event_timestamp
                )
                / 1000.0,
                0
            )
    END
    AS bytes_sent_per_second,

    CASE
        WHEN
            previous_timestamp IS NOT NULL

            AND cpu_interrupts
                >= previous_interrupts

        THEN
            (
                cpu_interrupts
                - previous_interrupts
            )
            /
            NULLIF(
                DATEDIFF_BIG(
                    MILLISECOND,
                    previous_timestamp,
                    event_timestamp
                )
                / 1000.0,
                0
            )
    END
    AS interrupts_per_second

FROM previous_values;
GO