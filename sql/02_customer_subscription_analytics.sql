SELECT
    COUNT(*) AS total_customers,
    COUNT(DISTINCT country) AS countries,
    COUNT(DISTINCT industry) AS industries
FROM customers;


SELECT
    DATE_FORMAT(signup_date, '%Y-%m') AS signup_month,
    COUNT(*) AS new_customers
FROM customers
GROUP BY DATE_FORMAT(signup_date, '%Y-%m')
ORDER BY signup_month;


SELECT
    plan,
    COUNT(*) AS total_subscriptions,
    ROUND(AVG(price), 2) AS average_price
FROM subscriptions
GROUP BY plan
ORDER BY total_subscriptions DESC;


SELECT
    status,
    COUNT(*) AS subscription_count,
    ROUND(
        100.0 * COUNT(*) / (SELECT COUNT(*) FROM subscriptions),
        2
    ) AS percentage_of_subscriptions
FROM subscriptions
GROUP BY status
ORDER BY subscription_count DESC;


SELECT
    plan,
    COUNT(*) AS total_subscriptions,
    SUM(status = 'Active') AS active_subscriptions,
    SUM(status = 'Cancelled') AS cancelled_subscriptions
FROM subscriptions
GROUP BY plan
ORDER BY total_subscriptions DESC;


SELECT
    plan,
    ROUND(
        100.0 * SUM(status = 'Cancelled') / COUNT(*),
        2
    ) AS churn_rate_percent
FROM subscriptions
GROUP BY plan
ORDER BY churn_rate_percent DESC;


SELECT
    DATE_FORMAT(end_date, '%Y-%m') AS cancellation_month,
    COUNT(*) AS cancellations
FROM subscriptions
WHERE status = 'Cancelled'
  AND end_date IS NOT NULL
GROUP BY DATE_FORMAT(end_date, '%Y-%m')
ORDER BY cancellation_month;


SELECT
    plan,
    ROUND(
        AVG(
            CASE
                WHEN end_date IS NOT NULL
                THEN DATEDIFF(end_date, start_date)
            END
        ),
        2
    ) AS average_customer_lifetime_days
FROM subscriptions
GROUP BY plan
ORDER BY average_customer_lifetime_days DESC;


SELECT
    c.industry,
    COUNT(DISTINCT c.customer_id) AS customers,
    COUNT(DISTINCT s.subscription_id) AS subscriptions,
    SUM(s.status = 'Active') AS active_subscriptions,
    SUM(s.status = 'Cancelled') AS cancelled_subscriptions
FROM customers c
JOIN subscriptions s
    ON c.customer_id = s.customer_id
GROUP BY c.industry
ORDER BY customers DESC;


SELECT
    c.country,
    COUNT(DISTINCT c.customer_id) AS customers,
    SUM(s.status = 'Active') AS active_subscriptions,
    SUM(s.status = 'Cancelled') AS cancelled_subscriptions
FROM customers c
JOIN subscriptions s
    ON c.customer_id = s.customer_id
GROUP BY c.country
ORDER BY customers DESC;


SELECT
    c.customer_id,
    c.company_name,
    c.industry,
    c.country,
    s.plan,
    s.status,
    s.start_date,
    s.end_date
FROM customers c
JOIN subscriptions s
    ON c.customer_id = s.customer_id
WHERE s.status = 'Cancelled'
ORDER BY s.end_date DESC;


SELECT
    c.customer_id,
    c.company_name,
    c.industry,
    c.country,
    s.plan,
    s.price,
    s.start_date,
    s.status
FROM customers c
JOIN subscriptions s
    ON c.customer_id = s.customer_id
WHERE s.status = 'Active'
ORDER BY s.price DESC;


SELECT
    s.plan,
    ROUND(AVG(s.price), 2) AS average_price,
    ROUND(SUM(s.price), 2) AS total_subscription_value
FROM subscriptions s
GROUP BY s.plan
ORDER BY total_subscription_value DESC;


SELECT
    c.customer_id,
    c.company_name,
    c.industry,
    c.country,
    s.plan,
    s.status,
    DATEDIFF(
        COALESCE(s.end_date, CURDATE()),
        s.start_date
    ) AS customer_lifetime_days
FROM customers c
JOIN subscriptions s
    ON c.customer_id = s.customer_id
ORDER BY customer_lifetime_days DESC;