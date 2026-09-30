SELECT
    COUNT(*) AS total_customers
FROM customers;


SELECT
    country,
    COUNT(*) AS customer_count
FROM customers
GROUP BY country
ORDER BY customer_count DESC;


SELECT
    industry,
    COUNT(*) AS customer_count
FROM customers
GROUP BY industry
ORDER BY customer_count DESC;


SELECT
    plan,
    COUNT(*) AS subscription_count
FROM subscriptions
GROUP BY plan
ORDER BY subscription_count DESC;


SELECT
    status,
    COUNT(*) AS subscription_count
FROM subscriptions
GROUP BY status
ORDER BY subscription_count DESC;


SELECT
    COUNT(DISTINCT customer_id) AS active_customers
FROM subscriptions
WHERE status = 'Active';


SELECT
    COUNT(DISTINCT customer_id) AS cancelled_customers
FROM subscriptions
WHERE status = 'Cancelled';


SELECT
    ROUND(
        100.0 * SUM(
            CASE
                WHEN status = 'Cancelled' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS churn_rate_percent
FROM subscriptions;


SELECT
    plan,
    status,
    COUNT(*) AS subscription_count
FROM subscriptions
GROUP BY
    plan,
    status
ORDER BY
    plan,
    status;


SELECT
    plan,
    COUNT(*) AS total_subscriptions,
    SUM(
        CASE
            WHEN status = 'Cancelled' THEN 1
            ELSE 0
        END
    ) AS cancelled_subscriptions,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN status = 'Cancelled' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS churn_rate_percent
FROM subscriptions
GROUP BY plan
ORDER BY churn_rate_percent DESC;


SELECT
    plan,
    ROUND(AVG(price), 2) AS average_price
FROM subscriptions
GROUP BY plan
ORDER BY average_price DESC;


SELECT
    subscription_id,
    customer_id,
    plan,
    status,
    start_date,
    end_date,
    CASE
        WHEN end_date IS NOT NULL
        THEN DATEDIFF(end_date, start_date)
        ELSE DATEDIFF(CURDATE(), start_date)
    END AS subscription_days
FROM subscriptions;


SELECT
    plan,
    ROUND(
        AVG(
            CASE
                WHEN end_date IS NOT NULL
                THEN DATEDIFF(end_date, start_date)
                ELSE DATEDIFF(CURDATE(), start_date)
            END
        ),
        2
    ) AS average_subscription_days
FROM subscriptions
GROUP BY plan
ORDER BY average_subscription_days DESC;


SELECT
    c.customer_id,
    c.company_name,
    c.industry,
    c.country,
    s.plan,
    s.status,
    s.price,
    s.start_date,
    s.end_date
FROM customers c
JOIN subscriptions s
    ON c.customer_id = s.customer_id
ORDER BY c.customer_id;


SELECT
    c.customer_id,
    c.company_name,
    c.industry,
    c.country,
    s.plan,
    s.status,
    ROUND(COALESCE(SUM(t.amount), 0), 2) AS total_revenue
FROM customers c
JOIN subscriptions s
    ON c.customer_id = s.customer_id
LEFT JOIN transactions t
    ON c.customer_id = t.customer_id
GROUP BY
    c.customer_id,
    c.company_name,
    c.industry,
    c.country,
    s.plan,
    s.status
ORDER BY total_revenue DESC;