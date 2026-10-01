-- Customer KPI analysis
-- Transaction and usage data are pre-aggregated separately before joining.
-- This prevents row multiplication when a customer has many transactions
-- and many monthly product-usage records.

WITH transaction_metrics AS (
    SELECT
        customer_id,
        ROUND(SUM(amount), 2) AS total_revenue,
        COUNT(DISTINCT transaction_id) AS total_transactions
    FROM transactions
    GROUP BY customer_id
),
usage_metrics AS (
    SELECT
        customer_id,
        ROUND(AVG(active_users), 2) AS average_active_users,
        ROUND(AVG(sessions), 2) AS average_sessions,
        ROUND(AVG(features_used), 2) AS average_features_used
    FROM product_usage
    GROUP BY customer_id
)
SELECT
    c.customer_id,
    c.company_name,
    c.industry,
    c.country,
    s.plan,
    s.status,
    s.monthly_price,
    COALESCE(t.total_revenue, 0) AS total_revenue,
    COALESCE(t.total_transactions, 0) AS total_transactions,
    COALESCE(u.average_active_users, 0) AS average_active_users,
    COALESCE(u.average_sessions, 0) AS average_sessions,
    COALESCE(u.average_features_used, 0) AS average_features_used
FROM customers c
LEFT JOIN subscriptions s
    ON c.customer_id = s.customer_id
LEFT JOIN transaction_metrics t
    ON c.customer_id = t.customer_id
LEFT JOIN usage_metrics u
    ON c.customer_id = u.customer_id
ORDER BY total_revenue DESC;


WITH transaction_metrics AS (
    SELECT
        customer_id,
        SUM(amount) AS total_revenue
    FROM transactions
    GROUP BY customer_id
),
usage_metrics AS (
    SELECT
        customer_id,
        AVG(active_users) AS average_active_users,
        AVG(sessions) AS average_sessions
    FROM product_usage
    GROUP BY customer_id
),
customer_metrics AS (
    SELECT
        c.customer_id,
        s.plan,
        COALESCE(t.total_revenue, 0) AS total_revenue,
        COALESCE(u.average_active_users, 0) AS average_active_users,
        COALESCE(u.average_sessions, 0) AS average_sessions
    FROM customers c
    LEFT JOIN subscriptions s
        ON c.customer_id = s.customer_id
    LEFT JOIN transaction_metrics t
        ON c.customer_id = t.customer_id
    LEFT JOIN usage_metrics u
        ON c.customer_id = u.customer_id
)
SELECT
    plan,
    COUNT(DISTINCT customer_id) AS customers,
    ROUND(SUM(total_revenue), 2) AS total_revenue,
    ROUND(AVG(total_revenue), 2) AS average_revenue_per_customer,
    ROUND(AVG(average_active_users), 2) AS average_active_users,
    ROUND(AVG(average_sessions), 2) AS average_sessions
FROM customer_metrics
GROUP BY plan
ORDER BY total_revenue DESC;


SELECT
    c.industry,
    COUNT(DISTINCT c.customer_id) AS customers,
    ROUND(COALESCE(SUM(t.amount), 0), 2) AS total_revenue,
    ROUND(AVG(t.amount), 2) AS average_transaction_value
FROM customers c
LEFT JOIN transactions t
    ON c.customer_id = t.customer_id
GROUP BY c.industry
ORDER BY total_revenue DESC;


SELECT
    c.country,
    COUNT(DISTINCT c.customer_id) AS customers,
    ROUND(COALESCE(SUM(t.amount), 0), 2) AS total_revenue,
    ROUND(AVG(t.amount), 2) AS average_transaction_value
FROM customers c
LEFT JOIN transactions t
    ON c.customer_id = t.customer_id
GROUP BY c.country
ORDER BY total_revenue DESC;


WITH transaction_metrics AS (
    SELECT
        customer_id,
        ROUND(SUM(amount), 2) AS total_revenue
    FROM transactions
    GROUP BY customer_id
),
usage_metrics AS (
    SELECT
        customer_id,
        ROUND(AVG(active_users), 2) AS average_active_users,
        ROUND(AVG(sessions), 2) AS average_sessions,
        ROUND(AVG(features_used), 2) AS average_features_used
    FROM product_usage
    GROUP BY customer_id
)
SELECT
    c.customer_id,
    c.company_name,
    c.industry,
    c.country,
    s.plan,
    s.status,
    COALESCE(t.total_revenue, 0) AS total_revenue,
    COALESCE(u.average_active_users, 0) AS average_active_users,
    COALESCE(u.average_sessions, 0) AS average_sessions,
    COALESCE(u.average_features_used, 0) AS average_features_used
FROM customers c
LEFT JOIN subscriptions s
    ON c.customer_id = s.customer_id
LEFT JOIN transaction_metrics t
    ON c.customer_id = t.customer_id
LEFT JOIN usage_metrics u
    ON c.customer_id = u.customer_id
ORDER BY
    average_active_users DESC,
    total_revenue DESC
LIMIT 20;
